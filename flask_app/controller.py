from flask import Flask, render_template
import localData
import utils

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/good')
def good():
    statusGoodL = utils.statusGoodL(localData.getGoodL("20200828_good.db"))
    print(statusGoodL)
    return render_template('good.html', goodL=statusGoodL, test="hi")


@app.route('/candidate')
def candidate():
    return render_template('candidate.html')


if __name__ == '__main__':
    print(localData.getStatus("1"))
