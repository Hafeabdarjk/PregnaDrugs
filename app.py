from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Connect to your database (modify as needed)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # For easy row handling
    return conn

# Route for displaying body systems
@app.route("/")
def systems():
    conn = get_db_connection()
    systems = conn.execute('SELECT * FROM systems').fetchall()
    conn.close()
    return render_template("systems.html", systems=systems)

# Route for displaying diseases of a selected system
@app.route('/diseases')
def diseases():
    system_id = request.args.get('system_id')  # Get the system_id from the query string
    conn = get_db_connection()
    
    # Query to fetch diseases for the selected system
    diseases = conn.execute('SELECT * FROM diseases WHERE system_id = ?', (system_id,)).fetchall()
    
    conn.close()
    return render_template('diseases.html', diseases=diseases)

# Route for displaying classes of a selected disease
@app.route('/classes')
def classes():
    disease_id = request.args.get('disease_id')  # Get the disease_id from the query string
    conn = get_db_connection()
    
    # Query to fetch classes for the selected disease
    classes = conn.execute('SELECT * FROM classes WHERE disease_id = ?', (disease_id,)).fetchall()
    
    conn.close()
    return render_template('classes.html', classes=classes)

# Route for displaying drugs of a selected class
@app.route('/drugs')
def drugs():
    class_id = request.args.get('class_id')  # Get the class_id from the query string
    conn = get_db_connection()
    
    # Query to fetch drugs for the selected class
    drugs = conn.execute('SELECT * FROM drugs WHERE class_id = ?', (class_id,)).fetchall()
    
    conn.close()
    return render_template('drugs.html', drugs=drugs)
    
@app.route('/drug_details/<int:drug_id>')
def get_drug_details(drug_id):
    conn = get_db_connection()

    # Fetch the drug details including the new `drug_details` column
    drug = conn.execute('SELECT drug_details FROM drugs WHERE drug_id = ?', (drug_id,)).fetchone()
    conn.close()

    # Return the details as a JSON response
    if drug:
        print(drug['drug_details'])  # Debugging line
        return {"drug_details": drug['drug_details'] or "No additional information available for this drug."}
    else:
        return {"error": "Drug not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
    