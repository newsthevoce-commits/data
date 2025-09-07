from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ enables CORS for all routes

VOTES_FILE = 'votes.json'
BB_FILE = 'biggbosspage.json'

# ---------------- Vote Read/Write ------------------

def read_votes():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, 'r') as f:
            return json.load(f)
    return {"votes1": 0, "votes2": 0, "votes3": 0}

def write_votes(votes):
    with open(VOTES_FILE, 'w') as f:
        json.dump(votes, f, indent=2)

# ---------------- BiggBoss Content Read/Write ------------------

def read_bb():
    if os.path.exists(BB_FILE):
        with open(BB_FILE, 'r') as f:
            return json.load(f)
    return []

def write_bb(data):
    with open(BB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ---------------- API Routes ------------------

@app.route('/votes', methods=['GET'])
def get_votes():
    return jsonify(read_votes())

@app.route('/votes', methods=['POST'])
def update_votes():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format, expected JSON object"}), 400

    current_votes = read_votes()
    current_votes.update(data)
    write_votes(current_votes)
    return jsonify(current_votes)

@app.route('/biggboss-content', methods=['GET'])
def get_biggboss_content():
    return jsonify(read_bb())

@app.route('/biggboss-content', methods=['POST'])
def update_biggboss_content():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_bb(data)
        return jsonify({"message": "BiggBoss content updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- Start Server ------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
