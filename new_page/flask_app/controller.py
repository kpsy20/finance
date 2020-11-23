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
    code_list = data.getCode()  # return dataframe
    name_list = data.getName()
    for i in range(len(code_list)):
        dataFrame = utils.crawlingAllInfo(code_list[i])
        if(len(dataFrame) != 0):
            data.saveDataFrame(dataFrame, name_list[i], code_list[i])
        # db에 저장.
        print(i)
    return "fetch finish!"


@app.route('/index_setscore/')
def index_setscore():
    dataFrameNameAndCode = data.getDataFrameNameAndCode()
    for name in dataFrameNameAndCode:
        score = []
        df = data.getDataFrame(name)  # 이러면 데이터 프레임 가져옴
        score.append(utils.setScore(df))
        data.setScore(score, name)
    # df 가지고 점수 내면 됨.
        print(name)
    return "score finish!"


if __name__ == '__main__':
    app.run()
