from flask import render_template
from tourbillon import app


@app.route('/')
def root():
    return app.send_static_file('index.html')
