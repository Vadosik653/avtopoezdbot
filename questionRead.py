import telebot

from telebot import types

token = "7094821440:AAEwNyNq44FNTDztbsMOqJF8GR_D3MXGM9w"
bot = telebot.TeleBot(token)


chat_id = None

current_question_index = {}
user_scores = {}

questions = [
    {#1
        "question": "Когда была основана Русь?",
        "options": ["в 862 году", "в 2023 году", "Такого не было на истории"],
        "correct": "в 862 году"
    },
    {#2
        "question": "Какой была первая правящая династия?",
        "options": ["Романовы", "Рюриковичи", "Годуновы"],
        "correct": "Рюриковичи"
    },
    {#3
        "question": "В каком году крестили Русь?",
        "options": ["988 год", "922 год", "1700 год"],
        "correct": "988 год"
    },
    {#4
        "question": "Кто возглавил руководство ополчением против польских интервентов в 1611-1612 годах? ",
        "options": ["Минин", "Пожарский", "Минин и Пожарский"],
        "correct": "Минин и Пожарский"
    },
    {#5
        "question": "В какие годы проходила Северная война?",
        "options": ["1700-1721 гг.", "1854-1855 гг.", "1941-1945 гг."],
        "correct": "1700-1721 гг."
    },
    {#6
        "question": "Каков был статус России после Северной войны?",
        "options": ["Империя", "Королевство", "Государство"],
        "correct": "Империя"
    },
    {#7
        "question": "В каком году был постороен город Севастополь?",
        "options": ["1725", "1516", "1783"],
        "correct": "1783"
    },
    {#8
        "question": "Кто был императором Франции на момент Бородинского сражения? ",
        "options": ["Пипин II", "Наполеон", "Лотарь I"],
        "correct": "Наполеон"
    },
    {#9
        "question": "В каком году было отменено крепостное право? ",
        "options": ["1700", "1861", "1917"],
        "correct": "1861"
    },
    {#10
        "question": "Когда завершилось правление династии Романовых? ",
        "options": ["В 1917", "В 1725", "В 1899"],
        "correct": "В 1917"
    },
    {#11
        "question": "В какой войне произошел инцидент, известный как атака мертвецов?",
        "options": ["В Первой Мировой", "Во Второй мировой", "Это миф"],
        "correct": "В Первой Мировой"
    },
    {#12
        "question": "В каком году было образовано СССР?",
        "options": ["В 1918", "В 1920", "В 1922"],
        "correct": "В 1922"
    },
    {#13
        "question": "Кто возглавил Октябрьскую революцию 1917 года?",
        "options": ["Иосиф Сталин", "Владимир Ленин", "Георгий Львов"],
        "correct": "Владимир Ленин"
    },
    {#14
        "question": "Какое событие произошло 22 июня 1941 года?",
        "options": ["Начало Второй Мировой войны", "Начало Первой Мировой войны", "Начало Великой Отечественной войны"],
        "correct": "Начало Великой Отечественной войны"
    },
    {#15
        "question": "Какова дата распада СССР?",
        "options": ["1990", "1991", "1993"],
        "correct": "1991"
    },
    {#16
        "question": "Кто нынешний президент России?",
        "options": ["Владимир Владимирович Путин"],
        "correct": "Владимир Владимирович Путин"
    },
]





def ask_question(chat_id, message):
    chat_id=message.chat.id
    question_index = current_question_index[chat_id]

    if question_index < len(questions):
        ques = questions[question_index]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for option in ques["options"]:
            markup.add(option)

        bot.send_message(chat_id, ques["question"], reply_markup=markup)

    else:
        bot.send_message(chat_id, f"Ваш счет: {user_scores[chat_id]}/15")
        bot.send_message(2079770501, f"Кто-то прошел викторину. Его счет: {user_scores[chat_id]}")



def add_question(question_text, options, correct_answer):
    new_question = {
        "question": question_text,
        "options": options,
        "correct": correct_answer
    }
    questions.append(new_question)
    return f"Вопрос добавлен: {question_text}"



def remove_question(question_index):
    if 0 <= question_index < len(questions):
        removed_question = questions.pop(question_index)
        return f"Вопрос удален: {removed_question['question']}"
    else:
        return "Некорректный индекс вопроса."