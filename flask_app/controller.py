from flask import Flask, request, render_template, jsonify
import localData
import utils

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/good')
def good():
    statusGoodL = utils.statusGoodL(localData.getGoodL("20200828_good.db"))
    return render_template('good.html', goodL=statusGoodL)


@app.route('/candidate')
def candidate():
    return render_template('candidate.html')


@app.route('/change_status')
def change_status():
    args = request.args
    code = args['code']
    status = args['status']
    newStatus = localData.changeStatus(code, status)
    if newStatus == "Having":
        buttonName = "매도"
        removeClass = "btn-warning"
        addClass = "btn-success"
    else:
        buttonName = "매수"
        removeClass = "btn-success"
        addClass = "btn-warning"
    return jsonify(newStatus=newStatus, buttonName=buttonName, removeClass=removeClass, addClass=addClass)


if __name__ == '__main__':
    localData.dataUpdate("20200910")
