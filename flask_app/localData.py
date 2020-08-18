import utils
import sqlite3
from datetime import datetime
import os

fileName = "data/"+datetime.today().strftime("%Y%m%d")+".db"


def atDayStart():
    if codeFileExist():
        codeL = getCodeFile()
    else:
        codeL = utils.getCodeL()
        putCodeFile(codeL)


def codeFileExist():
    if fileName in os.listdir("./"):
        return True
    return False


def getCodeFile():
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    c.execute("SELECT code FROM codeL")
    rows = c.fetchall()
    conn.close()
    codeL = [x[0] for x in rows]
    return codeL


def putCodeFile(codeL):
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    c.execute("CREATE TABLE codeL (code)")
    codeString = " ".join(["('" + x + "')," for x in codeL])[:-1]
    c.execute("INSERT INTO codeL VALUES " + codeString)
    conn.commit()
    conn.close()
