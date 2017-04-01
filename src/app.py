from flask import Flask, render_template, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import LoadJSONdata
import decimal

try:
    # when running locally...
    import config
except ImportError:
    # when installed and running from the command line...
    from . import config

# Flask likes to know the name of the script calling it.
app = Flask(__name__)
GoogleMaps(app)


@app.route("/")
def index():

  
  
    mydata = LoadJSONdata.GetLocationData()
    
    sndmap = Map("sndmap",mydata[0]["position"]["lat"], mydata[0]["position"]["lng"], style="height:600px;width:600px;margin:0;")
    for obj in mydata:
        name = obj["name"]
        address = obj["address"]
        lat = str(obj["position"]["lat"])
        time_stamp = obj['last_update']
        lng = str(obj["position"]["lng"])
        free = obj['available_bikes']
        number = obj["number"]
        bike_stands = obj["bike_stands"]
        available_bike_stands = obj['available_bike_stands']
        
        
    
        sndmap.markers.append({ 'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': lat,
             'lng': lng,
             'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands) })

    print(sndmap.markers)   
    return render_template("index.html", sndmap=sndmap)


def main():
    app.config.from_object(config.DevelopmentConfig)
    app.run()

if __name__ == "__main__":
    main()
