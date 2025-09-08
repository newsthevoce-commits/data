from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ enables CORS for all routes

VOTES_FILE = 'votes.json'
BB_FILE = 'biggbosspage.json'
meta_home = 'meta_home.json'
meta_bb = 'meta_bb.json'
meta_news = 'meta_news.json'
bigboss_contest = 'bigboss_contest.json'


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


def read_meta(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def write_meta(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


def read_bb_contest(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []
def write_meta(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)



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
    


@app.route('/bigboss_contest', methods=['GET'])
def get_bigboss_contest():
    return jsonify(read_bb_contest(bigboss_contest))

@app.route('/bigboss_contest', methods=['POST'])
def update_bigboss_contest():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_bb_contest(bigboss_contest, data)
        return jsonify({"message": "BiggBoss content updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






def update_meta_content(meta_file, data):
    try:
        
        if not isinstance(data, list):
            return jsonify({"error": "Expected a JSON list of content blocks"}), 400
        write_meta(meta_file, data)
        return jsonify({"message": "BiggBoss content updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ----------- Meta GET routes -----------

@app.route('/meta_home', methods=['GET'])
def get_meta_home():
    return jsonify(read_meta(meta_home))

@app.route("/meta_bb", methods=['GET'])
def get_meta_bb():
    return jsonify(read_meta(meta_bb))

@app.route("/meta_news", methods=['GET'])
def get_meta_news():
    return jsonify(read_meta(meta_news))


# ----------- Meta POST routes -----------

@app.route('/meta_home', methods=['POST'])
def update_meta_home():
    data = request.get_json()
    return update_meta_content(meta_home, data)

@app.route('/meta_bb', methods=['POST'])
def update_meta_bb():
    data = request.get_json()
    return update_meta_content(meta_bb, data)

@app.route('/meta_news', methods=['POST'])
def update_meta_news():
    data = request.get_json()
    return update_meta_content(meta_news, data)









# ---------------- Start Server ------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
