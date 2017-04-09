from flask import Flask, render_template, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import LoadJSONdata
from dbb import functions
from _symtable import FREE

try:
    # when running locally...
    import config
except ImportError:
    # when installed and running from the command line...
    from . import config

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
    data = functions.scan("name", "eq", "DAME STREET", None)

    
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
                              'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands)})
      
    #print(sndmap.markers)   
    return render_template("index.html", sndmap=sndmap)


def main():
    app.config.from_object(config.DevelopmentConfig)
    app.run()

if __name__ == "__main__":
    main()
