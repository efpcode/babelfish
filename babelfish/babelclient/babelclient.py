import os
from requests import request
from json import JSONDecoder as JsD


class BabelClient:
    def __str__(self):
        return "BabelClient.APICaller"

    def __repr__(self):
        return "BabelClient.Response[GET]"

    @classmethod
    def api_get(cls):
        j_object = JsD()
        call = cls.parse_api_get()
        response = request("GET", call)
        parse_response = {

            k: v for k, v in j_object.decode(response.text).items() if k in (
                "responseDetails", "responseStatus", "key")
        }

        try:
            parse_response["responseStatus"]
            parse_response["responseDetails"]

        except KeyError:
            os.environ["MY_APIKEY"] = parse_response.get("key")

        else:
            print(f"User was not able to contact 'MyMemory' server"
                  f"\nError code returned from server: -->"
                  f" {parse_response['responseStatus']}\n"
                  f"Error code caused by: {parse_response['responseDetails']}"
                  )

        finally:
            return response

    # static methods
    @staticmethod
    def get_env_data():
        return os.environ.get("MY_USERNAME"), os.environ.get("MY_PASSWORD")

    @staticmethod
    def parse_api_get():
        stem = "https://api.mymemory.translated.net/keygen?"
        web_auth = ("user=", "&pass=")
        user_data = BabelClient.get_env_data()
        login_data = ["".join(i) for i in list(zip(web_auth, user_data))]

        return "".join((stem, "".join(login_data)))
