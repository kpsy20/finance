import utils
import sqlite3
from datetime import datetime
import os
import logging

logging.getLogger().setLevel(logging.INFO)
codeFileName = datetime.today().strftime("%Y%m%d") + "_code.db"
sizeFileName = datetime.today().strftime("%Y%m%d") + "_size.db"


def atDayStart():
    if fileExist(codeFileName):
        logging.info("codeFile already Exist")
        codeL = getCodeFile()
    else:
        logging.info("new codeFile required")
        codeL = utils.getCodeL()
        putCodeFile(codeL)


def fileExist(fileName):
    if fileName in os.listdir("./data/"):
        return True
    return False


def getCodeFile():
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("SELECT code FROM codeL")
    rows = c.fetchall()
    conn.close()
    codeL = [x[0] for x in rows]
    return codeL


def putCodeFile(codeL):
    conn = sqlite3.connect("data/" + codeFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE codeL (code)")
    codeString = " ".join(["('" + x + "')," for x in codeL])[:-1]
    c.execute("INSERT INTO codeL VALUES " + codeString)
    conn.commit()
    conn.close()
