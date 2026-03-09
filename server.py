from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/list', methods=["GET"])
def lista_todos():
    




if __name__ == '__main__':
    app.run(debug=False)