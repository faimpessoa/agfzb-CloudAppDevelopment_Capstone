import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = ""
    if "apikey" in kwargs:
        api_key = kwargs["apikey"]
        try:
            print(f"With key:{api_key}")
            # Call get method of requests library with URL and parameters
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(f"With jsonData: {json_data}")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print("POST to {} ".format(url))
    print(f"Payload: {payload}")
    print(f"Args: {kwargs}")
    api_key = ""
    if "apikey" in kwargs:
        api_key = kwargs["apikey"]
        try:
            print(f"With key:{api_key}")
            # Call get method of requests library with URL and parameters
            response = requests.post(url, params=kwargs, json=payload,
                                        auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            print("Posting...")
            response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, json=payload)
            print("Posting... done.")
        except:
            # If any error occurs
            print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(f"With jsonData: {json_data}")
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=kwargs['id'])
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        for dealer_review in json_result:
            # Get its content in `doc` object
            review_doc = dealer_review
            sent = analyze_review_sentiments(review_doc["review"])
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment=sent,
                id=review_doc["id"])
            
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/96afe15a-80ff-48b2-95b5-e904a60a7601/v1/analyze"
    #apikey = "UWmQfDNS8ciMNOavBOXgv4zzJEaaW7sr6XgpBrkkBjzf"
    #version = "2019-04-07"
    json_result = get_request(url, version = "2019-04-07", text=text, features="sentiment",
                       apikey = "UWmQfDNS8ciMNOavBOXgv4zzJEaaW7sr6XgpBrkkBjzf")
    ret = "No Result"
    if json_result and "sentiment" in json_result \
       and "document" in json_result["sentiment"] \
       and "label" in json_result["sentiment"]["document"]:
        ret = json_result["sentiment"]["document"]["label"]
    
    return ret


