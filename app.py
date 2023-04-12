from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "askdlh7348r4378r3uihewu89f349f3483hio"

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("JWT")

        if not token:
            return jsonify({"msg" : "Token Required", "code": 403}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"msg" : "Token was Invalid", "code": 403}), 403

        return f(*args, **kwargs)
    return decorator

@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.json
        if (data['username'] == 'admin' and data['password'] == 'admin123'):
            token = jwt.encode({"user" : data['username'], "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        else:
            return jsonify({"msg" : "Wrong Credential", "code": 403}), 403
    except Exception as e:
        return jsonify({"msg" : str(e), "code": 403}), 403

@app.route("/", methods=['GET'])
@token_required
def root():
    return "Hello World!"

@app.route("/about", methods=['GET'])
def about():
    return make_response(jsonify({"nama": "fajar", "umur": 26}))

if "__main__" == __name__:
    app.run(debug=True)