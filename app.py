from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'healthcare.db'

# Helper function to interact with the database
def execute_query(query, params=(), fetch=False):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result
        conn.commit()
        conn.close()
    except Exception as e:
        return str(e)

# Initialize the database with required tables
def init_db():
    queries = [
        """CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            ailment TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS resources (
            name TEXT PRIMARY KEY,
            count INTEGER NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            time TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS checkin_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            checkin_time TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS collaborations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider1 TEXT NOT NULL,
            provider2 TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS hierarchy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT NOT NULL,
            role TEXT NOT NULL
        )"""
    ]
    for query in queries:
        execute_query(query)

# Initialize database before running the server
init_db()

# Route to handle all frontend commands
@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.json
        command = data['command']
        parts = command.split()
        action = parts[0]
        args = parts[1:]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        if action == "1":  # Add Patient
            if len(args) < 3:
                return jsonify({"error": "Not enough arguments for adding a patient."})
            name, age, ailment = args[0], int(args[1]), ' '.join(args[2:])
            cursor.execute("INSERT INTO patients (name, age, ailment) VALUES (?, ?, ?)", (name, age, ailment))
            connection.commit()
            return jsonify({"output": "Patient added successfully!"})

        elif action == "11":  # Show Patients
            cursor.execute("SELECT * FROM patients")
            patients = cursor.fetchall()
            if patients:
                output = '\n'.join([f"ID: {p[0]}, Name: {p[1]}, Age: {p[2]}, Ailment: {p[3]}" for p in patients])
            else:
                output = "No patients available."
            return jsonify({"output": output})

        elif action == "2":  # Schedule Appointment
            if len(args) < 2:
                return jsonify({"error": "Not enough arguments for scheduling an appointment."})
            patient_name, time = args[0], ' '.join(args[1:])
            cursor.execute("INSERT INTO appointments (patient_name, time) VALUES (?, ?)", (patient_name, time))
            connection.commit()
            return jsonify({"output": "Appointment scheduled successfully!"})

        elif action == "3":  # Add Resource
            if len(args) < 2:
                return jsonify({"error": "Not enough arguments for adding a resource."})
            resource_name, count = args[0], int(args[1])
            cursor.execute("INSERT INTO resources (name, count) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET count=count + ?", (resource_name, count, count))
            connection.commit()
            return jsonify({"output": f"Resource '{resource_name}' added or updated successfully!"})

        elif action == "4":  # Check Resource Availability
            if len(args) < 1:
                return jsonify({"error": "Resource name is required to check availability."})
            resource_name = args[0]
            cursor.execute("SELECT count FROM resources WHERE name=?", (resource_name,))
            result = cursor.fetchone()
            if result:
                output = f"Resource '{resource_name}' availability: {result[0]}"
            else:
                output = f"Resource '{resource_name}' not found."
            return jsonify({"output": output})

        elif action == "5":  # Patient Check-In
            if len(args) < 2:
                return jsonify({"error": "Not enough arguments for patient check-in."})
            patient_name, checkin_time = args[0], ' '.join(args[1:])
            cursor.execute("INSERT INTO checkin_queue (patient_name, checkin_time) VALUES (?, ?)", (patient_name, checkin_time))
            connection.commit()
            return jsonify({"output": f"Patient '{patient_name}' checked in at {checkin_time}"})

        elif action == "6":  # Next Check-In
            cursor.execute("SELECT * FROM checkin_queue ORDER BY id LIMIT 1")
            next_patient = cursor.fetchone()
            if next_patient:
                cursor.execute("DELETE FROM checkin_queue WHERE id=?", (next_patient[0],))
                connection.commit()
                output = f"Next patient: {next_patient[1]} at {next_patient[2]}"
            else:
                output = "No patients in check-in queue."
            return jsonify({"output": output})

        elif action == "7":  # Add Healthcare Provider
            if len(args) < 2:
                return jsonify({"error": "Not enough arguments for adding a healthcare provider."})
            provider, role = args[0], ' '.join(args[1:])
            cursor.execute("INSERT INTO hierarchy (provider, role) VALUES (?, ?)", (provider, role))
            connection.commit()
            return jsonify({"output": "Healthcare provider added to hierarchy!"})

        elif action == "8":  # Show Hierarchy
            cursor.execute("SELECT * FROM hierarchy")
            hierarchy = cursor.fetchall()
            if hierarchy:
                output = '\n'.join([f"ID: {h[0]}, Provider: {h[1]}, Role: {h[2]}" for h in hierarchy])
            else:
                output = "No hierarchy data available."
            return jsonify({"output": output})

        elif action == "9":  # Add Collaboration
            if len(args) < 2:
                return jsonify({"error": "Not enough arguments for adding a collaboration."})
            provider1, provider2 = args[0], args[1]
            cursor.execute("INSERT INTO collaborations (provider1, provider2) VALUES (?, ?)", (provider1, provider2))
            connection.commit()
            return jsonify({"output": "Collaboration added successfully!"})

        elif action == "10":  # Show Collaborations
            cursor.execute("SELECT * FROM collaborations")
            collaborations = cursor.fetchall()
            if collaborations:
                output = '\n'.join([f"ID: {c[0]}, {c[1]} collaborates with {c[2]}" for c in collaborations])
            else:
                output = "No collaborations available."
            return jsonify({"output": output})

        else:
            return jsonify({"error": "Invalid action specified."})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
