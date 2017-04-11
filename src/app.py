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
    
    #data = functions.scan("name", "eq", "SMITHFIELD NORTH", None)
    #print(data)
    #data = functions.scan("name", "eq", "JAMES STREET EAST", None)
    #data = functions.scan("name", "eq", "DAME STREET", None)
    #data = functions.QueryByLocation("JAMES STREET EAST")
    #print(data)

    
    #data = functions.querry("TALBOT STREET", )
    #print(data)
    
    
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
         
        #print(name)  
        #print(total_bike_stands)
          
    #Code reference: https://github.com/rochacbruno/Flask-GoogleMaps
    
        
        #print(marker_file)
        sndmap.markers.append({'icon':get_icon_url(free, total_bike_stands), 'lat': lat, 'lng': lng,
                              'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands) + '''<a onclick="drawChart(' '''  + str(name) + ''' ')" href=#>More Details</a>'''})
      
    #print(sndmap.markers)   
    return render_template("index.html", sndmap=sndmap)

@app.route("/getchartdata", methods=['POST'])
def getChartData():
    location = request.form['location'].strip()
    print("FINDME",location)
    data = functions.QueryByLocation(location)
    
    dayArray= [['Sunday', 0], ['Monday', 0], ['Tuesday', 0], ['Wednesday', 0], ['Thursday', 0], ['Friday', 0], ['Saturday', 0]]
    myArray = []

        
    
    for i in data["Items"]:
        #print(i["name"], "| free bikes |", i["free"], "| bike stands |", i["bike_stands"], "| free bike stands |", i["available_bike_stands"], "|", 
              
        day = datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%d'),
        month = datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%m'),
        year = datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%Y'),
        dayOfWeek = datetime.fromtimestamp(int(i["time_stamp"]) / 1000).strftime('%a'),
        free = int(i['free'])
        available_bike_stands = int(i['available_bike_stands'])
        total_bike_stands = int(i['bike_stands'])
        
        item=[dayOfWeek, free, available_bike_stands]
        myArray.append(item)
    #print (myArray)
    
    mondayTotal, tuesdayTotal, wednesdayTotal, thursdayTotal, fridayTotal, saturdayTotal, sundayTotal, = 0, 0, 0, 0, 0, 0, 0
    mondayFree, tuesdayFree, wednesdayFree, thursdayFree, fridayFree, saturdayFree, sundayFree, =  0, 0, 0, 0, 0, 0, 0
    mondayAvStands, tuesdayAvStands, wednesdayAvStands, thursdayAvStands, fridayAvStands, saturdayAvStands, sundayAvStands, =  0, 0, 0, 0, 0, 0, 0
    mondayFreeMean, tuesdayFreeMean, wednesdayFreeMean, thursdayFreeMean, fridayFreeMean, saturdayFreeMean, sundayFreeMean, = 0, 0, 0, 0, 0, 0, 0
    mondayAvStandsMean, tuesdayAvStandsMean, wednesdayAvStandsMean, thursdayAvStandsMean, fridayAvStandsMean, saturdayAvStandsMean, sundayAvStandsMean, = 0, 0, 0, 0, 0, 0, 0
    
    for j in myArray:
        #print("JAY", j[0])
        #print("JAY ZERO ZERO", j[0][0])
       
        if j[0][0] == "Sun":
           sundayTotal = sundayTotal +1
           sundayFree = sundayFree + j[1]
           sundayAvStands = sundayAvStands + j[2]
        if j[0][0] == "Mon":
           mondayTotal = mondayTotal +1
           mondayFree = mondayFree + j[1]
           mondayAvStands = mondayAvStands + j[2]
        if j[0][0] == "Tue":
           tuesdayTotal = tuesdayTotal +1
           tuesdayFree = tuesdayFree + j[1]
           tuesdayAvStands = tuesdayAvStands + j[2]
        if j[0][0] == "Wed":
           wednesdayTotal = wednesdayTotal +1
           wednesdayFree = wednesdayFree + j[1]
           wednesdayAvStands = wednesdayAvStands + j[2]
        if j[0][0] == "Thu":
           thursdayTotal = thursdayTotal +1
           thursdayFree = thursdayFree + j[1]
           thursdayAvStands = thursdayAvStands + j[2]
        if j[0][0] == "Fri":
           fridayTotal = fridayTotal +1
           fridayFree = fridayFree + j[1]
           fridayAvStands = fridayAvStands + j[2]
        if j[0][0] == "Sat":
           saturdayTotal = saturdayTotal +1
           saturdayFree = saturdayFree + j[1]
           saturdayAvStands = saturdayAvStands + j[2]
    #print("RESULTS", sundayTotal, sundayFree, sundayAvStands)
    #do stuff 
    #return json.dumps(data);
    sundayFreePcnt = int(((sundayFree/sundayTotal)/total_bike_stands)*100)
    mondayFreePcnt = int(((mondayFree/mondayTotal)/total_bike_stands)*100)
    tuesdayFreePcnt = int(((tuesdayFree/tuesdayTotal)/total_bike_stands)*100)
    wednesdayFreePcnt = int(((wednesdayFree/wednesdayTotal)/total_bike_stands)*100)
    thursdayFreePcnt = int(((thursdayFree/thursdayTotal)/total_bike_stands)*100)
    fridayFreePcnt = int(((fridayFree/fridayTotal)/total_bike_stands)*100)
    saturdayFreePcnt = int(((saturdayFree/saturdayTotal)/total_bike_stands)*100)
    
    print("SUN%", (sundayFreePcnt))
    
    sundayAvStandsMean = sundayAvStands/sundayTotal
    mondayAvStandsMean = mondayAvStands/mondayTotal
    tuesdayAvStandsMean = tuesdayAvStands/tuesdayTotal
    wednesdayAvStandsMean = wednesdayAvStands/wednesdayTotal
    thursdayAvStandsMean = thursdayAvStands/thursdayTotal
    fridayAvStandsMean = fridayAvStands/fridayTotal
    saturdayAvStandsMean = saturdayAvStands/saturdayTotal
    
    dayArray[0][1] = int(sundayFreePcnt)
    dayArray[1][1] = int(mondayFreePcnt)
    dayArray[2][1] = int(tuesdayFreePcnt)
    dayArray[3][1] = int(wednesdayFreePcnt)
    dayArray[4][1] = int(thursdayFreePcnt)
    dayArray[5][1] = int(fridayFreePcnt)
    dayArray[6][1] = int(saturdayFreePcnt)
    
    #print("ARRAY", dayArray)
    
    return json.dumps(dayArray)

    
    #(available_bikes / total_bike_stands) * 100


def main():
    args = get_args()
    app.config["SERVER_NAME"] = "127.0.0.1:"+str(args.port)
    app.config["DEBUG"] = args.debug
    app.run()

if __name__ == "__main__":
    main()
