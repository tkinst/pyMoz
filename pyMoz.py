import requests
import json

class HTTPException(Exception):
    pass # figure this out later

class Mozenda:

    def __init__(self, api_key, api_version='Mozenda10', debug=False):
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = "https://api.mozenda.com/rest"
        self.debug = debug
        # self.base_url = "https://api.mozenda.com/rest?WebServiceKey=" + self.api_key + "&Service=" + self.api_version

        self.url_dict = {'Service':api_version, 'WebServiceKey':api_key}


    """ COLLECTIONS """

    def add_collection(self, name, description=None):
        '''Adds an empty collection in your account.'''
        payload = {
            "Name" : name, 
            "Description" : description,
            "Operation" : "Collection.Add"
            }

        return self.send_req(payload)


    def add_item_to_collection(self, collection_id, fields=None):
        '''Adds an item to a collection with the values specified.
           Optional dictionary "fields" allows you to add fields to the item.'''

        payload = {
            "CollectionID" : collection_id,
            "Operation" : "Collection.AddItem"
        }

        for eachKey in fields:
            tempKey = "Field." + eachKey
            payload[tempKey] = fields[eachKey]

        return self.send_req(payload)


    def add_field_to_collection(self, collection_id, name, description=None):
        '''Adds a field to the desired collection'''

        payload = {
            "CollectionID": collection_id,
            "Field" : name,
            "FieldDescription" : description,
            "Operation" : "Collection.AddField"
        }

        return self.send_req(payload)


    def clear_collection(self, collection_id, retain=False):

        payload = {
            "CollectionID" : collection_id,
            "RetainCollectionHistory" : retain,
            "Operation" : "Collection.Clear"
        }

        return self.send_req(payload)


    def delete_collection(self, collection_id):
        payload = {
            "CollectionID" : collection_id,
            "Operation" : "Collection.Delete"
        }

        return self.send_req(payload)


    def delete_field_from_collection(self, collection_id, field):
        payload = {
            "CollectionID" : collection_id,
            "Field" : field,
            "Operation" : "Collection.DeleteField"
        }

        return self.send_req(payload)


    def delete_item_from_collection(self, collection_id, item_id):
        payload = {
            "CollectionID" : collection_id,
            "ItemID" : item_id,
            "Operation" : "Collection.DeleteItem"
        }

        return self.send_req(payload)


    def get_fields_from_collection(self, collection_id, include="All"):
        payload = {
            "CollectionID" : collection_id,
            "Include" : include,
            "Operation" : "Collection.GetFields"
        }

        return self.send_req(payload)


    def get_list_of_collections(self):
        payload = {
            "Operation" : "Collection.GetList"
        }

        return self.send_req(payload)


    def get_views_from_collection(self, collection_id):
        payload = {
            "CollectionID" : collection_id,
            "Operation" : "Collection.GetViews"
        }

        return self.send_req(payload)


    def update_field(self, collection_id, field_id, description=None, format=None, name=None):
        payload = {
            "CollectionID" : collection_id,
            "FieldID" : field_id,
            "Description" : description,
            "Format" : format,
            "Name" : name,
            "Operation" : "Collection.UpdateField"
        }

        return self.send_req(payload)


    def update_item(self, collection_id, item_id, fields=None):
        payload = {
            "CollectionID" : collection_id,
            "ItemID" : item_id,
            "Operation" : "Collection.UpdateItem"
        }

        for eachKey in fields:
            tempKey = "Field." + eachKey
            payload[tempKey] = fields[eachKey]

        return self.send_req(payload)



    """ INTERNAL FUNCS """
    def send_req(self, payload):
        payload.update(self.url_dict) # adds the api key to the request
        r = requests.get(self.base_url, params=payload) #send the request
        if self.debug:
            print r.url
            print payload
        if r.status_code == 200:
            return r.text
        else:
            return self.get_status_error(r.status_code)


    def get_status_error(self, status):
        if status == 400:
            raise HTTPException("400 Error - Bad Request")
        elif status == 401:
            raise HTTPException("401 Error - Invalid URL")
        elif status == 404:
            raise HTTPException("404 Error - Summoner Not Found")
        elif status == 500:
            raise HTTPException("500 Error - Internal Server Error")
        else:
            raise HTTPException(str(status) + " Error - Unknown")