from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'DIST-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_KAquino'
username = 'KAquino'
password = 'UpfX340*'

# Function to connect to the database
def get_db_connection():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )

@app.route('/')
def home():
    return "CW2 API is working!"

@app.route('/create-trail', methods=['POST'])
def create_trail():
    # Get data from the request
    data = request.get_json()
    trail_name = data['TrailName']
    length = data['Length']
    difficulty = data['Difficulty']
    elevation_gain = data['ElevationGain']
    route_type = data['RouteType']
    description = data['Description']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insert data into the Trail table
        cursor.execute("""
            INSERT INTO CW2.Trail (TrailID, TrailName, Length, Difficulty, ElevationGain, RouteType, Description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['TrailID'], trail_name, length, difficulty, elevation_gain, route_type, description))
        conn.commit()
        conn.close()
        return jsonify({"message": "Trail created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-trails', methods=['GET'])
def get_trails():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fetch all trails from the Trail table
        cursor.execute("SELECT * FROM CW2.Trail")
        rows = cursor.fetchall()
        conn.close()

        # Convert rows into a list of dictionaries
        trails = [
            {
                "TrailID": row[0],
                "TrailName": row[1],
                "Length": row[2],
                "Difficulty": row[3],
                "ElevationGain": row[4],
                "RouteType": row[5],
                "Description": row[6]
            }
            for row in rows
        ]
        return jsonify(trails), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-trail/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Update the trail in the Trail table
        cursor.execute("""
            UPDATE CW2.Trail
            SET TrailName = ?, Length = ?, Difficulty = ?, ElevationGain = ?, RouteType = ?, Description = ?
            WHERE TrailID = ?
        """, (data['TrailName'], data['Length'], data['Difficulty'], data['ElevationGain'], data['RouteType'], data['Description'], trail_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Trail updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-trail/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # First, delete all related entries in the Trail_Location table
        cursor.execute("DELETE FROM CW2.Trail_Location WHERE TrailID = ?", (trail_id,))
        conn.commit()

        # Then, delete the trail itself
        cursor.execute("DELETE FROM CW2.Trail WHERE TrailID = ?", (trail_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Trail and related locations deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

