import sqlite3
import pandas as pd


def setCodeList(data):
    conn = sqlite3.connect('NameAndCode.db')
    c = conn.cursor()
    c.executemany("INSERT INTO NameAndCode VALUES(?, ?)", data)
    print("setCodeList complet e")
    conn.commit()
    c.close()


def makeNameAndCode(name, col):
    conn = sqlite3.connect(name+".db")
    c = conn.cursor()
    cols = ''
    for content in col:
        cols = cols + content + ", "
    cols_insert = ''
    for content in col:
        cols_insert = cols_insert + "'"+content+"'"+", "
    c.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + cols[0:-2] + ")")

    #c.execute("INSERT INTO NameAndCode VALUES" + " (" + cols_insert[0:-2] + ")")
    conn.commit()
    c.close()


def getCode():
    conn = sqlite3.connect("NameAndCode.db")
    conn.row_factory = lambda cursor, row: row[0]  # 데이터 불러오는 형식을 바꿔주는 코드
    c = conn.cursor()
    result = c.execute("SELECT code FROM NameAndCode").fetchall()
    c.close()
    return result


def getName():
    conn = sqlite3.connect("NameAndCode.db")
    conn.row_factory = lambda cursor, row: row[0]  # 데이터 불러오는 형식을 바꿔주는 코드
    c = conn.cursor()
    result = c.execute("SELECT name FROM NameAndCode").fetchall()
    c.close()
    return result


def saveDataFrame(dataFrame, name, code, allMoney):
    conn = sqlite3.connect("dataFrame.db")
    conn2 = sqlite3.connect("dataFrameNameAndCode.db")
    c = conn.cursor()
    c2 = conn2.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS " + name +
              " ('연간실적.2017.12', '연간실적.2018.12', '연간실적.2019.12', '연간실적.2020.12','최근분기실적.2019.06', '최근분기실적.2019.09', '최근분기실적.2019.12','최근분기실적.2020.03', '최근분기실적.2020.06', '최근분기실적.2020.09')")
    c2.execute(
        "CREATE TABLE IF NOT EXISTS dataFrameNameAndCode (name, code, allMoney, scoreMoney, scorePercent)")
    c2.execute("INSERT INTO dataFrameNameAndCode(name, code, allMoney) VALUES(?, ?, ?)",
               [name, code, allMoney])
    conn2.commit()
    dataFrame.to_sql(name, conn, if_exists="replace")
    conn.commit()
    c2.close()
    c.close()
    return "save finish!"


def getDataFrameNameAndAllMoney():
    conn = sqlite3.connect('dataFrameNameAndCode.db')
    conn.row_factory = lambda cursor, row: row[0]  # 데이터 불러오는 형식을 바꿔주는 코드
    c = conn.cursor()
    name = c.execute("SELECT name FROM dataFrameNameAndCode").fetchall()
    allMoney = c.execute(
        "select allMoney from dataFrameNameAndCode").fetchall()
    c.close()
    return [name, allMoney]


def getDataFrame(name):
    conn = sqlite3.connect('dataFrame.db')
    # conn.row_factory = lambda cursor, row: row[0]
    df = pd.read_sql_query("SELECT * FROM " + name, conn)
    c = conn.cursor()
    c.close()
    return df


def setScore(score, name):
    conn = sqlite3.connect('dataFrameNameAndCode.db')
    c = conn.cursor()
    c.execute("update dataFrameNameAndCode set scoreMoney = '" +
              str(score[0]) + "'where name = '" + name+"'")
    c.execute("update dataFrameNameAndCode set scorePercent = '" +
              str(score[1])+"'where name = '" + name+"'")
    conn.commit()
    c.close()
    return "set Score finish!"
