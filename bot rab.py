import telebot
import math
import time
from telebot import types

bot = telebot.TeleBot("2136145760:AAEWlQ2RQLHPkltG_OPXo-Cz6YJMlSt8MRw")



# Старт бота


@bot.message_handler(content_types=['text'])
def start(message):

    
    if message.text != '':
        bot.send_message(message.from_user.id, "Здравствуйте! Зарегистрируйте команду.");
        bot.register_next_step_handler(message, regUserBD); #следующий шаг 

# Функция создания базы
global arrayDataUsers; # Общая база данных
arrayDataUsers = []
def regUserBD(message):
    if message.text !=".":
        arrayDataUsers.append(message.text) # Добавляем новый эллемент массива
        bot.send_message(message.from_user.id, "Готово! Следующий участник. В конце списка отправьте точку");
        bot.register_next_step_handler(message, regUserBD); #следующий шаг 
    else:
        computedString = "Ваш список готов!"
        for i in range(len(arrayDataUsers)):
            computedString += "\n" + str(i + 1) + ") " + str(arrayDataUsers[i]);
        bot.send_message(message.from_user.id, computedString);
        bot.send_message(message.from_user.id, "Какая у вас цель?");
        bot.register_next_step_handler(message, getTargetString); #следующий шаг

global arrayTarget;# Цель и сумма
arrayTarget = [];
arrayTarget.append("");

def getTargetString(message):
    arrayTarget[0] = message.text;
    computedString = str(arrayTarget[0]);
    for i in range(len(arrayDataUsers)):
        computedString += "\n" + str(i + 1) + ") " + str(arrayDataUsers[i]);
    bot.send_message(message.from_user.id, computedString);
    bot.send_message(message.from_user.id, "Участник №1 внес:");
    bot.register_next_step_handler(message, getDataMoney); #следующий шаг

    
global arrayDataMoney;# Массив внесенных денег
arrayDataMoney = [];
# Функция добавления денег
def getDataMoney(message):
    if len(arrayDataMoney) != (len(arrayDataUsers) - 1) :
        arrayDataMoney.append(message.text)
        bot.send_message(message.from_user.id, "Участник №"+str(len(arrayDataMoney) + 1)+" внес:");
        bot.register_next_step_handler(message, getDataMoney); #следующий шаг
    else:
        arrayDataMoney.append(message.text)
        bot.send_message(message.from_user.id, "Расчет:");
        getCalcFinans(message) #следующий шаг
        

# Котрольная функция расчета долгов
def getCalcFinans(message):
    # Массив внесенных денег arrayDataMoney
    # Массив имен уродов arrayDataUsers

    summ = 0; #Сумма 
    for i in range(len(arrayDataMoney)):
        summ += int(arrayDataMoney[i])

    proc = round(summ / 100, 1); # Процент

    arrayProcData = []; # Массив индивидуальных процентов
    for a in range(len(arrayDataMoney)):
        arrayProcData.append(float(arrayDataMoney[a]) / proc)

    idealProc = round(100 / len(arrayDataUsers), 2) # Идеальный процент

    arrayDataFinans = [];# Массив финальных долгов
    for y in range(len(arrayProcData)):
        arrayDataFinans.append(round(arrayProcData[y] - idealProc, 2))
    print(arrayDataFinans)

                                    # Собираем финальную строку
    stringFinal = "Контрольные значения"
    for o in range(len(arrayDataFinans)):
        countFinal = round(arrayDataFinans[o] * proc, 1);
        if countFinal > 0:
            countFinal = "ему вернут " + str(abs(round(countFinal)))
        else:
            countFinal = "он должен вернуть " + str(abs(round(countFinal)))
            
        stringFinal += "\n" + str(o + 1) + ") " + str(arrayDataUsers[o]) + " : " + str(arrayDataFinans[o]) + "% = " + countFinal;
    bot.send_message(message.from_user.id, str(stringFinal));
    
    time.sleep(3)
    bot.send_message(message.from_user.id, "Ну как там с деньгами?");
       
    
bot.infinity_polling()
