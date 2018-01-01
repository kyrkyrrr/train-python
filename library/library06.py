import numpy as np
import datetime
from collections import Counter

class trans_vector:
    
    def __init__(self):
        print('ライブラリ読み込み')
        self.__city_dic, self.__html_dic = self.__generate_dic()
        self.__num_city = len(self.__city_dic)
        self.__num_html = len(self.__html_dic)
    
    def __generate_dic(self):
        city_dic = dict()
        html_dic = dict()
        html_sets = set()
        city_sets = set()
        with open('./input/sample_work03.csv')as f:
            f.readline()
            for line in f:
                elements = line[:-1].split(',')
                date = elements[0]
                html = elements[3]
                index = html.split('/')[5].find('.html')
                html_sets.add(html.split('/')[5][:index])
                city = elements[5]
                city_sets.add(city if city != '' else '?')

            for i, v in enumerate(sorted(list(city_sets))):
                city_dic[v] = i
            for i, v in enumerate(sorted(list(html_sets))):
                html_dic[v] = i
        return  city_dic, html_dic

    def __trans_date(self, string_date):
        date = string_date.split(' UTC')[0]
        if date==' ':
            return(13)
        else:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # => datetime.datetime(2017, 7, 1, 12, 6, 19
        return(dt.month)

    def __trans_click(self, click_value):
        if click_value=='1':
            return(1)
        else:
            return(0)
    
    def __trans_numl(self, figures):
        c = Counter(figures)
        return c['1']
    
    def __trans_dummy_value(self, num_dim, number):
        dummy = []
        for index in range(num_dim):
            if number == index:
                dummy.append(1)
            else:
                dummy.append(0)
        return dummy
    
    def __trans_html(self, url_data):
        index = url_data.split('/')[5].find('.html')
        number = self.__html_dic[url_data.split('/')[5][:index]]
        return self.__trans_dummy_value(self.__num_html, number)
    
    def __trans_city(self, city_data):
        number = self.__city_dic[city_data]
        return self.__trans_dummy_value(self.__num_city, number)

    def generate_vector(self, line):
        vec = []
        elements = line.split(',')
        vec.append(self.__trans_click(elements[2]))
        vec.append(self.__trans_date(elements[0]))
        vec.extend(self.__trans_html(elements[3]))
        vec.extend(self.__trans_city(elements[5]))
        vec.append(self.__trans_numl(elements[7]))
        return vec

    def output(self, vectors, file_name):
        with open(file_name, 'w') as f:
            for vec in vectors:
                f.write(','.join(list(map(str, vec))) + '\n')