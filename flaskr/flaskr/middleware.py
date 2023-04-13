from flask import request

def add_location_header(response):
    if 302 >= response.status_code >= 200 and 'Location' not in response.headers: 
        response.headers['Location'] = request.url
    return response
