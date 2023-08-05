from ScopusWp.scopus.data import ScopusPublication

from ScopusWp.scopus.observe import ScopusObservationController

from ScopusWp.scopus.persistency import ScopusBackupController, ScopusCacheController
from ScopusWp.scopus.persistency import ScopusPublicationPickleCacheModel, ScopusAuthorPickleCacheModel

from ScopusWp.scopus.scopus import ScopusController

# TODO: Implement massive logging


class ScopusTopController:

    def __init__(self):
        self.observation_controller = ScopusObservationController()
        self.scopus_controller = ScopusController()
        self.backup_controller = ScopusBackupController()
        self.cache_controller = ScopusCacheController(ScopusPublicationPickleCacheModel, ScopusAuthorPickleCacheModel)

    #####################
    # TOP LEVEL METHODS #
    #####################

    def get_publication(self, scopus_id):
        # Checking if the publication is in the cache and returning the cached value if possible
        is_cached = self.cache_controller.contains_publication(scopus_id)
        if is_cached:
            publication = self.cache_controller.select_publication(scopus_id)
        else:
            # If the publication is not cached, getting it from the scopus website
            publication = self.scopus_controller.get_publication(scopus_id)
        return publication

    def get_multiple_publications(self, scopus_id_list):
        publication_list = []
        for scopus_id in scopus_id_list:
            publication = self.get_publication(scopus_id)
            publication_list.append(publication)
        return publication_list

    def get_publications_observed(self):
        # Getting the author ids of all the observed authors for the scopus database
        author_id_list = self.observation_controller.all_observed_ids()
        # Getting the author profiles for all the authors
        author_profile_list = self.scopus_controller.get_multiple_author_profiles(author_id_list)
        # Getting the publications for all the author profiles
        publication_list = []
        for author_profile in author_profile_list:
            _publications = self.scopus_controller.get_author_publications(author_profile)
            publication_list += _publications
        return publication_list

    def get_publication_ids_observed(self):
        # Getting the list of observed authors from the observation controller
        observed_author_id_list = self.observation_controller.all_observed_ids()

        publication_id_list = []
        for author_id in observed_author_id_list:
            # Attempting to get the author profiles for the publication id lists from the cache and if the cache
            # does not contain them, requesting them from scopus
            is_cached = self.cache_controller.contains_author_profile(author_id)
            if is_cached:
                author_profile = self.cache_controller.select_author_profile(author_id)
            else:
                author_profile = self.scopus_controller.get_author_profile(author_id)
            publication_difference_list = list(set(author_profile.publications) - set(publication_id_list))
            publication_id_list += publication_difference_list

        return publication_id_list

    def request_publication_ids_observed(self):
        # Getting the author ids of all the observed authors for the scopus database
        author_id_list = self.observation_controller.all_observed_ids()
        # Getting the author profiles for all the authors
        author_profile_list = self.scopus_controller.get_multiple_author_profiles(author_id_list)
        # Assembling the list of publications for each author profile
        scopus_id_list = []
        for author_profile in author_profile_list:
            difference = list(set(author_profile.publications) - set(scopus_id_list))
            scopus_id_list += difference
        return scopus_id_list

    def reload_cache_observed(self):
        # Clearing the cache
        self.cache_controller.wipe()
        self.cache_controller.save()

        # Loading the cache anew
        self.load_cache_observed()

    def load_cache_observed(self, load_citations=True):
        """
        First loads the observed authors profiles into the cache (requests only those not already in the cache).
        Based on those author profiles loads the publications of all the observed authors into the cache and if the
        load_citations flag is set (default), all the publications, that have cited those publications will also be
        loaded into the cache.

        :param load_citations: boolean flag of whether or not to load the citation publications into the cache as well
        :return: void
        """
        # Loading the author profiles into the cache
        self._load_cache_observed_authors()

        # Loading the publications of the observed authors into the cache
        self._load_cache_observed_publications(load_citations=load_citations)

    def load_publications_cache(self, scopus_id_list, auto_save_interval=20, reload=False):
        """
        Loads the publication info about the publications described by the scopus ids in the list from the scopus
        website and saves them in the cache.

        Although only specifically requests those publications from the web, that are not already in the cache, for
        network performance reasons. All the publications can be requested by setting reload to true.
        Also the cache auto saves after the specified amount for the auto save interval in case of connection error.

        :param scopus_id_list: The list of scopus ids, for all the publications to be loaded into the cache
        :param auto_save_interval: The amount of publications to be fetched from the scopus website, before the
            cache saves the progress. default on 20
        :param reload: The boolean value of whether or not to get all the specified publications from the scopus
            website or leave out those, already in the cache
        :return: void
        """
        # Getting the list of publication ids for those publications, that are still in the cache
        cache_scopus_id_list = self.cache_controller.select_all_publication_ids()

        # If the reload flag is True, using the whole scopus id list as the list to be requested from the scopus site
        # else, only using those ids, that are not in the cache already
        if reload:
            difference_scopus_id_list = scopus_id_list
        else:
            difference_scopus_id_list = list(set(scopus_id_list) - set(cache_scopus_id_list))

        auto_save_count = 0
        for scopus_id in difference_scopus_id_list:
            # Auto saving if the count has reached the specified interval and then resetting the counter
            if auto_save_count == auto_save_interval:
                self.cache_controller.save()
                auto_save_count = 0

            # Getting the publication from the scopus website
            publication = self.scopus_controller.get_publication(scopus_id)
            self.cache_controller.insert_publication(publication)

            auto_save_count += 1

        self.cache_controller.save()

    def load_authors_cache(self, author_id_list, auto_save_interval=20, reload=False):
        """
        Loads the author profiles for the authors given by the author id list into the cache, by requesting them
        from the scopus website.

        On default, only those author profiles, that cannot already be found in the cache will be explicitly
        requested from the scopus website. When reload is True, all the author profiles will be requested and the
        possibly existing cache will be overwritten.
        Also the cache auto saves after the specified amount for the auto save interval, in case of connection
        error or exception.

        :param author_id_list: The list of author ids for the author profiles to be loaded into the cache
        :param auto_save_interval: The int amount of author profiles to be requested before the cache saves the
            progress into persistency.
        :param reload: The boolean value of whether or not the
        :return: void
        """
        cache_author_id_list = self.cache_controller.select_all_author_ids()

        # Subtracting the the observed from the cached ids and adding only the left over to the cache
        if reload:
            difference_author_id_list = author_id_list
        else:
            difference_author_id_list = list(set(author_id_list) - set(cache_author_id_list))

        auto_save_counter = 0
        for author_id in difference_author_id_list:
            # Saving during the process, so progress is not lost after connection error
            if auto_save_counter == auto_save_interval:
                self.cache_controller.save()
                auto_save_counter = 0

            # Requesting the author profile from the scopus website
            author_profile = self.scopus_controller.get_author_profile(author_id)
            self.cache_controller.insert_author_profile(author_profile)
            auto_save_counter += 1
        self.cache_controller.save()

    def _load_cache_observed_authors(self):
        """
        Loads the author profiles for all the observed authors into the cache, but only specifically requests those,
        which are not already in the cache.

        :return: void
        """
        # Getting the list of author ids for the observed authors from the observation controller
        observed_author_id_list = self.observation_controller.all_observed_ids()

        # Loading all those author profiles of the observed authors into the cache
        self.load_authors_cache(observed_author_id_list)

    def _load_cache_observed_publications(self, load_citations=True):
        """
        Loads all the publications of the observed authors into the cache, but only those, that are not already in the
        cache. Also loads all the publication, that have cited the observed publications into the cache if enabled.

        :param load_citations: boolean flag of whether or not to also load the citation publications into the cache
        :return: void
        """
        # Getting the list of publication ids for all the observed authors from the cache
        observed_publication_id_list = self.get_publication_ids_observed()

        # Loading all those publications into the cache after having them requested from the scopus website
        self.load_publications_cache(observed_publication_id_list)

        if load_citations:
            # Getting the citations scopus id list from every one of those publications
            citation_scopus_id_list = []
            for scopus_id in observed_publication_id_list:
                publication = self.cache_controller.select_publication(scopus_id)

                difference = list(set(publication.citations) - set(citation_scopus_id_list))
                citation_scopus_id_list += difference

            # Loading all those publications into the cache as well
            self.load_publications_cache(citation_scopus_id_list)

    ######################
    # THE SCOPUS METHODS #
    ######################

    def request_publication(self, scopus_id):
        return self.scopus_controller.get_publication(scopus_id)

    def request_multiple_publications(self, scopus_id_list):
        return self.scopus_controller.get_multiple_publications(scopus_id_list)

    ###########################
    # THE OBSERVATION METHODS #
    ###########################

    def filter_by_observation(self, publication_list):
        return self.observation_controller.filter(publication_list)

    def publication_observation_keywords(self, publication):
        return self.observation_controller.get_publication_keywords(publication)

    ######################
    # THE BACKUP METHODS #
    ######################

    def select_publication_backup(self, scopus_id):
        return self.backup_controller.select_publication(scopus_id)

    def select_multiple_publications_backup(self, scopus_id_list):
        return self.backup_controller.select_multiple_publications(scopus_id_list)

    def select_all_publications_backup(self):
        return self.backup_controller.select_all_publications()

    def insert_publication_backup(self, publication):
        self.backup_controller.insert_publication(publication)

    def insert_multiple_publication_backup(self, publication_list):
        self.backup_controller.insert_multiple_publications(publication_list)

    #####################
    # THE CACHE METHODS #
    #####################

    def select_publication_cache(self, scopus_id):
        return self.cache_controller.select_publication(scopus_id)

    def select_multiple_publications_cache(self, scopus_id_list):
        return self.cache_controller.select_multiple_publications(scopus_id_list)

    def select_all_publications_cache(self):
        return self.cache_controller.select_all_publications()

    def insert_publication_cache(self, publication):
        self.cache_controller.insert_publication(publication)

    def insert_multiple_publications_cache(self, publication_list):
        self.cache_controller.insert_multiple_publications(publication_list)

