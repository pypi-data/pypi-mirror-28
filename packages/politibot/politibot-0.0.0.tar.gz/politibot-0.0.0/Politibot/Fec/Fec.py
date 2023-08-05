from ..ApiTools.ResultSet import ResultSet
from ..ApiTools.QueryString import QueryString
from ..ApiTools.Pagination import Pagination as FecPagination

import requests

class Fec:

    def __init__(self, key, cycle="2018", max_pages=25):
        self.max_pages=max_pages
        self.API_KEY = key
        self.cycle = cycle
        
        # not user-defined
        self.base_url = "https://api.open.fec.gov/"
        self.version = "v1"

    def url(self, path, query):
        return str(self.base_url)\
            + str(self.version) + "/"\
            + str(path)\
            + "?api_key=" + str(self.API_KEY) \
                          + "&cycle=" + str(self.cycle)\
                                      + query

    # def get_all(self, path, query=""):

    #     ret = ResultSet([])
    #     pages_left = 

    #     while True:

    #         ret.append(current_page)
    #         next_page = current_page["next"]()            

    #         if next_page is None:
    #             break

    #         current_page = next_page

    #     return ret

    def get(self, path, query=""):

        first_page = self.get_page(path, query=query, page=1)
        current_page = first_page

        ret = ResultSet([])
        
        while True:
            ret.add(current_page.page(0))

            p = FecPagination(current_page.page(0)["pagination"])
            
            # if p.pages > self.max_pages:
            #     raise Exception("Error: Too many results. Try narrowing your query")

            if p.has_next():
                current_page = self.get_page(path, query, p.next_page())
            else:
                break

        return ret
    
    def get_page(self, path, query="", page=1):

        req_url = self.url(path, query +  "&page=" + str(page))

        resp = requests.get(req_url)

        if resp.status_code != 200:
            raise Exception ("HTTP Error")

        # p = FecPagination(resp.json()["pagination"])

        # get_next = lambda: None
        
        # if p.has_next():
        #     get_next = lambda: self.get(path, query=query,page=p.next_page())
        

        ret = ResultSet([])

        ret.add(resp.json())
        
        # ret = {
        #     "next":get_next,
        #     "json":resp.json()
        # }

        return ret
            
    def committees(self, query_obj={} ):
        return self.get("committees",
                        QueryString(query_obj).no_q())

    def candidate(self, cand_id, query_obj={}):
        return self.get("candidate/" + str(cand_id),
                        query=QueryString(query_obj).no_q())
    

    def filings(self, query_obj={}):
        return self.get("filings/",
                        QueryString(query_obj).no_q())

    def efiling(self, query_obj={}):
        return self.get("efile/filings/",
                        query=QueryString(query_obj).no_q())
