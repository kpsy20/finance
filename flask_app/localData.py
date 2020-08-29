import utils
import sqlite3
from datetime import datetime
import os
import logging

logging.getLogger().setLevel(logging.INFO)


def dataUpdate(date):
    if date == "":
        codeFileName = datetime.today().strftime("%Y%m%d") + "_code.db"
        sizeFileName = datetime.today().strftime("%Y%m%d") + "_size.db"
        goodFileName = datetime.today().strftime("%Y%m%d") + "_good.db"
    else:
        codeFileName = date + "_code.db"
        sizeFileName = date + "_size.db"
        goodFileName = date + "_good.db"

    if fileExist(codeFileName):
        logging.info("codeFile already Exist")
        codeL = getCodeL(codeFileName)
    else:
        logging.info("new codeFile required")
        codeL = utils.getCodeL()
        putCodeL(codeFileName, codeL)

    if fileExist(sizeFileName):
        logging.info("sizeFile already Exist")
        size3, size10 = getSize3Size10(sizeFileName)
    else:
        logging.info("new sizeFile required")
        size3, size10 = utils.getSize3Size10()
        putSize3Size10(sizeFileName, size3, size10)

    if fileExist(goodFileName):
        logging.info("goodFile already Exist")
        goodL = getGoodL(goodFileName)
    else:
        logging.info("new goodFile required")
        goodL = utils.getGoodL(codeL)
        logging.info("succeed in getting goodFile")
        putGoodL(goodFileName, goodL)


def fileExist(fileName):
    if fileName in os.listdir("./data/"):
        return True
    return False


def getCodeL(codeFileName):
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("SELECT code FROM codeL")
    rows = c.fetchall()
    conn.close()
    codeL = [x[0] for x in rows]
    return codeL


def putCodeL(codeFileName, codeL):
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE codeL (code)")
    codeString = " ".join(["('" + x + "')," for x in codeL])[:-1]
    c.execute("INSERT INTO codeL VALUES " + codeString)
    conn.commit()
    conn.close()


def getSize3Size10(sizeFileName):
    conn = sqlite3.connect("data/" + sizeFileName)
    c = conn.cursor()
    c.execute("SELECT size3, size10 FROM sizeL")
    rows = c.fetchall()
    conn.close()
    size3, size10 = rows[0]
    return size3, size10


def putSize3Size10(sizeFileName, size3, size10):
    conn = sqlite3.connect("data/" + sizeFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE sizeL (size3, size10)")
    sizeString = "('" + str(size3) + "', '" + str(size10) + "')"
    c.execute("INSERT INTO sizeL VALUES " + sizeString)
    conn.commit()
    conn.close()


def getGoodL(goodFileName):
    conn = sqlite3.connect("data/" + goodFileName)
    c = conn.cursor()
    c.execute("SELECT * FROM goodL")
    rows = c.fetchall()
    conn.close()
    goodL = [[x[0], x[1]] for x in rows]
    return goodL


def putGoodL(goodFileName, goodL):
    conn = sqlite3.connect("data/" + goodFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE goodL (code, name)")
    goodString = " ".join(["('" + x[0] + "', '" + x[1] + "')," for x in goodL])[:-1]
    c.execute("INSERT INTO goodL VALUES " + goodString)
    conn.commit()
    conn.close()


def getStatus(code):
    conn = sqlite3.connect("data/status.db")
    c = conn.cursor()
    c.execute("SELECT status FROM statusTable WHERE code='" + code + "'")
    rows = c.fetchall()
    conn.close()
    if len(rows) == 0:
        return "Not Having"
    return rows[0][0]


def putStatus(code, status):
    conn = sqlite3.connect("data/status.db")
    c = conn.cursor()
    # c.execute("CREATE TABLE statusTable (code UNIQUE, status)")
    c.execute("REPLACE INTO statusTable VALUES ('" + code + "', '" + status + "')")
    conn.commit()
    conn.close()
