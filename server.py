from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    data = '{"type": "Feature", "properties": { "title": "City Hall", "description": "0"}, "geometry": { "coordinates": [-79.384293, 43.653908 ], "type": "Point" }}'
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)