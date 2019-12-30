from flask import render_template
from tourbillon import tourbillon


@tourbillon.route('/')
def root():
    return tourbillon.send_static_file('index.html')
