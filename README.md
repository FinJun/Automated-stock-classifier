위 파일들은 아주대학교 금융공학과 금융소프트웨어 기말 프로젝트 입니다.
저희는 키움증권의 Open API 를 이용하여 저희가 직접 설정한 기준들에 맞게 종목을 걸러서 추천해준 후 재무제표와 근 1개월간 뉴스자료를 제공해주는 프로그램을 만들었습니다.
API 를 사용하는 이유는 단지 주가 조회만을 목적으로 하는 것이 아닌 차후에 더욱 다양한 기능을 사용자 편의에 맞게 추가할 수 있게끔 하기 위함입니다. 한정적인 프로젝트 기간상 다른 기능은 추가하지 못하였지만, api 를 이용하여 주식의 매수 매도, 계좌 잔고 조회등 다양한 기능을 직접 추가 가능합니다.
어떤식으로 파일을 이용해야 하는지와 저희의 코드 설명을 드리도록 하겠습니다.
추가적으로 다양한 사진과 함께 실제 적용하기 쉽도록 Word 파일을 첨부하도록 할테니 이 글을 읽고 이해가 되지 않거나 제대로 실행되지 않는 부분은 word 파일을 참고해 주시기 바랍니다.
저희가 업로드 한 asda 파일을 그대로 전부 다운로드 하신 후, init 파일을 실행해 주시면 됩니다. 실행 전에 open api 설치와 아나콘다 가상환경 설정을 전부 끝내주시길 바랍니다.

<<프로그램 실행시 유의해야 할 점입니다!!!!!>>
Open API 사용 설정과 32비트의 가상환경 설정 후, 저희가 올려드린 파일을 그대로 다운 받으셔서 해당 파일에 들어 있는 __init__.py 를 실행하면 프로그램이 작동 됩니다. 
이 프로그램 실행 시, anaconda 를 강제로 32비트로 설정해 줘야 하며 가상환경 설정시 python 3.7 버전으로 같이 생성을 해줘서 __init__.py 실행 시 인터프리터를 올바른 경로로 설정해 주는 것이 중요합니다. python 버전이 다르면 패키지 설정에 문제가 생길 가능성이 높아 최선 버전 보단 가상환경 설정 시, 가상환경 내에서 python 3.7 을 사용하는 것을 권합니다. 

위 설정이 끝났다면 실제로 Open API 를 설치해 줘야 하는데, 키움증권 홈페이지에 접속하여 Open api 를 클릭한 후, api를 신청하고 설치합니다. 다음으로는 KOA studio 를 설치해야 하는데, 2개의 파일을 압축 풀기 할 수 있습니다. 그 2개의 파일을 c 드라이브의 open api 파일에 넣어주면 됩니다.


<<아래는 anaconda 32bit 설정 방법입니다.>>

키움 증권 api 는 32비트에 최적화 되어있기 때문에 환경 설정이 중요합니다.
아나콘다 설치 후, cmd 창을 열어
set CONDA FORCE32BIT=1 을 입력해 줍니다
위는 아나콘다 환경을 32bit 로 설정해 주는 과정입니다.
conda create -n (원하는이름) python=3.7 anaconda 입력해줍니다.
위는 우리가 원하는 이름의 가상환경을 python 3.7 버전을 포함하도록 만들어 주는 과정입니다.
이제 설치가 되게 됩니다.
conda env list 를 통해 만들어진 가상환경의 파일 경로를 확인 가능합니다.
activate (설정해준 파일 이름) 을 입력하여 활성화 한 후,
python 을 입력하여 32bit 로 표현이 됐는지 확인해 주면 됩니다.
python 정보가 32bit 로 올바르게 표현 된다면 해당 가상환경 파일 경로 안에 있는 python.exe 파일을 인터프리터로 설정해주면 됩니다.




<<아래부터는 프로젝트 과정에 대한 설명입니다.>>

저희는 sns를 이용하여 여러 투자활동의 근거와 서비스 이용 의사를 확인했고, 사람들이 정보 접근의 진입장벽은 낮기에 쉽게 접근하지만 이를 해석하고 정보의 양이 많아지면 많아질 수록 힘들어 한다는 것을 알게 되었습니다. 이를 통해 저희는 투자자의 편의를 위한 주식 종목 추천 서비스를 만들고자 하였습니다.
1차 과정에서는 기술적 분석을 바탕으로 종목을 선별했고, 2차 과정에서 선별된 종목을 업종 per을 기준으로 다시 선별했습니다. 마지막 최종 단계에서는 최종 선별된 종목의 근 1개월간 뉴스 10개와 종목 이름을 불러오게 하였습니다.

1차 과정에서 저희는 적절한 차트에 대한 기준을 세웠습니다. 저희의 결론은 '최근 시장의 관심을 받은 주식 중에 저평가에 해당하는 주식의 차트' 를 가져오기로 하였습니다. 그 기준은 과거 주가에 비해 현저히 낮은 상태에서 거래량이 크게 증가한 주식들이 되었습니다. 등락률이 높은 종목이나 거래량이 높은 종목을 대략 400개 불러온 후, 각각의 종목 데이터를 가져와서 오늘날의 가격이 과거 300일 전의 주가보다 현저히 낮은 수준이면서 거래량이 증가한 '골든크로스 종목'을 찾아오게끔 코딩을 해 주었습니다. 

2차 과정에서는 company guide 라는 사이트에서 재무비율을 크로링해오면서 처리하였습니다. Company guide 라는 사이트의 재무비율 위츠는 corp_group2>dl>dd 에 순서대로 들어가 있음을 확인 가능하빈다. 이를 dom tree 구조로 가져오면서 순서대로 뽑히도록 코딩을 해줬습니다. 

마지막 과정에서는 위와 마찬가지로 네이버 뉴스에서 크롤링을 해왔고 종목명과 n개의 뉴스 (최근 1개월) 이라는 str을 함께 추가하여 차례대로 출력하게 하였습니다. 




추가적으로 다양한 사진과 함께 실제 적용하기 쉽도록 Word 파일을 첨부하도록 할테니 이 글을 읽고 이해가 되지 않거나 제대로 실행되지 않는 부분은 word 파일을 참고해 주시기 바랍니다.!!!


<<출처>>
저희 프로그램을 만들면서 저희가 참조했던 사이트들을 설명드리겠습니다. 일단 기본적으로 저희는 공부와 참조의 목적으로 사이트나 영상을 참조했지 코드를 그대로 사용하거나 이용하는 과정은 없었음을 알려드립니다.

아나콘다 32bit 환경 설정 : https://blog.naver.com/opgj123/222081189758
키움 증권 open api 사용 방법 : 유튜브 "프로그램 동산"
class 구조 활용, ocx 제어함수, 이벤트 루프 : 유튜브 "프로그램 동산"
asda > wer > kiwoom > errorCode.py : 유튜브 "프로그램 동산"
beautifulSoup 활용법과 html parsing : 유튜브 "프로그래머 김플 스튜디오"
