import argparse
import decimal
from flask import Flask, render_template, url_for
from flask_googlemaps import GoogleMaps
import json
from datetime import datetime
from flask_googlemaps import Map
from flask import request
import LoadJSONdata
from dbb import functions
from _symtable import FREE
try:
    import LoadJSONdata
except ImportError:
    # when installed, import like this works
    from . import LoadJSONdata

def get_args():
    """all the argparse stuff.
    params:  -
    returns: namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", dest="port", type=int)
    parser.add_argument("--debug", dest="debug", action="store_true")
    parser.set_defaults(port=5000)
    parser.set_defaults(debug=False)
    return parser.parse_args()

# Flask likes to know the name of the script calling it.
app = Flask(__name__)
GoogleMaps(app)


def get_icon_url(available_bikes, total_bike_stands):
    """ Returns colour based on percentage occupancy:
     0-25% Red
    26-50% Orange
    51-75% Yellow
    76-100% Green
    
    params:
        available_bikes (int), total_bike_stands (int)
    returns: 
        string or None
    """
    base_url = 'http://maps.google.com/mapfiles/ms/icons/'
    pcnt = (available_bikes / total_bike_stands) * 100
    if pcnt == 0:
        return base_url + "purple-dot.png"
    if pcnt <26:
        return base_url+"red-dot.png"
    if pcnt < 51:
        return base_url+"orange-dot.png"
    if pcnt < 76:
        return base_url+"yellow-dot.png"
    if pcnt <= 100:
        return base_url+"green-dot.png"

    

@app.route("/")
def index():
    '''This method retrieves data from the Dublin Bikes API, it itterates through the data
    and presents markers on a google map'''

    mydata = LoadJSONdata.GetLocationData()
    
    sndmap = Map("sndmap",mydata[0]["position"]["lat"], mydata[0]["position"]["lng"], style="height:600px;width:600px;margin:0;")
    for obj in mydata:
        name = obj["name"]
        lat = str(obj["position"]["lat"])
        time_stamp = obj['last_update']
        lng = str(obj["position"]["lng"])
        free = obj['available_bikes']
        available_bike_stands = obj['available_bike_stands']
        total_bike_stands = obj['bike_stands']
          
    #Code reference: https://github.com/rochacbruno/Flask-GoogleMaps
        sndmap.markers.append({'icon':get_icon_url(free, total_bike_stands), 'lat': lat, 'lng': lng,
                              'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands) + '''<a onclick="drawChart(' '''  + str(name) + ''' ')" href=#>More Details</a>'''})
        
    return render_template("index.html", sndmap=sndmap)

#get daily data
@app.route("/getdailychartdata", methods=['POST'])
def getDailyChartData():
    '''This function gets daily data back from the database based on a single location
        This function returns the following:
        DayOfWeek, %Available Bikes, %Available Bike Stands
        in JSON format'''
    
    #Gets location from the form and queries database based on location clicked for all records
    location = request.form['location'].strip()
    data = functions.QueryByLocation(location)
    
    #Initialize arrays
    dayArray = []
    weekdayArray= [['Sunday', 0, 0], ['Monday', 0, 0], ['Tuesday', 0, 0], ['Wednesday', 0, 0], ['Thursday', 0, 0], ['Friday', 0, 0], ['Saturday', 0, 0]]
    
    for i in range (1, 7 +1):
         dayItem=[i, 0, 0, 0]
         dayArray.append(dayItem) 
         
    #Iterate through data
    for i in data["Items"]:          
        dayOfWeek = datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%w'),
        free = int(i['free'])
        available_bike_stands = int(i['available_bike_stands'])
        total_bike_stands = int(i['bike_stands'])

        #add record to running total, sums available bikes and sums available bikes stands per day of week.
        dayArray[int(dayOfWeek[0][0])][3]= dayArray[int(dayOfWeek[0][0])][3]+1
        dayArray[int(dayOfWeek[0][0])][1]= dayArray[int(dayOfWeek[0][0])][1]+free
        dayArray[int(dayOfWeek[0][0])][2]= dayArray[int(dayOfWeek[0][0])][2]+available_bike_stands
    
    #Get average & calculate percentages of available bikes/bike stands
    for i in range(0, 7):
        weekdayArray[i][1]= int(((dayArray[i][1]/dayArray[i][3])/total_bike_stands)*100)
        weekdayArray[i][2]= int(((dayArray[i][2]/dayArray[i][3])/total_bike_stands)*100)
        
    return json.dumps(weekdayArray)


@app.route("/gethourlychartdata", methods=['POST'])
def getHourlyChartData():
    '''This function gets hourly data back from the database based on a single location
        This function returns the following:
        Hour, %Available Bikes, %Available Bike Stands
        in JSON format'''
    #Gets location from the form and queries database based on location clicked for all records
    location = request.form['location'].strip()
    data = functions.QueryByLocation(location)
    
    #Initialize arrays
    hourArray = []
    finalHourArray = []

    for i in range (1, 24 +1):
         hourItem=[i, 0, 0, 0]
         finalHourItem= [i, 0, 0]
         hourArray.append(hourItem)
         finalHourArray.append(finalHourItem)
         
    #Iterate through data
    for i in data["Items"]:
              
        hour = int(datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%H'))
        free = int(i['free'])
        available_bike_stands = int(i['available_bike_stands'])
        total_bike_stands = int(i['bike_stands'])
        
        #Add record to running total, sum all available bikes/bike stands
        hourArray[hour][3]= hourArray[hour][3]+1
        hourArray[hour][1]= hourArray[hour][1]+free
        hourArray[hour][2]= hourArray[hour][2]+available_bike_stands
    
    #Get average & calculate percentages of available bikes/bike stands
    for i in range(0, 24):
        finalHourArray[i][1]= int(((hourArray[i][1]/hourArray[i][3])/total_bike_stands)*100)
        finalHourArray[i][2]= int(((hourArray[i][2]/hourArray[i][3])/total_bike_stands)*100)

    return json.dumps(finalHourArray)


def main():
    args = get_args()
    app.config["SERVER_NAME"] = "127.0.0.1:"+str(args.port)
    app.config["DEBUG"] = args.debug
    app.run()

if __name__ == "__main__":
    main()
