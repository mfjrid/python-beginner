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

@app.route("/", methods=['GET'])
@token_required
def root():
    return "Hello World!"

@app.route("/about", methods=['GET'])
def about():
    return make_response(jsonify({"nama": "fajar", "umur": 26}))

if "__main__" == __name__:
    app.run(debug=True)