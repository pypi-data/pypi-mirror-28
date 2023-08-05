class ResultSet:

    def add(self, obj):
        self.arr.append(obj)

    def page(self, n=0):
        return self.arr[n]

    def results(self):
        ret = []

        for page in self.arr:
            ret += page["results"]

        return ret

    # merge with another ResultSet
    def merge(self, other_set):
        self.arr += other_set.arr
    
    def __init__(self, arr=[]):
        self.arr = arr
