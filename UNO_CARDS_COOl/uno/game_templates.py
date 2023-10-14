import random

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.utils import timezone

from .models import Student, Game, winner, Lobby

cards = ['1g','2g','3g','4g','5g','6g','7g','8g','9g','0g',
         '1y','2y','3y','4y','5y','6y','7y','8y','9y','0y',
         '1r','2r','3r','4r','5r','6r','7r','8r','9r','0r',
         '1b','2b','3b','4b','5b','6b','7b','8b','9b','0b',

         'sg', '+g', 'rg',
         'sy', '+y', 'ry',
         'sr', '+r', 'rr',
         'sb', '+b', 'rb',

         'un', '+4'
         'un', '+4'
         ]

def leavelobby(student_id, lobby):
    if lobby.Player_Count == "1":
        lobby.delete()
    else:
        if lobby.Player_Count == "2":
            lobby.player1 = lobby.player2
        elif lobby.Player_Count == "3":
            lobby.player1 = lobby.player3
        elif lobby.Player_Count == "4":
            lobby.player1 = lobby.player4

        lobby.Player_Count = str(int(lobby.Player_Count) - 1)
        lobby.save()

def now_query(lobby):
    if lobby.Query_Count == "1":
        lobby.Query_Count = "0"
        saveret = lobby.query1
        lobby.query1 = "None"
        lobby.save()
        return saveret
    if lobby.Query_Count == "2":
        lobby.Query_Count = "1"
        saveret = lobby.query2
        lobby.query2 = "None"
        lobby.save()
        return saveret
    if lobby.Query_Count == "3":
        lobby.Query_Count = "2"
        saveret = lobby.query3
        lobby.query3 = "None"
        lobby.save()
        return saveret

def joinlobby(student_id, lobby):
    if lobby.Player_Count != "4":
        if lobby.Player_Count == "1":
            lobby.player2 = student_id
        elif lobby.Player_Count == "2":
            lobby.player3 = student_id
        elif lobby.Player_Count == "3":
            lobby.player4 = student_id

        student = Student.objects.get(id = student_id)
        student.lobby_id = lobby.id
        student.save()

        lobby.Player_Count = str(int(lobby.Player_Count) + 1)
        lobby.save()


def lobbyList(student_id):
    lobby = Lobby.objects.get(id=Student.objects.get(id = student_id).lobby_id)
    lst = [Student.objects.get(id=lobby.player1)]
    if int(lobby.Player_Count) > 1:
        lst.append(Student.objects.get(id=lobby.player2))
    if int(lobby.Player_Count) > 2:
        lst.append(Student.objects.get(id=lobby.player3))
    if int(lobby.Player_Count) > 3:
        lst.append(Student.objects.get(id=lobby.player4))
    return lst

def lobbyUserList(student_id):
    students_lst = lobbyList(student_id)
    user_lst = []
    for i in students_lst:
        user_lst.append(User.objects.get(password = i.id))
    return user_lst


def strtolist(s: str):
    d = []
    for i in range(len(s)//2):
        d.append(s[i*2] + s[i*2 + 1])
    return sorted(d)


def listtostrwithwhitespaces(l):
    s = ""
    for i in l:
        s += ' ' + str(i)
    return s


def GenerateRandom4Cards():
    s = ''
    for i in range(4):
        s += cards[random.randint(0, len(cards) - 1)]

    return s


def GenerateRandom2Cards():
    s = ''
    for i in range(2):
        s += cards[random.randint(0, len(cards) - 1)]

    return s



def GenerateRandomCards(student):
    s = ''
    for i in range(7):
        s += cards[random.randint(0, len(cards) - 1)]

    student.card_list = s
    student.save()

def listtostr(l):
    s = ""
    for i in l:
        s += str(i)
    return s


def CanPlay(card, card_on_table):
    if card == "": return False
    if card == "un" or card == "+4":
        return True
    if card[1] == card_on_table[1] or card[0] == card_on_table[0]:
        return True
    return False



def dospes(el, game):
    id = (int(game.how_can_play) + game.is_reverse + int(game.Player_Count))%int(game.Player_Count)

    if el[0] == '+':
        if el[1] != '4':
            if id == 0:
                game.card_list1 += GenerateRandom2Cards()
            elif id == 1:
                game.card_list2 += GenerateRandom2Cards()
            elif id == 2:
                game.card_list3 += GenerateRandom2Cards()
            elif id == 3:
                game.card_list4 += GenerateRandom2Cards()
        else:
            if id == 0:
                game.card_list1 += GenerateRandom4Cards()
            elif id == 1:
                game.card_list2 += GenerateRandom4Cards()
            elif id == 2:
                game.card_list3 += GenerateRandom4Cards()
            elif id == 3:
                game.card_list4 += GenerateRandom4Cards()

    if el[0] == 's' or el[0] == '+':
        game.how_can_play = str(
            (int(game.how_can_play) + game.is_reverse + int(game.Player_Count)) % int(game.Player_Count))

    if el[0] == 'r':
        if game.is_reverse == 1:
            game.is_reverse = -1
        else:
            game.is_reverse = 1
    game.save()


def get_random_char():
    lst = ['g', 'r', 'b', 'y']
    return lst[random.randint(0, len(lst) - 1)]


def CanPut(game):
    while True:
        if len(game.card_list1) == 0 or len(game.card_list2) == 0 or \
                (int(game.Player_Count) > 2 and len(game.card_list3) == 0) or \
                (int(game.Player_Count) > 3 and len(game.card_list4) == 0):
            win = winner.objects.all().first()
            if len(game.card_list1) == 0 and Student.objects.filter(id = game.player1).exists():
                win.name = Student.objects.get(id = game.player1).name
            elif len(game.card_list2) == 0 and Student.objects.filter(id = game.player2).exists():
                win.name = Student.objects.get(id = game.player2).name
            elif len(game.card_list3) == 0 and Student.objects.filter(id = game.player3).exists():
                win.name = Student.objects.get(id = game.player3).name
            elif len(game.card_list4) == 0 and Student.objects.filter(id = game.player4).exists():
                win.name = Student.objects.get(id = game.player4).name

            win.save()

            while len(User.objects.all()):
                try:
                    u = User.objects.all().first()
                    student = Student.objects.get(id=int(u.password))
                    student.delete()
                    u.delete()
                except:
                    print("DELET USER ERROR")
            game.delete()
            break
        game.how_can_play = str((int(game.how_can_play) + game.is_reverse + int(game.Player_Count))%int(game.Player_Count))


        card_can_play = ['no']

        if game.how_can_play == "0":
            for i in strtolist(game.card_list1):
                if CanPlay(i, game.card_ontable):
                    card_can_play.append(i)
            if Student.objects.filter(id = game.player1).exists():
                game.card_can_play1 = listtostr(card_can_play)
                student = Student.objects.get(id = game.player1)
                student.card_can_play = game.card_can_play1
                student.flag = False
                student.save()
                game.save()
                break
            else:
                el = card_can_play[random.randint(0, len(card_can_play) - 1)]
                if el == 'no':
                    game.card_list1 += cards[random.randint(0, len(cards) - 1)]
                else:
                    lst = strtolist(game.card_list1)
                    lst.remove(el)
                    game.card_list1 = listtostr(lst)
                    dospes(el, game)
                    if el == "un" or el == "+4":
                        el = el[0] + get_random_char()



                    game.card_ontable = el
                game.save()
        elif game.how_can_play == "1":
            for i in strtolist(game.card_list2):
                if CanPlay(i, game.card_ontable):
                    card_can_play.append(i)
            if Student.objects.filter(id = game.player2).exists():
                game.card_can_play2 = listtostr(card_can_play)
                student = Student.objects.get(id = game.player2)
                student.card_can_play = game.card_can_play2
                student.flag = False
                student.save()
                game.save()
                break
            else:
                el = card_can_play[random.randint(0, len(card_can_play) - 1)]
                if el == 'no':
                    game.card_list2 += cards[random.randint(0, len(cards) - 1)]
                else:
                    lst = strtolist(game.card_list2)
                    lst.remove(el)
                    game.card_list2 = listtostr(lst)
                    dospes(el, game)
                    if el == "un" or el == "+4":
                        el = el[0] + get_random_char()

                    game.card_ontable = el
                game.save()
        elif game.how_can_play == "2":
            for i in strtolist(game.card_list3):
                if CanPlay(i, game.card_ontable):
                    card_can_play.append(i)
            if Student.objects.filter(id = game.player3).exists():
                game.card_can_play3 = listtostr(card_can_play)
                student = Student.objects.get(id = game.player3)
                student.card_can_play = game.card_can_play3
                student.flag = False
                student.save()
                game.save()
                break
            else:
                el = card_can_play[random.randint(0, len(card_can_play) - 1)]
                if el == 'no':
                    game.card_list3 += cards[random.randint(0, len(cards) - 1)]
                else:
                    lst = strtolist(game.card_list3)
                    lst.remove(el)
                    game.card_list3 = listtostr(lst)
                    dospes(el, game)
                    if el == "un" or el == "+4":
                        el = el[0] +  get_random_char()

                    game.card_ontable = el
                game.save()
        elif game.how_can_play == "3":
            for i in strtolist(game.card_list4):
                if CanPlay(i, game.card_ontable):
                    card_can_play.append(i)
            if Student.objects.filter(id = game.player4).exists():
                game.card_can_play4 = listtostr(card_can_play)
                student = Student.objects.get(id = game.player4)
                student.card_can_play = game.card_can_play4
                student.flag = False
                student.save()
                game.save()
                break
            else:
                el = card_can_play[random.randint(0, len(card_can_play) - 1)]
                if el == 'no':
                    game.card_list4 += cards[random.randint(0, len(cards) - 1)]
                else:
                    lst = strtolist(game.card_list4)
                    lst.remove(el)
                    game.card_list4 = listtostr(lst)
                    dospes(el, game)
                    if el == "un" or el == "+4":
                        el = el[0] +  get_random_char()

                    game.card_ontable = el
                game.save()



def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


def CreateGame(Players):

    game = Game()
    game.save()
    game.Player_Count = len(Players)
    game.how_can_play = "0"
    game.card_ontable = "0g"

    game.player1 = Student.objects.get(name = Players[0]).id
    GenerateRandomCards(Student.objects.get(name = Players[0]))
    game.card_list1 = Student.objects.get(name = Players[0]).card_list
    student = Student.objects.get(name = Players[0])
    student.game_index = str(game.id)
    student.game_id = "0"
    student.save()

    game.player2 = Student.objects.get(name = Players[1]).id
    GenerateRandomCards(Student.objects.get(name=Players[1]))
    game.card_list2 = Student.objects.get(name=Players[1]).card_list
    student = Student.objects.get(name=Players[1])
    student.game_index = str(game.id)
    student.game_id = "1"
    student.save()
    if len(Players) > 2:
        game.player3 = Student.objects.get(name=Players[2]).id
        GenerateRandomCards(Student.objects.get(name=Players[2]))
        game.card_list3 = Student.objects.get(name=Players[2]).card_list
        student = Student.objects.get(name=Players[2])
        student.game_index = str(game.id)
        student.game_id = "2"
        student.save()
    if len(Players) > 3:
        game.player4 = Student.objects.get(name=Players[3]).id
        GenerateRandomCards(Student.objects.get(name=Players[3]))
        game.card_list4 = Student.objects.get(name=Players[3]).card_list
        student = Student.objects.get(name=Players[3])
        student.game_index = str(game.id)
        student.game_id = "3"
        student.save()
    game.save()

    Lobby.objects.filter(id = student.lobby_id).delete()

    CanPut(game)

def TeamList(l):
    l1 = []
    for i in l:
        l1.append(Student.objects.get(id=int(i.password)).is_ready)
    return dict(zip(l, l1))


def get_all_logged_in_users_request(request):

    if Student.objects.get(id = request.user.password).game_index != "None" and \
            Game.objects.filter(id = Student.objects.get(id = request.user.password).game_index).exists():
        return HttpResponse("готовтесь (если долго нет ответа, то f5)")


    s = ""
    all_users = lobbyUserList(request.user.password)
    lst = list(all_users)
    d = TeamList(all_users)
    lets_start = True
    margin = " style = 'margin-top: 30px; padding-top: 6px; padding-bottom: 10px;' "
    for i in d:
        if d[i]:
            s += "<p class = 'is__ready' " + margin + ">" + str(i) + "</p>"
        else:
            lets_start = False
            s += "<p " + margin + ">" + str(i) + "</p>" # not ready

    if lets_start and len(d) > 1:
        CreateGame(lst)
    return HttpResponse(s)


def object_exists(model, **kwargs):
    try:
        model.objects.get(**kwargs)
        return True
    except model.DoesNotExist:
        return False

def Hello_World(request):
    return HttpResponse('Hello World!')

def ChangePlayerReady(request):
    student = Student.objects.get(id=int(request.user.password))

    student.is_ready = not student.is_ready
    student.save()
    return HttpResponse("Done ;)")