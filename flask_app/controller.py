from flask import Flask
import utils

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    goodL = utils.getGoodList(utils.getCodeL())
    print(goodL)
