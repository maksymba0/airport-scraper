from flask import Flask, jsonify
import Home

app = Flask(__name__)

@app.route("/")
def home():
    return Home.home_()

@app.route("/api/ping")
def ping():
    return jsonify({"status":"ok","message":"Flask is alive"})

def main():
    print("Starting")
    app.run(debug=True)
print("Hello world")
if __name__ == '__main__':
    main()