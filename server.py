import os
import random

import requests
from flask import Flask, render_template, request, session, jsonify, Response
from waitress import serve
from dotenv import load_dotenv

import jisho

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

FALLBACK = [
    jisho.make_question("すし", "寿司", ["sushi"]),
    jisho.make_question("はい", None, ["yes"]),
    jisho.make_question("にほん", "日本", ["Japan"]),
    jisho.make_question("わたし", "私", ["I", "me"]),
    jisho.make_question("あなた", None, ["you"]),
    jisho.make_question("ごはん", "ご飯", ["cooked rice", "meal"]),
]


def new_question() -> dict[str, list[str]]:
    """Pick the next word and record its answers in the session."""
    try:
        question = jisho.random_word()
    except (requests.RequestException, ValueError, IndexError):
        question = random.choice(FALLBACK)
    session["kana"] = question["kana"]
    session["accepted"] = question["accepted"]
    session["kanji"] = question["kanji"]
    session["meaning"] = question["meaning"]
    return question


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index() -> str | Response:
    """Main function"""
    if request.method == "POST":
        guess = (request.form.get("response") or "").strip().lower()
        accepted = session.get("accepted", [])
        if not guess:
            return jsonify(word=session.get("kana", ""), correct=None)

        correct = guess in set(accepted)
        answer = accepted[0] if accepted else ""
        kanji = session.get("kanji")
        meaning = session.get("meaning", [])
        return jsonify(
            word=new_question()["kana"],
            correct=correct,
            correct_answer=answer,
            kanji=kanji,
            meaning=meaning,
        )

    return render_template('index.html', word=new_question()["kana"])


if __name__ == "__main__":
    try:
        jisho.load_pool()
    except requests.RequestException as exc:
        print(f"Jisho unavailable ({exc}); using the fallback word list.")
    serve(app, host="0.0.0.0", port=7000)
