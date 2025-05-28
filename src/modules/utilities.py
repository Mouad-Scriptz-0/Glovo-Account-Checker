import json, base64, yaml


config = yaml.safe_load(open('src/input/config.yml'))

def json_to_string(data: dict) : return json.dumps(data, separators=(",",":"))

def string_to_json(data: str)  : return json.loads(data)

def b64_encode(data: str | bytes) -> str:
    if type(data) == str:
        data = data.encode()
    return base64.b64encode(data).decode()

def b64_decode(data: str | bytes) -> str:
    if type(data) == bytes:
        data = data.decode()
    return base64.b64decode(data).decode()

def get_lines(file_path: str) -> list:
    lines = []
    with open(file_path, "rb") as f:
        for line in f.read().splitlines():
            try:
                lines.append(line.decode())
            except:
                pass
    return lines

def format_proxy(proxy: str):
    try:
        colon_splitted = proxy.split(":")
        if colon_splitted[1].isdigit():
            separator_index = proxy.index(colon_splitted[1]) + len(colon_splitted[1])
            separator = proxy[separator_index]
            if separator == "@":  # host:port@username:password
                address, credentials = proxy.split("@")
                (host, port), (username, password) = address.split(":"), credentials.split(":")
            elif separator == ":":  # host:port:username:password
                host, port, username, password = proxy.split(":")
            else:
                raise ValueError("Invalid proxy format")
        elif colon_splitted[3].isdigit():  # username:password:host:port
            credentials, address = proxy.split("@")
            (username, password), (host, port) = credentials.split(':'), address.split(':')
        else:
            raise ValueError("Invalid proxy format")
        
        return True, f"{username}:{password}@{host}:{port}"
    except Exception as e:
        return False, str(e)

def between(string: str, first: str, last: str):
    return string.split(first)[1].split(last)[0]