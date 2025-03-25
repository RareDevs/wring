import os

import orjson
import requests

steam_api_url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
version = 3

if __name__ == "__main__":
    have_more_results = True
    last_appid = 0

    if (steam_api_key := os.environ.get("STEAM_API_KEY", None)) is None:
        print("Missing steam api key!")
        exit(1)

    payload = {
        "key": steam_api_key,
        "include_games": True,
        "max_results": 25000,
    }

    games = {}
    while have_more_results:
        payload.update({"last_appid": last_appid})
        resp = requests.get(steam_api_url, params=payload)
        response = orjson.loads(resp.text)["response"]
        if have_more_results := response.get("have_more_results", False):
            last_appid = response["last_appid"]
        for app in response["apps"]:
            games.update({app["name"]: str(app["appid"])})

    with open("steam_appids.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps({"version": version, "games": games}).decode("utf-8"))
    with open("steam_appids_version.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps({"version": version}).decode("utf-8"))
