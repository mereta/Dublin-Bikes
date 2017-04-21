import argparse
from datetime import datetime
import decimal
import json

from flask import Flask, render_template, url_for, request
from flask_googlemaps import GoogleMaps, Map

from _symtable import FREE

try:
    import LoadJSONdata
    import dynamo
except ImportError:
    # when installed, import like this works
    from . import LoadJSONdata
    from . import dynamo


def get_args():
    """all the argparse stuff.
    params:  -
    returns: namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", type=str)
    parser.add_argument("--port", dest="port", type=int)
    parser.add_argument("--debug", dest="debug", action="store_true")
    parser.set_defaults(host="127.0.0.1")
    parser.set_defaults(port=5000)
    parser.set_defaults(debug=False)
    return parser.parse_args()


# Flask likes to know the name of the script calling it.
app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyD6QVQToPw7ZOngdE5aJCmFczRpLSGh4-U"
GoogleMaps(app)


def get_icon_url(available_bikes, total_bike_stands):
    """ Returns colour based on percentage occupancy:
     0% Purple
     1-25% Red
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
    if pcnt < 26:
        return base_url + "red-dot.png"
    if pcnt < 51:
        return base_url + "orange-dot.png"
    if pcnt < 76:
        return base_url + "yellow-dot.png"
    if pcnt <= 100:
        return base_url + "green-dot.png"


@app.route("/")
def index():
    '''This method retrieves data from the Dublin Bikes API, it itterates through the data
    and presents markers on a google map'''

    mydata = LoadJSONdata.GetLocationData()

    sndmap = Map("sndmap", mydata[0]["position"]["lat"], mydata[0]
                 ["position"]["lng"], style="height:500px;")
    for obj in mydata:
        name = obj["name"]
        lat = str(obj["position"]["lat"])
        time_stamp = obj['last_update']
        lng = str(obj["position"]["lng"])
        free = obj['available_bikes']
        available_bike_stands = obj['available_bike_stands']
        total_bike_stands = obj['bike_stands']

    # Code reference: https://github.com/rochacbruno/Flask-GoogleMaps
        sndmap.markers.append({'icon': get_icon_url(free, total_bike_stands), 'lat': lat, 'lng': lng,
                               'infobox': "<b>Name: " + name + "</b></br>Available Bikes: " + str(free) + "</br>Available Bike Stands: " + str(available_bike_stands) + '''<br><a onclick="drawChart(' ''' + str(name) + ''' ')" href=#>Occupancy Details</a></br>'''})

    return render_template("index.html", sndmap=sndmap)

# get daily data


@app.route("/getdailychartdata", methods=['POST'])
def getDailyChartData():
    '''This function gets daily data back from the database based on a single location
        This function returns the following:
        DayOfWeek, %Available Bikes, %Available Bike Stands
        in JSON format'''

    # Gets location from the form and queries database based on location
    # clicked for all records
    location = request.form['location'].strip()
    data = dynamo.QueryByLocation(location)

    # Initialize arrays
    #[0]th = 1-7 corresponding to weekday
    #[1]st = total free bikes
    #[2]nd = total available bike stands
    #[3]rd = total of all entries needed to get the mean
    dayArray = []

    # weekdayArray :
    #[0]th = Sunday/Monday etc.
    #[1]st = average percentage of free bikes per station
    #[2]nd = average percentage of available bike stands per station
    weekdayArray = [['Sunday', 0, 0], ['Monday', 0, 0], ['Tuesday', 0, 0], [
        'Wednesday', 0, 0], ['Thursday', 0, 0], ['Friday', 0, 0], ['Saturday', 0, 0]]

    # In dayArray creates 7 sub-arrays with 4 elements, first element being
    # 1-7 corresponding to day of week in each sub-array
    for i in range(1, 7 + 1):
        dayItem = [i, 0, 0, 0]
        dayArray.append(dayItem)

    # Iterate through data
    for i in data["Items"]:
        dayOfWeek = datetime.fromtimestamp(
            int(i["time_stamp"]) / 1000).strftime('%w'),
        free = int(i['free'])
        available_bike_stands = int(i['available_bike_stands'])
        total_bike_stands = int(i['bike_stands'])

        # add record to running total, sums available bikes and sums available
        # bikes stands per day of week

        # uses day array with element 0 = day of week(1-7) - Sunday-Saturday
        #[0] = day of week, [1] = total of all free bikes/per station
        #[2] = total of all available bike stands per station, [3] = total number of entries for that station
        dayArray[int(dayOfWeek[0][0])][3] = dayArray[int(
            dayOfWeek[0][0])][3] + 1
        dayArray[int(dayOfWeek[0][0])][1] = dayArray[int(
            dayOfWeek[0][0])][1] + free
        dayArray[int(dayOfWeek[0][0])][2] = dayArray[int(
            dayOfWeek[0][0])][2] + available_bike_stands

    # Get average & calculate percentages of available bikes/bike stands
    # sort by [0]th element, [3] = total entries
    #[1]st entry = total free bikes/ total entries gives you mean, then divide by total bike stands
    # per that station and multiply by 100 to give (average) percentage of free bikes --> write to weekdayArray
    # [2]nd entry = total available bike stands/ total entries gives you mean, then divide by total bike stands
    # per that station and multiply by 100 to give (average) percentage of available bike stands --> write to weekdayArray
    # [0]th entry from day array matches to 'Sunday' 'Monday' etc via 1-7 correlation in weekdayArray
    for i in range(0, 7):
        weekdayArray[i][1] = int(
            ((dayArray[i][1] / dayArray[i][3]) / total_bike_stands) * 100)  # free bikes
        weekdayArray[i][2] = int(
            ((dayArray[i][2] / dayArray[i][3]) / total_bike_stands) * 100)  # available bike stnds

    return json.dumps(weekdayArray)


@app.route("/gethourlychartdata", methods=['POST'])
def getHourlyChartData():
    '''This function gets hourly data back from the database based on a single location
        This function returns the following:
        Hour, %Available Bikes, %Available Bike Stands
        in JSON format'''
    # Gets location from the form and queries database based on location
    # clicked for all records
    location = request.form['location'].strip()
    data = dynamo.QueryByLocation(location)

    # Initialize arrays
    hourArray = []
    #[0]th = 1-24 corresponding tp hour
    #[1]st = total free bikes
    #[2]nd = total available bike stands
    #[3]rd = total of all entries needed to get the mean
    finalHourArray = []
    #[0]th = hour
    #[1]st = average percentage of free bikes per station
    #[2]nd = average percentage of available bike stands per station

    # creates 24 sub-arrays for both hourArray & finalHourArray
    # adds hour as [0]th element in all sub-arrays in both hourArray and
    # finalHourArray

    for i in range(1, 24 + 1):
        hourItem = [i, 0, 0, 0]
        finalHourItem = [i, 0, 0]
        hourArray.append(hourItem)
        finalHourArray.append(finalHourItem)

    # Iterate through data
    for i in data["Items"]:

        hour = int(datetime.fromtimestamp(
            int(i["time_stamp"]) / 1000).strftime('%H'))
        free = int(i['free'])
        available_bike_stands = int(i['available_bike_stands'])
        total_bike_stands = int(i['bike_stands'])

        # Add record to running total, sum all available bikes/bike stands
        # uses hourArray with element 0 = corresponding to hour of day (1-24)
        #[0] = hour, [1] = total of all free bikes/per station
        #[2] = total of all available bike stands per station, [3] = total number of entries for that station
        hourArray[hour][3] = hourArray[hour][3] + 1
        hourArray[hour][1] = hourArray[hour][1] + free
        hourArray[hour][2] = hourArray[hour][2] + available_bike_stands

    # Get average & calculate percentages of available bikes/bike stands

    # sort by [0]th element, [3] = total entries
    #[1]st entry = total free bikes/ total entries gives you mean, then divide by total bike stands
    # per that station and multiply by 100 to give (average) percentage of free bikes --> write to weekdayArray
    # [2]nd entry = total available bike stands/ total entries gives you mean, then divide by total bike stands
    # per that station and multiply by 100 to give (average) percentage of
    # available bike stands --> write to weekdayArray
    for i in range(0, 24):
        finalHourArray[i][1] = int(
            ((hourArray[i][1] / hourArray[i][3]) / total_bike_stands) * 100)  # free bikes
        finalHourArray[i][2] = int(
            ((hourArray[i][2] / hourArray[i][3]) / total_bike_stands) * 100)  # available bike stands

    return json.dumps(finalHourArray)


def main():
    args = get_args()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
