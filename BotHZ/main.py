import pyautogui
import time
import pytesseract
from itertools import repeat
import cv2
import numpy as np
import os

def remover_fundo_branco(input_path='imagem.png', output_path='imagem_sem_fundo.png'):
    image = cv2.imread(input_path)
    if image is None:
        print(f"Imagem {input_path} não encontrada.")
        return

    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    lower_white = np.array([240, 240, 240, 0], dtype=np.uint8)
    upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(image_rgba, lower_white, upper_white)
    image_rgba[mask == 255] = [255, 255, 255, 0]

    cv2.imwrite(output_path, image_rgba)

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


def exists_btn(img, confidence=0.55):
    try:
        pos = pyautogui.locateCenterOnScreen(img, confidence=confidence)
        return pos is not None
    except pyautogui.ImageNotFoundException:
        return False


def attack(players):
    count = 1
    aux = []
    for i in players:
        aux.extend(repeat(i, 3))

    for player in aux:
        while True:
            pos = click_btn('img/courage-bar.png')

            if pos == pyautogui.Point(-1, -1):
                print("Não encontrou a barra de coragem.")
                time.sleep(10)
                continue

            x = int(pos[0])
            y = int(pos[1])
            time.sleep(2)

            try:
                image = pyautogui.screenshot(region=(x - 40, y - 10, 130, 25))
                courage = pytesseract.image_to_string(image, config='--psm 6').strip()
                courage = ''.join(filter(str.isdigit, courage))  # Remove caracteres não numéricos
            except Exception as e:
                print(f"Erro ao tirar screenshot ou interpretar coragem: {e}")
                time.sleep(10)
                continue

            if courage.isdigit() and int(courage) < 20:
                print(f'Coragem insuficiente ({courage}), aguardando...')
                time.sleep(10)

            else:
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
                time.sleep(10)   # espera 10 segundos pro ataque acabar
                pyautogui.moveRel(-20, -20)   # usa o local q o mouse esta (botao de ataque) e sobe/esquerda 20 pixels para clicar no ok
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


def mission():
    while True:
        time.sleep(10)    # 7 segundos para fechar o terminal e deixar o mouse dentro do jogo
        pos = click_btn('img/luva_sem_fundo.png')

        time.sleep(5)

        if exists_btn('img/medium.png'):     # se achar missao media/dificil, realiza elas, se nao vai para proxima zona
            click_btn('img/medium.png', offset_x=250, offset_y=300)
        elif exists_btn('img/hard.png'):
            click_btn('img/hard.png', offset_x=250, offset_y=300)
        elif exists_btn('img/easy.png'):
            click_btn('img/easy.png', offset_x=710, offset_y=-265)
            time.sleep(5)
            click_btn('img/skip-zone.png')
        else:
            mission()

# para selecionar qual bot usar = duelo duas primeiras linhas (142, 143) missao duas linhas finais (144, 145), usar # nas linhas do bot n usado
#players = load_players('players.txt')        
#attack(players)
remover_fundo_branco('img/fight-mission.png', 'img/luva_sem_fundo.png')  
mission()
