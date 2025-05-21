from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)



print("Current working directory:", os.getcwd())



# MySQL connection details — CHANGE these to your settings
db = mysql.connector.connect(
    host="ls-1d6ea89422474da42fe45c9a5b96cb4d7faf6f1a.cc4xzbvug12w.ap-southeast-2.rds.amazonaws.com",
    user="stratasure_user",
    password="f5MoD1g68o",
    database="uwt_dev"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Candidate info
    candidate_name = request.form.get('candidate_name')

    # Answers q1 to q20
    q_answers = []
    for i in range(1, 21):
        q_answers.append(request.form.get(f'q{i}'))

    # Reading fields (5 questions)
    reading_q1 = request.form.get('reading_q1')
    reading_q2 = request.form.get('reading_q2')
    reading_q3 = request.form.get('reading_q3')
    reading_q4 = request.form.get('reading_q4')
    reading_q5 = request.form.get('reading_q5')

    # Reading2 fields (5 questions)
    reading2_q1 = request.form.get('reading2_q1')
    reading2_q2 = request.form.get('reading2_q2')
    reading2_q3 = request.form.get('reading2_q3')
    reading2_q4 = request.form.get('reading2_q4')
    reading2_q5 = request.form.get('reading2_q5')

    # Email fields
    email_apology = request.form.get('email_apology')
    email_complaint_response = request.form.get('email_complaint_response')

    # SQL Insert statement with 33 placeholders matching fields
    sql = """
    INSERT INTO candidates 
    (candidate_name, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
     q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
     reading_q1, reading_q2, reading_q3, reading_q4, reading_q5,
     reading2_q1, reading2_q2, reading2_q3, reading2_q4, reading2_q5,
     email_apology, email_complaint_response)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s)
    """

    val = (
        candidate_name, *q_answers,
        reading_q1, reading_q2, reading_q3, reading_q4, reading_q5,
        reading2_q1, reading2_q2, reading2_q3, reading2_q4, reading2_q5,
        email_apology, email_complaint_response
    )

    cursor.execute(sql, val)
    db.commit()

    return "Data saved to database successfully!"

if __name__ == '__main__':
    app.run(debug=True)
