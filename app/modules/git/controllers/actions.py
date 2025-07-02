from flask import request, jsonify, json
from datetime import datetime, timezone
from app.modules.git.models import create

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
    # Check Content-Type header 
    content_type = request.headers.get('Content-Type', '')
    
    if not content_type.startswith('application/json'):
        return jsonify({
            "error": "Unsupported Content-Type. Expected application/json."
        }), 415  # HTTP 415 Unsupported Media Type

    # Parse JSON body
    data = request.get_json()  # it is equivalent to request.json

    doc = {
        "request_id": str(data["pull_request"]["id"]),
        "author": data["pull_request"]["user"]["login"],
        "action": "PULL",  # or "PULL_REQUEST" based on your design
        "from_branch": data["pull_request"]["head"]["ref"],
        "to_branch": data["pull_request"]["base"]["ref"],
        "timestamp": datetime.now(timezone.utc)
    }

    create(doc)

    # Dump to string for debugging / or return as response
    # it is also available in sys log
    dump = json.dumps(data)
    print(dump)

    return dump, 200

# capture PUSH action on rpository
def push():
    # Check Content-Type header 
    content_type = request.headers.get('Content-Type', '')
    
    if not content_type.startswith('application/json'):
        return jsonify({
            "error": "Unsupported Content-Type. Expected application/json."
        }), 415  # HTTP 415 Unsupported Media Type

    # Parse JSON body
    data = request.get_json()  # it is equivalent to request.json

    doc = {
        "request_id": str(data["head_commit"]["id"]),       # use commit SHA as request_id
        "author": data["pusher"]["name"],                   # pusher name
        "action": "PUSH",                                   # "PUSH" for push events
        "from_branch": data["ref"].replace("refs/heads/", ""),  # remove 'refs/heads/' prefix
        "to_branch": data["repository"]["default_branch"],  # usually "main" or "master"
        "timestamp": datetime.now(timezone.utc)             # current UTC datetime
    }

    create(doc)

    # Dump to string for debugging / or return as response
    dump = json.dumps(data)
    print(dump)

    return dump, 200

# capture MERGE action on rpository
def Merge():
    # Check Content-Type header 
    content_type = request.headers.get('Content-Type', '')
    
    if not content_type.startswith('application/json'):
        return jsonify({
            "error": "Unsupported Content-Type. Expected application/json."
        }), 415  # HTTP 415 Unsupported Media Type

    # Parse JSON body
    data = request.get_json()  # it is equivalent to request.json

    doc = {
        "request_id": str(data["head_commit"]["id"]),           # use latest commit id as request_id
        "author": data["pusher"]["name"],                       # name of the person who pushed / merged
        "action": "MERGE",                                      # action type is MERGE
        "from_branch": data["base_ref"].replace("refs/heads/", ""),  # source branch before merge
        "to_branch": data["ref"].replace("refs/heads/", ""),    # target branch after merge
        "timestamp": datetime.now(timezone.utc)
    }
    create(doc)
    # Dump to string for debugging / or return as response  
    dump = json.dumps(data)
    print(dump)

    return dump, 200