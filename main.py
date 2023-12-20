from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
csrf = CSRFProtect(app)

users = []

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = 'cuacatani'

@app.route('/register', methods=['POST', 'GET'])
@csrf.exempt  # Use this line to exempt CSRF protection for the /register endpoint
def register():
    if request.method == 'POST':
        data = request.get_json()

        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': True, 'message': '"username", "email", and "password" are required'}), 400

        user = {
            'username': data['username'],
            'email': data['email'],
            'password': generate_password_hash(data['password'], method='pbkdf2:sha256:50000')
        }
        users.append(user)

        return jsonify({'error': False, 'message': 'Registration successful'}), 200
    elif request.method == 'GET':
        return jsonify(users), 200

@app.route('/login', methods=['POST', 'GET'])
@csrf.exempt
def login():
    if request.method == 'POST':
        data = request.get_json()

        if 'email' not in data or 'password' not in data:
            return jsonify({'error': True, 'message': '"email" and "password" are required'}), 400

        for user in users:
            if user['email'] == data['email'] and check_password_hash(user['password'], data['password']):
                # Modify the response structure
                login_result = {
                    'email': user['email'],  # Replace 'userId' with 'email'
                    'username': user.get('username', ''),
                }
                response = {
                    'error': False,
                    'message': 'success',
                    'loginResult': login_result
                }
                return jsonify(response), 200

        return jsonify({'error': True, 'message': 'User not found or incorrect password'}), 401
    elif request.method == 'GET':
        return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)
