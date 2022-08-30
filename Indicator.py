from pandas import Series, DataFrame
import os
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
import itertools
#import keras
#from keras.preprocessing.text import text_to_word_sequence
import re
import string
from nltk.corpus import stopwords
import os
import pandas as pd
import numpy as np
import xlrd
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date,timedelta
import msoffcrypto
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
from email.mime.image import MIMEImage
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import figure
from matplotlib.ticker import MaxNLocator
from dateutil.relativedelta import relativedelta
import calendar
from datetime import date,timedelta


#------------------------------------------------UI/UX----------------------------------------------------------------------------------------------------------
print("-----------[This is AI for helping Quality Jobs]-----------")
print("                                       <Made by Eunbi Yoon>")
print("Collecting the data. Please wait. ")

#-----------------------------------------------train_data의  DataFrame 생성----------------------------------------------------------------------------------------------------------
## 데이터 불러오기
#AGT_svc_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/1_Daily SVC Report/1_AGT Model.xlsx',sheet_name='SVC')
Pro2_svc_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/1_Daily SVC Report/2_Pro2 Model.xlsx',sheet_name='SVC')
#Plus_svc_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/1_Daily SVC Report/3_Plus Model.xlsx',sheet_name='SVC')
#Win_svc_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/1_Daily SVC Report/4_Win Model.xlsx',sheet_name='SVC')
#CK_svc_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/1_Daily SVC Report/5_CK 5.0 Model.xlsx',sheet_name='SVC')

# Production data 불러오기
prod_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/0_Other/Production Qty.xlsx')
prod_data=prod_data.drop(['Month','Suffix'],axis=1)
prod_data=prod_data.T
prod_data=prod_data.reset_index()
prod_data.rename(columns={'index':'Prod_Month'},inplace=True)

sales_data=pd.read_excel('//US-SO11-NA08765/R&D Secrets/M+3 task/200 Top Loader/0_Other/Sales Qty.xlsx')
sales_data=sales_data.drop(['Month'],axis=1)
sales_data=sales_data.T
sales_data=sales_data.reset_index()
sales_data.rename(columns={'index':'Sales_Month'},inplace=True)


server = smtplib.SMTP('lgekrhqmh01.lge.com:25')
server.ehlo()
msg=MIMEMultipart()
msg['From']='eunbi1.yoon@lge.com'
msg['To']='eunbi1.yoon@lge.com'



# 수신자 발신자 지정
msg['From']='eunbi1.yoon@lge.com'
msg['Subject']='HAQDX Field Quality Analysis Solution'


#명령 받기
print("Choose one of below model")
print("=============list================")
print("0.  Total Model")
print("1.  Agitator Model")
print("2.  Pro2 Model")
print("3.  Plus Model")
print("4.  Win Model")
print("5.  CK 5.0 Model")
print("=================================")
print("Are you ready? Then type below")
model=input()


# 데이터 선택
if model == '0':
    svc_data=pd.DataFrame(Total_svc_data)
    meg_Function2_Models='Total'
    prod_data=prod_data.iloc[0]
    prod_data = prod_data.rename(columns={0: 'qty'})
    sales_data=sales_data.iloc[0]
    sales_data = sales_data.rename(columns={0: 'qty'}) 
    
if model == '1':
    svc_data=pd.DataFrame(AGT_svc_data)
    meg_Function2_Models='Agitator'
    prod_data=prod_data[['Prod_Month',1]]
    prod_data = prod_data.rename(columns={1: 'qty'})
    sales_data=sales_data[['Sales_Month',1]]
    sales_data = sales_data.rename(columns={1: 'qty'})

elif model=='2':
    svc_data=pd.DataFrame(Pro2_svc_data)
    meg_Function2_Models='Pro2'
    prod_data=prod_data[['Prod_Month',2]]
    prod_data = prod_data.rename(columns={2: 'qty'})
    sales_data=sales_data[['Sales_Month',2]]
    sales_data = sales_data.rename(columns={2: 'qty'})

elif model=='3':
    svc_data=pd.DataFrame(Plus_svc_data)
    meg_Function2_Models='Plus'
    prod_data=prod_data[['Prod_Month',3]]
    prod_data = prod_data.rename(columns={3: 'qty'})
    sales_data=sales_data[['Sales_Month',3]]
    prod_data = prod_data.rename(columns={3 : 'qty'}) 

elif model=='4':
    svc_data=pd.DataFrame(Win_svc_data)
    meg_Function2_Models='Win'
    prod_data=prod_data[['Prod_Month',4]]
    prod_data = prod_data.rename(columns={4: 'qty'})
    sales_data=sales_data[['Sales_Month',4]]
    sales_data = sales_data.rename(columns={4 : 'qty'}) 

elif model=='5':
    svc_data=pd.DataFrame(CK_svc_data)
    meg_Function2_Models='CK5.0'
    prod_data=prod_data[['Prod_Month',5]]
    prod_data = prod_data.rename(columns={5: 'qty'})
    sales_data=sales_data[['Sales_Month',5]]
    sales_data = sales_data.rename(columns={5 : 'qty'}) 

else:
    print("Error :: Please try again")
    
prod_data=prod_data.dropna()
sales_data=sales_data.dropna()
fdrffr_index=sales_data['Sales_Month']
print("1prod_Data")
print(prod_data)
print("1sales_Data")
print(sales_data)


# Close Month, Production 추출
svc_data['CLOSE_DT_RTN_DT'] = svc_data['CLOSE_DT_RTN_DT'].apply(str)
svc_data['GQISClosingMonth']=svc_data['CLOSE_DT_RTN_DT'].str[2:6]

svc_data['ProductionY']=svc_data['SERIAL_NO 1'].str[0]
dictionary = {'8': '1', '9': '1', '0': '2', '1': '2'}
svc_data["ProductionY"] = svc_data["ProductionY"].map(dictionary)
svc_data['ProductionMonth']=svc_data["ProductionY"]+svc_data['SERIAL_NO 1'].str[:3]


##데이터 프레임 표시
svc_data=pd.DataFrame(svc_data[["Symptoms","detail","detail2","ProductionMonth","GQISClosingMonth"]])

# Symptom detail 통일
svc_data["Symptoms"]=svc_data["Symptoms"].str.upper()
svc_data["detail"]=svc_data["detail"].str.lower()



#---------------------------------------------------------------------------UI/ UX------------------------------------------------------------------------------------------------------------
## UI UX구성
print("What kind of Symptoms?")
print("Choose one of below list")
print("=============list================")
print("0.  All")
print("1.  DRAIN")
print("2.  EXPLANATION")
print("3.  EXTERIOR")
print("4.  FILLING")
print("5.  LEAK")
print("6.  LID")
print("7.  MISASSEMBLY")
print("8.  MOTOR")
print("9.  NOISE/VIBRATION")
print("10. OTHER")
print("11. PCB")
print("12. RTN")
print("=================================")
print("Are you ready? Then type below")
Function2_Symptoms=input()


##Function2 Pyramid, Hazard, AAR&PPM, FDR&FFR 할 데이터를 고름
if Function2_Symptoms=='0':
    meg_Function2_Symptoms='All'
    svc_data=svc_data
    title='Total'

elif Function2_Symptoms=='1':
    meg_Function2_Symptoms='DRAIN'
    is_sort = svc_data['Symptoms'] == 'DRAIN'
    svc_data = svc_data[is_sort]
    title='Drain'
       
elif Function2_Symptoms=='2':
    meg_Function2_Symptoms='EXPLANATION'
    is_sort = svc_data['Symptoms'] == 'EXPLANATION'
    svc_data = svc_data[is_sort]
    title='Explanation'

elif Function2_Symptoms=='3':
    meg_Function2_Symptoms= 'EXTERIOR'
    is_sort = svc_data['Symptoms'] == 'EXTERIOR'
    svc_data = svc_data[is_sort]
    title='Exterior'
   
elif Function2_Symptoms=='4':
    meg_Function2_Symptoms='FILLING'
    is_sort = svc_data['Symptoms'] == 'FILLING'
    svc_data = svc_data[is_sort]
    title='Filling'

elif Function2_Symptoms=='5':
    meg_Function2_Symptoms='LEAK'
    is_sort = svc_data['Symptoms'] == 'LEAK'
    svc_data = svc_data[is_sort]
    title='Leak'

elif Function2_Symptoms=='6':
    meg_Function2_Symptoms='LID'
    is_sort = svc_data['Symptoms'] == 'LID'
    svc_data = svc_data[is_sort]
    title='Lid'

elif Function2_Symptoms=='7':
    meg_Function2_Symptoms='MISASSEMBLY'
    is_sort = svc_data['Symptoms'] == 'MISASSEMBLY'
    svc_data = svc_data[is_sort]
    title='Misassembly'

elif Function2_Symptoms=='8':
    meg_Function2_Symptoms='MOTOR'
    is_sort = svc_data['Symptoms'] == 'MOTOR'
    svc_data = svc_data[is_sort]
    title='Motor'

elif Function2_Symptoms=='9':
    meg_Function2_Symptoms='NOISE/VIBRATION'
    is_sort = svc_data['Symptoms'] == 'NOISE/VIBRATION'
    svc_data = svc_data[is_sort]
    title='Noise/Vibration'

elif Function2_Symptoms=='10':
    meg_Function2_Symptoms='OTHER'
    is_sort = svc_data['Symptoms'] == 'OTHER'
    svc_data = svc_data[is_sort]
    title='Other'

elif Function2_Symptoms=='11':
    meg_Function2_Symptoms='PCB'
    is_sort = svc_data['Symptoms'] == 'PCB'
    svc_data = svc_data[is_sort]
    title='PCB'

elif Function2_Symptoms=='12':
    meg_Function2_Symptoms='RTN'
    is_sort = svc_data['Symptoms'] == 'RTN'
    svc_data = svc_data[is_sort]
    title='RTN'

else:
    print("Error. Please restart this program.")

   
print("I understand what you want. You choose "+meg_Function2_Symptoms)
print(" ")
print(" ")
print("What fuction do you want to do for "+meg_Function2_Symptoms)
print("Choose one of below list")
print("=============list================")
print("1. Pyramid Table ")
print("2. Hazard Graph ")
print("3. AAR & PPM ")
print("4. FDR & FFR ")
print("=================================")
print("Are you ready? Then type below")
Function2_Indicators=input()
   
if Function2_Indicators=='1':
    meg_Function2_Indicators="Pyramid Table"
elif Function2_Indicators=='2':
    meg_Function2_Indicators='Hazard Graph'
elif Function2_Indicators=='3':
    meg_Function2_Indicators='AAR & PPM'
elif Function2_Indicators=='4':
    meg_Function2_Indicators='FDR & FFR'
else:
    print("Error. Please restart this program.")
       
print("I understand what you want. You choose "+meg_Function2_Indicators)


################################# 데이터의 기본인 Pivot table 만들기 ###############################
# Pivot Table 가로 세로 열 정리
idx = prod_data['Prod_Month'].to_list()
idx = list(map(str, idx))
idx.extend(['Total'])

#PROD QTY 정리
prod_data=prod_data.drop(['Prod_Month'],axis=1)
prod_data=prod_data.reset_index()
prod_data=prod_data.drop('index',axis=1)
prod_data=prod_data.T
prod_data=prod_data.reset_index()
prod_data=prod_data.drop('index',axis=1)
print(prod_data)

#SALES QTY 정리
sales_data=sales_data.drop(['Sales_Month'],axis=1)
sales_data=sales_data.reset_index()
sales_data=sales_data.drop('index',axis=1)
sales_data.columns=['sales_data']
print('sales_data')
print(sales_data)

    
##pivot table
pivot_table = pd.crosstab(index=svc_data.GQISClosingMonth, columns=svc_data.ProductionMonth, margins=True, margins_name="Total")

#idx2 = pivot_table.columns.union(pivot_table.index) # 가로 세로 동일한 index
pyramid_table = pivot_table.reindex(index = idx, columns=idx, fill_value=0)
    
## pyramid_table의 value 추출, tranpose 행렬 A^T in list
var = [ ]
for column in pyramid_table.columns.values:
    var.append ( pyramid_table [ column ].tolist () )
numpy_array = np.array(var)
transpose = numpy_array.T
pyramid_vals = transpose.tolist()

################################################################################################    
        
if Function2_Indicators=='1':
    print(pyramid_table)
    #값이 0이면 데이터 값 없애기 -> 너무 많은 0을 제거
    pyramid_table = pyramid_table.replace(0,'', regex=True)
    print(pyramid_table)
    
    # 모델에 따라 종이 사이즈 조절 가능
    ######### 코드 작성하기
    
    # 테이블 사이즈, 제목 설정
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 10)
    ax.set_axis_off()
    a=plt.table(cellText=pyramid_table.values,rowLabels=pyramid_table.index,colLabels=pyramid_table.columns, loc='center',cellLoc='center')
    plt.title('Pyramid Table (Model : '+meg_Function2_Models+'  / Symptoms : '+meg_Function2_Symptoms+')', fontweight ="bold", pad=0.1)

    ##대각선,total 부분 색깔 생성
    #gray
    i=1
    k=0
    for i in range(len(idx)-1):
        k=i+1
        a[(k, i)].set_facecolor("#d9d9d9")
        i=i+1
    #orange
    for i in range(len(pyramid_table.columns)+1):
        a[(len(pyramid_table.columns),i-1)].set_facecolor("#fdeada")
        i=i+1
    for i in range(len(pyramid_table.columns)+1):
        a[(i,len(pyramid_table.columns)-1)].set_facecolor("#fdeada")
        i=i+1

    #값이 0이면 데이터 값 없애기
    a.auto_set_font_size(False)
    a.set_fontsize(9)
    a.auto_set_column_width(col=list(range(len(pyramid_table.columns))))
    plt.tight_layout()

    print("Mission Complete !")
    print(pyramid_table)


elif Function2_Indicators=="2":
    ##마지막 열 삭제
    pyramid_vals.pop(len(pyramid_vals)-1)
    pyramid_vals=pd.DataFrame(pyramid_vals)
    pyramid_vals= pyramid_vals [pyramid_vals.columns [:-1]]
    pyramid_vals.drop(columns=[len(pyramid_vals)-1])

    #a의 원소들을 모두 int형으로 변환
    A=pyramid_vals.apply(pd.to_numeric)

    ## Hazard 그래프 그리기 시작
    ## 삼각행렬을 위로 올리기
    b=pd.DataFrame()
    i=0
    j=0
    for i in range(len(A)):
        for j in range(len(A)):
            if i==j:
                k=A.at[i,j]
                b.at[0,j]=k
                j=j+1
            elif i>j:
                k=A.at[i,j]
                b.at[i-j,j]=k
                j=j+1

    print("A")
    print(A)
    print("b")
    print(b)
    #### 삼각행렬 누적 더하기
    b=b.replace(np.nan,0, regex=True)
    c=pd.DataFrame()

    #첫번쨰 열 처리
    for i in range(1):
        for j in range(len(A)):
            k=b.at[0,j]
            c.at[0,j]=k

    # 두번째 열 처리 -> 첫번쨰 시작하는 열은 1번째인데 i가 0부터 인식함으로 i+1로 식을 전개 
    for i in range(len(A)-1):
        for j in range(len(A)-i-1):
            M=b.at[i+1,j]
            N=c.at[i,j]
            c.at[i+1,j]=M+N
    print("c")
    print(c)
                             

    # Hazard 그래프 전 마지막 테이블
    hazard_table=pd.DataFrame()
    i=0
    j=0
    print(len(idx)-1)
    print(idx)
    for i in range(len(idx)-1): # idx에 total도 포함되어 있다.
        #for j in range(len(idx)-i):
        for j in range(len(idx)-1):
            d=c.at[i,j]
            if d==np.nan:
                hazard_table.at[i,j]=np.nan
            else:
                e=int(prod_data.at[0,j])
                if e==0:
                    k=0
                else:
                    k=d*100/e
                hazard_table.at[i,j]=k
                j=j+1

    print(hazard_table)
    
     ## 그래프 꾸미기    
    fig = plt.figure()
    fig.set_size_inches(10, 6)
    ax = fig.add_subplot(111)

    plt.plot(hazard_table,color='#BFBFBF')

    color_matrix=['#FF0000','#C00000','#006600','#7030A0','#FFC000','#FF33CC']

    # Remark를 위한 장
    today=date.today()

    print(len(idx)-2)
    #len(idx)-2 -> last length (total, 개수 0부터 시작해서 -> 순서는 -1 해야 함)
    for i in range(6):
        if i==0:
                hazard_table[len(idx)-2].plot(marker='o',markersize=10,color=color_matrix[i])
                #x0=hazard_table.at[i,len(idx)-i-2]
                #remark=today+relativedelta(months=i)
                #remark=remark.strftime('%y.%m')
                #ax.annotate(remark,xy=(i,x0),va='bottom',color=color_matrix[i],fontsize=9)
        else:
            if hazard_table.at[i,len(idx)-2-i]==0:
                print("Zero Value")
            else:
                hazard_table[len(idx)-i-2].plot(color=color_matrix[i])
                x0=hazard_table.at[i,len(idx)-i-2]
                remark=today-relativedelta(months=i)
                remark=remark.strftime('%y.%m')
                ax.annotate(remark,xy=(i,x0),va='bottom',color=color_matrix[i],fontsize=9)
            


    # x, y축 값 조정
    month=pd.DataFrame()
    for i in range(len(idx)-1):
        month.at[0,i]=str(i+1)+'M'
    ax_list=list(map(lambda x: str(x)+'M', range(1,len(idx))))
    ax.set_xticks(np.arange(len(idx)-1))
    ax.set_xticklabels(ax_list)
    ax.set_ylim(bottom=0)

            
    plt.title('Hazard Graph (Model : '+meg_Function2_Models+'  / Symptoms : '+meg_Function2_Symptoms+')', fontweight ="bold", pad=0.1)
    print("Mission Complete !")


       
elif Function2_Indicators=='3':
    ##마지막 열 삭제
    pyramid_vals.pop(len(pyramid_vals)-1)
    pyramid_vals=pd.DataFrame(pyramid_vals)
    pyramid_vals= pyramid_vals [pyramid_vals.columns [:-1]]
    pyramid_vals.drop(columns=[len(pyramid_vals)-1])

    #a의 원소들을 모두 int형으로 변환
    A=pyramid_vals.apply(pd.to_numeric)

    print("How many months ago was it improved? [(ex)Improvement Month :2103, last production closing Month: 2106 --> input : 3 ")
    improving_month=input()
    print("Improving Month: "+improving_month)

    print(A)

    #AAR개선전
    i=0
    j=0
    k=0
    n=int(improving_month)
    for i in range(n):
        for j in range(n):
            k=A.at[len(A)-i-1-n,len(A)-j-1-n]+k
            j=j+1
    before_ImprovSVC=k

    #AAR개선후
    i=0
    j=0
    k=0
    for i in range(n):
        for j in range(n):
            k=A.at[len(A)-i-1,len(A)-j-1]+k
            j=j+1
    after_ImprovSVC=k


    #prod_data=prod_data.reset_index()
    #print(prod_data)

    

    ##Prod Qty 개선전
    i=0
    k=0
    n=int(improving_month)
    for i in range(n):
        print(str(i)+"This is before improvement")
        print(prod_data.at[len(prod_data)-i-1-n,'qty'])
        k=prod_data.at[len(prod_data)-i-1-n,'qty']+k
        i=i+1
    before_ProdQty=int(k)


    ##Prod Qty 개선후
    i=0
    k=0
    for i in range(n):
        print(str(i)+"This is after improvement")
        print(prod_data.at[len(prod_data)-i-1,'qty'])
        k=prod_data.at[len(prod_data)-i-1,'qty']+k
        i=i+1
    after_ProdQty=int(k)

    ##AAR PPM dataframe 생성하고 값 배치
    ARPMdata=pd.DataFrame()
    ARPMdata.at[1,1]=str(before_ImprovSVC)+' ea'
    ARPMdata.at[1,2]=str(after_ImprovSVC)+' ea'
    ARPMdata.at[2,1]=str(before_ProdQty)+' ea'
    ARPMdata.at[2,2]=str(after_ProdQty)+' ea'

    ##PPM
    ARPMdata.at[3,1]=str(round(before_ImprovSVC*1000000/before_ProdQty,2))+' ppm'
    before_AAR=round(before_ImprovSVC*1000000/before_ProdQty,2) # 최종 개선율 구하기 위해

    ARPMdata.at[3,2]=str(round(after_ImprovSVC*1000000/after_ProdQty,2))+' ppm'
    after_AAR=round(after_ImprovSVC*1000000/after_ProdQty,2)# 최종 개선율 구하기 위해 

    ##AAR
    ARPMdata.at[4,1]=""
    ARPMdata.at[4,2]=str(round((before_AAR-after_AAR)*100/before_AAR,2))+' %'

    ##칼럼 인덱스 이름 바꾸기
    ARPMdata.columns = ["Before Improvement", "After Improvement"]
    ARPMdata.index = ["SVC", "Production Qty","PPM","AAR"]

    ###matplotlib table value 생성
    ARPMdata_var = [ ]
    for column in ARPMdata.columns.values:
        ARPMdata_var.append ( ARPMdata [ column ].tolist () )
    ARPMdata_numpy_array = np.array(ARPMdata_var)
    ARPMdata_transpose = ARPMdata_numpy_array.T
    ARPMdata_transpose_list = ARPMdata_transpose.tolist()
    ARPMdata_table_vals=ARPMdata_transpose_list

    ## table value 넣고 테이블 정리
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_axis_off()
    table_vals=ARPMdata_table_vals
    row_labels=ARPMdata.index
    col_labels=ARPMdata.columns
    a=plt.table(cellText=table_vals,rowLabels=row_labels,colLabels=col_labels,loc='center',rowColours=['#EFFDFF','#C9F6FC','#2ECFE4','#0393A6'],colColours=['#C6C2CF','#C6C2CF'])

    plt.title('AAR & PPM Table (Model : '+meg_Function2_Models+'  / Symptoms : '+meg_Function2_Symptoms+')', fontweight ="bold", pad=0.1)

    a.auto_set_column_width(col=list(range(len(col_labels))))
    print("Mission Complete !")



elif Function2_Indicators=='4':

    
    ## L12_SVC, L12_Sales, Weight_Sales dataframe
    L12_SVC = pd.DataFrame(index=range(0,len(idx)-1),columns=['L12_SVC']) # total 까지 포함한 값
    L12_Sales = pd.DataFrame(index=range(0,len(idx)-1),columns=['L12_Sales'])
    Weight_Sales = pd.DataFrame()
    FDR = pd.DataFrame(index=range(0,len(idx)-1),columns=['FDR'])
    FFR = pd.DataFrame(index=range(0,len(idx)-1),columns=['FFR'])

    # 반복문을 위해 index를 셋팅
    SVC_table=pyramid_table.reset_index()
    SVC_table=SVC_table.drop('GQISClosingMonth',axis=1)
    SVC_table=SVC_table.T
    SVC_table=SVC_table.reset_index()
    SVC_table=SVC_table.drop('ProductionMonth',axis=1)


    #####################################################
    ##### L12 SVC 만들기
    i=0
    k=0
    j=0
    t=-1

    for i in range(len(idx)-1):
        if i<12:
            k=0
            for t in range(i):
                for j in range(i):
                    k=SVC_table.at[i-t,i-j]+k
                    j=j+1
        else:
            k=0
            for t in range(12):
                for j in range(12):
                    k=SVC_table.at[i-t,i-j]+k
                    j=j+1
        L12_SVC.at[i,'L12_SVC']=k
        i=i+1
    print("L12_SVC")
    print(L12_SVC)
        
    #####################################################

    # Accumulate Sales
    Acc=sales_data.cumsum()
    Acc=Acc.reset_index()
    Acc=Acc.drop(['index'],axis=1)
    Acc.columns=['Acc']



    # Accumulate 한 것 빼기
    k=0
    for i in range(len(idx)-1):
        if i<12:
            k=Acc.at[i,'Acc']
        else:
            k=Acc.at[i,'Acc']-Acc.at[i-12,'Acc']
        L12_Sales.at[i,'L12_Sales']=int(k)
        i=i+1


    #####################################################
    ##### Weight Sales 만들기
    for i in range(len(idx)-1):
        if i<12:
            j=0
            k=0
            for j in range(i+1):
                k=sales_data.at[j,"sales_data"]*(i+1-j)/12+k
                Weight_Sales.at[i,'Weight_Sales']=k
                j=j+1
        else:
            k=0
            for t in range(12):
                k=sales_data.at[t+i-11,"sales_data"]*(12-t)/12+k
                t=t+1
        Weight_Sales.at[i,'Weight_Sales']=int(k)
        i=i+1

    print(L12_Sales)
    print(Weight_Sales)
    

    #####################################################
    ##### FDR 만들기
    condition=0
    for i in range(len(idx)-1):
        condition=L12_Sales.at[i,'L12_Sales']
        print("condition")
        print(condition)
        if condition==0:
            #np.nan
            FDR.at[i,'FDR']=0
            print(FDR.at[i,'FDR'])
        else:
            FDR.at[i,'FDR']=L12_SVC.at[i,'L12_SVC']*100/L12_Sales.at[i,'L12_Sales']
            print(FDR.at[i,'FDR'])
        i=i+1

    #####################################################
    ##### FFR 만들기
    condition=0
    for i in range(len(idx)-1):
        condition=Weight_Sales.at[i,'Weight_Sales']
        if condition==0:
            FFR.at[i,'FFR']=0
            print(FFR.at[i,'FFR'])
        else:
            FFR.at[i,'FFR']=L12_SVC.at[i,'L12_SVC']*100/Weight_Sales.at[i,'Weight_Sales']
            print(FFR.at[i,'FFR'])
        i=i+1

    print("FDR")
    print(FDR)
    print("FFR")
    print(FFR)
    ##############################################그래프 만들기##########################################################3
    ############## plot의 요소들을 하나로 묶기
    fdrffr=pd.concat([FDR,FFR],axis=1)
    fdrffr=fdrffr.astype(float)
    fdrffr=fdrffr.round(2)# 소숫점 둘째 자리
    print("ffrfdr")
    print(fdrffr)

    today=date.today()
    thisyear_cutoff=int(today.strftime("%m"))
    print("thisyear_cutoff")
    print(thisyear_cutoff)

    FDR_1Y=pd.DataFrame()
    FFR_1Y=pd.DataFrame()

    FDR_2Y=pd.DataFrame()
    FFR_2Y=pd.DataFrame()

    FDR_3Y=pd.DataFrame()
    FFR_3Y=pd.DataFrame()

    FDR_4Y=pd.DataFrame()
    FFR_4Y=pd.DataFrame()


    ###################### 어차피 데이터는 3개년 2019 부터 시작
    # 일단 행렬에 넣고 
    for i in range(len(idx)-1): # Total 제
        if i<12:
            FDR_1Y.at[i,'FDR_1Y']=fdrffr.at[len(idx)-2-i,'FDR'] # Total, 0 부터 숫자 세기 시작함
            FFR_1Y.at[i,'FFR_1Y']=fdrffr.at[len(idx)-2-i,'FFR']
        elif i<24:
            FDR_2Y.at[i,'FDR_2Y']=fdrffr.at[len(idx)-2-i,'FDR']
            FFR_2Y.at[i,'FFR_2Y']=fdrffr.at[len(idx)-2-i,'FFR']
        elif i<36:
            FDR_3Y.at[i,'FDR_3Y']=fdrffr.at[len(idx)-2-i,'FDR']
            FFR_3Y.at[i,'FFR_3Y']=fdrffr.at[len(idx)-2-i,'FFR']
        elif i<48:
            FDR_4Y.at[i,'FDR_4Y']=fdrffr.at[len(idx)-2-i,'FDR']
            FFR_4Y.at[i,'FFR_4Y']=fdrffr.at[len(idx)-2-i,'FFR']

        else:
            print("done!")


    #  FFR FDR 합친 행렬 생성 --> 빈행렬의 가능성으로 모든 연도 합쳐서는 생성 불가
    FDRFFR_1Y= pd.concat([FDR_1Y,FFR_1Y],axis=1)
    FDRFFR_2Y= pd.concat([FDR_2Y,FFR_2Y],axis=1)
    FDRFFR_3Y= pd.concat([FDR_3Y,FFR_3Y],axis=1)
    FDRFFR_4Y= pd.concat([FDR_4Y,FFR_4Y],axis=1)

    F1Y=pd.DataFrame()
    F2Y=pd.DataFrame()
    F3Y=pd.DataFrame()
    F4Y=pd.DataFrame()

    print("before")
    print(FDRFFR_1Y)
    print(FDRFFR_2Y)
    print(FDRFFR_3Y)
    print(FDRFFR_4Y)

    
    # 그래프 그리기
    fig = plt.figure()
    fig.set_size_inches(10, 6)
    ax = fig.add_subplot(111)

    # reverse 행렬 만들기
    if FDRFFR_1Y.empty:
        print("FDRFFR_1Y empty")
    else:
        FDRFFR_1Y=FDRFFR_1Y[::-1]
        FDRFFR_1Y=FDRFFR_1Y.reset_index()
        FDRFFR_1Y=FDRFFR_1Y.drop('index',axis=1)
        
        #최신 연도로 해서 밀리는 것
        if len(FDRFFR_1Y)!=12:
            for i in range(len(FDRFFR_1Y)):
                F1Y.at[i+12-len(FDRFFR_1Y),'FDR_1Y']=FDRFFR_1Y.at[i,'FDR_1Y']
                F1Y.at[i+12-len(FDRFFR_1Y),'FFR_1Y']=FDRFFR_1Y.at[i,'FFR_1Y']
            FDRFFR_1Y=F1Y

        FDRFFR_1Y['FDR_1Y'].plot(color='#FF8C8C',style='--',marker='o',markerfacecolor='white',axes=ax,label='Recent 1Y FDR')
        FDRFFR_1Y['FFR_1Y'].plot(color='#FF8C8C',marker='o',markerfacecolor='white',axes=ax,label='Recent 1Y FFR')

        for i in range(len(FDRFFR_1Y)):
            ax.annotate(FDRFFR_1Y.at[i+12-len(FDRFFR_1Y),'FDR_1Y'],xy=(i+12-len(FDRFFR_1Y)-0.02,FDRFFR_1Y.at[i+12-len(FDRFFR_1Y),'FDR_1Y']),va='bottom',color='red',fontsize=9)
            ax.annotate(FDRFFR_1Y.at[i+12-len(FDRFFR_1Y),'FFR_1Y'],xy=(i+12-len(FDRFFR_1Y)-0.02,FDRFFR_1Y.at[i+12-len(FDRFFR_1Y),'FFR_1Y']),va='bottom',color='red',fontsize=9)


    if FDRFFR_2Y.empty:
        print("FDRFFR_2Y empty")
    else:
        FDRFFR_2Y=FDRFFR_2Y[::-1]
        FDRFFR_2Y=FDRFFR_2Y.reset_index()
        FDRFFR_2Y=FDRFFR_2Y.drop('index',axis=1)

        #최신 연도로 해서 밀리는 것
        if len(FDRFFR_2Y)!=12:
            for i in range(len(FDRFFR_2Y)):
                F2Y.at[i+12-len(FDRFFR_2Y),'FDR_2Y']=FDRFFR_2Y.at[i,'FDR_2Y']
                F2Y.at[i+12-len(FDRFFR_2Y),'FFR_2Y']=FDRFFR_2Y.at[i,'FFR_2Y']
            FDRFFR_2Y=F2Y

        FDRFFR_2Y['FDR_2Y'].plot(color='#ACD7AC',style='--',marker='o',markerfacecolor='white',axes=ax,label='Recent 2Y FDR')
        FDRFFR_2Y['FFR_2Y'].plot(color='#ACD7AC',marker='o',markerfacecolor='white',axes=ax,label='Recent 2Y FFR')

        for i in range(len(FDRFFR_2Y)):
            ax.annotate(FDRFFR_2Y.at[i+12-len(FDRFFR_2Y),'FDR_2Y'],xy=(i+12-len(FDRFFR_2Y)-0.02,FDRFFR_2Y.at[i+12-len(FDRFFR_2Y),'FDR_2Y']),va='bottom',color='#006600',fontsize=9)
            ax.annotate(FDRFFR_2Y.at[i+12-len(FDRFFR_2Y),'FFR_2Y'],xy=(i+12-len(FDRFFR_2Y)-0.02,FDRFFR_2Y.at[i+12-len(FDRFFR_2Y),'FFR_2Y']),va='bottom',color='#006600',fontsize=9)


    if FDRFFR_3Y.empty:
        print("FDRFFR_3Y empty")
    else:
        FDRFFR_3Y=FDRFFR_3Y[::-1]
        FDRFFR_3Y=FDRFFR_3Y.reset_index()
        FDRFFR_3Y=FDRFFR_3Y.drop('index',axis=1)

        #최신 연도로 해서 밀리는 것
        if len(FDRFFR_3Y)!=12:
            for i in range(len(FDRFFR_3Y)):
                F3Y.at[i+12-len(FDRFFR_3Y),'FDR_3Y']=FDRFFR_3Y.at[i,'FDR_3Y']
                F3Y.at[i+12-len(FDRFFR_3Y),'FFR_3Y']=FDRFFR_3Y.at[i,'FFR_3Y']    
            FDRFFR_3Y=F3Y
            
        FDRFFR_3Y['FDR_3Y'].plot(color='#D2CFF0',style='--',marker='o',markerfacecolor='white',axes=ax,label='Recent 3Y FDR')
        FDRFFR_3Y['FFR_3Y'].plot(color='#D2CFF0',marker='o',markerfacecolor='white',axes=ax,label='Recent 3Y FFR')

        for i in range(len(FDRFFR_3Y)):
            ax.annotate(FDRFFR_3Y.at[i+12-len(FDRFFR_3Y),'FDR_3Y'],xy=(i+12-len(FDRFFR_3Y)-0.02,FDRFFR_3Y.at[i+12-len(FDRFFR_3Y),'FDR_3Y']),va='bottom',color='#7F74F2',fontsize=9)
            ax.annotate(FDRFFR_3Y.at[i+12-len(FDRFFR_3Y),'FFR_3Y'],xy=(i+12-len(FDRFFR_3Y)-0.02,FDRFFR_3Y.at[i+12-len(FDRFFR_3Y),'FFR_3Y']),va='bottom',color='#7F74F2',fontsize=9)

            
    if FDRFFR_4Y.empty:
        print("FDRFFR_4Y empty")
    else:
        FDRFFR_4Y=FDRFFR_4Y[::-1]
        FDRFFR_4Y=FDRFFR_4Y.reset_index()
        FDRFFR_4Y=FDRFFR_4Y.drop('index',axis=1)

        #최신 연도로 해서 밀리는 것
        if len(FDRFFR_4Y)!=12:
            for i in range(len(FDRFFR_4Y)):
                F4Y.at[i+12-len(FDRFFR_4Y),'FDR_4Y']=FDRFFR_4Y.at[i,'FDR_4Y']
                F4Y.at[i+12-len(FDRFFR_4Y),'FFR_4Y']=FDRFFR_4Y.at[i,'FFR_4Y']
            FDRFFR_4Y=F4Y
            
        FDRFFR_4Y['FDR_4Y'].plot(color='#DCDBDB',style='--',marker='o',markerfacecolor='white',axes=ax,label='Recent 4Y FDR')
        FDRFFR_4Y['FFR_4Y'].plot(color='#DCDBDB',marker='o',markerfacecolor='white',axes=ax,label='Recent 4Y FFR')

        for i in range(len(FDRFFR_4Y)):
            ax.annotate(FDRFFR_4Y.at[i+12-len(FDRFFR_4Y),'FDR_4Y'],xy=(i+12-len(FDRFFR_4Y)-0.02,FDRFFR_4Y.at[i+12-len(FDRFFR_4Y),'FDR_4Y']),va='bottom',color='#98989E',fontsize=9)
            ax.annotate(FDRFFR_4Y.at[i+12-len(FDRFFR_4Y),'FFR_4Y'],xy=(i+12-len(FDRFFR_4Y)-0.02,FDRFFR_4Y.at[i+12-len(FDRFFR_4Y),'FFR_4Y']),va='bottom',color='#98989E',fontsize=9)

    print("graph")
    print(FDRFFR_1Y)
    print(FDRFFR_2Y)
    print(FDRFFR_3Y)
    print(FDRFFR_4Y)

    

    #ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xticks(np.arange(12))

    today=date.today()
    MONTH=pd.DataFrame(columns=["0"])
    for i in range(12):
        month=today-relativedelta(months=i)
        print(month)
        month=month.strftime('%b')
        print(month)
        MONTH.at[12-i,"0"]=month
        i=i+1
        
    MONTH=MONTH[::-1]
    MONTH=MONTH.reset_index()
    MONTH=MONTH.drop('index',axis=1)
        
    print(MONTH)
    print(MONTH.values)
        
    ax.set_xticklabels(MONTH["0"])

    plt.title('FFR & FDR Graph (Model : '+meg_Function2_Models+'  / Symptoms : '+meg_Function2_Symptoms+')', fontweight ="bold", pad=0.1)
    #plt.legend()
    plt.legend(borderaxespad=1,ncol=2)
    #plt.legend(bbox_to_anchor=(0, 1.5), borderaxespad=1,ncol=2)
    print("Mission Complete !")
    
plt.savefig('fig.png')
plt.show()

#첨부 파일3
with open('fig.png', 'rb') as f:
        img_data = f.read()
image = MIMEImage(img_data, name=os.path.basename('fig.png'))
msg.attach(image)

#첨부 파일3
with open('sign.png', 'rb') as f:
        img_data = f.read()
image = MIMEImage(img_data, name=os.path.basename('sign.png'))
msg.attach(image)

#메세지 보내고 확인하기
#server.send_message(msg)
server.close()
print("Sucess!!!")

msg.attach(image)

