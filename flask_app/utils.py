import requests
from bs4 import BeautifulSoup as bs
import localData

report_url = "https://navercomp.wisereport.co.kr/v2/company/c1050001.aspx?cn=&cmp_cd="
code_url = "https://finance.naver.com/item/main.nhn?code="
consensus_url = "https://navercomp.wisereport.co.kr/company/ajax/c1050001_data.aspx?flag=2&finGubun=MAIN&frq=0" \
                "&chartType=svg&cmp_cd= "
size_market_url_0 = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
size_market_url_1 = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page="


# ham..

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


def isETNByName(name):
    if "ETN" in name:
        return True
    return False


def isFirstByName(name):
    if name[-1] == "우":
        return True
    if name[-2:] in ["우A", "우B", "우C"]:
        return True
    return False


def isStockByName(name):
    if "ETF" in name or "ETN" in name:
        return False
    return isFirstByName(name)


# 주식 선택위해 사용할 조건들
def perUnder7(soup_report):
    try:
        per_str = [x.text.split()[1] for x in soup_report.select_one(".td0301").select(".line-left") if
                   x.text.split()[0] == "PER"][0]
        per_float = float(cleanText(per_str))
        if 0 < per_float < 7:
            return per_float
        return -1
    except:
        return -1


def pbrUnder1(soup_report):
    try:
        pbr_str = [x.text.split()[1] for x in soup_report.select_one(".td0301").select(".line-left") if
                   x.text.split()[0] == "PBR"][0]
        pbr_float = float(cleanText(pbr_str))
        if 0 < pbr_float < 1:
            return pbr_float
        return -1
    except:
        return -1


def per_avg(soup_report):
    try:
        per_str = [x.text.split()[1] for x in soup_report.select_one(".td0301").select(".line-left") if
                   x.text.split()[0] == "업종PER"][0]
        per_float = float(cleanText(per_str))
        if per_float > 0:
            return per_float
        return -1
    except:
        return -1


def marketSumInRange(soup, size3, size10):
    try:
        marketSum = int(cleanText(soup.select_one("#_market_sum").text))
        if marketSum <= size3 or marketSum >= size10:
            return True
        return False
    except:
        return False


# 시가총액 3분위, 10분위 기준 구하기
def getSize3Size10():
    # TODO: 해당 일자에 구해둔 결과가 있으면 해당 결과로 반환하도록 리팩토링
    sizeL = []
    for i in range(1, 33):
        soup = bs(requests.get(size_market_url_0 + str(i)).text, 'html.parser')
        tempL = [x.select("td.number")[4].text for x in
                 soup.select("table")[1].select_one("tbody").findAll("tr", {"onmouseout": "mouseOut(this)"}) if
                 isStockByName(x.select_one("a.tltle").text)]
        sizeL += [int(x.replace(",", "")) for x in tempL]
    for i in range(1, 30):
        soup = bs(requests.get(size_market_url_1 + str(i)).text, 'html.parser')
        tempL = [x.select("td.number")[4].text for x in
                 soup.select("table")[1].select_one("tbody").findAll("tr", {"onmouseout": "mouseOut(this)"}) if
                 isStockByName(x.select_one("a.tltle").text)]
        sizeL += [int(x.replace(",", "")) for x in tempL]
    sizeL = sorted(sizeL)
    size = len(sizeL)
    size3 = sizeL[:int(size * 0.3)][-1]
    size10 = sizeL[-int(size * 0.1):][0]
    return size3, size10


# 전체 code list 구하기 (하루 한번)
def getCodeL():
    codeL = []
    for i in range(1, 33):
        soup = bs(requests.get(size_market_url_0 + str(i)).text, 'html.parser')
        tempL = [x.attrs["href"].split("code=")[1] for x in
                 soup.select("table ")[1].select_one("tbody").select("a.tltle")]
        codeL += tempL
    for i in range(1, 30):
        soup = bs(requests.get(size_market_url_1 + str(i)).text, 'html.parser')
        tempL = [x.attrs["href"].split("code=")[1] for x in
                 soup.select("table ")[1].select_one("tbody").select("a.tltle")]
        codeL += tempL
    codeL.reverse()
    return codeL


# 좋은 종목 리스트 구하기
def getGoodL(codeL):
    goodL = []
    size3, size10 = getSize3Size10()

    for code in codeL:
        soup = getSoupFromCode(code)
        # 시가총액에 맞는 애들만 선별
        if not marketSumInRange(soup, size3, size10):
            continue
        soup_report = getSoupFromReport(code)
        name = getName(soup)

        # etf/etn/우선주 제외
        if isETF(soup) or isETNByName(name) or isFirstByName(name):
            continue

        # 0<per<7, 0<pbr<1
        per = perUnder7(soup_report)
        pbr = pbrUnder1(soup_report)
        perAvg = per_avg(soup_report)
        if per == -1 or pbr == -1 or perAvg == -1:
            continue

        # 출력
        goodL.append([code, name])
    return goodL


def statusGoodL(goodL):
    result = [x + [localData.getStatus(x[0])] for x in goodL]
    return result
