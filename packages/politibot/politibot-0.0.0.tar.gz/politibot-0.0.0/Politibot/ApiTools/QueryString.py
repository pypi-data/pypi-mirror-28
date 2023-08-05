import urllib

class QueryString:

    def __init__(self, obj):
        self.obj = obj

    def lead_q(self):

        ret = self.no_q()
        
        if len(ret) > 0:
            ret[0] = "?"
            
        return ret


    def no_q(self):
        # ret = ""
        # for k in self.obj.keys():
        #     ret += "&" + str(k) + "=" + str(self.obj[k])

        return "&" + urllib.urlencode(self.obj)
