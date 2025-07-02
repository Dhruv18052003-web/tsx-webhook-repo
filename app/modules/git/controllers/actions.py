from flask import request, jsonify, json

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

# capture PULL action on rpository
def pull():
    # Check Content-Type header 
    content_type = request.headers.get('Content-Type', '')
    
    if not content_type.startswith('application/json'):
        return jsonify({
            "error": "Unsupported Content-Type. Expected application/json."
        }), 415  # HTTP 415 Unsupported Media Type

    # Parse JSON body
    data = request.get_json()  # it is equivalent to request.json

    # Dump to string for debugging / or return as response
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

    # Dump to string for debugging / or return as response
    dump = json.dumps(data)
    print(dump)

    return dump, 200