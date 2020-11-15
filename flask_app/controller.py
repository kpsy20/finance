from flask import Flask, request, render_template, jsonify
import localData
import utils
import requests
from bs4 import BeautifulSoup as bs

global date
date = "20201113_good.db"

app = Flask(__name__)


@app.route('/')
def index_screener():
    return render_template('screener.html')


@app.route('/screener')
def screener():
    return render_template('screener.html')


@app.route('/good')
def good():
    global date
    statusGoodL = utils.statusGoodL(localData.getGoodL(date))
    return render_template('good.html', goodL=statusGoodL)


@app.route('/good_vue')
def candidate():
    return render_template('good_vue.html')


@app.route('/getGoodL')
def getGoodL():
    global date
    return jsonify(goodL=utils.statusGoodL(localData.getGoodL(date)))


@app.route('/screener_filter')
def screener_filter():
    args = request.args
    minPer = (args['minPer'])
    maxPer = (args['maxPer'])
    minRoe = (args['minRoe'])
    maxRoe = (args['maxRoe'])
    minmaxIndex = ["minPer", "maxPer", "minRoe", "maxRoe"]
    minmaxL = {"minPer": minPer, "maxPer": maxPer,
               "minRoe": minRoe, "maxRoe": maxRoe}
    for i in range(0, len(minmaxIndex)):
        if(minmaxL[minmaxIndex[i]] != ''):
            try:
                minmaxL[minmaxIndex[i]] = float(minmaxL[minmaxIndex[i]])
            except:
                return "error"
        else:  # 공백으로 넘겨준 경우
            if(i == 0 or i == 2):
                minmaxL[minmaxIndex[i]] = float('-inf')
            if(i == 1 or i == 3):
                minmaxL[minmaxIndex[i]] = float('inf')

    dataL = utils.crawlingSiseOption(minmaxL, minmaxIndex)
    return jsonify(dataL=dataL)


@app.route('/screener_sise')
def screener_sise():
    # 이거 페이지 32페이지 까지 있음
    dataL = utils.crawlingSise()
    return jsonify(dataL=dataL)


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
    localData.dataUpdate("20201113")
    app.run()
