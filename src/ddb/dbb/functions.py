'''
Created on 30 Mar 2017

@author: liga
'''
from datetime import datetime
import src.ddb.dbb.config as conf
import boto3
from boto3.dynamodb.conditions import Key, Attr


def connect():
    db = boto3.resource('dynamodb',
                        aws_access_key_id=conf.ACESS_KEY,
                        aws_secret_access_key=conf.SECRET_KEY,
                        region_name="eu-west-1"
                        )
    return db


def table(db):
    table = db.Table('DublinBikes')
    return table


def printResp(response):
    for i in response["Items"]:
        print(i["name"], "| free bikes |", i["free"], "| bike stands |", i["bike_stands"], "| free bike stands |", i["available_bike_stands"], "|", datetime.fromtimestamp(int(
            i["time_stamp"]) / 1000).strftime('%H:%M:%S %d.%m.%Y'),
        )


def queryEq(station_name, time):
    """Querry finds rows with specified primary key and sort key values
    is faster because doesn't scan through whole table, returns python dictionary"""

    response = table(connect()).query(
        KeyConditionExpression=Key('name').eq(station_name) & Key(
            "time_stamp").eq(time),
    )
    printResp(response)
    return response


def queryBetween(station_name, time_from, time_to):
    "Returns query for specified station name and time from and to. Returns a dictionary"

    response = table(connect()).query(
        KeyConditionExpression=Key('name').eq(station_name) & Key(
            'time_stamp').between(time_from, time_to)
    )
    printResp(response)
    return response


def scan(key, condition, value, value2):
    """Scan let's to choose key attribute and value for filtering the results. Returns a python dictionary

    +    key - name of the attribute, 
    +    value - attribute value, 
    +    condition - condition for comparison
    +    value2 - high value for condition between, if empty, write None

    valid conditions:
        - eq(value)     =
        - between(low_value, high_value)
        - exists()
        """
    # filter expressions
    if condition == "eq":
        fe = Attr(key).eq(value)
    elif condition == "exists":
        fe = Attr(key).exists()
    elif condition == "between":
        fe = Attr(key).between(value, value2)

    response = table(connect()).scan(
        FilterExpression=fe,
    )

    while 'LastEvaluatedKey' in response:
        response = table(connect()).scan(
            FilterExpression=fe,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        printResp(response)
    return response


def scanAll():
    "Returns whole table as python dictionary "

    response = table(connect()).scan(Select='ALL_ATTRIBUTES')
    while 'LastEvaluatedKey' in response:
        response = table(connect()).scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        printResp(response)
    return response


#scan("name", "eq", "DAME STREET", None)
#queryEq("DAME STREET", 1490903091000)
# scanAll()
