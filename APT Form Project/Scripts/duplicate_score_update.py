from flask import Flask, jsonify, request
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

@app.route('/api/GetDataAPI' , method = ['PUT'])
def get_data():
    try:
        data = request.get_json()
        candidate_name = data.get('Candidate_Name')
        email_apology = data.get('email_apology')
        email_apology_score = data.get('email_apology_score')
        email_complaint_response = data.get('email_complaint_response')
        email_complaint_response_score = data.get('email_complaint_response_score')
        total_score = data.get('Total_score')

        if not candidate_name:
            return jsonify({'error': 'Candidate_Name is required'}), 400\
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE candidates
            SET email_apology = email_apology,
                email_apology_score = %s,
                email_complaint_response = email_complaint_response,
                email_complaint_response_score = %s,
                Total_score = Total_score
            WHERE Candidate_Name = Candidate_Name
        """

        # Execute the UPDATE statement with provided data
        cursor.execute(update_query, (
            email_apology,
            email_apology_score,
            email_complaint_response,
            email_complaint_response_score,
            total_score,
            candidate_name
        ))

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Candidate record updated successfully'}), 200
        



    except Exception as e:
        return jsonify({'error': str(e)}), 500   

if __name__ == '__main__':
    app.run(debug=True)
