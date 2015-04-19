import pandas as pd
import googlemaps
from googlemaps import Convert
from googlemaps.convert import as_list
import datetime
import time
import json

key = '(api key)'
client = googlemaps.Client(key)

def distance_matrix(client, origins, destinations,
                    mode=None, language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None):
    params = {
        "origins": origins,
        "destinations": destinations
    }
    if mode:
		if mode not in ["driving", "walking", "bicycling", "transit"]:
			raise ValueError("Invalid travel mode.")
			params["mode"] = mode

    if language:
        params["language"] = language

    if avoid:
        if avoid not in ["tolls", "highways", "ferries"]:
            raise ValueError("Invalid route restriction.")
        params["avoid"] = avoid

    if units:
        params["units"] = units

    if departure_time:
        params["departure_time"] = convert.time(departure_time) #This function does not work

    if arrival_time:
        params["arrival_time"] = convert.time(arrival_time)

    if departure_time and arrival_time:
        raise ValueError("Should not specify both departure_time and"
                         "arrival_time.")

    if transit_mode:
        params["transit_mode"] = convert.join_list("|", transit_mode)

    if transit_routing_preference:
        params["transit_routing_preference"] = transit_routing_preference

    return client._get("/maps/api/distancematrix/json", params)


dptime = int(time.mktime(datetime.datetime.strptime("04-12-2015 12:00:00", "%m-%d-%Y %H:%M:%S").timetuple()))

pd.options.mode.chained_assignment = None 
df = pd.read_csv('dca.csv')

for i in range(len(df)):   
    
    df['time_to_BH'][i] = int(distance_matrix(client, df['Origin_Zip'][i] , df['Destination_BH'][i], departure_time = dptime)['rows'][0]['elements'][0]['duration']['value']/60)
    df['time_to_SM'][i] = int(distance_matrix(client, df['Origin_Zip'][i] , df['Destination_SM'][i], departure_time = dptime)['rows'][0]['elements'][0]['duration']['value']/60)
    
    df['time_to_BH'][i] =  distance_matrix(client, df['Origin_Zip'][i] , df['Destination_BH'][i], departure_time = departure_time)['rows'][0]['elements'][0]['duration']['text']
    df['time_to_SM'][i] =  distance_matrix(client, df['Origin_Zip'][i] , df['Destination_SM'][i], departure_time = departure_time)['rows'][0]['elements'][0]['duration']['text']
    
    print df['time_to_BH'][i]
    print df['time_to_SM'][i]

df.to_csv('dca.csv')
