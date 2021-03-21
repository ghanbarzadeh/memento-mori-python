
import os
import ctypes
import numpy as np
import cv2
import textwrap
from PIL import ImageFont, ImageDraw, Image
from datetime import date

def draw_empty_rectangles(img, nx, ny):
    startx = 116
    starty = 80
    boxw = 13
    boxy = 13
    box_x_space = 3
    box_y_space = 3
    block_x_space = 8
    block_y_space = 8
    block_x_jump = 26
    block_y_jump = 10

    for i in range(nx):
        for j in range(ny):
            x1 = startx + i * boxw + i * box_x_space + i//block_x_jump * block_x_space
            x2 = startx + (i+1) * boxw + i * box_x_space + i//block_x_jump * block_x_space
            y1 = starty + j * boxy + j * box_y_space + j//block_y_jump * block_y_space
            y2 = starty + (j+1) * boxy + j * box_y_space + j//block_y_jump * block_y_space
            cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 1)
    return img

def fill_in_rectangles(img, nx, ny, weeks):
    startx = 116
    starty = 80
    boxw = 13
    boxy = 13
    box_x_space = 3
    box_y_space = 3
    block_x_space = 8
    block_y_space = 8
    block_x_jump = 26
    block_y_jump = 10

    full_ny = weeks//nx
    left_over = weeks%nx
    for i in range(nx):
        for j in range(full_ny):
            x1 = startx + i * boxw + i * box_x_space + i//block_x_jump * block_x_space
            x2 = startx + (i+1) * boxw + i * box_x_space + i//block_x_jump * block_x_space
            y1 = starty + j * boxy + j * box_y_space + j//block_y_jump * block_y_space
            y2 = starty + (j+1) * boxy + j * box_y_space + j//block_y_jump * block_y_space
            cv2.rectangle(img, (x1, y1), (x2, y2), box_color, -1)
    for i in range(left_over):
        for j in range(full_ny+1):
            x1 = startx + i * boxw + i * box_x_space + i//block_x_jump * block_x_space
            x2 = startx + (i+1) * boxw + i * box_x_space + i//block_x_jump * block_x_space
            y1 = starty + j * boxy + j * box_y_space + j//block_y_jump * block_y_space
            y2 = starty + (j+1) * boxy + j * box_y_space + j//block_y_jump * block_y_space
            cv2.rectangle(img, (x1, y1), (x2, y2), box_color, -1)
    return img



text_color = (255,255,255)
box_color = (255,255,255)
image_name = "wa.jpg"
b_date = date(1997, 7, 9)
alpha=0.85


height = 1080
width = 1920
image = cv2.imread(image_name)
image_copy = cv2.imread(image_name)


d1 = b_date
d2 = date.today()
d3 = date(date.today().year, 7, 9)
weeks = (d2.year-d1.year)*52 + (d2-d3).days//7
image = draw_empty_rectangles(image, 2*52, 40)
image = fill_in_rectangles(image, 2*52, 40, weeks)


image=cv2.addWeighted(image, alpha, image_copy,1-alpha, gamma=0)


text =  '  It is not that we have a short space of time, but that we waste much of it. Life is long enough, and it has been given in \nsufficiently generous measure to allow the accomplishment of the very greatest things if the whole of it is well invested.'
fontpath = "DMSerifText-Italic.ttf"     
font = ImageFont.truetype(fontpath, 22)
img_pil = Image.fromarray(image)
draw = ImageDraw.Draw(img_pil)
draw.text((400, 830),  text, font = font, fill = text_color)
text =  '- S E N E C A -'
fontpath = "DMSerifText-Regular.ttf"     
font = ImageFont.truetype(fontpath, 32)
draw = ImageDraw.Draw(img_pil)
draw.text((870, 930),  text, font = font, fill = text_color)
image = np.array(img_pil)


cv2.imwrite("image.png",image)


ctypes.windll.user32.SystemParametersInfoW(20, 0, "\image.png" , 0)
