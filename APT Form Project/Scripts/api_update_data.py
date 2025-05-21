from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection details
db_config = {
    "host": "ls-1d6ea89422474da42fe45c9a5b96cb4d7faf6f1a.cc4xzbvug12w.ap-southeast-2.rds.amazonaws.com",
    "user": "stratasure_user",
    "password": "f5MoD1g68o",
    "database": "uwt_dev"
}

@app.route('/api/GetDataAPI', methods=['GET', 'PUT'])

def get_or_update_data():
    if request.method == 'PUT':
        try:
                data = request.get_json()
                print("Received payload:", data)  # DEBUG

                candidate_name = data.get('Candidate_Name')
                email_apology_score = data.get('Email_apology_score')
                email_complaint_response_score = data.get('Email_complaint_response_score')

                if not candidate_name:
                    return jsonify({"error": "Candidate_Name is required"}), 400

                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                query = """
                    UPDATE candidates
                    SET email_apology_score = %s,
                        email_complaint_response_score = %s
                    WHERE Candidate_Name = %s
                """
                cursor.execute(query, (email_apology_score, email_complaint_response_score, candidate_name))
                conn.commit()

                if cursor.rowcount == 0:
                    return jsonify({"message": "No matching candidate found"}), 404

                cursor.close()
                conn.close()

                return jsonify({"message": "Score updated!"})

        except Exception as e:
                return jsonify({"error": str(e)}), 500
            
    else:  # GET request
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT email_apology, Candidate_Name, email_complaint_response, email_complaint_response_score , email_apology_score 
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
