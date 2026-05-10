def success_response(message, data=None):
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(message, code=400):
    return {
        "success": False,
        "message": message,
        "error_code": code
    }
