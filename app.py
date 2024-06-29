from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

user_input = "responses"

@app.route('/')
def start_page():
    return render_template("home.html", survey=satisfaction_survey)

@app.route('/start_survey', methods=["POST"])
def start_session():
    session[user_input] = []
    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def find_question(qid):
        responses = session.get(user_input)
        if (responses is None):
            return redirect('/')
        elif (len(responses) != qid):
            flash(f"Invalid command. Please complete question {len(responses)+1}.")
            return redirect(f"/questions/{len(responses)}")
        else:
            return render_template("question.html", survey=satisfaction_survey, qid=qid)

@app.route('/answer', methods=["POST"])
def collect_answer():
    choice = request.form['answer']
    responses = session[user_input]
    responses.append(choice)
    session[user_input] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def thank_you():
    return render_template("complete.html")