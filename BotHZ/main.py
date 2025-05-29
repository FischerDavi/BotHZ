import pyautogui
import time
import pytesseract
from itertools import repeat
import cv2
import numpy as np
import os

# Caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'


def click_btn(img, timeout=6, region=None, offset_x=0, offset_y=0):
    start = time.time()
    while True:
        try:
            pos = pyautogui.locateCenterOnScreen(img, confidence=0.65)
        except pyautogui.ImageNotFoundException:
            pos = None

        if pos is not None:
            x, y = pos
            pyautogui.moveTo(x + offset_x, y + offset_y, duration=0.6)
            pyautogui.click()
            time.sleep(2)
            return pyautogui.Point(x + offset_x, y + offset_y)
        else:
            if time.time() - start < timeout:
                continue
            else:
                return pyautogui.Point(-1, -1)

def attack(players):
    count = 2
    aux = []
    for i in players:
        aux.extend(repeat(i, 3))

    for player in aux:
        while True:
            time.sleep(5)   #5s para abrir a tela do hz
            pos = click_btn('img/courage-bar.png')

            x = int(pos[0])
            y = int(pos[1])
            time.sleep(2)

            print(f'Rodando ataque para {player}')
            click_btn('img/ranking.png')             # clica no icone do ranking
            click_btn('img/search-btn.png', offset_x=-120)   # usa a imagem do botao pesquisar e clica 120 pixels a esquerda
            pyautogui.moveRel(50, 0)      # ao fazer isso, ele clica na barra de pesquisa
            pyautogui.keyDown('backspace')
            time.sleep(2)
            pyautogui.keyUp('backspace')  # remove o que esta escrito
            pyautogui.write(player)       # escreve o nome/poiscao do jogador no arquivo txt
            pyautogui.moveRel(0, 50)
            click_btn('img/search-btn.png')   # clica em pesquisar
            click_btn('img/show-hero-btn.png')    # exibe o heroi
            click_btn('img/attack-btn.png', offset_y=-100)  # usa a foto da misao especial, mas 100 pixels acima, no botao de ataque
            pyautogui.moveRel(0, 20)   # pular combate
            pyautogui.click()
            time.sleep(3)
            pyautogui.moveRel(-20, -60)   # usa o local q o mouse esta (botao de ataque) e sobe/esquerda 20 pixels para clicar no ok
            pyautogui.click()
            click_btn('img/discount.png')
            click_btn('img/catch-btn.png')
            click_btn('img/close-btn.png')

            count += 1
            if count == 3:
                count = 0
            time.sleep(600)
            break


def load_players(file):
    with open(file, 'r') as file:
        players = file.readlines()
    return [player.strip() for player in players]

players = load_players('players.txt')        
attack(players)