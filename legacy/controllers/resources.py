import stringcase

def resource_to_sql(root_path, resource_name, operation, default):
    snake_resource = stringcase.snakecase(resource_name)
    try:
        with open("{}/resources/sql/{}".format(root_path, snake_resource)) as f:
            return f.read()
    except FileNotFoundError:
        try:
            with open("{}/resources/sql/{}.{}.sql".format(root_path, snake_resource, operation)) as f:
                return f.read()
        except:
            return default
