import time
from decimal import Decimal

import seaborn
from matplotlib import legend
from scipy.stats import stats
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# The path to where you have your chrome webdriver stored:
webdriver_path = 'C:/SHARING KNOWLEDGE/FK/chromedriver.exe'

# Add arguments telling Selenium to not actually open a window
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')

# Fire up the headless browser
browser = webdriver.Chrome(executable_path=webdriver_path,
                           chrome_options=chrome_options)

#DATA PEMILU BALI
url3 = 'https://kawalpemilu.org/#pilpres:53241'

# Load webpage
browser.get(url3)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse the raw into delicious soup
soup3 = BeautifulSoup(browser.page_source, 'html.parser')

#DATA PENDUDUK BALI
url4 = 'https://bali.bps.go.id/statictable/2018/02/15/33/penduduk-provinsi-bali-menurut-agama-yang-dianut-hasil-sensus-penduduk-2010.html'

# Load webpage
browser.get(url4)

# It can be a good idea to wait for a few seconds before trying to parse the page
# to ensure that the page has loaded completely.
time.sleep(10)

# Parse the raw into delicious soup
soup4 = BeautifulSoup(browser.page_source, 'html.parser')

def suaraBali():
    tabel = soup3.find('table', attrs={'class':'table'})
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

        row.append('BALI')
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
    ax.set_ylabel('Score')

    # Set the chart's title
    ax.set_title('HASIL PEMILU 2019 Prov. Bali')

    # Set the position of the x ticks
    ax.set_xticks([p + 0.5  * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['WILAYAH'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.ylim(100000,2500000)

    # Adding the legend and showing the plot
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x() + .04, i.get_height() + 12000, \
                str(round((i.get_height()), 2)), fontsize=11, color='black')
    plt.legend(['JOKOWI', 'PRABOWO'], loc='upper right')
    plt.grid()
    plt.show()

    tabel2 = soup4.find('table', attrs={'class': 'xl9418499'})
    hasil2 = tabel2.find_all('tr', attrs={'height': '27'})
    print(hasil2)

    islam = []
    katolik = []
    protestan = []
    hindu = []
    budha = []
    konghucu = []
    lainnya = []
    tidak_terjawab = []
    tidak_tanya = []

    # loop over hasil
    for h2 in hasil2:
        # find all columns per result
        dataTot2 = h2.find_all('td', attrs={'class': 'xl9918499'})
        # check that columns have data
        if len(dataTot2) == 0:
            continue
        i = dataTot2[0].getText()
        k = dataTot2[1].getText()
        p = dataTot2[2].getText()
        h = dataTot2[3].getText()
        b = dataTot2[4].getText()
        ko = dataTot2[5].getText()
        l = dataTot2[6].getText()
        t = dataTot2[7].getText()
        ti = dataTot2[8].getText()

        i = i.replace(' ', '').encode('ascii', 'ignore')
        k = k.replace(' ', '').encode('ascii', 'ignore')
        p = p.replace(' ', '').encode('ascii', 'ignore')
        h = h.replace(' ', '').encode('ascii', 'ignore')
        b = b.replace(' ', '').encode('ascii', 'ignore')
        ko = ko.replace(' ', '').encode('ascii', 'ignore')
        l = l.replace(' ', '').encode('ascii', 'ignore')
        t = t.replace(' ', '').encode('ascii', 'ignore')
        ti = ti.replace(' ', '').encode('ascii', 'ignore')

        i = float(i)
        k = float(k)
        p = float(p)
        h = float(h)
        b = float(b)
        ko = float(ko)
        l = float(l)
        t = float(t)
        ti = float(ti)

        islam.append(i)
        katolik.append(k)
        protestan.append(p)
        hindu.append(h)
        budha.append(b)
        konghucu.append(ko)
        lainnya.append(l)
        tidak_terjawab.append(t)
        tidak_tanya.append(ti)

    agama = []
    tot = katolik + protestan + hindu + budha + konghucu + lainnya + tidak_terjawab + tidak_tanya
    res = sum(tot[0:len(tot)])
    nonMuslim = []
    nonMuslim.append(res)
    print(res)
    agama.append('AGAMA')
    raw_data = {'AGAMA': agama,
                'Islam': islam, 'Non-Muslim': nonMuslim}
    df = pd.DataFrame(raw_data, columns=['AGAMA', 'Islam', 'Non-Muslim'])
    print(df)

    # Setting the positions and width for the bars
    pos = list(range(len(df['AGAMA'])))
    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 5))
    # plt.subplot(2, 1, 1)
    # Create a bar with pre_score data,
    # in position pos,
    plt.bar(pos,
            # using df['pre_score'] data,
            df['Islam'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            # with label the first value in first_name
            label=df['AGAMA'][0])

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos],
            # using df['mid_score'] data,
            df['Non-Muslim'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#F78F1E',
            # with label the second value in first_name
            label=df['AGAMA'][0])

    # Set the y axis label
    ax.set_ylabel('Jumlah Suara')

    # Set the chart's title
    ax.set_title('Penduduk Provinsi Bali Menurut Agama')

    # Set the position of the x ticks
    ax.set_xticks([p + 0.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['AGAMA'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.ylim(0, 3500000)

    # # Adding the legend and showing the plot
    # set individual bar lables using above list
    for xx in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(xx.get_x() + .04, xx.get_height() + 12000, \
                str(round((xx.get_height()), 2)), fontsize=11, color='black')
    plt.legend(['Islam', 'Non-Muslim'], loc='upper right')
    plt.grid()
    plt.show()

def korelasiBali():
    tabel = soup3.find('table', attrs={'class':'table'})
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

        # satu = dataTot[1].find('a').getText()
        dua = dataTot[2].find('span', attrs={'class':'abs'}).getText()
        tiga = dataTot[3].find('span', attrs={'class':'abs'}).getText()
        dua = dua.replace('.','')
        tiga = tiga.replace('.','')
        dua = float(dua)
        tiga = float(tiga)

        row.append('BALI')
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
    tabel2 = soup4.find('table', attrs={'class':'xl9418499'})
    hasil2 = tabel2.find_all('tr', attrs={'height':'20'})
    print(hasil2)

    islam = []
    katolik = []
    protestan = []
    hindu = []
    budha = []
    konghucu = []
    lainnya = []
    tidak_terjawab = []
    tidak_tanya = []

    # loop over hasil
    for h2 in hasil2:
        # find all columns per result
        dataTot2 = h2.find_all('td', attrs={'class':'xl9818499'})
        # check that columns have data
        if len(dataTot2) == 0:
            continue
        i = dataTot2[0].getText()
        k = dataTot2[1].getText()
        p = dataTot2[2].getText()
        h = dataTot2[3].getText()
        b = dataTot2[4].getText()
        ko = dataTot2[5].getText()
        l = dataTot2[6].getText()
        t = dataTot2[7].getText()
        ti = dataTot2[8].getText()

        i = i.replace(' ','').encode('ascii', 'ignore')
        k = k.replace(' ','').encode('ascii', 'ignore')
        p = p.replace(' ','').encode('ascii', 'ignore')
        h = h.replace(' ','').encode('ascii', 'ignore')
        b = b.replace(' ','').encode('ascii', 'ignore')
        ko = ko.replace(' ','').encode('ascii', 'ignore')
        l = l.replace(' ','').encode('ascii', 'ignore')
        t = t.replace(' ','').encode('ascii', 'ignore')
        ti = ti.replace(' ','').encode('ascii', 'ignore')

        i = float(i)
        k = float(k)
        p = float(p)
        h = float(h)
        b = float(b)
        ko = float(ko)
        l = float(l)
        t = float(t)
        ti = float(ti)

        islam.append(i)
        katolik.append(k)
        protestan.append(p)
        hindu.append(h)
        budha.append(b)
        konghucu.append(ko)
        lainnya.append(l)
        tidak_terjawab.append(t)
        tidak_tanya.append(ti)
    np_islam = np.array(islam)
    np_katolik = np.array(katolik)
    np_protestan = np.array(protestan)
    np_hindu = np.array(hindu)
    np_budha = np.array(budha)
    np_konghucu = np.array(konghucu)
    np_lain = np.array(lainnya)
    np_jwb = np.array(tidak_terjawab)
    np_tny = np.array(tidak_tanya)
    non = np_katolik+np_protestan+np_hindu+np_budha+np_konghucu+np_lain+np_jwb+np_tny
    print('NON IS', non)
    agama = []
    # nonMuslim = []
    # nonMuslim.append(non)
    # non = np.array(non)
    print('nonmus', non)
    agama.append('AGAMA')
    raw_data = {'AGAMA': agama,
                'Islam': islam,'Non-Muslim': non}
    # df = pd.DataFrame(raw_data, columns=['AGAMA', 'Islam','Non-Muslim'])
    islam = np.array(islam)
    nonMuslim = np.array(non)
    print(nonMuslim)
    # print(df)

    # pearson correlation

    indeks = []
    X = row01
    X2 = row02
    y = nonMuslim


    def pearson01(X, y):
        r, p = stats.pearsonr(X, y)
        print('R_VALUE 01 =', r)
        print('P_VALUE 01= ', p)

        # plot bivariate scatterplots
        fig = plt.figure(figsize=(17, 5))
        seaborn.regplot(X, y, fit_reg=True);
        plt.xlabel('Jumlah Suara Jokowi di Provinsi Bali 2019');
        plt.ylabel('Jumlah Penduduk Menurut Agama di Provinsi Bali 2010');
        plt.title('Pemilu 2019 - Penduduk Menurut Agama di Bali 2010');
        fig.tight_layout()
        plt.show()

    def pearson02(X2, y):
        r, p = stats.pearsonr(X2, y)
        print('R_VALUE 02 =', r)
        print('P_VALUE 02= ', p)

        # plot bivariate scatterplots
        fig = plt.figure(figsize=(17, 5))
        seaborn.regplot(X2, y, fit_reg=True);
        plt.xlabel('Jumlah Suara Prabowo di Provinsi Bali 2019');
        plt.ylabel('Jumlah Penduduk Menurut Agama di Provinsi Bali 2010');
        plt.title('Pemilu 2019 - Penduduk Menurut Agama di Bali 2010');
        fig.tight_layout()
        plt.show()

    pearson01(X, y)
    pearson02(X2, y)

suaraBali()
korelasiBali()