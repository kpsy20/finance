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
    data.makeNameAndCode('NameAndCode', ['code', 'name'])
    allKospiList = utils.crawingAllKospiNameAndCode()  # 모든 얘들 코드와 이름 가져옴
    dbFormat = utils.makeDBFormat(allKospiList)  # 위에 가져온걸 db형식에 맞게 변경
    data.setCodeList(dbFormat)  # NameAndCode.db에 저장
    return "finish!!"


@app.route('/index_getdata/')
def index_getdata():
    code_list = data.getCode()  # return dataframe
    name_list = data.getName()
    for i in range(len(code_list)):
        # dataFrame[0] == 데이터 프레임, dataFrame[1] == 시가총액
        dataFrame = utils.crawlingAllInfo(code_list[i])
        if(len(dataFrame[0]) != 0 and ((name_list[i][-1] != '우' and name_list[i][-2:] != '우B' and name_list[i][-3:] != '우전환') or name_list[i] == '미래에셋대우')):
            data.saveDataFrame(
                dataFrame[0], name_list[i], code_list[i], dataFrame[1])
        # db에 저장.
        print(i)
    return "fetch finish!"


@app.route('/index_setscore/')
def index_setscore():
    # [0] == names, [1] == allMoneys
    dataFrameNameAndAllMoney = data.getDataFrameNameAndAllMoney()
    index = 0
    for name in dataFrameNameAndAllMoney[0]:
        df = data.getDataFrame(name)  # 이러면 데이터 프레임 가져옴
        score = utils.setScore(df, dataFrameNameAndAllMoney[1][index])
        data.setScore(score, name)
    # df 가지고 점수 내면 됨.
        print(name)
        index = index+1
    return "score finish!"


if __name__ == '__main__':
    app.run()
