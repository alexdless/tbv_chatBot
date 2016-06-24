"""список команд;
ping, say, roll, random_user, schedule, smile, random_video, random_audio ---- для юзеров,
alert, banid ---- для админа
"""

from random import randrange, choice
from time import sleep

from vklancer import api
from vklancer import utils

access_token = utils.oauth('LOGIN', 'PASSWORD')
vk = api.API(token=access_token)
chat_id = 22 #22, 35
chat_id2 = 2000000022 #22, 35

class System:
    def sendMsgToGroup(msg, attachment=""):
        sleep(4)
        if attachment == "":
            vk.messages.send(peer_id=chat_id2, message=msg)
        elif attachment != "":
            vk.messages.send(peer_id=chat_id2, message=msg, attachment=attachment)


    def commands_array(lstmsg):
        commands = ["!ping", "!say", "!roll", "!random_user", "!schedule", "!smile", "!random_video", "!random_audio", "!alert", "!banid"]
        if commands.count(lstmsg["body"]) == 1:
            return True
        elif commands.count(lstmsg["body"]) == 0:
            return False
        else:
            return None


    def security_msg(lstmsg):
        f = open("/root/bot/admins_ids.txt", "r")
        admin = []
        for i in f.readlines():
            admin.append(int(str(i).strip()))
        f.close()
        if admin.count(lstmsg["user_id"]) == 1:
            return True
        elif admin.count(lstmsg["user_id"]) == 0:
            System.sendMsgToGroup("bot: недостаточно прав", attachment="photo229768010_398775794")
            return False
        else:
            return None


    def is_banned(lstmsg):
        f = open("/root/bot/ban_ids.txt", "r")
        ids_banned = []
        for i in f.readlines():
            ids_banned.append(int(str(i).strip()))
        f.close()
        if ids_banned.count(lstmsg["user_id"]) == 1:
            return True
        elif ids_banned.count(lstmsg["user_id"]) == 0:
            return False
        else:
            return None


    def banid(lstmsg):
        f = open("/root/bot/ban_ids.txt", "w")
        s = lstmsg["body"][7:] + "\n"
        f.write(s)
        f.close()

class Commands:
    def wait_command():
        #да, криво, но работает.
        lstmsg = Commands.last_msg()
        body = lstmsg["body"]
        if System.is_banned(lstmsg) and System.commands_array(lstmsg):
            sleep(5)
            System.sendMsgToGroup("bot: закрыты на тех. работы", attachment="photo229768010_398775794")
        elif "!ping" in body:
            Commands.ping()
        elif "!say" in body:
            Commands.say(body)
        elif "!roll" in body:
            Commands.roll(body)
        elif "!random_user" in body:
            Commands.randomUser()
        elif "!schedule" in body:
            Commands.schedule(body)
        elif "!help" in body:
            Commands.help()
        elif "!smile" in body:
            Commands.smile()
        elif "!alert" in lstmsg["body"]:
            if System.security_msg(lstmsg):
                #lstmsg для проверки id
                Commands.alert(body)
        elif "!banid" in body:
            if System.security_msg(lstmsg):
                System.banid(lstmsg)
                #lstmsg для проверки id
        elif "!random_video" in body:
            Commands.randVideo()
        elif "!random_audio" in body:
            Commands.randAudio(lstmsg)
            #lstmsg для проверки id
        elif "!getcat" in body:
            Commands.getCat()
        else:
            pass


    def last_msg():
        #дает последнее сообщение
        sleep(3) #фризы задрали, не убирать. нужный костыль
        return vk.messages.getHistory(count=1, peer_id=chat_id2)["response"]["items"][0]


    def ping():
        #аналог hello_world
        System.sendMsgToGroup("bot: хуинг! долбоеб блять!")


    def say(msg):
        #вам правда нужны коментарии к ЭТОМУ?
        tmp = "bot: " + msg[5:]
        System.sendMsgToGroup(tmp)


    def roll(lstmsg):
        #аналог ролла из доты, ничего сложного
        msg, array = lstmsg.replace("!roll ", "").split(" "), []
        try:
            array.append(int(msg[0]))
            array.append(int(msg[1]))
            if array[0] < array[1] and array[0] != array[1]:
                rnd = "bot: " + str(randrange(array[0], array[1]))
                System.sendMsgToGroup(rnd)
            else:
                System.sendMsgToGroup("bot: введите нормальный данные")
        except:
            System.sendMsgToGroup("bot: введите нормальный данные")


    def randomUser():
        #рандомный пользователь беседы, id которой берется из %___chat_id___%
        id = choice(vk.messages.getChat(chat_id=chat_id)["response"]["users"])
        sleep(5)
        array = vk.users.get(user_ids=id)["response"]
        s = "bot: " + array[0]["first_name"] + " " + array[0]["last_name"]
        sleep(3)
        System.sendMsgToGroup(s)


    def schedule(msg):
        #сделать расписание из файлов, возможность замены расписания прямо из чата
        tmp = msg[10:12]
        s = ""
        if tmp == "1":
            with open("/root/bot/schedule/1.txt") as f:
                for i in f.readlines():
                    s += i
        elif tmp == "2":
            with open("/root/bot/schedule/2.txt") as f:
                for i in f.readlines():
                    s += i
        elif tmp == "3":
            with open("/root/bot/schedule/3.txt") as f:
                for i in f.readlines():
                    s += i
        elif tmp == "4":
            with open("/root/bot/schedule/4.txt") as f:
                for i in f.readlines():
                    s += i
        elif tmp == "5":
            with open("/root/bot/schedule/5.txt") as f:
                for i in f.readlines():
                    s += i
        else:
            s = "\n1 -- 5"
        m = "bot: Расписание: \n" + s
        System.sendMsgToGroup(m)


    def smile():
        #просто смайл, было нечего делать
        System.sendMsgToGroup("bot: (╯°□°）╯︵ ┻━┻")


    def alert(msg):
        #способ сделать вопрос заметнее
        s = "==========\n\n\n%s\n\n\n==========" % (msg[7:].upper())
        System.sendMsgToGroup(s)


    def randVideo():
        #рандомное видео из паблика WebM
        local_owner_id = -99126464
        response = vk.video.get(owner_id=local_owner_id, album_id=-2)
        rnd = randrange(1, 100)
        rndid = str(response["response"]["items"][rnd]["id"])
        vk.messages.send(peer_id=chat_id2, attachment="video%i_%s" % (local_owner_id, rndid))

    def randAudio(lstmsg):
        #рандомное аудио из аудиозаписей запросившего
        response = vk.audio.get(owner_id=lstmsg["user_id"], need_user=0, count=50)
        rnd = randrange(0, 49)
        rndid = response["response"]["items"][rnd]["id"]
        owner_id = response["response"]["items"][rnd]["owner_id"]
        s = "audio%i_%i" % (owner_id, rndid)
        System.sendMsgToGroup(msg="bot:", attachment=s)


    def getCat():
        owner_id = -25789975
        album_id = "wall"
        response = vk.photos.get(owner_id=owner_id, album_id=album_id, count=100)
        rnd = randrange(100)
        msg, attachment = "bot: ", "photo%i_%i" % (owner_id, response["response"]["items"][rnd]["id"])
        System.sendMsgToGroup(msg=msg, attachment=attachment)

    def help():
        array, s = ["=====HELP=====\n",
             "1. ping - просто пинг\n",
             "2. say - скажет то, что написали после\n",
             "3. roll - напишет рандомное число в заданном диапазоне (roll 0 255)\n",
             "4. random_user - напишет рандомного юзера из беседы\n",
             "5. schedule - напишет расписание на указанный день (1 - понедельник, 2 - вторник и т.д)\n",
             "6. smile\n",
             "7. random_video\n",
             "8. random_audio\n",
             "v1.3",
             "=== Все команды начинать с восклицательного знака ==="], ""
        for i in array:
            s += i
        System.sendMsgToGroup(s)