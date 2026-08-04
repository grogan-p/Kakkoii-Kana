import os 
from flask import Flask, render_template, request, session, jsonify, Response
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index() -> str | Response:
    """Main function"""
    questions = {"すし" : "sushi", "はい" : "hai", "にほん" : "nihon", "わたし" : "watashi", "あなた" : "anata", "ごはん": "gohan"}
    keys = list(questions.keys())
    correct: bool | None = None

    current_index = session.get("current_index", 0)
    if not 0 <= current_index < len(questions):
        current_index = 0
    session["current_index"] = current_index
    kana = keys[current_index]
    answer = questions[kana]

    if request.method == "POST":
        guess = request.form.get("response")
        if guess:
            correct = guess.lower() == answer
            session["current_index"] = (current_index + 1) % len(questions)
        new_kana = keys[session["current_index"]]
        return jsonify(word=new_kana, correct=correct, correct_answer=answer)

    if request.method == "GET":
        return render_template('index.html', word=kana)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=7000)