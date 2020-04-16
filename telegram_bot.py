import telegram

bot = telegram.Bot(token = '1018659286:AAFcAg5VqnM_miAWgijd0v3Iybu7cBmb9Vo')

#for i in bot.getUpdates():
#   print(i.message)

bot.sendMessage(chat_id=1180409106 , text="테스트")