import utils
import sqlite3
from datetime import datetime
import os
import logging

logging.getLogger().setLevel(logging.INFO)
codeFileName = datetime.today().strftime("%Y%m%d") + "_code.db"
sizeFileName = datetime.today().strftime("%Y%m%d") + "_size.db"
goodFileName = datetime.today().strftime("%Y%m%d") + "_good.db"


def atDayStart():
    if fileExist(codeFileName):
        logging.info("codeFile already Exist")
        codeL = getCodeL()
    else:
        logging.info("new codeFile required")
        codeL = utils.getCodeL()
        putCodeL(codeL)

    if fileExist(sizeFileName):
        logging.info("sizeFile already Exist")
        size3, size10 = getSize3Size10()
    else:
        logging.info("new sizeFile required")
        size3, size10 = utils.getSize3Size10()
        putSize3Size10(size3, size10)


def fileExist(fileName):
    if fileName in os.listdir("./data/"):
        return True
    return False


def getCodeL():
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("SELECT code FROM codeL")
    rows = c.fetchall()
    conn.close()
    codeL = [x[0] for x in rows]
    return codeL


def putCodeL(codeL):
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE codeL (code)")
    codeString = " ".join(["('" + x + "')," for x in codeL])[:-1]
    c.execute("INSERT INTO codeL VALUES " + codeString)
    conn.commit()
    conn.close()


def getSize3Size10():
    conn = sqlite3.connect("data/" + sizeFileName)
    c = conn.cursor()
    c.execute("SELECT size3, size10 FROM sizeL")
    rows = c.fetchall()
    conn.close()
    size3, size10 = rows[0]
    return size3, size10


def putSize3Size10(size3, size10):
    conn = sqlite3.connect("data/" + sizeFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE sizeL (size3, size10)")
    sizeString = "('" + str(size3) + "', '" + str(size10) + "')"
    c.execute("INSERT INTO sizeL VALUES " + sizeString)
    conn.commit()
    conn.close()