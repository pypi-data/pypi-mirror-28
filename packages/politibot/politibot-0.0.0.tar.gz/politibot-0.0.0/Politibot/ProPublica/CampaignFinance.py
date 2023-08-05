from ProPublicaApi import ProPublicaApi

class CampaignFinance(ProPublicaApi):

    # get independent expenditures
    def expenditures(self, fec_id):
        method = "candidates/" + fec_id + "/independent_expenditures.json"

        return self.get(method)

    # get all the candidates in races in a given state
    def races(self, state_code):

        method = "races/" + state_code + ".json"

        return self.get(method)

    # search for a committee
    def committee_search(self, search_term):
        method = "committees/search.json"
        query = {"query":search_term}

        return self.get(method, query=query)

    # get details on a specific committee
    def committee(self, fec_id):

        method = "committees/" + fec_id

        return self.get(method)

    # search for a candidate
    def candidate_search(self, search_term):
        method = "candidates/search.json"
        query = {"query":search_term}

        return self.get(method, query)

    def candidate(self, fec_id):
        method = "candidates/" + str(fec_id) + ".json"

        return self.get(method)
    

    def __init__(self, key, version="v1", cycle="2016", max_pages=1):

        # Max number of pages to get
        # self.max_pages = max_pages
        # self.key = key
        self.version = version
        self.cycle = cycle

        # Not user modifiable
        # self.page_size = 20
        base_url = "https://api.propublica.org/campaign-finance/" \
                   + str(version) + "/" + str(cycle) + "/"

        super(CampaignFinance, self).__init__(key, base_url)
    
