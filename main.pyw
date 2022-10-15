import datetime
import json
import os

import numpy as np
import pyglet
from PIL import Image
from pyglet.gl import *

import sceneManager

cells: np.ndarray = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    ], dtype=int
)
np.random.seed(datetime.datetime.now().microsecond)
home = os.path.expanduser("~")
try:
    with open(home + "\\AGame_of_life\\saves.gol", "r") as file:
        pass
except FileNotFoundError:
    try:
        os.mkdir(home + "\\AGame_of_life")
    except FileExistsError:
        pass
    with open(home + "\\AGame_of_life\\saves.gol", "w") as file:
        json.dump({
            1: (
                (
                    (1, ),
                ),
                (
                    (2, 3),
                    (3, )
                )
            ),
            2: (
                (
                    (1, ),
                ),
                (
                    (2, 3),
                    (3, )
                )
            ),
            3: (
                (
                    (1, ),
                ),
                (
                    (2, 3),
                    (3, )
                )
            ),
            4: (
                (
                    (1, ),
                ),
                (
                    (2, 3),
                    (3, )
                )
            ),
            5: (
                (
                    (1, ),
                ),
                (
                    (2, 3),
                    (3, )
                )
            ),
        }, file)
temp_cells = cells.copy()
win = pyglet.window.Window(fullscreen=1, caption="Game of Life")
win.set_icon(pyglet.image.load("sprites/icon.png"))
win.config.alpha_size = 8
glEnable(GL_BLEND)
frame = pyglet.gui.Frame(win)
sm = sceneManager.Manager(win, frame=frame)
gap_size = (win.width - win.height * 0.7) / 2
W_MINUS_70H = win.width - (win.height * 0.7)


def load_image(fp: str | Image.Image, size: tuple[int, int], resample=2):
    if isinstance(fp, str):
        fp = Image.open(fp)
    fp = fp.resize(size, resample=resample)
    return pyglet.image.ImageData(fp.width, fp.height, fp.mode, fp.tobytes(), pitch=-fp.width * len(fp.mode)), fp


play = load_image("sprites/play.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

pause = load_image("sprites/pause.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

checked = load_image("sprites/checked.png", (int(gap_size / 9), int(gap_size / 9)))[0]

unchecked = load_image("sprites/unchecked.png", (int(gap_size / 9), int(gap_size / 9)))[0]

start_p = load_image("sprites/start_pressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

start_d = load_image("sprites/start_depressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

saves_p = load_image("sprites/saves_pressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

saves_d = load_image("sprites/saves_depressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

exit_p = load_image("sprites/exit_pressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

exit_d = load_image("sprites/exit_depressed.png", (int(win.height * 0.18), int(win.height * 0.09)))[0]

arrow_up_p = load_image("sprites/arrow_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))
arrow_down_p = pyglet.image.ImageData(arrow_up_p[0].width, arrow_up_p[0].height, 'RGBA',
                                      arrow_up_p[1].rotate(180).tobytes(), pitch=-arrow_up_p[0].width * 4)
arrow_up_p = arrow_up_p[0]

arrow_up_d = load_image("sprites/arrow_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))
arrow_down_d = pyglet.image.ImageData(arrow_up_d[0].width, arrow_up_d[0].height, 'RGBA',
                                      arrow_up_d[1].rotate(180).tobytes(), pitch=-arrow_up_d[0].width * 4)
arrow_up_d = arrow_up_d[0]

home_p = load_image("sprites/home_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

home_d = load_image("sprites/home_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

clear_p = load_image("sprites/clear_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

clear_d = load_image("sprites/clear_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

random_p = load_image("sprites/random_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

random_d = load_image("sprites/random_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

save_p = load_image("sprites/save_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

save_d = load_image("sprites/save_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

load_p = load_image("sprites/load_pressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

load_d = load_image("sprites/load_depressed.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

speed1 = load_image("sprites/speed1.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

speed2 = load_image("sprites/speed2.png", (int(win.height * 0.09), int(win.height * 0.09)))[0]

background = Image.open("sprites/background.png").crop((0, 0, 456, (456 * win.height) // win.width))
background = load_image(background, (win.width, win.height), resample=0)[0]

background2 = Image.open("sprites/background2.png").crop((0, 0, 456, (456 * win.height) // win.width))
background2 = load_image(background2, (win.width, win.height), resample=0)[0]

mainMenuBatch = pyglet.graphics.Batch()
savesMenuBatchForeground = pyglet.graphics.Batch()
savesMenuBatchBackground = pyglet.graphics.Batch()
gameBatchBackground = pyglet.graphics.Batch()
gameBatchForeground = pyglet.graphics.Batch()
startMenuBatchBackground = pyglet.graphics.Batch()
startMenuBatchForeground = pyglet.graphics.Batch()
field_size = 20
_ = (
    pyglet.shapes.Rectangle(0, win.height * 0.85, win.width, win.height * 0.15, color=(30, 30, 30),
                            batch=gameBatchBackground),
    pyglet.text.Label("Game of Life", batch=gameBatchForeground, font_size=win.height / 20,
                      x=win.width / 2, y=win.height * 0.925, anchor_x="center", anchor_y="center"),
    # 2
    pyglet.gui.ToggleButton(win.height * 0.15, win.height * 0.88, play, pause,
                            batch=gameBatchForeground),
    pyglet.gui.PushButton(win.width * 0.06 + win.height * 0.09, win.height * 0.45, clear_p, clear_d,
                          batch=startMenuBatchForeground),
    pyglet.text.Label("Game of Life - Main Menu", batch=mainMenuBatch, font_size=win.height / 20,
                      x=win.width / 2, y=win.height * 0.925, anchor_x="center", anchor_y="center"),
    # 5
    pyglet.gui.PushButton(win.width * 0.05, win.height * 0.4, start_p, start_d, batch=mainMenuBatch),
    pyglet.gui.PushButton(win.height * 0.03, win.height * 0.88, home_p, home_d, batch=gameBatchForeground),
    pyglet.gui.PushButton(win.width * 0.05, win.height * 0.25, exit_p, exit_d, batch=mainMenuBatch),
    pyglet.shapes.Rectangle(0, win.height * 0.85, win.width, win.height * 0.15, color=(30, 30, 30),
                            batch=startMenuBatchBackground),
    pyglet.text.Label("Game of Life - Start Menu", batch=startMenuBatchForeground, font_size=win.height / 20,
                      x=win.width / 2, y=win.height * 0.925, anchor_x="center", anchor_y="center"),
    # 10
    pyglet.gui.PushButton(win.height * 0.03, win.height * 0.88, home_p, home_d, batch=startMenuBatchForeground),
    pyglet.gui.PushButton((win.width - start_p.width) / 2, win.height * 0.05, start_p, start_d,
                          batch=startMenuBatchForeground),
    pyglet.gui.PushButton(win.width * 0.03, win.height * 0.64, arrow_up_p, arrow_up_d, batch=startMenuBatchForeground),
    pyglet.gui.PushButton(win.width * 0.03, win.height * 0.42, arrow_down_p, arrow_down_d,
                          batch=startMenuBatchForeground),
    pyglet.shapes.BorderedRectangle(win.width * 0.03, win.height * 0.53, win.height * 0.09, win.height * 0.09,
                                    batch=startMenuBatchBackground, color=(43, 43, 43), border_color=(217, 217, 217),
                                    border=5),
    pyglet.text.Label("20", x=win.width * 0.03 + win.height * 0.045, y=win.height * 0.575,
                      batch=startMenuBatchForeground,
                      anchor_x="center", anchor_y="center", font_size=win.height / 20),
    # 16
    pyglet.gui.PushButton(win.width * 0.06 + win.height * 0.09, win.height * 0.6, random_p, random_d,
                          batch=startMenuBatchForeground),
    (pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35, win.height * 0.6, checked, unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9, win.height * 0.6, checked, unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 2, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 3, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 4, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 5, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 6, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 7, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 8, win.height * 0.6, checked,
                             unchecked,
                             batch=startMenuBatchForeground)),
    (pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35, win.height * 0.6 - gap_size / 9, checked, unchecked,
                             batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 2, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 3, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 4, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 5, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 6, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 7, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground),
     pyglet.gui.ToggleButton(win.width * 0.5 + win.height * 0.35 + gap_size / 9 * 8, win.height * 0.6 - gap_size / 9,
                             checked, unchecked, batch=startMenuBatchForeground)),
    pyglet.text.Label("Правила мира.\nПервый ряд - условия жизни\nВторой ряд - условия рождения", multiline=True,
                      width=gap_size, align="center", batch=startMenuBatchForeground, anchor_x="center",
                      anchor_y="center", x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 9,
                      y=win.height * 0.6 + gap_size / 18 * 6,
                      font_size=win.width * 0.01),
    (pyglet.text.Label("0", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("1", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 3,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("2", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 5,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("3", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 7,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("4", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 9,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("5", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 11,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("6", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 13,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("7", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 15,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center"),
     pyglet.text.Label("8", y=win.height * 0.6 + gap_size / 18 * 3, font_size=win.width * 0.025,
                       x=win.width * 0.5 + win.height * 0.35 + gap_size / 18 * 17,
                       batch=startMenuBatchForeground, anchor_y="center", anchor_x="center")),
    # 21
    pyglet.text.Label("Game of Life - Saves Menu", batch=savesMenuBatchForeground, font_size=win.height / 20,
                      x=win.width / 2, y=win.height * 0.925, anchor_x="center", anchor_y="center"),
    pyglet.gui.PushButton(win.width * 0.05, win.height * 0.15, saves_p, saves_d, batch=startMenuBatchForeground),
    pyglet.gui.PushButton(win.height * 0.03, win.height * 0.88, home_p, home_d, batch=savesMenuBatchForeground),
    (pyglet.shapes.Rectangle(win.width * 0.15, win.height * 0.70, win.width * 0.7, win.height * 0.10,
                             color=(100, 100, 100),
                             batch=savesMenuBatchBackground),
     pyglet.shapes.Rectangle(win.width * 0.15, win.height * 0.55, win.width * 0.7, win.height * 0.10,
                             color=(100, 100, 100),
                             batch=savesMenuBatchBackground),
     pyglet.shapes.Rectangle(win.width * 0.15, win.height * 0.40, win.width * 0.7, win.height * 0.10,
                             color=(100, 100, 100),
                             batch=savesMenuBatchBackground),
     pyglet.shapes.Rectangle(win.width * 0.15, win.height * 0.25, win.width * 0.7, win.height * 0.10,
                             color=(100, 100, 100),
                             batch=savesMenuBatchBackground),
     pyglet.shapes.Rectangle(win.width * 0.15, win.height * 0.10, win.width * 0.7, win.height * 0.10,
                             color=(100, 100, 100),
                             batch=savesMenuBatchBackground),
     pyglet.text.Label("Save 1", batch=savesMenuBatchBackground, font_size=win.height / 40, x=win.width * 0.175,
                       y=win.height * 0.75,
                       anchor_y="center"),
     pyglet.text.Label("Save 2", batch=savesMenuBatchBackground, font_size=win.height / 40, x=win.width * 0.175,
                       y=win.height * 0.60,
                       anchor_y="center"),
     pyglet.text.Label("Save 3", batch=savesMenuBatchBackground, font_size=win.height / 40, x=win.width * 0.175,
                       y=win.height * 0.45,
                       anchor_y="center"),
     pyglet.text.Label("Save 4", batch=savesMenuBatchBackground, font_size=win.height / 40, x=win.width * 0.175,
                       y=win.height * 0.30,
                       anchor_y="center"),
     pyglet.text.Label("Save 5", batch=savesMenuBatchBackground, font_size=win.height / 40, x=win.width * 0.175,
                       y=win.height * 0.15,
                       anchor_y="center")),
    (pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.095, win.height * 0.705, save_p, save_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.095, win.height * 0.555, save_p, save_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.095, win.height * 0.405, save_p, save_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.095, win.height * 0.255, save_p, save_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.095, win.height * 0.105, save_p, save_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.195, win.height * 0.705, load_p, load_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.195, win.height * 0.555, load_p, load_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.195, win.height * 0.405, load_p, load_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.195, win.height * 0.255, load_p, load_d,
                           batch=savesMenuBatchForeground),
     pyglet.gui.PushButton(win.width * 0.85 - win.height * 0.195, win.height * 0.105, load_p, load_d,
                           batch=savesMenuBatchForeground),),
    pyglet.shapes.Rectangle(0, win.height * 0.85, win.width, win.height * 0.15, color=(30, 30, 30),
                            batch=savesMenuBatchBackground),
)
last_time = datetime.datetime.now()
is_playing = True
speed = 1
rects: list[list[pyglet.shapes.Rectangle]] = []
born_values = {3}
live_values = {2, 3}
for checkbox in live_values:
    _[17][checkbox].value = True
for checkbox in born_values:
    _[18][checkbox].value = True
prev_pos = (-1, -1)


def load_rules():
    for i in range(9):
        _[17][i].value = False
        _[18][i].value = False
    for i in live_values:
        _[17][i].value = True
    for i in born_values:
        _[18][i].value = True


@_[25][0].event
def on_release():
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        save = json.load(f)
    save["1"] = (cells.tolist(), (list(live_values), list(born_values)))
    with open(home+"\\AGame_of_life\\saves.gol", "w") as f:
        json.dump(save, f)
    sm.load_scene("start menu")


@_[25][1].event
def on_release():
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        save = json.load(f)
    save["2"] = (cells.tolist(), (list(live_values), list(born_values)))
    with open(home+"\\AGame_of_life\\saves.gol", "w") as f:
        json.dump(save, f)
    sm.load_scene("start menu")


@_[25][2].event
def on_release():
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        save = json.load(f)
    save["3"] = (cells.tolist(), (list(live_values), list(born_values)))
    with open(home+"\\AGame_of_life\\saves.gol", "w") as f:
        json.dump(save, f)
    sm.load_scene("start menu")


@_[25][3].event
def on_release():
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        save = json.load(f)
    save["4"] = (cells.tolist(), (list(live_values), list(born_values)))
    with open(home+"\\AGame_of_life\\saves.gol", "w") as f:
        json.dump(save, f)
    sm.load_scene("start menu")


@_[25][4].event
def on_release():
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        save = json.load(f)
    save["5"] = (cells.tolist(), (list(live_values), list(born_values)))
    with open(home+"\\AGame_of_life\\saves.gol", "w") as f:
        json.dump(save, f)
    sm.load_scene("start menu")


@_[25][5].event
def on_release():
    global cells, field_size, live_values, born_values
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        load = json.load(f)
        cells = np.array([list(map(int, i)) for i in load["1"][0]])
        live_values, born_values = [set(map(int, i)) for i in load["1"][1]]
        load_rules()
        field_size = cells.shape[0]
        _[15].text = str(field_size)
    sm.load_scene("start menu")


@_[25][6].event
def on_release():
    global cells, field_size, live_values, born_values
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        load = json.load(f)
        cells = np.array([list(map(int, i)) for i in load["2"][0]])
        live_values, born_values = [set(map(int, i)) for i in load["2"][1]]
        load_rules()
        field_size = cells.shape[0]
        _[15].text = str(field_size)
    sm.load_scene("start menu")


@_[25][7].event
def on_release():
    global cells, field_size, live_values, born_values
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        load = json.load(f)
        cells = np.array([list(map(int, i)) for i in load["3"][0]])
        live_values, born_values = [set(map(int, i)) for i in load["3"][1]]
        load_rules()
        field_size = cells.shape[0]
        _[15].text = str(field_size)
    sm.load_scene("start menu")


@_[25][8].event
def on_release():
    global cells, field_size, live_values, born_values
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        load = json.load(f)
        cells = np.array([list(map(int, i)) for i in load["4"][0]])
        live_values, born_values = [set(map(int, i)) for i in load["4"][1]]
        load_rules()
        field_size = cells.shape[0]
        _[15].text = str(field_size)
    sm.load_scene("start menu")


@_[25][9].event
def on_release():
    global cells, field_size, live_values, born_values
    with open(home+"\\AGame_of_life\\saves.gol", "r") as f:
        load = json.load(f)
        cells = np.array([list(map(int, i)) for i in load["5"][0]])
        live_values, born_values = [set(map(int, i)) for i in load["5"][1]]
        load_rules()
        field_size = cells.shape[0]
        _[15].text = str(field_size)
    sm.load_scene("start menu")


@_[17][0].event
def on_toggle(_):
    live_values.symmetric_difference_update({0})


@_[18][0].event
def on_toggle(_):
    born_values.symmetric_difference_update({0})


@_[17][1].event
def on_toggle(_):
    live_values.symmetric_difference_update({1})


@_[18][1].event
def on_toggle(_):
    born_values.symmetric_difference_update({1})


@_[17][2].event
def on_toggle(_):
    live_values.symmetric_difference_update({2})


@_[18][2].event
def on_toggle(_):
    born_values.symmetric_difference_update({2})


@_[17][3].event
def on_toggle(_):
    live_values.symmetric_difference_update({3})


@_[18][3].event
def on_toggle(_):
    born_values.symmetric_difference_update({3})


@_[17][4].event
def on_toggle(_):
    live_values.symmetric_difference_update({4})


@_[18][4].event
def on_toggle(_):
    born_values.symmetric_difference_update({4})


@_[17][5].event
def on_toggle(_):
    live_values.symmetric_difference_update({5})


@_[18][5].event
def on_toggle(_):
    born_values.symmetric_difference_update({5})


@_[17][6].event
def on_toggle(_):
    live_values.symmetric_difference_update({6})


@_[18][6].event
def on_toggle(_):
    born_values.symmetric_difference_update({6})


@_[17][7].event
def on_toggle(_):
    live_values.symmetric_difference_update({7})


@_[18][7].event
def on_toggle(_):
    born_values.symmetric_difference_update({7})


@_[17][8].event
def on_toggle(_):
    live_values.symmetric_difference_update({8})


@_[18][8].event
def on_toggle(_):
    born_values.symmetric_difference_update({8})


@_[2].event
def on_toggle(state: bool):
    global is_playing
    is_playing = not state


@_[5].event
def on_release():
    sm.load_scene("start menu")


@_[22].event
def on_release():
    sm.load_scene("saves")


@_[23].event
@_[10].event
@_[6].event
def on_release():
    sm.load_scene("main menu")


@_[11].event
def on_release():
    sm.load_scene("game")


@_[12].event
def on_release():
    global field_size, cells, temp_cells
    field_size = min(100, field_size + 1)
    _[15].text = str(field_size)
    cells = np.random.randint(0, 2, (field_size, field_size))
    temp_cells = cells.copy()
    on_cells_resize()


@_[16].event
def on_release():
    global cells, temp_cells
    cells = np.random.randint(0, 2, (field_size, field_size))
    temp_cells = cells.copy()


@_[3].event
def on_release():
    global cells, temp_cells
    cells = np.zeros((field_size, field_size))
    temp_cells = cells.copy()


@_[13].event
def on_release():
    global field_size, cells, temp_cells
    field_size = max(1, field_size - 1)
    _[15].text = str(field_size)
    cells = np.random.randint(0, 2, (field_size, field_size))
    temp_cells = cells.copy()
    on_cells_resize()


def on_cells_resize():
    global rects
    size = win.height * 0.7 / cells.shape[0]
    width_shift = W_MINUS_70H / 2
    rects = [
        [
            pyglet.shapes.Rectangle(width_shift + size * j, win.height * 0.15 + size * i, size, size,
                                    batch=startMenuBatchForeground,
                                    color=(255, 255, 255) if cells[i][j] else (0, 0, 0))
            for j in range(cells.shape[0])
        ]
        for i in range(cells.shape[0])
    ]


def start_menu_on_mouse_drag_or_press(*args):
    global prev_pos
    x, y = args[:2]
    if W_MINUS_70H / 2 < x < ((win.width + (win.height * 0.7)) / 2) and win.height * 0.15 < y < win.height * 0.85:
        size = (win.height * 0.7 / cells.shape[0])
        pos = (int((x - (W_MINUS_70H / 2)) // size), int((y - win.height * 0.15) // size))
        if prev_pos != pos:
            cells[pos[1]][pos[0]] = (cells[pos[1]][pos[0]] + 1) % 2
            temp_cells[pos[1]][pos[0]] = (temp_cells[pos[1]][pos[0]] + 1) % 2
            prev_pos = pos


def start_menu_release(*_):
    global prev_pos
    prev_pos = (-1, -1)


@_[7].event
def on_release():
    pyglet.app.exit()


def gol_on_mouse_release(x, y, _, __):
    global speed
    if win.height * 0.27 < x < win.height * 0.36 and win.height * 0.88 < y < win.height * 0.97:
        speed = speed % 2 + 1


def gol_draw(_):
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    match speed:
        case 1:
            speed1.blit(win.height * 0.27, win.height * 0.88)
        case 2:
            speed2.blit(win.height * 0.27, win.height * 0.88)


def gol_start(batches):
    global last_time
    last_time = datetime.datetime.now()
    size = win.height * 0.85 / cells.shape[0]
    width_shift = (win.width - (win.height * 0.85)) / 2
    rectangles = [
        [
            pyglet.shapes.Rectangle(width_shift + size * j, size * i, size, size, batch=batches[1],
                                    color=(255, 255, 255) if cells[i][j] else (0, 0, 0))
            for j in range(cells.shape[0])
        ]
        for i in range(cells.shape[0])
    ]
    return rectangles


def gol_update(rectangles: list[list[pyglet.shapes.Rectangle]]):
    global cells, last_time
    if datetime.datetime.now() - last_time >= datetime.timedelta(seconds=0.05 / speed) and is_playing:
        last_time = datetime.datetime.now()
        for i in range(cells.shape[0] - 1):
            for j in range(cells.shape[0] - 1):
                sum_ = cells[i - 1][j - 1] + cells[i][j - 1] + cells[i + 1][j - 1] + cells[i - 1][j] + cells[i + 1][
                    j] + cells[i - 1][j + 1] + cells[i][j + 1] + cells[i + 1][j + 1]
                if cells[i][j]:
                    if sum_ not in live_values:
                        temp_cells[i][j] = 0
                else:
                    if sum_ in born_values:
                        temp_cells[i][j] = 1
        for i in range(cells.shape[0] - 1):
            sum_ = cells[i - 1][cells.shape[0] - 2] + cells[i][cells.shape[0] - 2] + cells[i + 1][
                cells.shape[0] - 2] + cells[i - 1][cells.shape[0] - 1] + cells[i + 1][cells.shape[0] - 1] + cells[
                       i - 1][0] + cells[i][0] + cells[i + 1][0]
            if cells[i][cells.shape[0] - 1]:
                if sum_ not in live_values:
                    temp_cells[i][cells.shape[0] - 1] = 0
            else:
                if sum_ in born_values:
                    temp_cells[i][cells.shape[0] - 1] = 1
        for i in range(cells.shape[0] - 1):
            sum_ = cells[cells.shape[0] - 2][i - 1] + cells[cells.shape[0] - 2][i] + cells[cells.shape[0] - 2][
                i + 1] + cells[cells.shape[0] - 1][i - 1] + cells[cells.shape[0] - 1][i + 1] + cells[0][i - 1] + cells[
                       0][i] + cells[0][i + 1]
            if cells[cells.shape[0] - 1][i]:
                if sum_ not in live_values:
                    temp_cells[cells.shape[0] - 1][i] = 0
            else:
                if sum_ in born_values:
                    temp_cells[cells.shape[0] - 1][i] = 1
        sum_ = cells[cells.shape[0] - 2][cells.shape[0] - 2] + cells[cells.shape[0] - 2][cells.shape[0] - 1] + cells[
            cells.shape[0] - 2][0] + cells[cells.shape[0] - 1][cells.shape[0] - 2] + cells[cells.shape[0] - 1][
                   0] + cells[0][cells.shape[0] - 2] + cells[0][cells.shape[0] - 1] + cells[0][0]
        if cells[cells.shape[0] - 1][cells.shape[0] - 1]:
            if sum_ not in live_values:
                temp_cells[cells.shape[0] - 1][cells.shape[0] - 1] = 0
        else:
            if sum_ in born_values:
                temp_cells[cells.shape[0] - 1][cells.shape[0] - 1] = 1
        cells = temp_cells.copy()
    rects_update(cells, rectangles)


def start_menu_update():
    rects_update(cells, rects)


def rects_update(cells_, rects_):
    for i in range(cells_.shape[0]):
        for j in range(cells_.shape[0]):
            if cells_[i][j]:
                rects_[i][j].color = (255, 255, 255)
            else:
                rects_[i][j].color = (0, 0, 0)


def pass_func():
    pass


sm.add_scene(
    "game",
    (
        [
            "Script",
            gol_start,
            ("batches",),
            gol_update,
            ("return_from_start",),
            pass_func,
            (),
        ],
        [
            "Gui",
            _[2]
        ],
        [
            "Event",
            "on_mouse_release",
            gol_on_mouse_release,
        ],
        [
            "DrawScript",
            gol_draw
        ],
        [
            "BackgroundImage",
            background2,
            (0, 0)
        ],
        [
            "Gui",
            _[6]
        ]
    ),
    [gameBatchBackground, gameBatchForeground]
)
sm.add_scene(
    "main menu",
    (
        [
            "BackgroundImage",
            background,
            (0, 0)
        ],
        [
            "Gui",
            _[5]
        ],
        [
            "Gui",
            _[7]
        ],
    ),
    [gameBatchBackground, mainMenuBatch]
)
sm.add_scene(
    "start menu",
    (
        [
            "BackgroundImage",
            background2,
            (0, 0)
        ],
        [
            "Gui",
            _[10]
        ],
        [
            "Gui",
            _[11]
        ],
        [
            "Gui",
            _[12]
        ],
        [
            "Gui",
            _[13]
        ],
        [
            "Script",
            on_cells_resize,
            (),
            start_menu_update,
            (),
            pass_func,
            (),
        ],
        [
            "Gui",
            _[16]
        ],
        [
            "Gui",
            _[3]
        ],
        [
            "Event",
            "on_mouse_drag",
            start_menu_on_mouse_drag_or_press,
        ],
        [
            "Event",
            "on_mouse_press",
            start_menu_on_mouse_drag_or_press,
        ],
        [
            "Event",
            "on_mouse_release",
            start_menu_release,
        ],
        *[["Gui", _[17][i]] for i in range(9)],
        *[["Gui", _[18][i]] for i in range(9)],
        ["Gui", _[22]]
    ),
    [startMenuBatchBackground, startMenuBatchForeground]
)
sm.add_scene(
    "saves",
    (
        [
            "BackgroundImage",
            background,
            (0, 0)
        ],
        ["Gui", _[23]],
        *[["Gui", _[25][i]] for i in range(10)],
    ),
    [savesMenuBatchBackground, savesMenuBatchForeground]
)
sm.load_scene("main menu")

pyglet.app.run()
