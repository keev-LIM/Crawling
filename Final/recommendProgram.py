import math
import sys
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QWidget
, QLCDNumber, QDial, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox, QLabel, QTextEdit)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    gu_all = ['종로구', '중구', '용산구', '성동구', '광진구',
              '동대문구', '중랑구', '성북구', '강북구', '도봉구',
              '노원구', '은평구', '서대문구', '마포구', '양천구',
              '강서구', '구로구', '금천구', '영등포구', '동작구',
              '관악구', '서초구', '강남구', '송파구', '강동구']
    df_total = pd.read_csv('정리.csv', index_col=0, encoding='CP949', engine='python')
    CateGory = ''
    li1=[]
    li2=[]
    result = []
    canConfirm = 0
    def initUI(self):
        #라벨
        la = []
        font = QFont("궁서체", 15, weight=QFont.DemiBold)
        title = QLabel('지역 추천 프로그램', self)
        title.move(100, 10)
        title.setFont(font)
        title2 = QLabel('추천 지역', self)
        title2.move(490, 10)
        title2.setFont(font)
        label = QLabel('업종',self)
        label.move(20,70)
        la.append(label)
        label = QLabel('임대 시세', self)
        label.move(20, 120)
        la.append(label)
        label = QLabel('점포 수', self)
        label.move(20, 170)
        la.append(label)
        for i in range(len(la)):
            la[i].setFont(font)
        self.checkbox = []
        #체크박스
        #1
        self.cb_font = QFont("궁서체", 10,weight=QFont.DemiBold)
        self.checkTemp=[]
        self.cb1 = QCheckBox('음식점', self)
        self.cb1.move(150,70)
        self.cb2 = QCheckBox('카페', self)
        self.cb2.move(250, 70)
        self.cb3 = QCheckBox('술집', self)
        self.cb3.move(350, 70)
        self.checkTemp.append(self.cb1)
        self.checkTemp.append(self.cb2)
        self.checkTemp.append(self.cb3)
        self.checkbox.append(self.checkTemp)
        #2
        self.checkTemp = []
        self.cb1 = QCheckBox('많음', self)
        self.cb1.move(150, 120)
        self.cb2 = QCheckBox('보통', self)
        self.cb2.move(250, 120)
        self.cb3 = QCheckBox('적음', self)
        self.cb3.move(350, 120)
        self.checkTemp.append(self.cb1)
        self.checkTemp.append(self.cb2)
        self.checkTemp.append(self.cb3)
        self.checkbox.append(self.checkTemp)
        #3
        self.checkTemp = []
        self.cb1 = QCheckBox('많음', self)
        self.cb1.move(150, 170)
        self.cb2 = QCheckBox('보통', self)
        self.cb2.move(250, 170)
        self.cb3 = QCheckBox('적음', self)
        self.cb3.move(350, 170)
        self.checkTemp.append(self.cb1)
        self.checkTemp.append(self.cb2)
        self.checkTemp.append(self.cb3)
        self.checkbox.append(self.checkTemp)
        for i in range(3):
            for j in range(3):
                self.checkbox[i][j].setFont(self.cb_font)
                self.checkbox[i][j].stateChanged.connect(self.chkFunction)
                if i==1 or i==2:
                    self.checkbox[i][j].setDisabled(True)
        #체크박스들 이벤트 처리
        # cb.stateChanged.connect(self.changeTitle)
#######################################
        #텍스트에딧
        self.qte = QTextEdit(self)
        self.qte.move(420,40)
        self.qte.setFixedSize(250,240)
        self.qte.setReadOnly(True)
#######################################
        ##################################
        #버튼 위치, 크기 조정, 버튼 이벤트 처리 등
        btn1 = QPushButton('확인하기', self)
        btn1.move(30, 250)
        btn1.resize(350, 30)
        btn1.clicked.connect(self.confirm)
        btn1.setFont(font)
        ####################################
        self.setWindowTitle('지역 추천 프로그램')
        self.setFixedSize(700, 300)
        #self.setGeometry(200, 200, 600, 500)
        self.show()
    def setText(self, check=1):
        self.qte.setText('')
        if check==0:    #음식점, 술집, 카페 선택지의 경우
            for i in range(len(self.gu_all)):
                self.qte.append(self.gu_all[i] + ' ')
        else:  #아닌 경우
            for i in range(len(self.result)):
                self.qte.append(self.result[i]+' ')
    def confirm(self):
        if(self.canConfirm==0):
            QMessageBox.information(
                self, '흐음..', "점포 수와 임대 시세 중 하나는 필수적으로 체크가 되어야 합니다!",
                QMessageBox.Cancel
            )
        else:
            li1=self.sorting('인구수', 2, '')  # 상위 8개 데이터 추가
            li1.extend(self.sorting('인구수', 1, ''))  # 중위 8개 데이터 추가
            li1.extend(self.sorting('인구수', 0, ''))  # 하위 9개 데이터 추가
            li1_grade = []
            for i in range(len(self.result)):
                for j in range(len(li1)):
                    if self.result[i]==li1[j]:  #만약 체크박스를 통해 간추린 데이터들중 구의 이름이 같으면
                        li1_grade.append(j) #등수 0~24 중 값이 입력됨
            if self.CateGory=='음식점':
                li2 = self.sorting('리뷰', 2, self.CateGory)  # 상위 8개 데이터 추가
                li2.extend(self.sorting('리뷰', 1, self.CateGory))  # 중위 8개 데이터 추가
                li2.extend(self.sorting('리뷰', 0, self.CateGory))  # 하위 8개 데이터 추가
            if self.CateGory == '카페':
                li2 = self.sorting('역세권', 2, self.CateGory)  # 상위 8개 데이터 추가
                li2.extend(self.sorting('역세권', 1, self.CateGory))  # 중위 8개 데이터 추가
                li2.extend(self.sorting('역세권', 0, self.CateGory))  # 하위 8개 데이터 추가
            if self.CateGory=='술집':
                li2 = self.sorting('직장인구', 2, self.CateGory)  # 상위 8개 데이터 추가
                li2.extend(self.sorting('직장인구', 1, self.CateGory))  # 중위 8개 데이터 추가
                li2.extend(self.sorting('직장인구', 0, self.CateGory))  # 하위 8개 데이터 추가
            li2_grade=[]
            for i in range(len(self.result)):
                for j in range(len(li2)):
                    if self.result[i] == li2[j]:  # 만약 체크박스를 통해 간추린 데이터들중 구의 이름이 같으면
                        li2_grade.append(j)  # 등수 0~24 중 값이 입력됨
            li_Final_grade=[]
            for i in range(len(self.result)):
                li_Final_grade.append(li1_grade[i]+li2_grade[i])    #등수의 합을 구해서 등수의 합이 높은 경우 선택!
            count=math.ceil(len(self.result)/3) #총 개수/3의 올림으로 추천 구 개수를 정한다.
            FINAL_LIST_GU=[]   #최종 값을 저장할 리스트이다.
            FINAL_LIST_INDEX=[] #최종 값들의 인덱스를 저장한다.
            li_Final_grade_temp = li_Final_grade #등수의 값을 바꾸므로 임시적으로 저장해 사용
            for i in range(count):
                Min = min(li_Final_grade)   #최소값을 찾고
                index = li_Final_grade.index(Min)   #그 최소값의 인덱스를 구한다음에
                FINAL_LIST_GU.append(self.result[index])      #그 인덱스에 해당하는 구를 삽입.
                FINAL_LIST_INDEX.append(index)
                li_Final_grade[index]=49 #등수의 합의 최대값은 0~24 + 0~24 해서 48등이므로 49를 넣으면 이 값은 사용 안함
            #정렬 실행 단, 남은 결과에서 최종 점수가 같을 경우, 그리고 인구수 등수가 왼쪽 원소가 더 작을 경우에 바꾼다.
            for i in range(count - 1):
                for j in range(count - i-1):
                    if li_Final_grade_temp[FINAL_LIST_INDEX[j]]==li_Final_grade_temp[FINAL_LIST_INDEX[j+1]]:    #최종 등수가 갚을 경우!
                        if li1_grade[FINAL_LIST_INDEX[j]]>li1_grade[FINAL_LIST_INDEX[j+1]]:
                            FINAL_LIST_GU[j], FINAL_LIST_GU[j + 1] = FINAL_LIST_GU[j + 1], FINAL_LIST_GU[j]  # swap
            self.qte.setText('')
            for i in range(count):
                self.qte.append(str(i+1) + '순위 : ' + FINAL_LIST_GU[i]+' ')
    def chkFunction(self):
        li = []
        #CheckBox는 여러개가 선택될 수 있기 때문에 elif를 사용하지 않습니다.
        #음식점, 카페, 술집 중 고르기
        if self.checkbox[0][0].isChecked() == True:
            self.CateGory = '음식점'
            self.disable1()
            self.setText(0)
        if self.checkbox[0][1].isChecked() == True:
            self.CateGory = '카페'
            self.disable1()
            self.setText(0)
        if self.checkbox[0][2].isChecked() == True:
            self.CateGory = '술집'
            self.disable1()
            self.setText(0)

        #임대시세 많음, 보통, 적음
        if self.checkbox[1][0].isChecked() == True:
            li1 = self.sorting('임대시세', 2,'')
            if len(self.result)==0:
                self.result = li1
            else:
                self.result = list(set(li1).intersection(self.result))
            self.disable2()
            self.setText()
            self.canConfirm = 1
        if self.checkbox[1][1].isChecked() == True:
            li1 = self.sorting('임대시세', 1, '')
            if len(self.result) == 0:
                self.result = li1
            else:
                self.result = list(set(li1).intersection(self.result))
            self.disable2()
            self.setText()
            self.canConfirm = 1
        if self.checkbox[1][2].isChecked() == True:
            li1 = self.sorting('임대시세', 0, '')
            if len(self.result) == 0:
                self.result = li1
            else:
                self.result = list(set(li1).intersection(self.result))
            self.disable2()
            self.setText()
            self.canConfirm = 1
        #점포수 많음, 보통, 적음
        if self.checkbox[2][0].isChecked() == True:
            li2 = self.sorting('점포수', 2,self.CateGory)
            #중복만 뽑는다.
            if len(self.result) == 0:
                self.result = li2
            else:
                self.result = list(set(li2).intersection(self.result))
            self.disable3()
            self.setText()
            self.canConfirm = 1
        if self.checkbox[2][1].isChecked() == True:
            li2 = self.sorting('점포수', 1, self.CateGory)
            if len(self.result) == 0:
                self.result = li2
            else:
                self.result = list(set(li2).intersection(self.result))
            self.disable3()
            self.setText()
            self.canConfirm = 1
        if self.checkbox[2][2].isChecked() == True:
            li2 = self.sorting('점포수', 0, self.CateGory)
            if len(self.result) == 0:
                self.result = li2
            else:
                self.result = list(set(li2).intersection(self.result))
            self.disable3()
            self.setText()
            self.canConfirm = 1

    def sorting(self,string,select,category):    #select : 2,1,0  category
        if category == '':
            temp = self.df_total
            temp = temp.sort_values(by=[string], axis=0, ascending=False)
            temp = temp.reset_index()
            temp = temp.loc[:, ['구', string]]
            temp = temp.drop_duplicates("구", keep="first")
            list_total = temp['구'].values.tolist()
            top = []  # 상위 8개 리스트
            middle = []  # 보통 8개
            bottom = []  # 하위 9개
            for i in range(25):
                if i < 8:
                    top.append(list_total[i])  # append로 요소 추가
                elif i < 16:
                    middle.append(list_total[i])
                else:
                    bottom.append(list_total[i])
            if select == 2:
                return top
            if select == 1:
                return middle
            if select == 0:
                return bottom
        if category !='':
            temp = self.df_total
            temp = temp.sort_values(by=[string], axis=0, ascending=False)
            temp = temp.reset_index()
            temp = temp.loc[:, ['구', '카테고리', string]]
            temp = temp[temp['카테고리'] == category]
            temp = temp.drop(columns='카테고리')
            list_total = temp['구'].values.tolist()
            top = []  # 상위 8개 리스트
            middle = []  # 보통 8개
            bottom = []  # 하위 9개

            for i in range(25):
                if i < 8:
                    top.append(list_total[i])  # append로 요소 추가
                elif i < 16:
                    middle.append(list_total[i])
                else:
                    bottom.append(list_total[i])
            if select == 2:
                return top
            if select == 1:
                return middle
            if select == 0:
                return bottom

    #라디오 버튼처럼 사용하도록 disable
    def disable1(self):
        self.checkbox[0][0].setDisabled(True)
        self.checkbox[0][1].setDisabled(True)
        self.checkbox[0][2].setDisabled(True)
        self.checkbox[1][0].setDisabled(False)
        self.checkbox[1][1].setDisabled(False)
        self.checkbox[1][2].setDisabled(False)
        self.checkbox[2][0].setDisabled(False)
        self.checkbox[2][1].setDisabled(False)
        self.checkbox[2][2].setDisabled(False)

    def disable2(self):
        self.checkbox[1][0].setDisabled(True)
        self.checkbox[1][1].setDisabled(True)
        self.checkbox[1][2].setDisabled(True)
    def disable3(self):
        self.checkbox[2][0].setDisabled(True)
        self.checkbox[2][1].setDisabled(True)
        self.checkbox[2][2].setDisabled(True)
    def disable_reset(self):
        self.checkbox[0][0].setDisabled(False)
        self.checkbox[0][1].setDisabled(False)
        self.checkbox[0][2].setDisabled(False)
        self.checkbox[1][0].setDisabled(True)
        self.checkbox[1][1].setDisabled(True)
        self.checkbox[1][2].setDisabled(True)
        self.checkbox[2][0].setDisabled(True)
        self.checkbox[2][1].setDisabled(True)
        self.checkbox[2][2].setDisabled(True)
        for i in range(3):
            for j in range(3):
                if(self.checkbox[i][j].isChecked()):
                    self.checkbox[i][j].toggle()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())