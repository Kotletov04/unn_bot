from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types.web_app_info import WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from config.parser_config import read_config
from parser.parser import Parser
from aiogram.types import InputFile
#from main import Bot_DB



import datetime

import pandas as pd

import configparser


import requests
import json


URL = read_config(name_key='URL', name_value='URL', name_file='config_settings.ini')
TOKEN = read_config(name_key='TOKEN', name_value='TOKEN', name_file='config_settings.ini')





storage = MemoryStorage()


class RegisterFSM(StatesGroup):
    
    login_input = State()
    password_input = State()
    id_input = State()
    fullname_input = State()
    



BOT = Bot(TOKEN)
DP = Dispatcher(BOT, storage=storage)










@DP.message_handler(commands=['start'])
async def start_command(message: types.Message):  
    
    buttons = [
        [
            types.KeyboardButton(text='Сегодня'),
            types.KeyboardButton(text='Завтра'),
            types.KeyboardButton(text='Профиль', web_app=WebAppInfo(url=URL)),   
        ],

        [
            types.KeyboardButton(text='Анекдоты точка ру'),
            types.KeyboardButton(text='Регистрация'),
            types.KeyboardButton(text='Новости')
        ],

        [
            types.KeyboardButton(text='Настройки')
            ]
    ]
    
    markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(text='Привет', reply_markup=markup)
    await message.delete()



@DP.message_handler(filters.Text(equals='Сегодня'))
async def today_button(message: types.Message):
    #Bot_DB.add_name(user_id=message.from_user.id, name=message.from_user.full_name, button='Сегодня', time=datetime.datetime.now())
    
    date = datetime.datetime.now()
    
    today = str(date.date().strftime("%m.%d"))
    week_today = date.date() + datetime.timedelta(days=7) 
    week_today = str(week_today.strftime("%m.%d"))
    dataframe = Parser(first_date=today, second_date=week_today).rasp()
    
    raspisaniye = dataframe[dataframe['date'] == date.date().strftime("%Y.%m.%d")]
    discipline = raspisaniye['discipline'].tolist()
    lecturer = raspisaniye['lecturer'].tolist()
    week = raspisaniye['dayOfWeekString'].tolist()
    date = raspisaniye['date'].tolist()
    time_first = raspisaniye['beginLesson'].tolist()
    time_last = raspisaniye['endLesson'].tolist()
    building = raspisaniye['building']
    type = raspisaniye['kindOfWork'].tolist()
    auditorium = raspisaniye['auditorium'].tolist()
    if raspisaniye.empty:
        await message.answer(text='Нет занятий')
    else:
        text_list = 'Расписание на сегодня:\n'
        for i, j, k, t_f, w, ty, t_l, bu, dis in zip(lecturer, date, auditorium, time_first, week, type, time_last ,building, discipline):
            text = f'\nПреподаватель {i} \nДата занятия {j} ({w}) \nАудитория ({bu}) {k} \nВремя {t_f} - {t_l} \nТип занятия: {ty} \nПара: {dis} \n'
            text_list = text_list+text
        await message.answer(text=text_list)

@DP.message_handler(filters.Text(equals='Завтра'))
async def today_button(message: types.Message):
    #Bot_DB.add_name(user_id=message.from_user.id, name=message.from_user.full_name, button='Завтра', time=datetime.datetime.now())
    
    date = datetime.datetime.now() + datetime.timedelta(days=1)
    
    today = str(date.date().strftime("%m.%d"))
    week_today = date.date() + datetime.timedelta(days=7) 
    week_today = str(week_today.strftime("%m.%d"))
    dataframe = Parser(first_date=today, second_date=week_today).rasp()

    dataframe = Parser(first_date=today, second_date=week_today).rasp()
    
    raspisaniye = dataframe[dataframe['date'] == date.date().strftime("%Y.%m.%d")]
    lecturer = raspisaniye['lecturer'].tolist()
    week = raspisaniye['dayOfWeekString'].tolist()
    date = raspisaniye['date'].tolist()
    time_first = raspisaniye['beginLesson'].tolist()
    time_last = raspisaniye['endLesson'].tolist()
    building = raspisaniye['building']
    type = raspisaniye['kindOfWork'].tolist()
    auditorium = raspisaniye['auditorium'].tolist()
    discipline = raspisaniye['discipline'].tolist()
    if raspisaniye.empty:
        await message.answer(text='Нет занятий')
    else:
        text_list = 'Расписание на завтра:\n'
        for i, j, k, t_f, w, ty, t_l, bu, dis in zip(lecturer, date, auditorium, time_first, week, type, time_last ,building, discipline):
            text = f'\nПреподаватель: {i} \nДата занятия: {j} ({w}) \nАудитория: ({bu}) {k} \nВремя: {t_f} - {t_l} \nТип занятия: {ty} \nПара: {dis} \n'
            text_list = text_list+text
        await message.answer(text=text_list)

@DP.message_handler(filters.Text(equals='Регистрация'))
async def reg(message: types.Message):
    #Bot_DB.add_name(user_id=message.from_user.id, name=message.from_user.full_name, button='Зачетка', time=datetime.datetime.now())
    
    menu_inline = types.InlineKeyboardMarkup().insert(types.InlineKeyboardButton(text='Продолжить >>', callback_data='dalee'))
    photo = InputFile('cat.jpg')
    await BOT.send_photo(photo=photo, chat_id=message.from_user.id, caption='Для того, чтобы пользоваться полным функционалом профиля необходимо указать логин и пароль от портала', reply_markup=menu_inline)
    #await RegisterFSM.id_input.set()


    





@DP.callback_query_handler(lambda c: c.data == 'dalee')
async def process_callback_button1(callback_query: types.CallbackQuery):
    #Bot_DB.add_name(user_id=message.from_user.id, name=message.from_user.full_name, button='Зачетка', time=datetime.datetime.now())
    
    config = configparser.ConfigParser()
    config.read('bot/config/config_users.ini', encoding="latin-1")
    print(callback_query.from_user.id)
    if callback_query.from_user.id in list([int(i[5:]) for i in config.sections()]):
        
        await callback_query.answer("Вы уже зарегистрированы!")
        
    else:
        
        await callback_query.message.answer("Укажите ваш логин")
        
        await RegisterFSM.login_input.set()

    

@DP.message_handler(state=RegisterFSM.login_input)
async def input_login(message: types.Message, state: FSMContext):
    if len(message.text) > 15:
        await message.answer("Никнейм не должен превышать 15 символов")
        return
    async with state.proxy() as data:
        data['LOGIN'] = message.text
    
    await message.answer('Укажите пароль')
    await RegisterFSM.next()
    

@DP.message_handler(state=RegisterFSM.password_input)
async def input_password(message: types.Message, state: FSMContext):
    
    
    try:    

        


        async with state.proxy() as data:
            data_ = {
            'AUTH_FORM': 'Y',
            'TYPE': 'AUTH',
            'backurl': '/auth/?backurl=%2Fapp%2Fprofile%3Bmode%3Dedu%2Fmarks',
            'USER_LOGIN': data['LOGIN'],
            'USER_PASSWORD': message.text,
                    }

            


            session = requests.Session()
                    
            session.post(url='https://portal.unn.ru', data=data_)
            request = session.get('https://portal.unn.ru/bitrix/vuz/api/profile/bootstrap').text

            data_json = json.loads(request)
            name = data_json['profile']['user']['fullname']


            config = configparser.ConfigParser()
            config[f'USER-{message.from_user.id}'] = {
                'ID': message.from_user.id,
                'NAME': message.from_user.full_name,
                'LOGIN': data['LOGIN'],
                'PASSWORD': message.text,
                'FULL_NAME': name
            }
            with open('bot/config/config_users.ini', 'a', encoding='utf-8') as configfile:
                config.write(configfile)
    

        await message.answer(f'Регистрация заверена, вас зовут {name}')
    
        await state.finish()

    except Exception as ex:
        print(ex)
        await message.answer('Данные указаны неверно')
        await state.finish()
    
    
    






@DP.message_handler(filters.Text(equals='Настройки'))
async def test(message: types.Message):
    buttons = [
        [
            types.KeyboardButton(text='Выбрать период расписания'),
            types.KeyboardButton(text='Выбрать тему расписания'),
            types.KeyboardButton(text='Включить/Отключить рассылку')

         ],

         [
            types.KeyboardButton(text='Назад'),
         ],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(text='Привет', reply_markup=markup)
    













