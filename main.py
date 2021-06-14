
import telebot
import requests
import speech_recognition as sr
from pydub import AudioSegment

token = 'Тут токен'

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
    if "привет" in r.recognize_google(audio, language="ru").lower().split():
      bot.send_message(message.from_user.id, "И Вам привет! =)")
    if "дела" in r.recognize_google(audio, language="ru").lower().split():
      bot.send_message(message.from_user.id, "Дела отлично, вот Ваш голос распознаю.")
  except sr.UnknownValueError:
      print("Его голос не удалось распознать.")
      bot.send_message(message.from_user.id, "Не удалось распознать голос. Повторите попытку.")
  except sr.RequestError as e:
      print("Произошла ошибка.")
      bot.send_message(message.from_user.id, "Произошла ошибка. Попробуйте еще раз.")
 
bot.polling()
