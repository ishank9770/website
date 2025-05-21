from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection details — CHANGE these to your settings
db_config = {
    "host": "ls-1d6ea89422474da42fe45c9a5b96cb4d7faf6f1a.cc4xzbvug12w.ap-southeast-2.rds.amazonaws.com",
    "user": "stratasure_user",
    "password": "f5MoD1g68o",  # <-- make sure this is your real password
    "database": "uwt_dev"
}

@app.route('/api/GetDataAPI')
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # dictionary=True gives column names in result
        query = """
            SELECT email_apology, Candidate_Name, Total_score, email_complaint_response  , email_complaint_response_score, email_apology_score 
            FROM candidates
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
