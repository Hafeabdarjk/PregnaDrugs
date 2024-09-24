from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Connect to database
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

# Route for searching by class
@app.route('/search')
def search():
    query = request.args.get('search', '').strip()  # Get the search term from the form input
    conn = get_db_connection()

    # Find the class by name
    pharmacological_class = conn.execute('''
        SELECT class_id FROM classes WHERE class_name LIKE ?
    ''', ('%' + query + '%',)).fetchone()

    conn.close()

    # If the class is found, redirect to the /drugs page with the class_id
    if pharmacological_class:
        return redirect(url_for('drugs', class_id=pharmacological_class['class_id']))
    else:
        # If no class is found, you could return a "no results" page or redirect to a generic page
        return render_template('no_results.html', query=query)

# Route for suggestions
@app.route('/autocomplete')
def autocomplete():
    search_term = request.args.get('term', '').strip()  # Get the typed input
    conn = get_db_connection()

    # Fetch class names that match the typed input
    class_names = conn.execute('''
        SELECT class_name FROM classes WHERE class_name LIKE ?
    ''', ('%' + search_term + '%',)).fetchall()

    conn.close()

    # Return a list of class names as a JSON response
    return jsonify(suggestions=[class_name['class_name'] for class_name in class_names])

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
    
# Route for fetching drug details
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