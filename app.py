from flask import Flask, render_template, jsonify, request

import json
from flask_cors import CORS


app = Flask(__name__)

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})


@app.route('/hello/<name>')
def hello_page(name):
    return 'Hello %s!' % name


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/operations')
def operations():
    return render_template('demo.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    req_obj = request.get_json('username')
    username = req_obj['username']
    first_name = req_obj['first_name']
    last_name = req_obj['last_name']

    with open('db.json', 'rb') as f:
        data = f.read()
        json_obj = json.loads(data)
        
        if username in json_obj:
            return "User exists", 500

        json_obj[username]= {
                        'first_name': first_name,
                        'last_name': last_name,
                        }

    with open('db.json', 'w') as f:
        json.dump(json_obj, f)
    
    return "Success", 201



@app.route('/delete_user', methods=['DELETE'])
def delete_user():

    req_obj = request.get_json('username')
    username = req_obj['username']

    with open('db.json', 'rb') as f:
        data = f.read()
        json_obj = json.loads(data)
        
        if username not in json_obj:
            return "User not found", 500
    
    del json_obj[username]

    with open('db.json', 'w') as f:
        json.dump(json_obj, f)
    
    return "Success", 201



@app.route('/get_users', methods=['GET'])
def get_users():

    with open('db.json', 'rb') as f:
        data = f.read()
        json_obj = json.loads(data)
        return json_obj, 200       

if __name__ == '__main__':
    app.run(debug=True)
