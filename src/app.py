from flask import Flask, request, jsonify
import upreverse

app = Flask(__name__)

@app.get("/v1")
def howdy():
    return "Hey! Please post to this endpoint with a payload of {'data': 'your string here'}"

@app.post("/v1")
def upcase_and_reverse():
    if request.is_json:
        req_body = request.get_json()
        return {"data": upreverse.upcase(upreverse.reverse(req_body["data"]))}
