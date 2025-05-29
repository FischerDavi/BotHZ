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
    
def mission():
    while True:
        time.sleep(7)    # 7 segundos para abrir a tela do hz
        pos = click_btn('img/luva_sem_fundo.png')

        time.sleep(1)

        if exists_btn('img/medium.png'):     # se achar missao media/dificil, realiza elas, se nao vai para proxima zona
            click_btn('img/medium.png', offset_x=250, offset_y=300)
        elif exists_btn('img/hard.png'):
            click_btn('img/hard.png', offset_x=250, offset_y=300)
        elif exists_btn('img/easy.png'):
            click_btn('img/easy.png', offset_x=710, offset_y=-265)
            time.sleep(2)
            click_btn('img/skip-zone.png')
        else:
            mission()

remover_fundo_branco('img/fight-mission.png', 'img/luva_sem_fundo.png')  
mission()