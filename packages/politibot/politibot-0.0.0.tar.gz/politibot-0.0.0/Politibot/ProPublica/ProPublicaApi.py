#
# Common features across at least two ProPublica APIs
#

from ..ApiTools.ResultSet import ResultSet
from ..ApiTools.QueryString import QueryString
from Pagination import ProPublicaPagination

import requests

class ProPublicaApi(object):

    def __init__(self, key, base_url, page_size=20, max_pages=50):
        self.key = key
        self.base_url = base_url
        self.page_size = page_size
        self.max_pages = max_pages

    def headers(self, header_dict=None):

        if header_dict is None:
            header_dict = {}

        header_dict["X-API-Key"] = self.key

        return header_dict
        
    # Form a request URL 
    def url(self, path, query={}, offset=0):

        return self.base_url \
            + str(path) \
            + "?offset=" + str(offset)\
                         + QueryString(query).no_q()


    # Make a request. Will try to exhaust all 
    def get(self, path, query=""):

        pages_left = self.max_pages
        s = requests.Session()
        ret = ResultSet(arr=[])
        offset = 0

        while True:

            s.headers.update(self.headers())

            resp = s.get(self.url(path, query=query, offset=offset))

            if resp.status_code != 200:
                print resp.content
                print resp.status_code
                raise Exception("HTTP Error")

            resp_obj = resp.json()

            p = ProPublicaPagination(resp_obj, offset)

            # Break if the request is too big
            if p.pages > self.max_pages:
                raise Exception("Maximum pages exceeded. Try narrowing your query.")

            # Add the response object to the ResultSet
            ret.add(resp_obj)

            if not p.has_next():
                break

            else:
                offset = p.next_offset()
            
        return  ret
