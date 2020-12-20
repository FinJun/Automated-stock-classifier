from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from wer.config.errorCode import * #로그인 에러를 알아보기 위해 따로 만든 파일입니다. / 파일이 있는지 확인해주셔야합니다!!
from PyQt5.QtWidgets import *
import sys


class Kiwoom(QAxWidget):  # QAxContainer은  디자인구성을 컨트롤하고 재사용하는 기능들을 포함!
    def __init__(self):
        super().__init__()



        # 이벤트 루프 먼저 설정 / 요청값을 받을 동안 다른 코드로 넘어가지 않게끔 해줌.
        self.login_event_loop = None
        self.trading_boom_eventloop =None
        self.date_candle_loop = None

        #변수 앞에다 미리 써놓았습니다.
        self.trading_boom_list=[] #api로 요청한 뒤 급등 종목을 넣어줄 리스트
        self.code_list=[] # 걸러진 종목의 코드를 넣어줄 리스트
        self.last_name_list = [] #걸러진 종목의 이름을 넣어줄 리스트

        #스크린 번호 : api 사용시 필요할 경우가 있지만 이번 프로젝트에서는 그다지 중요하지는 않습니다.
        self.num = 2002

        print("Kiwoom() class start.")
        self.get_ocx_instance()  # ocx제어
        self.event_slots()  # 키움으로부터 요청값을 받아줄 수 있는 이벤트슬롯 열어줌
        self.signal_login_commConnect()  # 로그인 함수 (KOA studio 참고)


        self.trading_boom_stock_find() #거래량이 높은 상위권 종목을 불러오는 함수
        self.up_down_stock() #당일 가격 상승률 상위권 종목들을 불러오는 함수
        self.trading_boom_list=set(self.trading_boom_list) # 중복되는 코드들을 제거하는 과정
        for i in self.trading_boom_list: # 거래량이 높거나 가격상승률이 높은 종목들을 하나씩 분석하는 과정
            self.candle(i) # 종목에 대한 주가및 다양한 정보를 가져옴
            self.standard_array_stock(i) # 이평선 전부 가져옴
            if len(self.data) < 300 : #데이터수가 300보다 작으면 충분한 주가데이터가 없으므로 skip하게끔 하였다 # self.data의 리스트 [[날짜1,종가,시가,저가,고가,거래량],[날짜2,종가,시가,저가,고가,거래량],...] 이렇게 리스트 속에 리스트로 이루어져있습니다. candle 함수 참고!
                continue
            else:
                if {self.last10_moving_price[0] > self.last20_moving_price[0] > self.last60_moving_price[0] > self.last120_moving_price[0] # last_moving_price변수는 standard_array_stock 함수를 불러올시 변수가 설정이 됩니다.
                    or self.last10_moving_price[1] > self.last20_moving_price[1] > self.last60_moving_price[1] > self.last120_moving_price[1]} : # 이동평균선이 오늘 또는 전날 기준으로 상승 추세에 있는 것만 뽑게끔 하였습니다. 이동평균선이 위에서부터 10 20 60 120 순으로 배열되어 있는 것을 정배열이라고 합니다.
                    #self.data의 리스트의 경우,  날짜 종가 시가 저가 고가 거래량 순으로 리스트 형태도 배열되게끔 candle 함수에서 설정하였습니다.
                    if (self.data[0][1] > self.last20_moving_price[0] and self.data[0][2] < self.last20_moving_price[0]) or (self.data[0][4]>self.data[0][3]>self.last20_moving_price[0]) : # 골든크로스일 경우 또는 20일선 위에 저가 고가가 상승으로 형성될경우
                        self.high_price=0 #과거 300일치의 주가 평균
                        for e in range(1,300):
                            self.high_price+=self.data[e][1]
                        self.high_price=(self.high_price/300)
                        if self.data[0][1] < (self.high_price) and self.data[0][5] > 2*self.data[1][5] : # 300일전의 주가평균보다 현주가가 낮은 상태 이고 전날보다 거래량이 2배이상 증가할 경우
                            self.code_list.append(i) #위의 조건식이 전부 true일 경우 리스트에 추가하기로 하였습니다.
        print(self.code_list)

        for see_code_name in self.code_list:  # set은 중복제거
            real_name = self.dynamicCall("GetMasterCodeName(s)", see_code_name)
            self.last_name_list.append(real_name) # 종목코드와 종목명을 매치하기 위해 네임리스트 역시 따로 불러와줘서 만들었습니다.

        print(self.last_name_list)

        if self.code_list == [] : #해당종목이 없을 경우 프로그램 종료하게끔 하였습니다.
            print("해당하는 종목이 없습니다!!","아침에 할 경우, 종목들이 최신화되어 나오지 않을 수 있습니다.")
            exit()

        self.last_num=1 # _init_에서 키움 이벤트루프를 종료시키기위한 수단으로 활용된다.











    def event_slots(self):  # 시그널을 넣을 슬롯 설정
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)


    def login_slot(self, err_code):  # 로그인 슬롯 설정 및 이벤트루프 종료
        print(errors(err_code)) # 에러코드 인자 출력
        self.login_event_loop.exit()  # 이벤트루프종료

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 응용프로그램 제어하게해줌

    def signal_login_commConnect(self):  # 로그인 요청
        self.dynamicCall("CommConnect()")  # 데이터전송이 가능한 함수 dynamicCall
        self.login_event_loop = QEventLoop()  # Qtcore 임포트 해야함.
        self.login_event_loop.exec() #이벤트루프를 지속시키는 코드

    def up_down_stock(self,sPrevNext="0"): #가격 급등 종목 가져오는것
        self.dynamicCall("SetInputValue(s,s)", "시장구분", "000")# 데이터전송이 가능한 함수 dynamicCall
        self.dynamicCall("SetInputValue(s,s)", "등락구분", "1")
        self.dynamicCall("SetInputValue(s,s)", "기간구분", "100")
        self.dynamicCall("SetInputValue(s,s)", "시간", "5")
        self.dynamicCall("SetInputValue(s,s)", "거래량구분", "00150")
        self.dynamicCall("SetInputValue(s,s)", "종목조건", "0")
        self.dynamicCall("SetInputValue(s,s)", "신용조건", "0")
        self.dynamicCall("SetInputValue(s,s)", "가격조건", "0")
        self.dynamicCall("SetInputValue(s,s)", "상하한포함", "0")
        self.dynamicCall("CommRqData(string,string,int,string)", "가격급등락요청", "OPT10019", sPrevNext, "2006")

        self.trading_boom_eventloop = QEventLoop()
        self.trading_boom_eventloop.exec_()

    def trading_boom_stock_find(self,sPrevNext="0"): #거래량 종목들 불러오는 함수
        self.dynamicCall("SetInputValue(s,s)", "시장구분", "000")
        self.dynamicCall("SetInputValue(s,s)", "정렬구분", "2")
        self.dynamicCall("SetInputValue(s,s)", "거래량구분", "300")
        self.dynamicCall("SetInputValue(s,s)", "시간", "5")
        self.dynamicCall("SetInputValue(s,s)", "종목조건", "1")
        self.dynamicCall("SetInputValue(s,s)", "가격구분", "0")
        self.dynamicCall("CommRqData(string,string,int,string)", "거래량급증요청", "OPT10023", sPrevNext,"2005")
        self.trading_boom_eventloop = QEventLoop()
        self.trading_boom_eventloop.exec_()

    def candle(self, code=None, date="", sPrevNext="0"):  # 일봉데이터 가져오기
        QTest.qWait(500)  # PyQtTest에서 함수사용! time sleep과 같은 기능을 하며, 발표당시보다 시간을 더욱 줄여주어 프로그램 작동 시간을 단축해보았습니다. / 너무 빠르게 조회를 하면 api서버로 부터 차단이 되는 것 같습니다.

        self.dynamicCall("SetInputValue(s,s)", "종목코드", code)
        self.dynamicCall("SetInputValue(s,s)", "기준일자", date)
        self.dynamicCall("SetInputValue(s,s)", "수정주가구분", "1")
        self.dynamicCall("CommRqData(string,string,int,string)", "주식일봉차트조회요청", "opt10081", sPrevNext, self.num)
        self.data=[]
        self.caculator_eventloop = QEventLoop()
        self.caculator_eventloop.exec_()

    def standard_array_stock(self,code=""): #이동평균선을 만들어주는 함수입니다. 각각의 변수에 날짜에 따른 리스트형태로 불러오게끔 하였습니다. 최신날짜가 맨 앞으로 옵니다.

        self.last10_moving_price = [] #10일선 list 초기화 / 다른 종목을 분석하기위해 초기화를 해줍니다.
        self.last20_moving_price = [] #20일선 list 초기화
        self.last60_moving_price = [] #60일선 list 초기화
        self.last120_moving_price = [] #120일선 list 초기화


        for k in range(len(self.data)-10): #10일선
            moving_price = 0
            for i in self.data[k:10+k] : # self.data의 리스트 [[날짜1,종가,시가,저가,고가,거래량],[날짜2,종가,시가,저가,고가,거래량],...] 이렇게 리스트속에 리스트로 이루어져있습니다.
                moving_price+=int(i[1])

            last10_moving_price=(moving_price)/10
            self.last10_moving_price.append(last10_moving_price)

        for k in range(len(self.data)-20): #20일선
            moving_price = 0
            for i in self.data[k:20+k] :
                moving_price+=int(i[1])

            last10_moving_price=(moving_price)/20
            self.last20_moving_price.append(last10_moving_price)

        for k in range(len(self.data)-60): #60일선
            moving_price = 0
            for i in self.data[k:60+k] :
                moving_price+=int(i[1])

            last10_moving_price=(moving_price)/60
            self.last60_moving_price.append(last10_moving_price)

        for k in range(len(self.data)-120): #120일선
            moving_price = 0
            for i in self.data[k:120+k] :
                moving_price+=int(i[1])

            last10_moving_price=(moving_price)/120
            self.last120_moving_price.append(last10_moving_price)





    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):  # sPrevNext 다음 페이지가 있는지 알려주는거 2이면 더 있다.! #요청 받은 신호를 받고 출력하는 과정, 다음 함수 이용하는 과정은 KOA studio에 자세히 나와있습니다.
        #원하는 요청값에 따라 elif 문으로 계속 추가를 하여 작성하는 원리입니다. 여러 데이터 중, tr데이터에 해당하는 값들만 해당합니다. 실시간 데이터나 다른 데이터 역시 받을 수 있으며, tr데이터 형태가 아니면 다른 슬롯을 열어줘야합니다.
        if sRQName == "거래량급증요청" or sRQName == "가격급등락요청" : #급등락이나 거래량 급증 종목은 날짜에 따라 다르며, 장 중에서도 실시간 변화됩니다. 다만, 장시작전에 실행을 할 경우, 리스트가 나오지 않으며, 장 종료 후에 실행하면 항상 일정한 리스트가 나옵니다.
            count = self.dynamicCall("GetRepeatCnt(QString,Qstring)", sTrCode, sRecordName)
            for i in range(count) :
                name = self.dynamicCall("GetCommData(s,s,i,s)", sTrCode, sRQName, i, "종목코드")
                name=name.strip() #이름을 정제해야합니다. 불러오는데 이름에 공백이 포함이 됩니다.
                self.trading_boom_list.append(name)
            self.trading_boom_eventloop.exit() #이벤트루프를 종료하는 것! 다른 이벤트루프도 동일하게 이와같이 종료시켜야합니다.

        elif sRQName == "주식일봉차트조회요청":
            self.data=[] #기존의 데이터 삭제하기 위해 추가하였다.

            code = self.dynamicCall("GetCommData(s,s,i,s)", sTrCode, sRQName, 0, "종목코드")
            code = code.strip()
            print("%s 요청중!" % code)
            rows = self.dynamicCall("GetRepeatCnt(s,s)", sTrCode, sRQName)
            print("해당종목의",rows,"데이터 개수를 조회하였습니다.")

            for i in range(rows): #주식 불러온 데이터를 정제하는 과정입니다. 문자형태일 경우를 제거하였습니다.
                data = []
                current_price = self.dynamicCall("GetCommData(s,s,i,s)",sTrCode, sRQName, i, "현재가")
                current_price=int(current_price.strip())
                value = self.dynamicCall("GetCommData(s,s,i,s)",sTrCode, sRQName, i, "거래량")
                value=int(value.strip())
                date = self.dynamicCall("GetCommData(s,s,i,s)",sTrCode, sRQName, i, "일자")
                date=int(date.strip())
                start_price = self.dynamicCall("GetCommData(s,s,i,s)",sTrCode, sRQName, i, "시가")
                start_price=int(start_price.strip())
                low_price = self.dynamicCall("GetCommData(s,s,i,s)", sTrCode, sRQName, i, "저가")
                high_price = self.dynamicCall("GetCommData(s,s,i,s)", sTrCode, sRQName, i, "고가")
                low_price=int(low_price.strip())
                high_price=int(high_price.strip())
                data.append(date)
                data.append(current_price)
                data.append(start_price)
                data.append(low_price)
                data.append(high_price)
                data.append(value)
                self.data.append(data)  # self.data의 리스트 [[날짜1,종가,시가,저가,고가,거래량],[날짜2,종가,시가,저가,고가,거래량],...] 이렇게 리스트 속에 리스트로 이루어져있습니다.
                data = [] #마지막 끝나고 data 안의 리스트를 제거해주기 위해 설정하였다.

            self.caculator_eventloop.exit()
