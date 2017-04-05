import argparse

from flask import Flask, render_template, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

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
    parser.set_defaults(port=80)
    parser.set_defaults(debug=False)
    return parser.parse_args()

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
    args = get_args()
    app.config["SERVER_NAME"] = "127.0.0.1:"+str(args.port)
    app.config["DEBUG"] = args.debug
    app.run()

if __name__ == "__main__":
    main()
