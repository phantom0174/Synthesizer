from flask import Flask, render_template
from threading import Thread
from core.setup import Score_Board


app = Flask('')


@app.route('/')
def main():
    return render_template('index.html', score_board=Score_Board)


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
