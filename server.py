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
    correct: bool = False

    if "current_index" not in session:
        session["current_index"] = 0

    current_index = session["current_index"]
    kana = keys[current_index]
    answer = questions[kana]

    if request.method == "POST":
        response = request.form.get("response")
        if response:
            correct = response.lower() == answer
            session["current_index"] = (current_index + 1) % len(questions)
        new_kana = keys[session["current_index"]]
        return jsonify(word=new_kana, correct=correct, correct_answer=answer)

    if request.method == "GET":
        return render_template('index.html', word=kana, current_index=session["current_index"])

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=7000)