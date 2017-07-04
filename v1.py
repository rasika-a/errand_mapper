## This is the first version of the errands mapper/planner
## In this version, given any two locations you get data on the weather of those two locations


import json
import urllib.request
import urllib.parse

class v1API:
    def __init__(self):
        ##basic definitions required for runnning the Google Maps API and Open Weather Map API
        self._base_google_maps_url="https://maps.googleapis.com/maps/api/directions/json?"
        self._base_weather_url="http://api.openweathermap.org/data/2.5/weather?"

    def _get_keys(self):
        file_name=input("Enter the name of the text file that contains the API Keys:")
        file=open(file_name)
        file_data=[]
        for line in file:
            if "\n" in line:
                file_data.append(line[:-1])
            else:
                file_data.append(line)
        self._GOOGLE_MAPS_API_KEY,self._OPEN_WEATHER_API_KEY=tuple(file_data)

    def origin_input(self):
        ##accepts the origin location input from the user
        while True:
            try:
                orig=input("Enter the origin location:")
                orig_check=int(orig)

            except ValueError:
                return orig

    def destination_input(self):
    ##accepts the destination location input from the user
        while True:
            try:
                dest=input("Enter the destination location:")
                dest_check=int(dest)

            except ValueError:
                return dest

    def build_google_url(self,orig_dest_tup:tuple):
        ##builds the url for the Google Maps API based on input received from the user
        ##in the previous functions
        orig,dest=orig_dest_tup
        query_parameters=[("origin",orig),("destination",dest),("key",self._GOOGLE_MAPS_API_KEY)]

        return self._base_google_maps_url+urllib.parse.urlencode(query_parameters)

    def build_weather_url(self,lat_lng_tup:tuple):
        ##builds the Open Weather Maps url based on the lattitude and longitude given
        lat,lng=lat_lng_tup
        query_parameters=[("lat",lat),("lon",lng),("APPID",self._OPEN_WEATHER_API_KEY)]

        return self._base_weather_url+urllib.parse.urlencode(query_parameters)

    def get_result(self,url:str)->dict:
        '''This function takes a URL and returns a dictionary representing
        the JSON response'''
        response=None

        try:
            response=urllib.request.urlopen(url)
            print(response)
            json_text=response.read().decode(encoding='utf-8')

            return json.loads(json_text)
        finally:
            if response!=None:
                response.close()

if __name__=="__main__":
    trobj1=v1API()
    trobj1._get_keys()
    orig=trobj1.origin_input()
    dest=trobj1.destination_input()
    url=trobj1.build_google_url((orig,dest))
    maps_json_dict=trobj1.get_result(url)
    if maps_json_dict["status"]=="OK":
        orig_lat,orig_long=(maps_json_dict["routes"][0]["legs"][0]["start_location"]["lat"],maps_json_dict["routes"][0]["legs"][0]["start_location"]["lng"])
        dest_lat,dest_long=(maps_json_dict["routes"][0]["legs"][0]["end_location"]["lat"],maps_json_dict["routes"][0]["legs"][0]["end_location"]["lng"])
        orig_weather_dict=trobj1.get_result(trobj1.build_weather_url((orig_lat,orig_long)))
        dest_weather_dict=trobj1.get_result(trobj1.build_weather_url((dest_lat,dest_long)))
    else:
        print("Path not found")
