import time
from decimal import Decimal

import cor as cor
import seaborn as seaborn
import statistics as statistics
from matplotlib import legend
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import pearsonr
import statistics



# The path to where you have your chrome webdriver stored:
webdriver_path = 'C:/SHARING KNOWLEDGE/FK/chromedriver.exe'

# Add arguments telling Selenium to not actually open a window
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')

# Fire up the headless browser
browser = webdriver.Chrome(executable_path=webdriver_path,
                           chrome_options=chrome_options)
#DATA PEMILU PAPUA
url = 'https://kawalpemilu.org/#pilpres:78203'

# Load webpage
browser.get(url)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse the raw into delicious soup
soup = BeautifulSoup(browser.page_source, 'html.parser')


#DATA KEMISKINAN PAPUA
url2 = 'https://papua.bps.go.id/dynamictable/2019/05/15/281/jumlah-penduduk-miskin-menurut-kabupaten-di-provinsi-papua-2014--2018.html'

# Load webpage
browser.get(url2)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse the raw into delicious soup
soup2 = BeautifulSoup(browser.page_source, 'html.parser')



def suaraPapua():
    tabel = soup.find('table', attrs={'class':'table'})
    hasil = tabel.find_all('tr', attrs={'class':'footer'})
    # print(hasil)



    # create and write headers to a list
    row = []
    row01 = []
    row02 = []


    # loop over hasil
    for h in hasil:
        # find all columns per result
        dataTot = h.find_all('td')
        # check that columns have data
        if len(dataTot) == 0:
            continue

        # satu = dataTot[1].find('a').getText()
        dua = dataTot[2].find('span', attrs={'class':'abs'}).getText()
        tiga = dataTot[3].find('span', attrs={'class':'abs'}).getText()
        dua = dua.replace('.','')
        tiga = tiga.replace('.','')
        dua = float(dua)
        tiga = float(tiga)
        # print(satu)
        # print('01 : ',dua)
        # print('02 : ',tiga)
        row.append('PAPUA')
        row01.append(dua)
        row02.append(tiga)

    print(row)
    print(row01)
    print(row02)
    row01 = np.array(row01)
    row02 = np.array(row02)


    raw_data = {'WILAYAH': row,
            'JOKOWI': row01,
            'PRABOWO': row02}
    df = pd.DataFrame(raw_data, columns = ['WILAYAH', 'JOKOWI', 'PRABOWO'])
    print(df)

    # Setting the positions and width for the bars
    pos = list(range(len(df['WILAYAH'])))
    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 5))
    # plt.subplot(2, 1, 1)
    # Create a bar with pre_score data,
    # in position pos,
    plt.bar(pos,
            # using df['pre_score'] data,
            df['JOKOWI'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            # with label the first value in first_name
            label=df['WILAYAH'][0])

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos],
            # using df['mid_score'] data,
            df['PRABOWO'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#F78F1E',
            # with label the second value in first_name
            label=df['WILAYAH'][0])

    # Set the y axis label
    ax.set_ylabel('Jumlah Suara')

    # Set the chart's title
    ax.set_title('HASIL PEMILU 2019 Prov. PAPUA')

    # Set the position of the x ticks
    ax.set_xticks([p + 0.5  * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['WILAYAH'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.ylim(100000,1500000)

    # Adding the legend and showing the plot
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x() + .04, i.get_height() + 12000, \
                str(round((i.get_height()), 2)), fontsize=11, color='black')
    plt.legend(['JOKOWI', 'PRABOWO'], loc='upper right')
    plt.grid()
    plt.show()

    tabel2 = soup2.find('table', attrs={'id':'tableRightBottom'})
    hasil2 = tabel2.find_all('tr')
    print(hasil2)

    indeksKemiskinan = []
    t14 = []
    t15 = []
    t16 = []
    t17 = []
    t18 = []

    # loop over hasil
    for h2 in hasil2:
        # find all columns per result
        dataTot2 = h2.find_all('td', attrs={'class':'datas'})
        # check that columns have data
        if len(dataTot2) == 0:
            continue

        thn14 = dataTot2[0].getText()
        thn15 = dataTot2[1].getText()
        thn16 = dataTot2[2].getText()
        thn17 = dataTot2[3].getText()
        thn18 = dataTot2[4].getText()

        thn14 = float(thn14)*1000
        thn15 = float(thn15)*1000
        thn16 = float(thn16)*1000
        thn17 = float(thn17)*1000
        thn18 = float(thn18)*1000

        t14.append(thn14)
        t15.append(thn15)
        t16.append(thn16)
        t17.append(thn17)
        t18.append(thn18)
        # del t14[-1]
        # del t15[-1]
        # del t16[-1]
        # del t17[-1]
        # del t18[-1]
    indeksKemiskinan.append(t14[-1])
    indeksKemiskinan.append(t15[-1])
    indeksKemiskinan.append(t16[-1])
    indeksKemiskinan.append(t17[-1])
    indeksKemiskinan.append(t18[-1])

    # print(indeksKemiskinan)
    tahun = []
    tahun.append('2014')
    tahun.append('2015')
    tahun.append('2016')
    tahun.append('2017')
    tahun.append('2018')
    print(tahun)
    print(indeksKemiskinan)
    np_tahun = np.array(tahun)
    np_indeks = np.array(indeksKemiskinan)


#pearson correlation



    # # Naming label
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Penduduk Miskin di Provinsi Papua (Ribu Jiwa)')

    # styling x,y value
    plt.xticks(rotation=30,ha='right')
    plt.yticks(np.arange(np_indeks.min(),np_indeks.max(),4000000))

    # plot data
    # plt.subplot(2, 1, 2)
    plt.plot(np_tahun,np_indeks,color='red',label='Kemiskinan',linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)
    plt.title('Jumlah Penduduk Miskin di Provinsi Papua')
    plt.legend(loc='upper left')
    plt.yscale('linear')
    plt.grid()
    plt.show()


def korelasiPapua():
    tabel = soup.find('table', attrs={'class':'table'})
    hasil = tabel.find_all('tr', attrs={'class':'row'})
    # print(hasil)



    # create and write headers to a list
    row = []
    row01 = []
    row02 = []


    # loop over hasil
    for h in hasil:
        # find all columns per result
        dataTot = h.find_all('td')
        # check that columns have data
        if len(dataTot) == 0:
            continue

        satu = dataTot[1].find('a').getText()
        dua = dataTot[2].find('span', attrs={'class':'abs'}).getText()
        tiga = dataTot[3].find('span', attrs={'class':'abs'}).getText()
        dua = dua.replace('.','')
        tiga = tiga.replace('.','')
        dua = float(dua)
        tiga = float(tiga)
        # print(satu)
        # print('01 : ',dua)
        # print('02 : ',tiga)
        row.append(satu)
        row01.append(dua)
        row02.append(tiga)

    print(row)
    print(row01)
    print(row02)
    row = np.array(row)
    row01 = np.array(row01)
    row02 = np.array(row02)


    raw_data = {'WILAYAH': row,
            'JOKOWI': row01,
            'PRABOWO': row02}
    df = pd.DataFrame(raw_data, columns = ['WILAYAH', 'JOKOWI', 'PRABOWO'])
    print(df)

    tabel2 = soup2.find('table', attrs={'id':'tableRightBottom'})
    hasil2 = tabel2.find_all('tr')
    print(hasil2)

    indeksKemiskinan = []
    t14 = []
    t15 = []
    t16 = []
    t17 = []
    t18 = []

    # loop over hasil
    for h2 in hasil2:
        # find all columns per result
        dataTot2 = h2.find_all('td', attrs={'class':'datas'})
        # check that columns have data
        if len(dataTot2) == 0:
            continue

        thn14 = dataTot2[0].getText()
        thn15 = dataTot2[1].getText()
        thn16 = dataTot2[2].getText()
        thn17 = dataTot2[3].getText()
        thn18 = dataTot2[4].getText()

        thn14 = float(thn14)*1000
        thn15 = float(thn15)*1000
        thn16 = float(thn16)*1000
        thn17 = float(thn17)*1000
        thn18 = float(thn18)*1000

        t14.append(thn14)
        t15.append(thn15)
        t16.append(thn16)
        t17.append(thn17)
        t18.append(thn18)

    th14 = np.array(t14)
    th15 = np.array(t15)
    th16 = np.array(t16)
    th17 = np.array(t17)
    th18 = np.array(t18)

    indeksKemiskinan.append(t18)
    th14 = th14[:-1]
    th15 = th15[:-1]
    th16 = th16[:-1]
    th17 = th17[:-1]
    th18 = th18[:-1]

    tahun = th14+th15+th16+th17+th18
    np_indeks5 = np.array(tahun)

#pearson correlation

    indeks = []
    X = row01
    X2 = row02
    y = np_indeks5
    print('XXX',X)
    print('YYY',y)

    def pearson01(X,y):
        r, p = stats.pearsonr(X, y)
        print('R_VALUE 01 =', r)
        print('P_VALUE 01= ', p)

        # plot bivariate scatterplots
        fig = plt.figure(figsize=(17, 5))
        seaborn.regplot(X, y, fit_reg=True);
        plt.xlabel('Jumlah Suara Jokowi di Provinsi Papua 2019');
        plt.ylabel('Jumlah Penduduk Miskin di Provinsi Papua 2018');
        plt.title('Pemilu 2019 - Penduduk Miskin 2018 di Papua');
        fig.tight_layout()
        plt.show()

    def pearson02(X2,y):
        r, p = stats.pearsonr(X2, y)
        print('R_VALUE 02 =', r)
        print('P_VALUE 02= ',p)

        # plot bivariate scatterplots
        fig = plt.figure(figsize=(17, 5))
        seaborn.regplot(X2, y, fit_reg=True);
        plt.xlabel('Jumlah Suara Prabowo di Provinsi Papua 2019');
        plt.ylabel('Jumlah Penduduk Miskin di Provinsi Papua 2018');
        plt.title('Pemilu 2019 - Penduduk Miskin 2018 di Papua');
        fig.tight_layout()
        plt.show()

    pearson01(X,y)
    pearson02(X2,y)

suaraPapua()
korelasiPapua()




