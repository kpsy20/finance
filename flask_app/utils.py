import requests
from bs4 import BeautifulSoup as bs

report_url = "https://navercomp.wisereport.co.kr/v2/company/c1050001.aspx?cn=&cmp_cd="
consensus_url = "https://navercomp.wisereport.co.kr/company/ajax/c1050001_data.aspx?flag=2&finGubun=MAIN&frq=0" \
                "&chartType=svg&cmp_cd= "
code_url = "https://finance.naver.com/item/main.nhn?code="


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
