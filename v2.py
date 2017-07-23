# this version uses the yelp api and along
# with the google maps api and user input returns results
#to open in terminal type: "python3 v2.py"

from v1 import v1API
import requests
from urllib.parse import urlencode

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

SEARCH_LIMIT=10
SORT_BY="distance"

class IncorrectLocation(Exception):
    pass

class yelpapi(v1API):
    def __init__(self):
        self._yelp_base_url="https://api.yelp.com/v3/businesses/search"
        v1API.__init__(self)

    def _get_term(self):
        try:
            term=input("Enter term:")
            int_term=int(term)
        except ValueError:
            return term

    def get_user_input(self):
        self._orig=v1API.origin_input(self)
        self._term=self._get_term()


    def get_client_id_secret(self,file_name):
        data=open(file_name)
        new_lines=[i.replace("\n","") for i in data.readlines()]
        for index,line in enumerate(new_lines):
            if index==2:
                client_id=line
            elif index==3:
                client_secret=line

        return client_id,client_secret

    def get_access_token(self,host,path,client_id,client_secret):
        #taken from https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

        url = host+path
        print(url,client_id,client_secret)
        query_parameters=urlencode({"client_id":client_id,"client_secret":client_secret,"grant_type":GRANT_TYPE})
        headers={'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request('POST', url, data=query_parameters, headers=headers)
        access_token = response.json()['access_token']
        return access_token

    def request(self,host,path,access_token,query_params):
        url=host+path
        headers={'Authorization':'Bearer %s'%access_token,}
        response=requests.request('GET',url,headers=headers,params=query_params)

        return response.json()

    def yelp_search(self,access_token):
        query_params=urlencode([("term",self._term),
                                ("latitude",self._orig_lat),
                                ("longitude",self._orig_long),
                                ("limit",SEARCH_LIMIT),
                                ("sort_by",SORT_BY)])
        return self.request(API_HOST,SEARCH_PATH,access_token,query_params=query_params)


    def _get_weather_latlng(self):
        v1obj=v1API()
        v1obj._get_keys("api_keys.txt")
        url=v1obj.build_google_url(self._orig)
        print(url)
        orig_json_dict=v1obj.get_result(url)

        if orig_json_dict["status"]=="OK":
            self._orig_lat, self._orig_long = (orig_json_dict["results"][0]["geometry"]["location"]["lat"],
                                   orig_json_dict["results"][0]["geometry"]["location"]["lng"])
            orig_weather_dict = v1obj.get_result(v1obj.build_weather_url((self._orig_lat, self._orig_long)))
            weather_forecast=orig_weather_dict["weather"][0]["main"]
            return weather_forecast
        else:
            raise IncorrectLocation("Please check your address location")


    def get_yelp_results(self):
        client_id,client_secret=self.get_client_id_secret("api_keys.txt")
        access_token=self.get_access_token(API_HOST,TOKEN_PATH,client_id,client_secret)
        response=self.yelp_search(access_token)
        for places in response["businesses"]:
            print(places)




def main():
    yelp_obj=yelpapi()
    yelp_obj.get_user_input()
    weather_forecast=yelp_obj._get_weather_latlng()
    print(weather_forecast)
    yelp_obj.get_yelp_results()

if __name__=="__main__":
    main()


