import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import numpy as np


import datetime

class Parser:

    def __init__(self, first_date, second_date) -> None:
        self.first_date = first_date
        self.second_date = second_date


    def rasp_tosite(self):
        
        



        #first_date='09.05'
        #second_date='09.12'

        request = requests.get(f'https://portal.unn.ru/ruzapi/schedule/student/277268?start=2023.{self.first_date}&finish=2023.{self.second_date}&lng=1')
            
        soup = BeautifulSoup(request.text, 'lxml').text
        data = json.loads(soup)
        
        
        test = {
        'name_lesson':[],
        'first_time':[],
        'last_time':[],
        'type_lesson':[],
        'name_lecturer':[],
        'stream':[],
        'auditorium':[],
        'week':[],
        'date_lesson':[],
        
    }
    
    

        for j in data:
            
            test['name_lesson'].append(j['discipline'])
            test['date_lesson'].append(j['date'])
            test['first_time'].append(j['beginLesson'])
            test['last_time'].append(j['endLesson'])
            test['type_lesson'].append(j['kindOfWork'])
            test['name_lecturer'].append(j['lecturer'])
            test['stream'].append('Поток:' + j['stream'])
            test['auditorium'].append(j['auditorium'] + ' ' + j['building'])
            test['week'].append(j['dayOfWeekString'])


        
        dataframe = pd.DataFrame(test)
        dataframe['mes'] = [i[5:7] for i in dataframe['date_lesson']]
        dataframe['mes'] = dataframe['mes'].map({'01': 'Января',
            '02': 'Февраля',
            '03': 'Марта',
            '04': 'Апреля',
            '05': 'Мая',
            '06': 'Июня',
            '07': 'Июля',
            '08': 'Августа',
            '09': 'Сентября',
            '10': 'Октября',
            '11': 'Ноября',
            '12': 'Декабря',})
        
        power_lesson = [[len(dataframe[dataframe['date_lesson'] == i]['name_lesson'])]*len(dataframe[dataframe['date_lesson'] == i]['name_lesson']) for i in sorted(list(set(dataframe['date_lesson'].to_list())))]
        

        all=[]

        for lst in power_lesson:
            all.extend(lst)
        
        dataframe['power_lesson'] = all

        keys = [f'{i[-2:]} {j} {k}' for i, j, k in zip(dataframe['date_lesson'], dataframe['mes'], dataframe['week'])]
        values = []
        
        hh = {}
    
        for i, j in zip(dataframe['date_lesson'], keys):
            va = dataframe[dataframe['date_lesson'] == i].to_dict('list')
            hh[j] = va
            
        
        return hh


    def rasp(self):
    
        #first_date = '06.12'
        #second_date = '06.20'
        #range_date = int(self.second_date[-2:]) - int(self.first_date[-2:])
        
        date = datetime.datetime.now()
        today = date.date()
        week_today = date.date() + datetime.timedelta(days=7) 
        range_date = (week_today - today).days
        
        
        request = requests.get(f'https://portal.unn.ru/ruzapi/schedule/student/277268?start=2023.{self.first_date}&finish=2023.{self.second_date}&lng=1')
        
        soup = BeautifulSoup(request.text, 'lxml').text
        data = json.loads(soup)
        
        columns = ['auditorium', 'author', 'beginLesson', 'building', 'date', 'dayOfWeekString', 'kindOfWork', 'lecturer', 'parentschedule', 'stream', 'endLesson', 'discipline']
        needs_values = []
        for j in range(range_date):
            
            needs_values.append([data[j][i] for i in columns])
        dataframe = pd.DataFrame(np.matrix(needs_values), columns=columns)
        return dataframe
    
    def zach(password, login, semester, index_lesson):
        
        data_ = {
            'AUTH_FORM': 'Y',
            'TYPE': 'AUTH',
            'backurl': '/auth/?backurl=%2Fapp%2Fprofile%3Bmode%3Dedu%2Fmarks',
            'USER_LOGIN': login,
            'USER_PASSWORD': password,
        }
        session = requests.Session()
        
        session.post(url='https://portal.unn.ru', data=data_)
        request = session.get('https://portal.unn.ru/bitrix/vuz/api/marks2/').text
        
        data = json.loads(request)
        

        

        return data[0]['semesters'][semester]['data'][index_lesson]
        

    def news(self, login, password):
        
        au = {
            'AUTH_FORM': 'Y',
            'TYPE': 'AUTH',
            'backurl': '/auth/?backurl=%2Fapp%2Fprofile%3Bmode%3Dedu%2Fmarks',
            'USER_LOGIN': login,
            'USER_PASSWORD': password,
        }
        
        session = requests.Session()
        
        session.post(url='https://portal.unn.ru', data=au)
        request = session.get('https://portal.unn.ru/stream/')
        soup = BeautifulSoup(request.text, 'lxml')
        block = soup.find_all('div', class_="feed-item-wrap")
        for i in block:
            name = i.find('a', class_="feed-post-user-name").text
            time = i.find('div', class_="feed-post-time-wrap")
            text = i.find('div', class_='feed-post-contentview feed-post-text-block-inner')
            url = 'https://portal.unn.ru' + i.find('div', class_="feed-post-time-wrap").find('a').get('href')
            


