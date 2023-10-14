from django.db import models

class Card(models.Model):
    card_list = models.CharField('Рука', max_length=100)
    card_can_play = models.CharField('Активные', max_length=100)
    user = models.CharField('user', max_length=20)

    def __str__(self):
        return self.card_list

class Game(models.Model):
    Player_Count = models.CharField('количество игроков', max_length =20)
    is_reverse = models.IntegerField(max_length=10, default=1)
    how_can_play = models.CharField('ход', max_length=10)
    card_ontable = models.CharField('карта', max_length=10)

    player1 = models.CharField('айди игрока 1', max_length =20)
    card_list1 = models.CharField('Рука', max_length=100)
    card_can_play1 = models.CharField('Активные', max_length=100)

    player2 = models.CharField('айди игрока 2', max_length =20)
    card_list2 = models.CharField('Рука', max_length=100)
    card_can_play2 = models.CharField('Активные', max_length=100)

    player3 = models.CharField('айди игрока 3', max_length =20)
    card_list3 = models.CharField('Рука', max_length=100)
    card_can_play3 = models.CharField('Активные', max_length=100)

    player4 = models.CharField('айди игрока 4', max_length =20)
    card_list4 = models.CharField('Рука', max_length=100)
    card_can_play4 = models.CharField('Активные', max_length=100)

class Student(models.Model):
    is_ready = models.BooleanField('готов', max_length=10, default=False)
    name = models.CharField('Имя', max_length=100)
    flag = models.BooleanField('Флаг', max_length=10, default = False)

    card_list = models.CharField('Рука', max_length=100)
    card_can_play = models.CharField('Активные', max_length=100)
    need_card = models.CharField('Нужно ли положить карту', max_length=100, default="")

    game_id = models.CharField('номер человека в игре', max_length=20)
    game_index = models.CharField('номер игры', max_length=20, default="None")
    lobby_id = models.CharField('номер лобби', max_length=20, default= "None")

class winner(models.Model):
    name = models.CharField('Победитель', max_length = 10, default = '')


class Lobby(models.Model):
    Player_Count = models.CharField('количество игроков', max_length=20, default = "1")
    Query_Count = models.CharField('количество запросов', max_length=20, default = "0")
    name = models.CharField('Имя', max_length=100)

    player1 = models.CharField('айди игрока 1', max_length =20)
    player2 = models.CharField('айди игрока 2', max_length =20)
    player3 = models.CharField('айди игрока 3', max_length =20)
    player4 = models.CharField('айди игрока 4', max_length =20)

    query1 = models.CharField('айди игрока на запрос 1', max_length=20, default="None")
    query2 = models.CharField('айди игрока на запрос 1', max_length=20, default="None")
    query3 = models.CharField('айди игрока на запрос 1', max_length=20, default="None")