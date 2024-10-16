from flask import Flask, jsonify, session, request, render_template
from flask_wtf.csrf import CSRFProtect
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Enable CSRF protection
csrf = CSRFProtect(app)

# Initialize Firebase
cred = credentials.Certificate("creds.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

# A sample API route to simulate the Flask backend
@app.route('/api/data', methods=['GET'])
def get_data():
    # Example: Fetching data from Firestore
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    users = []
    for doc in docs:
        users.append(doc.to_dict())

    return jsonify({
        "status": "success",
        "data": users
    }), 200

# Simulate a protected route that requires a valid session
@app.route('/api/protected', methods=['POST'])
def protected():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    # Only accessible if the session is valid
    return jsonify({"message": "Protected content"}), 200

# Simple login route to simulate session creation
@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.json.get('username', 'guest')
    return jsonify({"message": f"Welcome, {session['user']}!"}), 200

# Simple logout route to clear the session
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
