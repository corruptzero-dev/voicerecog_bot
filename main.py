# ____________Модули___________
# pip install pytelegrambotapi - для тг бота
# pip install SpeechRecognition - для распознавания голоса
# pip install pydub - для конвертации формата ogg (голосовое сообщение) в wav для обработки SR


#____________Код_____________
import telebot
import requests
import speech_recognition as sr
from pydub import AudioSegment

token = '1638590590:AAGl7EIO8J6LHEb8Jvejz9bm09m5K9VsPA8'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['voice'])
def voice_handler(message):
  file_info = bot.get_file(message.voice.file_id)
  file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

  with open('voice.ogg','wb') as f:
    f.write(file.content)

  ogg_audio = AudioSegment.from_file("/content/voice.ogg", format="ogg")
  ogg_audio.export("voice.wav", format="wav")
  
  AUDIO_FILE = '/content/voice.wav'
  r = sr.Recognizer()
  
  with sr.AudioFile(AUDIO_FILE) as source:
      audio = r.record(source)  
  try:
    print(f'Вам написал пользователь с id {message.from_user.id}, имя: {message.from_user.first_name}')
    print("Он сказал: " + r.recognize_google(audio, language="ru"))
    bot.send_message(message.from_user.id, ("Вы сказали: " + r.recognize_google(audio, language="ru")))
  except sr.UnknownValueError:
      print("Не удалось распознать голос. Повторите попытку.")
  except sr.RequestError as e:
      print("Произошла ошибка. Попробуйте еще раз.")
 
bot.polling()
