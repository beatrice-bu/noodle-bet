import json

def readWrite(output_name: str, action: str, data: dict =None):
    with open(output_name + '.json', action) as json_data:
        if action == 'r':
            return json.load(json_data)
        elif action == 'w':
            try:
                if data == None:
                    raise ValueError("No dict given for write out action.")
            except ValueError as no_data_given:
                print(no_data_given)
                return
            else:
                json.dumps(data)


if __name__ == "__main__":
    readWrite()