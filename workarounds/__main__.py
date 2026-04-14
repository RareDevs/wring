import os
from typing import Union

import orjson
import requests

github_event = os.environ.get("WRING_EVENT", "test")

workarounds_url = "https://raredevs.github.io/wring/workarounds.json"
workarounds_version_url = "https://raredevs.github.io/wring/workarounds_version.json"

__os_compat: tuple = ("Linux", "Darwin", "FreeBSD")
__os_native: tuple = ("Windows",)
__os_all: tuple = (*__os_compat, *__os_native)

__workarounds: dict[str, dict[str, dict[str, dict[str, Union[str, tuple]]]]] = {
    # XCOM2
    "3be3c4d681bc46b3b8b26c5df3ae0a18": {
        "options": {
            "override_exe": {
                "value": "Binaries/Win64/XCom2.exe",
                "os": __os_all,
            },
        },
    },
    # Civilization VI
    "Kinglet": {
        "options": {
            "override_exe": {
                "value": "Base/Binaries/Win64EOS/CivilizationVI.exe",
                "os": __os_all,
            },
        },
    },
    # Bioshock 2 Remastered
    "b22ce34b4ce0408c97a888554447479b": {
        "options": {
            "override_exe": {
                "value": "Build/FinalEpic/Bioshock2HD.exe",
                "os": __os_all,
            },
        },
    },
    # Bioshock 1 Remastered
    "bc2c95c6ff564a16b26644f1d3ac3c55": {
        "options": {
            "override_exe": {
                "value": "Build/FinalEpic/BioshockHD.exe",
                "os": __os_all,
            },
        },
    },
    # Eternal Threads
    "ff1d9bf6b1304cb9a12b8754afa78ae5": {
        "options": {
            "override_exe": {
                "value": "EternalThreadsBuild/EternalThreads.exe",
                "os": __os_compat,
            },
        },
    },
    # Celeste
    "Salt": {
        "options": {
            "start_params": {
                "value": "/gldevice:OpenGL",
                "os": __os_compat,
            },
        },
    },
    # Borderlands: The Pre Sequel
    "Turkey": {
        "options": {
            "start_params": {
                "value": "-NoLauncher",
                "os": __os_compat,
            },
        },
    },
    # Borderlands 2
    "Dodo": {
        "options": {
            "start_params": {
                "value": "-NoLauncher",
                "os": __os_compat,
            },
            # "override_exe": { "value": "Binaries/Win32/Borderlands2.exe", "os": __os_compat, },
        },
    },
    # Tiny Tina's Assault on Dragon Keep: A Wonderlands One shot Adventure
    "9e296d276ad447108f12c654c3341d59": {
        "options": {
            "start_params": {
                "value": "-NoLauncher",
                "os": __os_compat,
            },
        },
    },
    # Brothers: A Tale of Two Sons
    "Tamarind": {
        "options": {
            "start_params": {
                # value set at runtime
                "value": "ResX={res_width} ResY={res_height} -nomovies -nosplash",
                "os": __os_compat,
            },
            "override_exe": {
                "value": "Binaries/Win32/Brothers.exe",
                "os": __os_compat,
            },
        },
    },
    # Borderlands: The Pre Sequel
    "9c203b6ed35846e8a4a9ff1e314f6593": {
        "options": {
            "start_params": {
                "value": "/autorun /ed /autoquit",
                "os": __os_compat,
            },
        },
    },
    # F1® Manager 2024
    "03c9fe3b2869452ba8433ee7708a3e93": {
        "options": {
            "override_exe": {
                "value": "F1Manager24/Binaries/Win64/F1Manage",
                "os": __os_all,
            },
        },
    },
    # Cities Skylines
    "bcbc03d8812a44c18f41cf7d5f849265": {
        "options": {
            "override_exe": {
                "value": "Cities.exe",
                "os": __os_all,
            },
        },
    },
}

if __name__ == "__main__":

    try:
        resp = requests.get(workarounds_version_url)
        text = resp.content.decode("utf-8")
        version = orjson.loads(text)["version"]
    except Exception as e:
        version = 1

    version = version if github_event == "schedule" else version + 1

    version_json = {
        "version": version,
        "entries": len(__workarounds),
    }

    workarounds_json = {
        "version": version,
        "entries": len(__workarounds),
        "workarounds": __workarounds,
    }

    with open("workarounds.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(workarounds_json).decode("utf-8"))
    with open("workarounds_version.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(version_json).decode("utf-8"))
