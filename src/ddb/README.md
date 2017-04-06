# ddb
DynamoDB querry package
To install use pip install git+

## To import use:
### from dbb import functions

## To run  a querry use:
### functions.querry(primary_key, sort_key)

    Querry finds rows with specified primary key and sort key values
    is faster because doesn't scan through the whole table, returns python dictionary
    
    primary key = "name"
    sort_key = time_stamp
    
    example querry("JAMES STREET EAST",1490979662000)
    
## To scan the table for specific attribute values use:
### functions.scan(key, condition, value, value2)

    Scan let's to choose key attribute and value for filtering the results. Returns a python dictionary

    +    key - name of the attribute, 
    +    value - attribute value, if empty write None
    +    condition - condition for comparison
    +    value2 - high value for condition between, if empty, write None

    valid conditions:
        - eq(value)     =
        - between(low_value, high_value)
        - exists()
    example def scanAll():
    "Returns whole table as python dictionary "
    response = table(connect()).scan(Select='ALL_ATTRIBUTES')
    printResp(response)
    return response
    
	example  scan("number", "eq", 16, None) returns Number of station equal to 16 

## To scan whole table use:
### scanAll()

	returns contents of whole table as a python dictionary
	
	

	

