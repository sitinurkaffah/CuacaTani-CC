import json
from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import os
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)
csrf = CSRFProtect(app)

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = 'cuacatani'

users = []

# Data JSON yang diberikan
json_data = '''
[
    {"type":"database","name":"plants"},
    {
        "type":"table",
        "name":"plants",
        "database":"plants",
        "data": [
            {"id":"1","name":"Padi","image":"https://storage.cloud.google.com/cuacatani.appspot.com/padi-removebg-preview.png","category":"grains"},
            {"id":"2","name":"Kacang Hijau","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kacang_hijau-removebg-preview.png","category":"grains"},
            {"id":"3","name":"Anggur","image":"https://storage.cloud.google.com/cuacatani.appspot.com/anggur-removebg-preview.png","category":"fruit"},
            {"id":"4","name":"Apel","image":"https://storage.cloud.google.com/cuacatani.appspot.com/apple-removebg-preview.png","category":"fruit"},
            {"id":"5","name":"Jeruk","image":"https://storage.cloud.google.com/cuacatani.appspot.com/jeruk-removebg-preview.png","category":"fruit"},
            {"id":"6","name":"Melon","image":"https://storage.cloud.google.com/cuacatani.appspot.com/melon-removebg-preview.png","category":"fruit"},
            {"id":"7","name":"Kapas","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kapas-removebg-preview.png","category":"fiber"},
            {"id":"8","name":"Pepaya","image":"https://storage.cloud.google.com/cuacatani.appspot.com/pepaya-removebg-preview.png","category":"fruit"},
            {"id":"9","name":"Semangka","image":"https://storage.cloud.google.com/cuacatani.appspot.com/semangka-removebg-preview.png","category":"fruit"},
            {"id":"10","name":"Jagung","image":"https://storage.cloud.google.com/cuacatani.appspot.com/jagung-removebg-preview.png","category":"grains"},
            {"id":"11","name":"Mangga","image":"https://storage.cloud.google.com/cuacatani.appspot.com/mangga-removebg-preview.png","category":"fruit"},
            {"id":"12","name":"Kopi","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kopi-removebg-preview.png","category":"grains"},
            {"id":"13","name":"Buncis","image":"https://storage.cloud.google.com/cuacatani.appspot.com/buncis-removebg-preview.png","category":"vegetable"},
            {"id":"14","name":"Kacang Polong","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kacang_polong.png","category":"vegetable"},
            {"id":"15","name":"Kacang Panjang","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kacang_panjang.png","category":"vegetable"},
            {"id":"16","name":"Lentil Hitam","image":"https://storage.cloud.google.com/cuacatani.appspot.com/lentil_hitam.png","category":"grains"},
            {"id":"17","name":"Lentil","image":"https://storage.cloud.google.com/cuacatani.appspot.com/lentil.png","category":"grains"},
            {"id":"18","name":"Delima","image":"https://storage.cloud.google.com/cuacatani.appspot.com/delima.png","category":"fruit"},
            {"id":"19","name":"Pisang","image":"https://storage.cloud.google.com/cuacatani.appspot.com/pisang.png","category":"fruit"},
            {"id":"20","name":"Kelapa","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kelapa.png","category":"fruit"},
            {"id":"21","name":"Kacang Merah","image":"https://storage.cloud.google.com/cuacatani.appspot.com/kacang_merah.png","category":"grains"}
        ]
    }
]
'''

# Mengonversi string JSON menjadi objek Python
plants_data = json.loads(json_data)[1]['data']

def k2c(kelvin):
    c = float(kelvin) - 273.15
    return round(c, 2)

def get_weather_data():
    appid = '211dec237321e8df95005da2c4b2976f'
    mode = 'xml'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Kediri,Jatim,id&mode=xml&appid=211dec237321e8df95005da2c4b2976f'
   
    try:
        raw = urllib.request.urlopen(url).read()
        root = ET.fromstring(raw.decode())

        city = root.find('city')
        temperature = root.find('temperature')
        humidity = root.find('humidity')
        pressure = root.find('pressure')

        weather_data = {
            'kota': city.attrib['name'],
            'temperatur': k2c(temperature.attrib['value']),
            'kelembaban': humidity.attrib['value'] + ' ' + humidity.attrib['unit'],
            'tekanan': pressure.attrib['value'] + ' ' + pressure.attrib['unit']
        }

        return weather_data
    except Exception as e:
        return {'error': True, 'message': str(e)}

@app.route('/register', methods=['POST', 'GET'])
@csrf.exempt
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

@app.route('/plants', methods=['GET'])
def get_plants_data():
    return jsonify(plants_data)

@app.route('/weather', methods=['GET'])
def weather():
    """Route to get weather information."""
    data = get_weather_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
