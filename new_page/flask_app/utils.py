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


def strToFloat(num):
    num = num.replace(',', '')
    if('조' in num):
        jo = num[0:num.find('조')]
        uk = num[num.find('조')+1:num.find('억')]
        result = int(jo)*10000+int(uk)
    else:
        result = num[0:num.find('억')]
    return int(result)


def crawlingAllInfo(code):
    url = 'https://finance.naver.com/item/main.nhn?code='
    res = requests.get(url + str(code))
    html = res.text
    soup = bs(html, 'html.parser')
    title = soup.find_all('td')
    df = pd.DataFrame([], columns=['default'])
    allMoney = 0
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
        allMoney = strToFloat(
            title[287].text.replace("\n", '').replace('\t', ''))
    return df, allMoney
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


def setScore(df, allMoney):
    element = []
    result = []
    for i in range(len(df)):
        element.append(df.iloc[i])
    result.append(scoreMoney(element, allMoney))
    result.append(scorePercent(element, allMoney))
    return result


def scoreMoney(ele, allMoney):  # ele = list
    # print(ele[0]) 매출액 0, 0, .. 10개
    i = [0, 1, 2]  # 매출액, 영업이익, 당기순이익
    score = []
    for index in i:
        year_score = []
        year = []
        divide = []
        for element in range(5, 11):
            if(ele[index][element] != '' and ele[index][element] != '-'):  # valid value
                year.append(ele[index][element])
                divide.append(element)
        #print("year", year)
        for num in range(len(year)-1):
            year_score.append(
                (float(year[num+1]) - float(year[num])) /
                (divide[len(divide)-num-1]-5))  # 옛날 자료는 비율 낮게.. 2017 - 2018 3으로 나눔, 2018 - 2019 2로 나눔 2019 - 2020 1로 나눔
        all = 0
        for last in range(len(year_score)):
            all = all + year_score[last]
            if(last == len(year_score)-1):
                all = all / (float(last) + 1) / int(allMoney)
        if(all != 0):
            score.append(all)
    result = 0
    for val in score:
        result = result + val
    if(len(score) != 0):
        result = (result / float(len(score))) * 100
    else:
        result = 0
    print(result)
    return result


def scorePercent(ele, allMoney):
    i = [3, 4, 5]  # 영업이익률, 순이익률, ROE
    score = []
    for index in i:
        year_score = []
        year = []
        divide = []
        for element in range(5, 11):
            if(ele[index][element] != '' and ele[index][element] != '-'):  # valid value
                year.append(ele[index][element])
                divide.append(element)
        #print("year", year)
        for num in range(len(year)-1):
            year_score.append(
                (float(year[num+1]) - float(year[num])) / (divide[len(divide)-num-1]-5))
            # 옛날 자료는 비율 낮게.. 2017 - 2018 3으로 나눔, 2018 - 2019 2로 나눔 2019 - 2020 1로 나눔
        all = 0
        for last in range(len(year_score)):
            all = all + year_score[last]
            if(last == len(year_score)-1):
                all = all / (float(last) + 1) / int(allMoney)
        if(all != 0):
            score.append(all)
    result = 0
    for val in score:
        result = result + val
    if(len(score) != 0):
        result = (result / float(len(score))) * 100
    else:
        result = 0
    print(result)
    return result
