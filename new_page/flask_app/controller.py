from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup as bs
import data
import utils

app = Flask(__name__)


@app.route('/index/')
def index():
    data.makeNameAndCode('NameAndCode', ['code', 'name'])
    return render_template('index.html')


@app.route('/index_database/')
def index_database():
    data.makeNameAndCode('NameAndCode', ['code', 'name'])  # 내가 하다가 지웠을때 때문에 추가
    allKospiList = utils.crawingAllKospiNameAndCode()
    dbFormat = utils.makeDBFormat(allKospiList)
    data.setCodeList(dbFormat)
    return "finish!!"


@app.route('/index_getdata/')
def index_getdata():
    print(data.getCode())
    return "fetch finish!"


if __name__ == '__main__':
    app.run()
