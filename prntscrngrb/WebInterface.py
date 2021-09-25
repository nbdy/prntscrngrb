from flask import Flask, render_template
from multiprocessing import Process


class WebInterface(Process):
    def __init__(self):
        Process.__init__(self)

        app = Flask(__name__)

        @app.route("/")
        def root():
            return render_template("")