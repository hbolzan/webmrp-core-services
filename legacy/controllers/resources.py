def resource_to_sql(root_path, resource_name, default):
    try:
        with open("{}/resources/sql/{}".format(root_path, resource_name)) as f:
            return f.read()
    except FileNotFoundError:
        try:
            with open("{}/resources/sql/{}.select.sql".format(root_path, resource_name)) as f:
                return f.read()
        except:
            return default
