# /ai4e_api_tools has been added to the PYTHONPATH, so we can reference those
# libraries directly.
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from ai4e_app_insights import AppInsights
from ai4e_app_insights_wrapper import AI4EAppInsights
from ai4e_service import AI4EWrapper
import sys
from os import getenv

import api_controller

blob_mapped_dir = "/mnt/output"

print("Creating Application")

api_prefix = getenv('API_PREFIX')
app = Flask(__name__)

api = Api(app)
print(api_prefix)

# Log requests, traces and exceptions to the Application Insights service
appinsights = AppInsights(app)

# Use the AI4EAppInsights library to send log messages.
log = AI4EAppInsights()

# The API4EWrapper instruments your functions so that trace metrics are logged.
ai4e_wrapper = AI4EWrapper(app)

# Healthcheck endpoint - this lets us quickly retrieve the status of your API.
@app.route('/', methods=['GET'])
def health_check():
    return "Health check OK"

# POST, sync API endpoint example
@app.route(api_prefix + '/', methods=['POST'])
def post():
    try:
        post_body = json.loads(request.data)
    except:
        return "Unable to parse the request body. Please request with valid json."

    # wrap_sync_endpoint wraps your function within a logging trace.
    return ai4e_wrapper.wrap_sync_endpoint(get_streamflow, "post:get_streamflow", json_body = post_body)
    # return jsonify(get_streamflow())

def get_streamflow(**kwargs):
    json_body = kwargs.get('json_body', None)
    if (not json_body):
        log.log_error("Body is missing")
        return -1

    if (not "region" in json_body):
        log.log_error("region is required as input.")
        return -1

    if (not "reach_id" in json_body):
        log.log_error("reach_id is required as input.")
        return -1

    try:
        # Extract the img_url input from the json body
        request = {"region": json_body["region"], "reach_id": json_body["reach_id"],
                   "stat": json_body["stat"], "return_format": json_body["return_format"]}

        # if (json_body["stat"]):
        #     request["stat"] = json_body["stat"]
        # if (json_body["date"]):
        #     request["date"] = json_body["date"]
        # if (json_body["units"]):
        #     request["units"] = json_body["units"]
        # else:
        #     request["units"] = ''
        #
        # if (json_body["return_format"]):
        #     request["return_format"] = json_body["return_format"]

        # Here's how to debug
        log.log_debug(json_body["region"], json_body["reach_id"])

        # Call the service endpoint
        results = api_controller.get_ecmwf_forecast(request)

        return results

        # # Construct the predictions for output
        # ret = []
        # for prediction in results.predictions:
        #     pred = {}
        #     pred['prediction'] = prediction.tag_name
        #     pred['confidence'] = "{0:.2f}%".format(prediction.probability * 100)
        #     ret.append(pred.copy())
        #
        # # Format and return output
        # return json.dumps(ret)
    except:
        print(sys.exc_info()[0])
        log.log_exception(sys.exc_info()[0])
        return "An unexpected error occured"

if __name__ == '__main__':
    app.debug = True
    app.run()
