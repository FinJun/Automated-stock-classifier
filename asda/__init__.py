from wer.kiwoom import * #파일위치 확인!!
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
class Start_kiwoom(): # 키움 api를 시작하는 class
    def __init__(self):
        print("kiwoom 작동")
        self.code_list=[] # 코드를 받아줄 list

        self.app= QApplication(sys.argv) #list 형태로 담겨져 있는데 파일경로를 앱처럼 쓸수있게끔 초기값잡아줌

        self.Kiwoom=Kiwoom() #kiwoom 모듈의 Kiwwom 클래스 접근
        while self.Kiwoom.last_num==1: #kiwoom 클래스의 마지막에 추가하였음. 이벤트루프를 종료하기위해 설정
            self.code_list=self.Kiwoom.code_list
            self.name_list=self.Kiwoom.last_name_list
            if self.code_list!=[] and self.name_list!=[]:

                break
            else:

                self.app.exec_() #exec의 경우, 종료함수가 따로 없으면 다음 코드로 넘어가지 않게끔 유지해주는 역할을 해줍니다.


# 키움 서버 접속
again ="프로그램을 반복 실행하기 위한 변수"
while again != 2: #프로그램을 실행 및 종료하기 위한 구성입니다.
    k=Start_kiwoom()

    code_list=k.code_list
    name_list=k.name_list

    dict_stock = {}

    for i in range(len(code_list)):
        dict_stock[code_list[i]]=name_list[i]

    print("1차로 거른 리스트 : ",dict_stock) #걸러진 종목들을 사전형태로 만들어줘서 다양한 곳에 쓰일 수 있게끔 만들어주었습니다.




    # 생성할 기업 재무 정보 DataFrame 생성
    corpinfo_card = pd.DataFrame({'code': [], 'PER': [], '12M PER': [], '업종 PER': [], 'PBR': [], '배당수익률': []})

    # URL을 통해 결과 요청
    code = code_list
    for i in code:
        # URL 통해 HTML 요청
        url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?'
        param = 'pGB=1&gicode=' + 'A' + i + '&cID=&MenuYn=Y&ReportGB=&NewMenuID=Y&stkGb=701'
        response = requests.get(url + param)
        # 에러 체크
        if (response.status_code != 200):
            print("Error Occur")
        # BeautifulSoup 활용하여 DOMtree로 가져오기
        soup = BeautifulSoup(response.text, 'html.parser')
        corpinfo = soup.select('.corp_group2 > dl > dd')
        # 종목 별 재무 지수 String으로 갖고 오기

        if len(corpinfo) == 0:
            continue

        PER = corpinfo[0].string
        PER_12M = corpinfo[1].string
        PER_sec = corpinfo[2].string
        PBR = corpinfo[3].string
        Div_Yie = corpinfo[4].string
        # corpinfo_card에 추가할 row 생성
        row = [i, PER, PER_12M, PER_sec, PBR, Div_Yie]
        # corpinfo_card에 새로운 행 추가
        corpinfo_card = corpinfo_card.append(pd.Series(row, index=corpinfo_card.columns), ignore_index=True)

    print(corpinfo_card)

    cod_list2 = []

    for i in range(len(corpinfo_card)):
        m = corpinfo_card['PER'][i].replace(",", "")
        n = corpinfo_card['업종 PER'][i].replace(",", "")
        if m == "-":
            m = 0

        if n == "-":
            n = 0

        if float(m) < float(n):
            cod_list2.append(corpinfo_card['code'][i])
        else:
            pass

    print("재무제표로 걸러진 리스트 !!", cod_list2, '\n')


    # 종목번호를 종목명으로 바꿔주는 작업
    name_list = []

    for i in cod_list2:
        name_list.append(dict_stock[i])

    # 기사 크롤링
    class Crawling:
        def __init__(self, first):
            self.setdata(first)

        def setdata(self, first):
            self.first = first

            from urllib.parse import quote_plus

            search_keyword = name_list[self.first]
            # 1개월 이내 네이버 뉴스
            url = f'https://search.naver.com/search.naver?where=news&query={quote_plus(search_keyword)}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=2&ds=&de=&docid=&nso=so%3Ar%2Cp%3A1m%2Ca%3Aall&mynews=0&refresh_start=0&related=0'
            #url 요청과 html 요소에 접근
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            news_titles = soup.find_all(class_='news_tit')

            print(name_list[self.first], len(news_titles), '개의 뉴스 (최근 1개월)')
            #제목과 주소 출력
            for i in news_titles:
                print(i.attrs['title'])
                print(i.attrs['href'])
    #선정 종목 모두에 대해 크롤링
    for i in range(len(name_list)):
        name_list_i = Crawling(i)
        print('\n')

    again=int(input("다시돌려보시겠습니까? 아니면 종료하시겠습니까? 1.다시 2.종료")) # 다른 기능을 추가할 수 있으며, api장점을 활용해 계좌 및 원하는 주식을 매수 매도, 계좌조희등을 할 수 있기에 추가해놓았습니다. 프로그래머가 원하는 방식에 따라 다양하게 활용할 수 있어서 넣었습니다.
    if again==2:
        print("프로그램을 종료합니다.")
        break
    else:
        continue



