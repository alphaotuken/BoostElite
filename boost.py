from colorama import Style
import discord
import datetime
import time
import flask
import requests
import json
import threading
import os
import random
import httpx
import sys
import base64
from flask import request
from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore, Style

if os.name == 'nt':
    import ctypes

app = flask.Flask(__name__)

class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

fingerprints = json.load(open("fingerprints.json", encoding="utf-8"))
config = json.load(open("config.json", encoding="utf-8"))
client_identifiers = ['safari_ios_16_0', 'safari_ios_15_6', 'safari_ios_15_5', 'safari_16_0', 'safari_15_6_1', 'safari_15_3', 'opera_90', 'opera_89', 'firefox_104', 'firefox_102']


class Variables:
    joins = 0
    boosts_done = 0
    success_tokens = []
    failed_tokens = []


def timestamp():
    timestamp = f"{Fore.RESET}[{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S')}{Fore.RESET}]"
    return timestamp


def check_empty(filename):
    mypath = Path(filename)
    if mypath.stat().st_size == 0:
        return True
    else:
        return False


def validate_invite(invite):
    client = httpx.Client()
    if 'type' in client.get
