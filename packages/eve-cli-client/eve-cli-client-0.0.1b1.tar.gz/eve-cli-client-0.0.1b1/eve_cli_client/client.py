import requests
import pprint
from api_key import SERVER_API_KEY


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    while True:
        user_in = ""
        while user_in == "":
            user_in = input("Enter the string: ")

        r = requests.post("http://localhost:5000/api/v1.0/process/", data={
            "key": SERVER_API_KEY,
            "text": user_in
        })

        pp.pprint(r.json())
        print("\n")
