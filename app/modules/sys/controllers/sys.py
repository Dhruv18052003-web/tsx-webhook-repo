from flask import request, jsonify

def home():
    return "welcome buddy"

def echo():
    # request.args is a MultiDict; convert to a plain dict
    query_params = dict(request.args)
    
    # Optionally: print them to console for debugging
    print(query_params)
    
    # Return as JSON response
    return jsonify(query_params)