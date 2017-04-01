import boto3


def query_table(table_name, query):
    """Query the database. 
    Return all results that contain all the corresponding key-value pairs
    contained in query.
    params :
        table_name : STRING name of the table to use.
        query      : DICTIONARY
    returns:
        LIST of DICTIONARIES, or NONE
    """
    raise NotImplementedError("This function hasn't been implimented.")
