import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random  # Импортируем random для перемешивания вопросов

from questionRead import *

chat_id = None
token = "7094821440:AAEwNyNq44FNTDztbsMOqJF8GR_D3MXGM9w"
bot = telebot.TeleBot(token)

# Инициализация переменных
current_question_index = {}  # индекс текущего вопроса для каждого пользователя
user_scores = {}  # счета пользователей
user_questions = {}  # вопросы для каждого пользователя

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_bot(message):
    global chat_id
    chat_id = message.chat.id
    but2 = InlineKeyboardButton('Квиз', callback_data='but2')

    inlinemarkup = InlineKeyboardMarkup()
    inlinemarkup.add( but2)

    bot.send_message(chat_id, 'Добро пожаловать в автоматизированную систему автопоезда «Россия – моя история»', reply_markup=types.ReplyKeyboardRemove())
    time.sleep(2)
    bot.send_message(chat_id, 'Выберите необходимую функцию: ', reply_markup=inlinemarkup)

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'but2':
        start_quiz(call.message.chat.id)
'''     helpb1 = types.ReplyKeyboardMarkup("Установить голосовой помощник")
        markup.row(helpb1)
        bot.send_message(call.message.chat.id, "Выберите то, что вас интересует", reply_markup=markup)'''



'''def mes_vo(message):
    if message.text == "Установить голосовой помощник":
        bot.send_message(message.chat.id, "https://cloud.mail.ru/public/YfV7/Q52xQ92Ce", reply_markup=types.ReplyKeyboardRemove())
        time.delay(2)
        bot.register_next_step_handler(message,start_bot)'''


def start_quiz(chat_id):
    current_question_index[chat_id] = 0  # Сброс индекса вопросов
    user_scores[chat_id] = 0  # Сброс счета
    user_questions[chat_id] = questions[:]  # Сохраняем вопросы для пользователя
    random.shuffle(user_questions[chat_id])  # Перемешиваем список вопросов
    ask_question(chat_id)

def ask_question(chat_id):
    question_index = current_question_index.get(chat_id, 0)

    if question_index < len(user_questions[chat_id]):  # Используем перемешанный список вопросов
        ques = user_questions[chat_id][question_index]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for option in ques["options"]:
            markup.add(option)

        bot.send_message(chat_id, ques["question"], reply_markup=markup)
    else:
        # Окончание викторины - убираем клавиатуру
        bot.send_message(chat_id, f"Спасибо за прохождение викторины❤️. Ваш счет: {user_scores.get(chat_id, 0)}/15",
                         reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.chat.id in user_scores)
def handle_answer(message):
    chat_id = message.chat.id
    question_index = current_question_index.get(chat_id, 0)

    if question_index < len(user_questions[chat_id]):  # Используем перемешанный список вопросов
        expected_answer = user_questions[chat_id][question_index]["correct"]

        if message.text == expected_answer:
            user_scores[chat_id] += 1
            bot.send_message(chat_id, 'Правильно!')  # Сообщение о правильном ответе
        else:
            bot.send_message(chat_id, 'Неправильно')  # Сообщение о неправильном ответе

        current_question_index[chat_id] += 1
        ask_question(chat_id)  # Вызываем следующий вопрос

@bot.message_handler(commands=['admpanel'])
def mainadminpanel(message):
    markup = types.ReplyKeyboardMarkup()
    but_addquestion = types.KeyboardButton("Добавить вопрос")
    but_delquestion = types.KeyboardButton("Удалить вопрос")
    markup.row(but_addquestion, but_delquestion)

    user_firstname = message.from_user.first_name
    bot.send_message(message.chat.id, f"Добро пожаловать, {user_firstname}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить вопрос")
def add_question(message):
    bot.send_message(message.chat.id, "Введите текст вопроса:")
    bot.register_next_step_handler(message, process_question)

def process_question(message):
    question_text = message.text
    bot.send_message(message.chat.id, "Введите варианты ответов через запятую:")
    bot.register_next_step_handler(message, process_options, question_text)

def process_options(message, question_text):
    options_input = message.text
    options = [option.strip() for option in options_input.split(',')]
    bot.send_message(message.chat.id, "Введите правильный ответ:")
    bot.register_next_step_handler(message, process_correct_answer, question_text, options)

def process_correct_answer(message, question_text, options):
    correct_answer = message.text

    new_question = {
        "question": question_text,
        "options": options,
        "correct": correct_answer
    }
    questions.append(new_question)
    bot.send_message(message.chat.id, f"Вопрос добавлен: {question_text}")

@bot.message_handler(func=lambda message: message.text == "Удалить вопрос")
def delete_question(message):
    if not questions:
        bot.send_message(message.chat.id, "Нет доступных вопросов для удаления.")
        return

    question_list = "\n".join([f"{index + 1}. {q['question']}" for index, q in enumerate(questions)])
    bot.send_message(message.chat.id, f"Выберите номер вопроса для удаления:\n{question_list}")
    bot.register_next_step_handler(message, process_delete_question)

def process_delete_question(message):
    try:
        question_index = int(message.text) - 1  # Переводим текстовое сообщение в индекс
        if 0 <= question_index < len(questions):
            removed_question = questions.pop(question_index)
            bot.send_message(message.chat.id, f"Вопрос '{removed_question['question']}' удален.")
        else:
            bot.send_message(message.chat.id, "Неверный номер вопроса.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректный номер вопроса.")




'''    # Добавление нового вопроса
    add_response = add_question("Какой цвет неба?", ["Синий", "Зеленый", "Красный"], "Синий")
    print(add_response)

    # Удаление вопроса по индексу
    remove_response = remove_question(0)  # Удаление первого вопроса
    print(remove_response)'''


bot.infinity_polling()
