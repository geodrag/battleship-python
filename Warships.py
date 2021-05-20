# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 13:39:16 2018

@author: copte
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 18:42:00 2018

@author: copte
"""
#%% Блок импортов
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import random
import time
#%% Блок описания классов и функций
#0 - пустая клетка
#1 - блок корабля
#2 - поврежденный блок корабля
#3 - промах
def starting_tile(event, field):                             #Задает начальную клетку для размещения корабля.
           incr=Position(int(event.xdata), int(event.ydata)) #Если начать с выбранной клетки возможно, передает её
           if event.inaxes is ax2:                           #в метод BuildShip класса Battlefield
               return None
           else:
               available=True
               for ship in field.ships:
                   for cell in ship.Cells:
                       if incr.same(cell):
                           available=False
                   for cell in ship.neighbors:
                       if incr.same(cell):
                           available=False
           if not(available):
               print("Невозможно разместить первую секцию корабля в этой клетке. Выберите другую!")
               return False
           else:
               field.BuildShip(CellCount, incr)
               return True
           
def evaluate_winner(player1, player2): #Определение победителя
    if player1.Field.Shipcount==0:
        return 'Player2'
    if player2.Field.Shipcount==0:
        return 'Player1'
    else:
        return False
    
class BattleField:
    xsize=10
    ysize=10
    Size = 10
    Shipcount=10
    def __init__(self, ax):
        self.grid=np.zeros((10,10))
        self.ships=np.array([])
        self.ax=ax
        
    def AddShips(self): #этот метод только управляет размером выстраиваемого корабля 
        global CellCount #и контролирует успешность его размещения
        ShipRestr={4:1, 3:2, 2:3, 1:4}
        for cells, units in ShipRestr.items():
            for n in range(units):
                self.ship_created=False
                print("Выберите начальную клетку для размещения корабля из {0} палуб".format(cells))
                while not(self.ship_created):
                    CellCount=cells
                    plt.waitforbuttonpress()
        return None
    
    def AddShipsBot(self): #Здесь весь процесс размещения кораблей автоматизирован
        print("Противник размещает корабли...")
        ShipRestr={4:1, 3:2, 2:3, 1:4}
        for cells, units in ShipRestr.items():
            for n in range(units):
                self.ship_created=False
                cellcount=cells
                while not(self.ship_created):
                    top=Position(random.randint(0,9), random.randint(0,9))
                    isVertical=random.choice([True, False])
                    candidate=Ship(top, isVertical, cellcount) #Создается корабль со случайными параметрами
                    available=True #Отражает возможность размещения такого корабля
                    for cell in candidate.Cells: #Если хотя бы одна из проверок не пройдена, контролирующая
                        if any([cell.x>9, cell.x<0, cell.y>9, cell.y<0]): #переменная принимант значение 
                            available=False                               #False
                    for cell in candidate.Cells:
                        for ship in self.ships:
                            for unit in ship.Cells:
                                if cell.same(unit):
                                    available=False
                            for neighbor in ship.neighbors:
                                if cell.same(neighbor):
                                    available=False
                    for neighbor in candidate.neighbors:
                        for ship in self.ships:
                            for unit in ship.Cells:
                                if neighbor.same(unit):
                                    available=False
                    if available: #Если все проверки пройдены, помещаем корабль на поле
                        self.ships=np.append(self.ships, candidate)
                        self.ship_created=True
                        for cell in candidate.Cells:
                            self.grid[cell.x][cell.y]=1
#                            block=ptch.Rectangle((cell.x, cell.y),1,1,color='blue')
#                            self.ax.add_patch(block)
#                            plt.draw() #Этот кусок позволяет в ходе теста проверить правильность размещения кораблей
                    else: continue
        print("Корабли противника размещены и готовы к бою!")
        return None
    
    def BuildShip(self, CellCount, start): #Получaет данные из starting_tile, завершает
        start=start                         #размещение корабля. Алгоритм проверок возможности
        if not(start is False):             #размещения отличается от аналога из BuildShipsBot
            if CellCount>1:
                isVertical=bool(int(input("Как ориентировать корабль? 0-горизонтально, 1-вертикально: ")))
            else: isVertical=True
            candidate=Ship(start, isVertical, CellCount)
            available=True #Эта переменная показывает возможность размещения корабля
            for cell in candidate.Cells:
                if any([cell.x>9, cell.x<0, cell.y>9, cell.y<0]):
                    available=False
                for ship in self.ships:
                    for unit in ship.Cells:
                        if unit.same(cell):
                            available=False
                    for neighbor in ship.neighbors:
                        if neighbor.same(cell):
                            available=False
            if available:
                print("Корабль успешно размещен!")
                self.ships=np.append(self.ships, candidate)
                self.ship_created=True
                for cell in candidate.Cells:
                    self.grid[cell.x][cell.y]=1
                    block=ptch.Rectangle((cell.x, cell.y),1,1,color='blue')
                    ax1.add_patch(block)
                    plt.draw()
                return None
            else:
                print("Невозможно разместить корабль с такими параметрами. Выберите другой вариант!")
                return None
    def damage_ship(self, ship, pos): #Обработчик попаданий по своим кораблям
            bool_mask=[(i.x==pos.x and i.y==pos.y) for i in ship.Cells]
            ship.Cells=np.delete(ship.Cells, np.where(bool_mask))
            if len(ship.Cells)==0:
                self.Shipcount-= 1 #Используется для определения победителя
                print("Корабль потоплен!")
                for n in ship.neighbors: #Разметка соседних с потопленным кораблем клеток как прострелянных
                    self.grid[n.x][n.y]=3 
                    block=ptch.Rectangle((n.x, n.y), 1, 1, color='grey')
                    self.ax.add_patch(block)
                return True #Случай уничтожения корабля
            else:
                return False #Случай повреждения корабля
class Player:
    def __init__(self, Name, Field, IsBot, IsOnTurn):
        self.Name=Name
        self.IsBot=IsBot
        self.IsOnTurn=IsOnTurn
        self.Field=Field
        if IsBot:
            self.prosp_targets=[] #Будем хранить здесь будущие цели (только для shoot_bot)
    def shoot(self, event, field): #Метод стрельбы для человека, здесь field - поле противника
        if event.inaxes != field.ax:
            return None
        else:
            x=int(event.xdata) #Получаем координаты точки щелчка в системе field.grid
            y=int(event.ydata)
            if field.grid[x][y]==1: #Если попали,
                for ship in field.ships: #Смотрим, клетка какого корабля расположена по этим координатам
                    for pos in ship.Cells:
                        if pos.x==x and pos.y==y:
                            field.grid[x][y]=2 #Обозначаем клетку как поврежденную
                            block=ptch.Rectangle((x,y),1,1,color='red')
                            field.ax.add_patch(block)
                            plt.draw()
                            print("Выстрел поразил цель")
                            field.damage_ship(ship, Position(x,y)) #Передаем обработку попадания методу
                            return None                            #вражеского поля
            elif field.grid[x][y]==0:
                print("Вы промахнулись") #Если промахнулись, помечаем клетку как прострелянную и передаем ход
                field.grid[x][y]=3       #противнику
                block=ptch.Rectangle((x,y), 1,1, color = 'grey')
                field.ax.add_patch(block)
                plt.draw()
                self.IsOnTurn=False
                return None
    def shoot_bot(self, field):# - алгоритм стрельбы для компьютера, field - поле противника
        def draw_targets(): #Функция, отрисовывающая клетки, в которых алгоритм предполагает наличие корабля
                for i in self.prosp_targets:
                    block=ptch.Rectangle((i.x,i.y),1,1,color='yellow')
                    field.ax.add_patch(block)
                    plt.draw()
        def shot_succesful(field, target): #Стандартная последовательность действий в случае попадания
            for ship in field.ships:
                    for pos in ship.Cells:
                        if pos.x==target.x and pos.y==target.y:
                            field.grid[target.x][target.y]=2
                            block=ptch.Rectangle((target.x,target.y),1,1,color='red')
                            field.ax.add_patch(block)
                            plt.draw()
                            print("Выстрел врага поразил цель!")
                            result=field.damage_ship(ship, Position(target.x,target.y))
                            return result #Потопили корабль или только зацепили?
        if len(self.prosp_targets)==0: #Если еще не зацепили корабль
            target=Position(random.randint(0,9), random.randint(0,9))
            if field.grid[target.x][target.y]==1: #Если попали
                result=shot_succesful(field, target) 
                if not(result): #Если не потопили
                    self.last_good_shot=target #Запоминаем координаты послднего успешного выстрела
                    self.prosp_targets=[Position(target.x-1, target.y), #Задаем область, где точно находится
                                               Position(target.x, target.y+1), #соседний блок,
                                               Position(target.x+1, target.y), #далее отметаем невозможные варианты
                                               Position(target.x, target.y-1)]
                    self.prosp_targets=list(filter(lambda x: not(any([x.x>9, x.y>9, x.x<0, x.y<0])), self.prosp_targets))
                    self.prosp_targets=list(filter(lambda x: not(any([field.grid[x.x][x.y]==2,
                                                                field.grid[x.x][x.y]==3])), self.prosp_targets))
#                    draw_targets()
                else: #Если потопили корабль,
                    self.prosp_targets=[] #Очищаем поле целей для обстрела
            elif field.grid[target.x][target.y]==0: #Если промахнулись - как в "ручном" методе shoot
                print('Противник промахнулся!')
                field.grid[target.x][target.y]=3
                block=ptch.Rectangle((target.x,target.y), 1,1, color = 'grey')
                field.ax.add_patch(block)
                plt.draw()
                self.IsOnTurn=False
            else: #В остальных случаях компьютер стреляет по уже проверенной им клетке, поэтому позволим ему переходить
                pass
        elif len(self.prosp_targets)>0: #Если уже "зацепили" корабль одним из предыдущих выстрелов
            target=random.choice(self.prosp_targets) #Выбираем только из "перспективных" клеток
            if field.grid[target.x][target.y]==1: #Если снова попали
                result=shot_succesful(field, target)
                if result: #Если потопили
                    self.prosp_targets=[]
                    self.last_good_shot=None
                else: #Если снова только зацепили, то теперь мы занем направление "простирания" корабля
                    if self.last_good_shot.y==target.y: # "Широтное простирание"
                        self.prosp_targets=list(filter(lambda x: x.y==target.y, self.prosp_targets)) #Выбрасываем все, что не по "простиранию" корабля
                        self.prosp_targets=self.prosp_targets+[Position(target.x+1, target.y), Position(target.x-1, target.y),
                                            Position(self.last_good_shot.x+1, self.last_good_shot.y), #Добавляем по одной клетке с каждой стороны корабля
                                            Position(self.last_good_shot.x-1, self.last_good_shot.y)] #по "простиранию" вне зависимости от
                                                                                                      #взаиморасположения двух пораженных клеток
                        self.prosp_targets=list(filter(lambda x: not(any([x.x>9, x.y>9, x.x<0, x.y<0])), self.prosp_targets)) #Выбрасываем невозможные
                        self.prosp_targets=list(filter(lambda x: not(any([field.grid[x.x][x.y]==2,                            #варианты
                                                                 field.grid[x.x][x.y]==3])), self.prosp_targets))
#                        draw_targets()
                    elif self.last_good_shot.x==target.x: #То же для "долготного простирания"
                        self.prosp_targets=list(filter(lambda x: x.x==target.x, self.prosp_targets))
                        self.prosp_targets=self.prosp_targets+[Position(target.x, target.y+1), Position(target.x, target.y-1),
                                            Position(self.last_good_shot.x, self.last_good_shot.y+1),
                                            Position(self.last_good_shot.x, self.last_good_shot.y-1)]
                        
                        self.prosp_targets=list(filter(lambda x: not(any([x.x>9, x.y>9, x.x<0, x.y<0])), self.prosp_targets))
                        self.prosp_targets=list(filter(lambda x: not(any([field.grid[x.x][x.y]==2,
                                                                 field.grid[x.x][x.y]==3])), self.prosp_targets))
#                        draw_targets()
                    self.last_good_shot=target       
            elif field.grid[target.x][target.y]==0: #Если промахнулись
                print('Противник промахнулся!')
                field.grid[target.x][target.y]=3
                block=ptch.Rectangle((target.x,target.y), 1,1, color = 'grey')
                field.ax.add_patch(block)
                plt.draw()
                self.IsOnTurn=False
                
            else:
                pass
class Position:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self): #Используется только в тестовых целях
        return "({0},{1})".format(self.x,self.y)
    def same(self, another_position): #Упрощает установление идентичности двух объектов
        return (self.x==another_position.x and self.y==another_position.y)
    
class Ship:
    def __init__(self, top, isVertical, cellCount):
        self.Cells = np.array([],dtype=object)
        self.IsVertical=isVertical
        for i in range(cellCount):
            self.Cells=np.append(self.Cells,(np.array(Position(top.x, top.y+i) if isVertical else Position(top.x+i,top.y))))
        self.Get_Neighbors()
    def Get_Neighbors(self):
        top=self.Cells[0]
        self.neighbors=np.array([])
        if self.IsVertical:
            self.neighbors=np.append(self.neighbors,
                                     np.array([Position(top.x-1,top.y-1),Position(top.x,top.y-1), Position(top.x+1,top.y-1),
                                           Position(self.Cells[-1].x-1,self.Cells[-1].y+1),# 6 клеток, прилежащих к крайним
                                           Position(self.Cells[-1].x,self.Cells[-1].y+1), #блокам корабля
                                           Position(self.Cells[-1].x+1,self.Cells[-1].y+1)]))
    
            for i in range(len(self.Cells)):
                    self.neighbors=np.append(self.neighbors, np.array([Position(self.Cells[i].x-1,self.Cells[i].y)]))
                    self.neighbors=np.append(self.neighbors, np.array([Position(self.Cells[i].x+1,self.Cells[i].y)]))
        else:
                self.neighbors=np.append(self.neighbors,
                                     np.array([Position(top.x-1,top.y-1),Position(top.x-1,top.y), Position(top.x-1,top.y+1),
                                           Position(self.Cells[-1].x+1,self.Cells[-1].y-1),
                                           Position(self.Cells[-1].x+1,self.Cells[-1].y),
                                           Position(self.Cells[-1].x+1,self.Cells[-1].y+1)]))
                for i in range(len(self.Cells)):
                     self.neighbors=np.append(self.neighbors, np.array([Position(self.Cells[i].x,self.Cells[i].y+1)]))
                     self.neighbors=np.append(self.neighbors, np.array([Position(self.Cells[i].x,self.Cells[i].y-1)]))
        bool_mask=[any([i.x>9, i.x<0, i.y>9, i.y<0]) for i in self.neighbors]
        self.neighbors=np.delete(self.neighbors, np.where(bool_mask))
#%% Блок игрового процесса
myname=input("Введите Ваше имя: ")
print("Приветствуем, {0}!".format(myname))
fig, (ax1, ax2)=plt.subplots(nrows=1,ncols=2) #Организация поля (моря?) боевых действий
for ax in [ax1, ax2]:
    ax.set_xticks(np.arange(1,11,1))
    ax.set_yticks(np.arange(1,11,1))
    ax.set_yticklabels(['\n \n К', '\n \n И', '\n \n З','\n \n Ж','\n \n Е','\n \n Д','\n \n Г',' \n \n В','\n \n Б','\n \n А'])
    ax.grid(color='r', linestyle='-')
ax1.title.set_text("Ваше поле")
ax2.title.set_text("Поле противника")
field1=BattleField(ax1)
field2=BattleField(ax2)
token=random.choice([True, False]) #Кому достанется первый ход?
Player1=Player(myname, field1, False, token) #Инициализация игроков
Player2=Player('Компьютер', field2, True, not(token))
plt.show()
#Фаза размещения кораблей
print("Разместите Ваши корабли:")
cid=fig.canvas.mpl_connect("button_press_event", lambda event: starting_tile(event, field1)) #Подключаем функцию для использования на конкретном поле
field1.AddShips() #Запускаем процесс размещения
#field1.AddShipsBot() # - для быстрого случайного размещения кораблей на нашем поле 
fig.canvas.mpl_disconnect(cid) #Отключаем возможность размещать корабли
field2.AddShipsBot() #Размещаем корабли противника
if Player1.IsOnTurn: #Объявляем очередность хода
    print("Вы будете ходить первым")
else:
    print("Противник будет ходить первым")
    time.sleep(0.7)
#Фаза боя
Winner=False
while Winner==False:
    if Player1.IsOnTurn:
        print("Ваш ход. Выберите цель для атаки")
        cid=fig.canvas.mpl_connect("button_press_event", lambda event: Player1.shoot(event, field2)) #Даем возможность стрелять
        plt.waitforbuttonpress() #Ждем щелчка
        if Player1.IsOnTurn==False:
            fig.canvas.mpl_disconnect(cid) #Отключаем возможность стрелять в чужой ход
            Player2.IsOnTurn=True
        Winner=evaluate_winner(Player1, Player2) #Проверяем, не победил ли игрок по итогам хода
    elif Player2.IsOnTurn:
        print("Ход противника")
        Player2.shoot_bot(Player1.Field)
        if Player2.IsOnTurn==False:
            Player1.IsOnTurn=True
        Winner=evaluate_winner(Player1, Player2)
if Winner=='Player1':
    print('Поздравляем, {0}, Вы одержали победу!'.format(Player1.Name))
else:
    print("Противник одержал победу!")
plt.draw()
fig.canvas.mpl_disconnect(cid)
time.sleep(2)
plt.close()
input()

