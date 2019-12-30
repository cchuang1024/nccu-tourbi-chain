"""
Troubillon - 陀飛輪，整個系統的核心與驅動部位
"""

from flask import Flask

tourbillon = Flask(__name__, static_folder='../static')


def init():
    pass


def run():
    tourbillon.run()
