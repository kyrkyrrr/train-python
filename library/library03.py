from datetime import datetime
import numpy as np
import collections

class trans_tool:
    def __init__(self):
        print('ライブラリ読み込み')
        self.__city_dic, self.__html_dic = self.__generate_dic()
        self.__num_city = len(self.__city_dic)
        self.__num_html = len(self.__html_dic)
        
    def __generate_dic(self):
        html_dic = dict()
        city_dic = dict()
        html_sets = set()
        city_sets = set()
        with open('./input/sample_work03.csv') as f:
            f.readline()
            for line in f:
                elements = line[:-1].split(',')
                html = elements[3]
                city = elements[5]
                city_sets.add(city if city != '' else '?')
                index = html.split('/')[5].find('.html')
                html_sets.add(html.split('/')[5][:index])
        for i, v in enumerate(sorted(list(city_sets))):
            city_dic[v] = i
        for i, v in enumerate(sorted(list(html_sets))):
            html_dic[v] = i
        return city_dic, html_dic
    
    def __trans_date(self, element):
        date = element.split(' ')[0]
        return datetime.strptime(date, '%Y-%m-%d').month if date != '' else 13
    
    def __trans_click(self, element):
        return int(element) if element != '' else 0
    
    def __trans_html(self, element):
        index = element.split('/')[5].find('.html')
        number = self.__html_dic[element.split('/')[5][:index]]
        return self.__trans_dummy_value(self.__num_html, number)
    
    def __trans_city(self, element):
        number = self.__city_dic[element if element != '' else '?']
        return self.__trans_dummy_value(self.__num_city, number)

    def __trans_num1(self, element):
        count_dict = collections.Counter(element.split(':'))
        return count_dict['1']
    
    def __trans_dummy_value(self, num_dim, number):
        return [1 if number == index else 0 for index in range(num_dim)]
    
    def generate_vector(self, line):
        vec = []
        elements = line.split(',')
        vec.append(self.__trans_click(elements[2]))
        vec.append(self.__trans_date(elements[0]))
        vec.extend(self.__trans_html(elements[3]))
        vec.extend(self.__trans_city(elements[5]))
        vec.append(self.__trans_num1(elements[7]))
        return vec
    
    def output(self, vectors, file_name):
        with open(file_name, 'w') as f:
            for vec in vectors:
                f.write(','.join(list(map(str, vec))) + '\n')