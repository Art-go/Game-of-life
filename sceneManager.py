from typing import Any

import pyglet


################
# Документация #
################
########################################################################################################################
# Содержание:                                                                                                          #
# Работа со сценами - строка 10                                                                                        #
# Работа с объектами - строка 25                                                                                       #
########################################################################################################################
################################################## Работа со сценами ###################################################
########################################################################################################################
#                           Для объявления менеджера sm = Manager(Окно, Фрейм(штука для GUI))                          #
########################################################################################################################
# Для создания и добавления сцены используйте                                                                          #
# sm.addScene(                                                                                                         #
#     Имя в str                                                                                                        #
#     (                                                                                                                #
#     	Объекты формата list - [тип, аргументы типа]                                                                   #
#     ),                                                                                                               #
#     Батчи сцены в Tuple                                                                                              #
# )                                                                                                                    #
########################################################################################################################
# Загрузка сцены: sm.loadScene(Имя)                                                                                    #
########################################################################################################################
################################################## Работа с объектами ##################################################
########################################################################################################################
#                                                  Все типы объектов:                                                  #
# ("Image", картинка, позиция)                                                                                         #
# ("BackgroundImage", картинка, позиция)                                                                               #
# ("Gui", элемент gui)                                                                                                 #
# ("Script", скрипт старта, аргументы скрипта, скрипт обновления, аргументы скрипта обновления, скрипт выхода,         №
# аргументы скрипта выхода)                                                                                            #
# ("Event", Название ивента, функция для него)                                                                         #
# ("DrawScript", Скрипт)                                                                                               #
########################################################################################################################
#                                                  Аргументы скрипта:                                                  #
# win - получить окно                                                                                                  #
# objects - объекты сцены                                                                                              #
# return_from_start - результат с выполнения скрипта старта                                                            #
# batches - батчи сцены                                                                                                #
########################################################################################################################


class Manager:
    def __init__(self, win: pyglet.window.Window, frame: pyglet.gui.Frame):
        self.scenes: dict[Any, Scene] = {}
        self.win = win
        self.active_scene = None
        self.frame = frame

        @win.event
        def on_draw():
            self.on_draw_func(self.win)
        
        @win.event
        def on_mouse_release(x, y, buttons, modifiers):
            self.on_mouse_release(x, y, buttons, modifiers)
            frame.on_mouse_release(x, y, buttons, modifiers)
        self.on_mouse_release = self.pass_func
        
        @win.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            frame.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self.on_mouse_drag = self.pass_func
        
        @win.event
        def on_mouse_motion(x, y, dx, dy):
            self.on_mouse_motion(x, y, dx, dy)
            frame.on_mouse_motion(x, y, dx, dy)
        self.on_mouse_motion = self.pass_func
        
        @win.event
        def on_mouse_scroll(x, y, index, direction):
            self.on_mouse_scroll(x, y, index, direction)
            frame.on_mouse_scroll(x, y, index, direction)
        self.on_mouse_scroll = self.pass_func

        @win.event
        def on_mouse_enter(x, y):
            self.on_mouse_enter(x, y)
        self.on_mouse_enter = self.pass_func
        
        @win.event
        def on_mouse_leave(x, y):
            self.on_mouse_leave(x, y)
        self.on_mouse_leave = self.pass_func
        
        @win.event
        def on_mouse_press(x, y, buttons, modifiers):
            self.on_mouse_press(x, y, buttons, modifiers)
            frame.on_mouse_press(x, y, buttons, modifiers)
        self.on_mouse_press = self.pass_func

        def update(_):
            self.scenes[self.active_scene].update(self.win)

        pyglet.clock.schedule_interval(update, 1 / 60.0)
        self.on_draw_func = None

    @staticmethod
    def pass_func(*args):
        pass

    def add_scene(self, name: str, objects: tuple, batch: list[pyglet.graphics.Batch]):
        self.scenes[name] = Scene(objects, batch)

    def load_scene(self, name: str):
        if self.active_scene is not None:
            for i in self.scenes[self.active_scene].temp_objects:
                if i[0] == "Gui":
                    self.frame.remove_widget(i[1])
                elif i[0] == "Script":
                    temp = []
                    for j in i[6]:
                        if j == "win":
                            temp.append(self.win)
                        elif j == "objects":
                            temp.append(self.scenes[self.active_scene].temp_objects)
                        elif j == "return_from_start":
                            temp.append(i[7])
                        elif j == "batches":
                            temp.append(self.scenes[self.active_scene].batches)
                    i[5](*temp)
                elif i[0] == "Event":
                    if i[1] == "on_mouse_release":
                        self.on_mouse_release = self.pass_func
                    elif i[1] == "on_mouse_drag":
                        self.on_mouse_drag = self.pass_func
                    elif i[1] == "on_mouse_motion":
                        self.on_mouse_motion = self.pass_func
                    elif i[1] == "on_mouse_scroll":
                        self.on_mouse_scroll = self.pass_func
                    elif i[1] == "on_mouse_enter":
                        self.on_mouse_enter = self.pass_func
                    elif i[1] == "on_mouse_leave":
                        self.on_mouse_leave = self.pass_func
                    elif i[1] == "on_mouse_press":
                        self.on_mouse_press = self.pass_func
        self.active_scene = name
        self.scenes[name].temp_objects = list(self.scenes[name].objects)
        scene = self.scenes[name]
        for i in scene.objects:
            if i[0] == "Gui":
                self.frame.add_widget(i[1])
            elif i[0] == "Script":
                _ = []
                for j in i[2]:
                    if j == "win":
                        _.append(self.win)
                    elif j == "objects":
                        _.append(scene.temp_objects)
                    elif j == "batches":
                        _.append(scene.batches)
                if len(i) == 7:
                    i.append(None)
                i[7] = (i[1](*_))
            elif i[0] == "Event":
                if i[1] == "on_mouse_release":
                    self.on_mouse_release = i[2]
                elif i[1] == "on_mouse_drag":
                    self.on_mouse_drag = i[2]
                elif i[1] == "on_mouse_motion":
                    self.on_mouse_motion = i[2]
                elif i[1] == "on_mouse_scroll":
                    self.on_mouse_scroll = i[2]
                elif i[1] == "on_mouse_enter":
                    self.on_mouse_enter = i[2]
                elif i[1] == "on_mouse_leave":
                    self.on_mouse_leave = i[2]
                elif i[1] == "on_mouse_press":
                    self.on_mouse_press = i[2]
        self.on_draw_func = scene.draw


class Scene:
    def __init__(self, objects: tuple, batches: list[pyglet.graphics.Batch]):
        self.objects = objects
        self.batches = batches
        self.temp_objects = list(objects)

    def draw(self, win: pyglet.window.Window):
        win.clear()
        for i in self.temp_objects:
            if i[0] == "BackgroundImage":
                i[1].blit(*i[2])
                break
        for batch in self.batches:
            batch.draw()
        for i in self.temp_objects:
            if i[0] == "Image":
                i[1].blit(*i[2])
            elif i[0] == "DrawScript":
                i[1](win)

    def update(self, win: pyglet.window.Window):
        for i in self.temp_objects:
            if i[0] == "Script":
                temp = []
                for j in i[4]:
                    if j == "win":
                        temp.append(win)
                    elif j == "objects":
                        temp.append(self.temp_objects)
                    elif j == "return_from_start":
                        temp.append(i[7])
                    elif j == "batches":
                        temp.append(self.batches)
                i[3](*temp)
