import os
import lzma

import orjson
import requests

isteamapps_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
istoreservice_url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
version = 3


def is_valid_title(title: str) -> bool:
    return bool(title) and len(title) > 2


if __name__ == "__main__":
    if (steam_api_key := os.environ.get("STEAM_API_KEY", None)) is None:
        print("Missing steam api key!")
        exit(1)

    data = {}

    for it in range(5):
        resp = requests.get(isteamapps_url)
        entries = orjson.loads(resp.text).get("applist", {}).get("apps", {})
        for entry in entries:
            if is_valid_title(entry["name"]):
                data[entry["name"]] = str(entry["appid"])

    for it in range(5):
        have_more_results = True
        last_appid = 0
        payload = {
            "key": steam_api_key,
            "include_games": True,
            "include_dlc": False,
            "max_results": 50000,
        }
        while have_more_results:
            payload["last_appid"] = last_appid
            resp = requests.get(istoreservice_url, params=payload)
            response = orjson.loads(resp.text).get("response", {})
            entries = response.get("apps", {})
            if have_more_results := response.get("have_more_results", False):
                last_appid = response["last_appid"]
                assert (len(entries) == payload.get("max_results", 10000))
            for entry in entries:
                if is_valid_title(entry["name"]):
                    data[entry["name"]] = str(entry["appid"])

    version_json = {
        "version": version,
        "entries": len(data),
    }

    print(version_json)

    appids_json = {
        "version": version,
        "entries": len(data),
        "games": data
    }

    with open("steam_appids.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(appids_json).decode("utf-8"))
    with open("steam_appids.json.xz", "wb") as f:
        f.write(lzma.compress(orjson.dumps(appids_json)))
    with open("steam_appids_version.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(version_json).decode("utf-8"))
