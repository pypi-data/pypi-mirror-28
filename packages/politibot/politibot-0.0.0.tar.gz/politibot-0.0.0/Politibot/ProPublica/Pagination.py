from ..ApiTools.Pagination import Pagination
import math

class ProPublicaPagination(Pagination):

    # Takes a response dict-like
    def __init__(self, response, offset):

        # hard-coded API feature
        self.per_page = 20

        if "num_results" in response:
            self.count = response["num_results"]
        elif "num_results" in response["results"]:
            self.count = response["results"]["num_results"]
        else:
            self.count = len(response["results"])
            
        self.pages = int(math.ceil(float(self.count) / float(self.per_page)))

        self.offset = offset
        
        self.page = 1 + self.offset / self.per_page

        
    # ProPublica uses offsets, not pages
    def next_offset(self):
        return self.offset + self.per_page

    def has_next(self):
        return (self.offset + self.per_page - 1) < self.count
        
