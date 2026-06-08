try:
    from flask import Flask # type: ignore
except ImportError:
    print('error al inportar flask')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!\n" 