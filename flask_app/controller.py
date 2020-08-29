from flask import Flask
import localData

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    localData.dataUpdate("20200828")
