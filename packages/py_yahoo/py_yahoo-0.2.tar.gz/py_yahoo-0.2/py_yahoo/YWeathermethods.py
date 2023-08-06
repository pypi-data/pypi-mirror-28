class YWeathermethods:
    
    def __init__(self,results):
        self.results=results
    
    def getlastbuilddate(self):
        return self.results["lastBuildDate"]
        
    def getatmosphere(self):
        return self.results["atmosphere"]
    
    def forecast(self):
        return self.results["item"]["forecast"]
    
    def getlatitude(self):
        return self.results["item"]["lat"]

    def getlongitude(self):
        return self.results["item"]["long"]

    def getlocation(self):
        return self.results["location"]

    def getunits(self):
        return self.results["units"]
    
    def getastronomy(self):
        return self.results["astronomy"]
    
    def getwind(self):
        return self.results["wind"]
    
    def weatheratwhatdatetime(self):
        return self.results["item"]["condition"]["date"]
    
    def getstatus(self):
        return self.results["item"]["condition"]["text"]
    
    def gettemp(self):
        return self.results["item"]["condition"]["temp"]
        