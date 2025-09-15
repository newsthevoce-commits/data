from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ enables CORS for all routes
DATA_DIR = "/data"
VOTES_FILE = 'votes.json'
BB_FILE = 'biggbosspage.json'
meta_home = 'meta_home.json'
meta_bb = 'meta_bb.json'
meta_news = 'meta_news.json'
bigboss_contest = 'bigboss_contest.json'
votes = os.path.join(DATA_DIR, "votes.json")


# ---------------- File Utilities ------------------

def read_file(file, default):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return default

def write_file(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


# ---------------- Votes ------------------

@app.route('/api/votes', methods=['GET'])
def get_votes():
    return jsonify(read_file(VOTES_FILE, {"votes1": 0, "votes2": 0, "votes3": 0}))

@app.route('/api/votes', methods=['POST'])
def update_votes():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format, expected JSON object"}), 400

    current_votes = read_file(VOTES_FILE, {"votes1": 0, "votes2": 0, "votes3": 0})
    current_votes.update(data)
    write_file(VOTES_FILE, current_votes)
    return jsonify(current_votes)


# ---------------- BiggBoss Page Content ------------------

@app.route('/api/biggboss-content', methods=['GET'])
def get_biggboss_content():
    return jsonify(read_file(BB_FILE, []))

@app.route('/api/biggboss-content', methods=['POST'])
def update_biggboss_content():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_file(BB_FILE, data)
        return jsonify({"message": "BiggBoss content updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- BiggBoss Contest ------------------

@app.route('/api/bigboss_contest', methods=['GET'])
def get_bigboss_contest():
    return jsonify(read_file(bigboss_contest, []))

@app.route('/api/bigboss_contest', methods=['POST'])
def update_bigboss_contest():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_file(bigboss_contest, data)
        return jsonify({"message": "BigBoss contest updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        
@app.route('/api/votes', methods=['GET'])
def get_bigboss_votes():
    return jsonify(read_file(votes, []))

@app.route('/api/votes', methods=['POST'])
def update_bigboss_votes():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_file(votes, data)
        return jsonify({"message": "BigBoss contest updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Meta ------------------

def update_meta_content(meta_file, data):
    try:
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_file(meta_file, data)
        return jsonify({"message": "Meta content updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meta_home', methods=['GET'])
def get_meta_home():
    return jsonify(read_file(meta_home, []))

@app.route('/api/meta_home', methods=['POST'])
def update_meta_home():
    data = request.get_json()
    return update_meta_content(meta_home, data)

@app.route('/api/meta_bb', methods=['GET'])
def get_meta_bb():
    return jsonify(read_file(meta_bb, []))

@app.route('/api/meta_bb', methods=['POST'])
def update_meta_bb():
    data = request.get_json()
    return update_meta_content(meta_bb, data)

@app.route('/api/meta_news', methods=['GET'])
def get_meta_news():
    return jsonify(read_file(meta_news, []))

@app.route('/api/meta_news', methods=['POST'])
def update_meta_news():
    data = request.get_json()
    return update_meta_content(meta_news, data)


# ---------------- Start Server ------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
