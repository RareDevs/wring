import os
from dataclasses import dataclass, field

import orjson
import requests

github_event = os.environ.get("WRING_EVENT", "test")

workarounds_url = "https://raredevs.github.io/wring/workarounds.json"
workarounds_version_url = "https://raredevs.github.io/wring/workarounds_version.json"

_os_compat: tuple = ("Linux", "Darwin", "FreeBSD")
_os_native: tuple = ("Windows",)
_os_all: tuple = (*_os_compat, *_os_native)


@dataclass
class Entry:
    name: str
    value: str
    opsys: tuple

    @property
    def __dict__(self):
        return {self.name: dict(value=self.value, os=self.opsys)}


@dataclass
class Game:
    appname: str
    options: list[Entry] = field(default_factory=list)
    environ: list[Entry] = field(default_factory=list)

    @property
    def __dict__(self):
        _options = {}
        for _opt in self.options:
            _options.update(vars(_opt))
        _environ = {}
        for _env in self.environ:
            _environ.update(vars(_env))
        return {self.appname: dict(options=_options, environ=_environ)}


@dataclass
class Workarounds:
    games: list[Game]

    @property
    def __dict__(self):
        _games = {}
        for _gwa in self.games:
            if _gwa.appname in _games:
                raise RuntimeError("AppName %s already in workarounds list", _gwa.appname)
            _games.update(vars(_gwa))
        return _games


games = [
    # XCOM2
    Game(
        appname="3be3c4d681bc46b3b8b26c5df3ae0a18",
        options=[Entry(name="override_exe", value="Binaries/Win64/XCom2.exe", opsys=_os_all)]
    ),
    # Civilization VI
    Game(
        appname="Kinglet",
        options=[Entry(name="override_exe", value="Base/Binaries/Win64EOS/CivilizationVI.exe", opsys=_os_all)]
    ),
    # Bioshock 2 Remastered
    Game(
        appname="b22ce34b4ce0408c97a888554447479b",
        options=[Entry(name="override_exe", value="Build/FinalEpic/Bioshock2HD.exe", opsys=_os_all)]
    ),
    # Bioshock 1 Remastered
    Game(
        appname="bc2c95c6ff564a16b26644f1d3ac3c55",
        options=[Entry(name="override_exe", value="Build/FinalEpic/BioshockHD.exe", opsys=_os_all)]
    ),
    # Eternal Threads
    Game(
        appname="ff1d9bf6b1304cb9a12b8754afa78ae5",
        options=[Entry(name="override_exe", value="EternalThreadsBuild/EternalThreads.exe", opsys=_os_compat)]
    ),
    # Celeste
    Game(
        appname="Salt",
        options=[Entry(name="start_params", value="/gldevice:OpenGL", opsys=_os_compat)]
    ),
    # Borderlands: The Pre Sequel
    Game(
        appname="Turkey",
        options=[Entry(name="start_params", value="-NoLauncher", opsys=_os_compat)]
    ),
    # Borderlands 2
    Game(
        appname="Dodo",
        options=[
            Entry(name="start_params", value="-NoLauncher", opsys=_os_compat),
            # Entry(name="override_exe", value="Binaries/Win32/Borderlands2.exe", opsys=_os_compat),
        ]
    ),
    # Tiny Tina's Assault on Dragon Keep: A Wonderlands One shot Adventure
    Game(
        appname="9e296d276ad447108f12c654c3341d59",
        options=[Entry(name="start_params", value="-NoLauncher", opsys=_os_compat)]
    ),
    # Borderlands: The Pre Sequel
    Game(
        appname="9c203b6ed35846e8a4a9ff1e314f6593",
        options=[Entry(name="start_params", value="/autorun /ed /autoquit", opsys=_os_compat)]
    ),
    # Brothers: A Tale of Two Sons
    Game(
        appname="Tamarind",
        options=[
            Entry(name="start_params", value="ResX={res_width} ResY={res_height} -nomovies -nosplash", opsys=_os_compat),
            Entry(name="override_exe", value="Binaries/Win32/Brothers.exe", opsys=_os_compat),
        ]
    ),
    # F1® Manager 2024
    Game(
        appname="03c9fe3b2869452ba8433ee7708a3e93",
     options=[Entry(name="override_exe", value="F1Manager24/Binaries/Win64/F1Manager24.exe", opsys=_os_all)]
    ),
    # Cities Skylines
    Game(
        appname="bcbc03d8812a44c18f41cf7d5f849265",
        options=[Entry(name="override_exe", value="Cities.exe", opsys=_os_all)]
    ),
    # Grand Theft Auto V Enhanced
    Game(
        appname="8769e24080ea413b8ebca3f1b8c50951",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Grand Theft Auto V
    Game(
        appname="9d2d0eb64d5c44529cece33fe2a46482",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Red Dead Redemption
    Game(
        appname="c180bd9859624278aa20f1333918498a",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Red Dead Redemption 2
    Game(
        appname="Heather",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Grand Theft Auto: San Andreas – The Definitive Edition
    Game(
        appname="0828ecd4297c4f89bfcc45420e695b67",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Grand Theft Auto: Vice City – The Definitive Edition
    Game(
        appname="bb5b67d981cd47779e98a3a678360238",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Grand Theft Auto III – The Definitive Edition
    Game(
        appname="3419b0161b3c4b5da5f33ab69ad030f0",
        environ=[Entry(name="LEGENDARY_WRAPPER_EXE", value="{wrapper_exe}", opsys=_os_all)]
    ),
    # Rocket League®
    Game(
        appname="Sugar",
        environ=[Entry(name="LANG", value="en_US.UTF-8", opsys=_os_compat)]
    ),
]

if __name__ == "__main__":

    try:
        resp = requests.get(workarounds_version_url)
        text = resp.content.decode("utf-8")
        version = orjson.loads(text)["version"]
    except Exception as e:
        version = 1

    version = version if github_event == "schedule" else version + 1

    workarounds = Workarounds(games=games)
    _workarounds = vars(workarounds)

    version_json = {"version": version, "entries": len(_workarounds), }

    workarounds_json = {"version": version, "entries": len(_workarounds), "workarounds": _workarounds, }

    with open("workarounds.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(workarounds_json).decode("utf-8"))
    with open("workarounds_version.json", "w", encoding="utf-8") as f:
        f.write(orjson.dumps(version_json).decode("utf-8"))
