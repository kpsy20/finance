import controller
import data
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def crawingAllKospiNameAndCode():
    code_result = []
    name_result = []
    for page in range(1, 33):
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page='
        res = requests.get(url+str(page))
        html = res.text

        soup = bs(html, 'html.parser')
        title = soup.find_all('th')
        title = [x.text for x in title]

        summary = soup.find_all('tr')
        for i in range(7, len(summary)-1):
            a = summary[i].find_all('a')
            if(a != []):
                code = str(a[0]).index('code=')
                last = str(a[0])[code:].index('"')
                code_result.append(str(a[0])[code+5:code+last])
                name_result.append(a[0].text.replace(
                    "-", "").replace("&", "").replace("(", "").replace(")", "").replace(" ", ""))
        print(page)
    return code_result, name_result  # ([code_result], [name_result]) 형태로 리턴


def makeDBFormat(codeAndNameList):  # codeAndNameList => ([1,2],[3,4])
    result = []
    for i in range(len(codeAndNameList[0])):
        result.append([codeAndNameList[0][i], codeAndNameList[1][i]])
    return result


def crawlingAllInfo(code):
    url = 'https://finance.naver.com/item/main.nhn?code='
    res = requests.get(url + str(code))
    html = res.text
    soup = bs(html, 'html.parser')
    title = soup.find_all('td')
    df = pd.DataFrame([], columns=['default'])
    if(len(title) == 410):  # 정상 얘들, 201118 기준 1575개 중 875개
        result = []
        for tds in range(57, 217):
            if(tds % 10 == 7):
                result.append([])
            result[len(result)-1].append(title[tds].text.replace('\n',
                                                                 '').replace('\t', '').replace(",", "").replace("\xa0", ""))
        row = ['연간실적.2017.12', '연간실적.2018.12', '연간실적.2019.12', '연간실적.2020.12', '최근분기실적.2019.06',
               '최근분기실적.2019.09', '최근분기실적.2019.12', '최근분기실적.2020.03', '최근분기실적.2020.06', '최근분기실적.2020.09']
        data_index = ["매출액(억원)", "영업이익(억원)", "당기순이익(억원)", "영업이익률(%)", "순이익률(%)", "ROE(%)",
                      "부채비율", "당좌비율", "유보율", "EPS(원)", "PER(배)", "BPS(원)", "PBR(배)", "주당배당금(원)", "시가배당률(%)", "배당성향(%)"]
        df = pd.DataFrame([], columns=row, index=data_index)

        for i in range(16):
            df.iloc[i] = result[i]
    return df
    # td 57~216까지가 기업실적분석표
    # td 217~286이 동일업종비교표
    # 연간실적(2017.12 2018.12 2019.12 2020.12), 최근분기실적(2019.06 2019.09, 2019.12, 2020.03, 2020.06, 2020.09)
    # 매출액 57~66
    # 영업이익 67
    # 당기순이익 77
    # 영업이익률 87
    # 순이익률 97
    # ROE 107
    # 부채비율 117
    # 당좌비율 127
    # 유보율 137
    # EPS 147
    # PER 157
    # BPS 167
    # PBR 177
    # 주당배당금 187
    # 시가배당률 197
    # 배당성향 207


def setScore(df):
    element = []
    for i in range(len(df)):
        element.append(df.iloc[i])
    result = scoreYearMoney(element)
    return result


def scoreYearMoney(ele):  # ele = list
    # print(ele[0]) 매출액 0, 0, .. 10개
    i = [0, 1, 2]
    score = []
    year_score = []
    for index in i:
        year = []
        for element in range(1, 5):
            if(ele[index][element] != '' and ele[index][element] != '-'):  # valid value
                year.append(ele[index][element])
        print("year", year)
        for num in range(len(year)-1):
            year_score.append(
                (float(year[num+1]) - float(year[num])) / float(year[num]))
        all = 0
        for last in range(len(year_score)):
            all = all + year_score[last]
            if(last == len(year_score)-1):
                if(last == 0):
                    all = 0
                else:
                    all = all / float(last)
        if(all != 0):
            score.append(all)
    result = 0
    for val in score:
        result = result + val
    if(len(score) != 0):
        result = (result / float(len(score))) * 100
    else:
        result = 0
    return result


def scoreYearPercent(ele):
    i = [3, 5, 6]
