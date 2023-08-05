class Pagination:

    def __init__(self, obj):
        self.count = obj["count"]
        self.pages = obj["pages"]
        self.per_page = obj["per_page"]        
        self.page = obj["page"]

    def __str__(self):
        return str(self.as_dict())

    def as_dict(self):

        return {
            "count":self.count,
            "pages":self.pages,
            "per_page":self.per_page,
            "page":self.page
        }

    def next_page(self):
        if not self.has_next():
            raise Exception("There are no more pages")
        return self.page + 1

    def prev_page(self):
        if not self.has_prev():
            raise Exception("There is no previous page")
        return self.page - 1

    def has_next(self):
        return self.page < self.pages

    def has_prev(self):
        return self.page > 1

    def pages_left(self):
        return self.pages - self.page

