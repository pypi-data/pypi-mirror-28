from ProPublicaApi import ProPublicaApi

class Congress(ProPublicaApi):

    def __init__(self, key, version="v1", congress="115"):

        self.version  = version
        self.congress = congress
        base_url = "https://api.propublica.org/congress/" \
                   + self.version + "/" 
        
        super(Congress, self).__init__(key, base_url)

    def chamber_delegation(self, state_code, chamber):
        method = "members/" + chamber + "/" + state_code + "/current.json"
        return self.get(method)

    def senate_delegation(self, state_code):
        return self.chamber_delegation(state_code, "senate")

    def house_delegation(self, state_code):
        return self.chamber_delegation(state_code, "house")

    def delegation(self, state_code):
        house = self.house_delegation(state_code)
        print house
        senate = self.senate_delegation(state_code)
        print senate

        ret = senate
        ret.merge(house)

        return ret

    def cosponsored(self, member_id):
        method = "members/"+member_id+"/bills/cosponsored.json"
        ret = self.get(method)

        assert(len(ret.results()) < 2)

        return ret
