from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup as bs
import data
import utils

app = Flask(__name__)


@app.route('/index/')
def index():
    data.makeNameAndCode('NameAndCode', ['name', 'code'])
    return render_template('index.html')


@app.route('/index_database/')
def index_database():
    allKospiList = utils.crawingAllKospiNameAndCode()
    dbFormat = utils.makeDBFormat(allKospiList)
    data.setCodeList(dbFormat)
    return "finish!!"


if __name__ == '__main__':
    app.run()
