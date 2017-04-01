from flask import Flask, render_template, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import LoadJSONdata

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
        
        if free > 0:
    #Code reference: https://github.com/rochacbruno/Flask-GoogleMaps
            sndmap.markers.append({ 'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': lat,
            'lng': lng,
            'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands) })
        else:
            sndmap.markers.append({ 'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
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
