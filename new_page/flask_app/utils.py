import controller
import data
import requests
from bs4 import BeautifulSoup as bs


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
        print(len(summary))
        for i in range(7, len(summary)-1):
            a = summary[i].find_all('a')
            if(a != []):
                code = str(a[0]).index('code=')
                last = str(a[0])[code:].index('"')
                code_result.append(str(a[0])[code+5:code+last])
                name_result.append(a[0].text)
    return code_result, name_result  # ([code_result], [name_result]) 형태로 리턴
