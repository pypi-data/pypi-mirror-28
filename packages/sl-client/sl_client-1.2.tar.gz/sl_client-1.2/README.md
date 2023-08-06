# ServiceLayerClient-python
## Purpose
Connecting to the Studyportals ServiceLayer using Studyportals reflector and retrieving data.

## Prerequisite working on it 
Run `pip install -r requirements.txt` to install all the needed packages for development
## Installation
Run `pip install sl_client` to install the package for usage
## How does it work?
Create ServiceLayer client with parameters:
* `reflector_url` - reflector url
* `path` - path in the ServiceLayer that you want to reach
* `sentinel_url` - sentinel url with a token which is allowed to reach the path in the ServiceLayer
* `request_headers` - request headers for the ServiceLayer request

ServiceLayer client can do two things:    
* `fetch_data` - fetches data from the ServiceLayer with specified request parameters or no parameters at all e.g.
    * `sl_client.fetch_data()`
    * `sl_client.fetch_data('q=id-5')`
    * `sl_client.fetch_data('q=id-5|oi-20,50')`
    
    Returns data as a list of dictionaries or a plain json if it is not parsable to dictionaries.
* `test_query_connection` - tests a connection to the ServiceLayer path with specific request parameters or no parameters at all.
Returns an amount of results or an error if the connection failed.