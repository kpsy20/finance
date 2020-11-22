import sqlite3


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
