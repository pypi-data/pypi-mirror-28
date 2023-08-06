import requests
from .YWeathermethods import YWeathermethods
class YWeather:
    
    baseurl="https://query.yahooapis.com/v1/public/yql"
    u='f'

    def weatherat(self,place):
        self.place=place
    
    def unit(self,u):
        self.u=u
    
    def getweather(self):
        url = "%s?q=select* from weather.forecast where woeid in (select woeid from geo.places(1) where text='%s') and u='%s' &format=json" % (self.baseurl, self.place,self.u)
        req = requests.get(url)
        self.results = req.json()
        if self.results['query']["count"] == 0:
            return self.results
        else:
            return YWeathermethods(self.results['query']['results']['channel'])
 