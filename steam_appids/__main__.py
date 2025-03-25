import os
import lzma

import orjson
import requests

isteamapps_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
istoreservice_url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
version = 3

if __name__ == "__main__":
    if (steam_api_key := os.environ.get("STEAM_API_KEY", None)) is None:
        print("Missing steam api key!")
        exit(1)

    data = {}

    resp = requests.get(isteamapps_url)
    apps = orjson.loads(resp.text).get("applist", {}).get("apps", {})
    data.update({str(app["appid"]): app["name"] for app in apps})

    have_more_results = True
    last_appid = 0
    payload = {
        "key": steam_api_key,
        "include_games": True,
        "include_dlc": True,
        "max_results": 5000,
    }

    while have_more_results:
        payload.update({"last_appid": last_appid})
        resp = requests.get(istoreservice_url, params=payload)
        response = orjson.loads(resp.text)["response"]
        if have_more_results := response.get("have_more_results", False):
            last_appid = response["last_appid"]
        data.update({str(app["appid"]): app["name"] for app in response["apps"]})

    # Invert key/value pairs
    data = {v: k for k, v in data.items() if bool(v) and len(v) > 2}

    with open("steam_appids.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps({"version": version, "games": data}).decode("utf-8"))
    with open("steam_appids.json.xz", "wb") as f:
        f.write(lzma.compress(orjson.dumps({"version": version, "games": data})))
    with open("steam_appids_version.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps({"version": version}).decode("utf-8"))
