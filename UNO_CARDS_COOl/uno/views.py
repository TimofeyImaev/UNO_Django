import random

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from json import dumps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import NameForm
from .game_templates import cards, strtolist, get_all_logged_in_users, listtostr, get_random_char, CanPut, dospes, \
    CanPlay, leavelobby, now_query, joinlobby
from .models import Card, Student, Game, winner, Lobby

from .utils import DataMixin


def PostTurn(request):
    student = Student.objects.get(id=int(request.user.password))
    if Game.objects.get(id = Student.objects.get(id = request.user.password).game_index).how_can_play == student.game_id:
        student.save()
        game = Game.objects.get(id = Student.objects.get(id = request.user.password).game_index)
        el = request.POST['hod']
        color = ""
        if len(el) == 3:
            color = el[2]
            el = el[:2]

        if student.need_card != "" and el != student.need_card:
            if el == "ge":
                if student.game_id == "0":
                    game.card_list1 += student.need_card
                elif student.game_id == "1":
                    game.card_list2 += student.need_card
                elif student.game_id == "2":
                    game.card_list3 += student.need_card
                elif student.game_id == "3":
                    game.card_list4 += student.need_card

                student.need_card = ""

                student.save()
                game.save()

                CanPut(game)
            return HttpResponse("nice")
        elif student.need_card != "":
            el = student.need_card

        if el == "no":
            student.need_card = cards[random.randint(0, len(cards) - 1)]
            if CanPlay(student.need_card, game.card_ontable):
                student.save()
                game.save()
                return HttpResponse("nice")

        if student.game_id == "0":
            if el == 'no':
                game.card_list1 += student.need_card
            else:
                lst = strtolist(game.card_list1)
                if student.need_card == "": lst.remove(el)
                game.card_list1 = listtostr(lst)
                dospes(el, game)
                if el == "un" or el == "+4":
                    el = el[0] + color

                game.card_ontable = el
            student.card_list = game.card_list1
        elif student.game_id == "1":
            if el == 'no':
                game.card_list2 += student.need_card
            else:
                lst = strtolist(game.card_list2)
                if student.need_card == "": lst.remove(el)
                game.card_list2 = listtostr(lst)
                dospes(el, game)
                if el == "un" or el == "+4":
                    el = el[0] + color

                game.card_ontable = el
            student.card_list = game.card_list2
        elif student.game_id == "2":
            if el == 'no':
                game.card_list3 += student.need_card
            else:
                lst = strtolist(game.card_list3)
                if student.need_card == "": lst.remove(el)
                game.card_list3 = listtostr(lst)
                dospes(el, game)
                if el == "un" or el == "+4":
                    el = el[0] + color

                game.card_ontable = el
            student.card_list = game.card_list3
        elif student.game_id == "3":
            if el == 'no':
                game.card_list4 += student.need_card
            else:
                lst = strtolist(game.card_list4)
                if student.need_card == "": lst.remove(el)
                game.card_list4 = listtostr(lst)
                dospes(el, game)
                if el == "un" or el == "+4":
                    el = el[0] + color

                game.card_ontable = el
            student.card_list = game.card_list4
        student.need_card = ""

        student.save()
        game.save()

        CanPut(game)
    return HttpResponse("nice")

def lobby_query(request):
    d = {}
    for i in Lobby.objects.all():
        if str(i.id) != Student.objects.get(id = request.user.password).lobby_id:
            d[i.name] = i.id

    return HttpResponse(dumps(d))

def GameStatus(request):
    if request.user.is_authenticated:
        student = Student.objects.get(id=int(request.user.password))
        if Student.objects.get(id = request.user.password).game_index != "None" and \
                Game.objects.filter(id = Student.objects.get(id = request.user.password).game_index).exists():
            form = NameForm

            right_pl = "none_pl___"
            left_pl = "none_pl___"
            front_pl = "none_pl___"

            game = Game.objects.get(id = Student.objects.get(id = request.user.password).game_index)

            if game.Player_Count == "2":
                if student.game_id == "0":
                    front_pl = Student.objects.get(id = game.player2).name
                else:
                    front_pl = Student.objects.get(id = game.player1).name
            elif game.Player_Count == "3":
                if student.game_id == "0":
                    front_pl = Student.objects.get(id=game.player3).name
                    right_pl = Student.objects.get(id=game.player2).name
                elif student.game_id == "1":
                    front_pl = Student.objects.get(id=game.player1).name
                    right_pl = Student.objects.get(id=game.player3).name
                else:
                    front_pl = Student.objects.get(id=game.player2).name
                    right_pl = Student.objects.get(id=game.player1).name
            elif game.Player_Count == "4":
                if student.game_id == "0":
                    front_pl = Student.objects.get(id=game.player3).name
                    right_pl = Student.objects.get(id=game.player2).name
                    left_pl = Student.objects.get(id=game.player4).name
                elif student.game_id == "1":
                    front_pl = Student.objects.get(id=game.player4).name
                    right_pl = Student.objects.get(id=game.player3).name
                    left_pl = Student.objects.get(id=game.player1).name
                elif student.game_id == "2":
                    front_pl = Student.objects.get(id=game.player1).name
                    right_pl = Student.objects.get(id=game.player4).name
                    left_pl = Student.objects.get(id=game.player2).name
                else:
                    front_pl = Student.objects.get(id=game.player2).name
                    right_pl = Student.objects.get(id=game.player1).name
                    left_pl = Student.objects.get(id=game.player3).name

            return render(request, 'uno/game.html', {
                'student' : strtolist(student.card_list),
                'form' : form,
                'right' : right_pl,
                'left' : left_pl,
                'front' : front_pl,
            })

        if Lobby.objects.filter(id = student.lobby_id).exists():

            lobby = Lobby.objects.get(id = student.lobby_id)

            lst = [Student.objects.get(id = lobby.player1)]
            if int(lobby.Player_Count) > 1:
                lst.append(Student.objects.get(id = lobby.player2))
            if int(lobby.Player_Count) > 2:
                lst.append(Student.objects.get(id = lobby.player3))
            if int(lobby.Player_Count) > 3:
                lst.append(Student.objects.get(id = lobby.player4))


            return render(request, 'uno/win.html',
                          {'users' : lst,
                           })
        return LogoutView(request)
    else:
        return HttpResponse("иди на <a href = " + reverse('home') + ">страницу регистрации</a>")


def index(request):
    if request.user.is_authenticated:
        return render(request, 'uno/win.html',
                      {'text' : "Поздравляю !",
                       'winner': winner.objects.all().first().name})
    else:
        return redirect('signin')


def Get_Cards(request):
    student = Student.objects.get(id = request.user.password)
    game = Game.objects.get(id = Student.objects.get(id = request.user.password).game_index)

    if student.game_id == "0":
        student.card_list = game.card_list1
    elif student.game_id == "1":
        student.card_list = game.card_list2
    elif student.game_id == "2":
        student.card_list = game.card_list3
    elif student.game_id == "3":
        student.card_list = game.card_list4

    other_player = ""
    i = (int(student.game_id) + 1)%int(game.Player_Count)
    while i != int(student.game_id):
        if i == 0:
            s1 =  str(len(game.card_list1)//2)
            if len(s1) == 1:
                s1 = "00" + s1
            else: s1 = "0" + s1
            other_player += s1
        if i == 1:
            s1 = str(len(game.card_list2) // 2)
            if len(s1) == 1:
                s1 = "10" + s1
            else:
                s1 = "0" + s1
            other_player += s1
        if i == 2 and int(game.Player_Count) > 2:
            s1 = str(len(game.card_list3) // 2)
            if len(s1) == 1:
                s1 = "20" + s1
            else:
                s1 = "0" + s1
            other_player += s1
        if i == 3 and int(game.Player_Count) > 3:
            s1 = str(len(game.card_list4) // 2)
            if len(s1) == 1:
                s1 = "30" + s1
            else:
                s1 = "0" + s1
            other_player += s1
        i = (i + 1) % int(game.Player_Count)

    other_player += "--" + game.card_ontable
    other_player += "--" + student.need_card
    other_player += "--" + str(int(str(game.is_reverse) == "1")) + '1'
    if game.how_can_play == student.game_id:

        s = ""
        for i in strtolist(student.card_can_play):
            s += i
        if len(student.need_card): s = student.need_card
        s += "--" + student.card_list
        return HttpResponse(s + "--" + str(int(game.how_can_play == student.game_id)) + other_player)

    return HttpResponse("--" + str(student.card_list) + "--" + str(int(game.how_can_play == student.game_id)) + other_player)

def join_lobby(request):
    lobby = Lobby.objects.get(id=Student.objects.get(id=request.user.password).lobby_id)

    if lobby.player1 == request.user.password:
        query = now_query(lobby)
        print(query)
        lobby1 = Lobby.objects.get(id=Student.objects.get(id=query).lobby_id)
        joinlobby(query, lobby)
        leavelobby(query, lobby1)
    return HttpResponse("ok")

def join_refuse(request):
    lobby = Lobby.objects.get(id=Student.objects.get(id=request.user.password).lobby_id)
    if lobby.player1 == request.user.password:
        query = now_query(lobby)
    return HttpResponse("ok")

def get_query(request):
    lobby = Lobby.objects.get(id=Student.objects.get(id=request.user.password).lobby_id)
    if lobby.player1 == request.user.password:
        if lobby.Query_Count == "1":
            return HttpResponse(Student.objects.get(id = lobby.query1).name)
        if lobby.Query_Count == "2":
            return HttpResponse(Student.objects.get(id = lobby.query2).name)
        if lobby.Query_Count == "3":
            return HttpResponse(Student.objects.get(id = lobby.query3).name)
    return HttpResponse("")
def join_query(request):
    lobby = Lobby.objects.get(id = request.POST['id'])
    if lobby.Query_Count != "3":
        flag = True
        if int(lobby.Query_Count) > 0:
            flag = flag and lobby.query1 != request.user.password

        if int(lobby.Query_Count) > 1:
            flag = flag and lobby.query2 != request.user.password

        flag = flag and lobby.player1 != request.user.password

        if int(lobby.Player_Count) > 1:
            flag = flag and lobby.player2 != request.user.password
        elif int(lobby.Player_Count) > 2:
            flag = flag and lobby.player3 != request.user.password
        elif int(lobby.Player_Count) > 3:
            flag = flag and lobby.player4 != request.user.password

        if flag:
            if lobby.Query_Count == "0":
                lobby.query1 = request.user.password
            if lobby.Query_Count == "1":
                lobby.query2 = request.user.password
            if lobby.Query_Count == "2":
                lobby.query3 = request.user.password
            lobby.Query_Count = str(int(lobby.Query_Count) + 1)
            lobby.save()
    return HttpResponse("ok")

def create_student(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data['name']

            student = Student.objects.create(name = student_name)
            lobby = Lobby.objects.create(player1=student.id, Player_Count="1", name = student.name)
            student.lobby_id = lobby.id

            student.save()

            user = User()
            user.username = student_name
            user.password = str(student.id)
            user.save()

            login(request, user)


            lobby.save()

            return redirect('game')


    form = NameForm
    return render(request, 'uno/index.html', {'form' : form})

def LogoutView(request):
    try:
        u = request.user
        student = Student.objects.get(id=int(u.password))
        student.delete()
        logout(request)
        u.delete()
    except:
        print("DELET USER ERROR")

    return redirect('home')


class RegisterUser(DataMixin, CreateView):
    pass

    # form_class = NameForm
    # template_name = 'uno/index.html'
    # success_url = reverse_lazy('home')
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Главная страница")
    #     return dict(list(context.items()) + list(c_def.items()))
    #
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('home')