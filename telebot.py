import telebot
from telebot import types

# Замените 'YOUR_TOKEN' на токен вашего бота
API_TOKEN = '7152286173:AAFWYwzZSyf_bDKkhugeg2lBzcXIQzBJxbY'
bot = telebot.TeleBot(API_TOKEN)

# Определяем вопросы и варианты ответов
questions = [
    {
        "question": "Какой язык программирования используется для создания ботов в Telegram?",
        "options": ["А) Python", "Б) Java", "В) C++", "Г) JavaScript"],
        "answer": "А"
    },
    {
        "question": "В каком году был создан Telegram?",
        "options": ["А) 2011", "Б) 2013", "В) 2015", "Г) 2017"],
        "answer": "Б"
    },
    {
        "question": "Какой протокол используется для передачи данных в Telegram?",
        "options": ["А) HTTP", "Б) UDP", "В) MTProto", "Г) FTP"],
        "answer": "В"
    },
    {
        "question": "Кто является основателем Telegram?",
        "options": ["А) Марк Цукерберг", "Б) Павел Дуров", "В) Илон Маск", "Г) Стив Джобс"],
        "answer": "Б"
    },
    {
        "question": "Какой тип сообщений доступен в Telegram?",
        "options": ["А) Только текстовые", "Б) Только голосовые", "В) Текстовые, аудио, видео, фото", "Г) Только фото"],
        "answer": "В"
    },
    # Добавьте остальные вопросы, если необходимо
]

user_scores = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Давай начнем тест. Напиши /test, чтобы начать.")

@bot.message_handler(commands=['test'])
def test(message):
    user_id = message.from_user.id
    user_scores[user_id] = {
        "score": 0,
        "current_question": 0
    }
    
    ask_question(message, user_id)

def ask_question(message, user_id):
    question_data = questions[user_scores[user_id]["current_question"]]
    question_text = question_data['question']
    options = question_data['options']

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in options:
        markup.add(option)
    
    bot.send_message(message.chat.id, question_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def answer(message):
    user_id = message.from_user.id
    user_answer = message.text.strip().split(')')[0]  # Получаем букву ответа

    if user_id in user_scores:
        current_question = user_scores[user_id]["current_question"]
        correct_answer = questions[current_question]["answer"]

        if user_answer == correct_answer:
            user_scores[user_id]["score"] += 1
            bot.reply_to(message, "Правильный ответ!")
        else:
            bot.reply_to(message, f"Неправильный ответ. Правильный: {correct_answer}")

        user_scores[user_id]["current_question"] += 1
        
        if user_scores[user_id]["current_question"] < len(questions):
            ask_question(message, user_id)
        else:
            final_score = user_scores[user_id]["score"]
            bot.reply_to(message, f"Тест завершен! Вы набрали {final_score} из {len(questions)} баллов.")
            del user_scores[user_id]  # Удаляем данные пользователя после завершения теста

if __name__ == "__main__":
    bot.polling(none_stop=True)