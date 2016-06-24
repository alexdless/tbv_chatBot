from vklancer import api
from vklancer import utils
from time import sleep
from random import randrange, choice
import bot_modules

print("Инициализация")
sleep(10)

k = 0
bot_modules.System.sendMsgToGroup("==========\nbot: bot on\n==========")
while True:
    #try:
    k += 1
    print(k)
    sleep(6)
    bot_modules.Commands.wait_command()
    #except:
    #bot_modules.System.sendMsgToGroup("==========\nbot: bot off\n==========")
        #exit()