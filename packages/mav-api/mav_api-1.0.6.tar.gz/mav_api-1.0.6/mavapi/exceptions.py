class MAVAPIExceptions(Exception):
    pass

class MAVAPIAuthError(MAVAPIExceptions):
    pass

class MAVAPIError(MAVAPIExceptions):
    error_list = [3,4,47]

    WRONG_ACCESSTOKEN = {'status': 'error', 'error_code': 4, 'error_msg': 'Wrong access_token.'}
    NO_ACCESSTOKEN = {'status': 'error', 'error_code': 3, 'error_msg': "Token isn't specified."}
    AUTH_IP_DENIED = {'status': 'error', 'error_code': 3, 'error_msg': "You cannot use this access_token from this IP address."}
    DATE_WRONG_FORMAT = {'status': 'error', 'error_code': 12, 'error_msg': 'Date in wrong format.'}