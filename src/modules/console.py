import os, threading

from pystyle import Colors as Clrs, Center, Colorate
from datetime import datetime

from .utilities import config


lock = threading.Lock()
Clrs.bg_reset = "\033[0m"

def get_bg_color(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

def get_fg_color(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def get_colored_time(
        clr_one: str = Clrs.gray,
        clr_two: str = Clrs.light_gray
    ):
    now = datetime.now().strftime(f"{clr_one}%H{clr_two}:{clr_one}%M{clr_two}:{clr_one}%S")
    return now

def get_prefix(string: str, color: str = Clrs.white, bg_color: str = Clrs.gray):
    if config['console']['show time'] == True:
        return f" {get_colored_time()} {Clrs.dark_gray}|{Clrs.reset} {get_bg_color(*bg_color)}{get_fg_color(*color)}{string}{Clrs.bg_reset} {Clrs.dark_gray}|{Clrs.reset}"
    return f" {get_bg_color(*bg_color)}{get_fg_color(*color)}{string}{Clrs.bg_reset} {Clrs.dark_gray}|{Clrs.reset}"

seperator = f'{Clrs.light_gray}>>{Clrs.reset}'

replacers = {
    ":": f"{Clrs.gray}:{Clrs.reset}",
    "|": f"{Clrs.gray}|{Clrs.reset}",
}

def replace(string: str):
    for old, new in replacers.items():
        string = string.replace(old, new)
    return string

class Console:
    def clear() : os.system('cls')

    def input(text: str):
        prefix = get_prefix('  INPUT  ', (66, 166, 81), (26, 214, 54))
        print(
            f'{prefix} {text}{Clrs.reset} {Clrs.gray}>>{Clrs.reset} ',
            end=''
        )
        return input()

    def checker(text: str, content: str = "", custom: bool = False):
        if not custom:
            if content != "":
                content = replace(content)
            text = replace(text)
        prefix = get_prefix('  GLOVO  ', (7, 164, 130), (251, 196, 68))
        if content == "":
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset}"
                )
        else:
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset} {seperator} {Clrs.StaticRGB(0, 255, 255)}{content}{Clrs.reset}"
                )

    def error(text: str, content: str = "", custom: bool = False):
        if not custom:
            if content != "":
                content = replace(content)
            text = replace(text)
        prefix = get_prefix('  ERROR  ', (180, 0, 0), (255, 0, 0))
        if content == "":
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset}"
                )
        else:
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset} {seperator} {Clrs.StaticRGB(255, 0, 0)}{content}{Clrs.reset}"
                )

    def information(text: str, content: str = "", custom: bool = False):
        if not custom:
            if content != "":
                content = replace(content)
            text = replace(text)
        prefix = get_prefix('  INFO   ', (180, 180, 0), (255, 255, 0))
        if content == "":
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset}"
                )
        else:
            with lock:
                print(
                    f"{prefix} {text}{Clrs.reset} {seperator} {Clrs.StaticRGB(255, 255, 0)}{content}{Clrs.reset}"
                )

    def resize(cols: int, lines: int) : os.system(f"mode con:cols={cols} lines={lines}")

    def sub_banner(text: str):
        print(Colorate.DiagonalBackwards(Clrs.blue_to_cyan, Center.XCenter(text)))
        print()