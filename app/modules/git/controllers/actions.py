import traceback
from flask import request, jsonify, json
from datetime import datetime, timezone
from app.modules.git.models.actions import create, latest

#################################################################
# Using three separate webhooks (push, pull, merge)
#   - Each webhook handles exactly one GitHub event.
#   - The receiver code can be simpler and focused only on logic for that event.
#   - Easily identify which event cause issue
#   - Logs and payloads are clearly separated
#   - easy to redirect respective action to different targets
# 
# However, it is also can be handled as 
#    if event == "push":
#        handle_push()
#    elif event == "pull_request":
#        handle_pr()
#    elif event == "merge":
#        handle_merge()
#################################################################

# capture PULL action on repository
def pull():
    try:
        # Check Content-Type header 
        content_type = request.headers.get('Content-Type', '')
        
        if not content_type.startswith('application/json'):
            return jsonify({
                "error": "Unsupported Content-Type. Expected application/json."
            }), 415  # HTTP 415 Unsupported Media Type

        # Parse JSON body
        data = request.get_json()  # it is equivalent to request.json

        # Check valid pull request
        if not data or "pull_request" not in data:
            return jsonify({
                "error": "Pull: Invalid request"
            }), 400  # 400 bad request

        doc = {
            "request_id": str(data["pull_request"]["id"]),
            "author": data["pull_request"]["user"]["login"],
            "action": "PULL",  # or "PULL_REQUEST" based on your design
            "from_branch": data["pull_request"]["head"]["ref"],
            "to_branch": data["pull_request"]["base"]["ref"],
            "timestamp": datetime.now(timezone.utc)
        }

        # Create a documnet in collection
        id = create(doc)

    except Exception as e:
        return jsonify({
            "action":"merge",
            "error": str(e),
            "stacktrace": traceback.format_exc()
        }), 500  # 500 = Internal Server Error
    
    return jsonify({
            "id": str(id)
        }), 200  # 200 = Success

# capture PUSH action on rpository
def push():

    try:
        # Check Content-Type header 
        content_type = request.headers.get('Content-Type', '')
        
        if not content_type.startswith('application/json'):
            return jsonify({
                "error": "Unsupported Content-Type. Expected application/json."
            }), 415  # HTTP 415 Unsupported Media Type

        # Parse JSON body
        data = request.get_json()  # it is equivalent to request.json

        # Check valid push request
        if not data or ("head_commit" not in data or "repository" not in data):
            return jsonify({
                "error": "Push: Invalid request"
            }), 400  # 400 bad request

        doc = {
            "request_id": str(data["head_commit"]["id"]),       # use commit SHA as request_id
            "author": data["pusher"]["name"],                   # pusher name
            "action": "PUSH",                                   # "PUSH" for push events
            "from_branch": data["ref"].replace("refs/heads/", ""),  # remove 'refs/heads/' prefix
            "to_branch": data["repository"]["default_branch"],  # usually "main" or "master"
            "timestamp": str(datetime.now(timezone.utc))              # current UTC datetime
        }

        # Create a documnet in collection
        id = create(doc)
    
    except Exception as e:
        return jsonify({
            "action":"push",
            "error": str(e),
            "stacktrace": traceback.format_exc()
        }), 500  # 500 = Internal Server Error
    
    return jsonify({
            "id": str(id)
        }), 200  # 200 = Success

# capture MERGE action on rpository
def merge():

    try:
        # Check Content-Type header 
        content_type = request.headers.get('Content-Type', '')
        
        if not content_type.startswith('application/json'):
            return jsonify({
                "error": "Unsupported Content-Type. Expected application/json."
            }), 415  # HTTP 415 Unsupported Media Type

        # Parse JSON body
        data = request.get_json()  # it is equivalent to request.json

        # Check valid merge request
        if not data or ("head_commit" not in data and "base_ref" not in data and "ref" not in data):
            return jsonify({
                "error": "Merge: Invalid request"
            }), 400  # 400 bad request

        doc = {
            "request_id": str(data["head_commit"]["id"]),           # use latest commit id as request_id
            "author": data["pusher"]["name"],                       # name of the person who pushed / merged
            "action": "MERGE",                                      # action type is MERGE
            "from_branch": data["base_ref"].replace("refs/heads/", ""),  # source branch before merge
            "to_branch": data["ref"].replace("refs/heads/", ""),    # target branch after merge
            "timestamp": datetime.now(timezone.utc)
        }
        
        # Create a documnet in collection
        id = create(doc)

    except Exception as e:
        return jsonify({
            "action":"merge",
            "error": str(e),
            "stacktrace": traceback.format_exc()
        }), 500  # 500 = Internal Server Error
    
    return jsonify({
            "id": str(id)
        }), 200  # 200 = Success

# return latest actions
def list():

    # last 10 records 
    limit = 10

    try:
        # Create a documnet in collection
        latest_entries = latest(limit)

    except Exception as e:
        return jsonify({
            "action":"list",
            "error": str(e),
            "stacktrace": traceback.format_exc()
        }), 500  # 500 = Internal Server Error
    
    return jsonify({
            "actions": latest_entries
        }), 200  # 200 = Success