import requests
from bs4 import BeautifulSoup as bs

report_url = "https://navercomp.wisereport.co.kr/v2/company/c1050001.aspx?cn=&cmp_cd="
code_url = "https://finance.naver.com/item/main.nhn?code="
consensus_url = "https://navercomp.wisereport.co.kr/company/ajax/c1050001_data.aspx?flag=2&finGubun=MAIN&frq=0" \
                "&chartType=svg&cmp_cd= "


# base code
def getSoupFromCode(code):
    soup = bs(requests.get(code_url + code).text, 'html.parser')
    return soup


def cleanText(text):
    return text.replace("\n", "").replace("\t", "").replace("조", "").replace(",", "")


def getName(soup):
    name = soup.select_one("#middle > div.h_company > div.wrap_company > h2 > a").text
    return name


def getSoupFromReport(code):
    soup = bs(requests.get(report_url + code).text, 'html.parser')
    return soup


def getJsonFromConsensus(code):
    return requests.get(consensus_url + code).json()


# stock name code
def isETF(soup):
    if len(soup.select(".e_summary")) == 0:
        return False
    return True


def isETN(soup):
    name = getName(soup)
    if "ETN" in name:
        return True
    return False


def isFirstByName(name):
    if name[-1] == "우":
        return True
    if name[-2:] in ["우A", "우B", "우C"]:
        return True
    return False


def isFirstBySoup(soup):
    name = getName(soup)
    return isFirstByName(name)


def isStockByName(name):
    if "ETF" in name or "ETN" in name:
        return False
    return isFirstByName(name)
