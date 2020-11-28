OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404

client_error_code = [BAD_REQUEST, NOT_FOUND]

def is_client_error(status_code):
    return status_code in client_error_code