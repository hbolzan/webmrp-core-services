def handle_exception(e):
    error_type = e.args[0].strip()
    if error_type == "NotFound":
        return 404, "Not found"
    else:
        return 500, "Internal server error"
