import pandas as pd
from ..ApiTools import ResultSet

class ConnAssembly:

    def __init__(self):
        self.cache = {}

    def get_dataframe(self, url):

        if url not in self.cache:
            self.cache = pd.read_csv(url)

        return self.cache

    def to_json(self, df):
        return df.to_json(orient="records")

    def to_dict(self, df):
        return df.to_dict(orient="records")

    def candidates(self, dataframe=False):
        url = "ftp://ftp.cga.ct.gov/pub/data/LegislatorDatabase.csv"

        df = self.get_dataframe(url)

        if dataframe:
            return df

        return self.to_json(df)
    
    def candidate(self, office, district):
        df = self.candidates(dataframe=True)

        print df.dtypes
        
        self.to_dict(df[
            (df["office code"] == str(office)) & (df["dist"] == district)
        ])


    def bill_history(self):
        url = "ftp://ftp.cga.ct.gov/pub/data/bill_history.csv"

        return self.to_dict(self.get_dataframe(url))
