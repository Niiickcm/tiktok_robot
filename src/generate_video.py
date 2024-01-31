import time

import cv2
import os
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import numpy as np
import textwrap

from actions_on_the_website import actions_on_the_website
from video_folder_control import get_latest_video


def calculate_font_size_and_line_width(video_width):
    # Ajuste esses fatores conforme necessário para obter o tamanho de fonte e largura de linha desejados
    font_size_factor = 0.040  # Percentual da largura do vídeo para o tamanho da fonte
    max_line_width = 55  # Máximo número de caracteres por linha

    font_size = int(video_width * font_size_factor)
    line_width = min(max_line_width, video_width // font_size)

    return font_size, line_width


def draw_text_with_pil(frame, text, font_path, font_size, color, line_width, line_spacing, bg_color, alpha):
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)
    font = ImageFont.truetype(font_path, font_size)

    lines = textwrap.wrap(text, width=line_width)

    # Calculando a altura máxima de uma linha de texto
    max_line_height = max([draw.textsize(line, font=font)[1] for line in lines])
    total_text_height = len(lines) * (max_line_height + line_spacing) - line_spacing
    starting_y = frame.shape[0] // 2 - total_text_height // 2

    # Desenha o retângulo de fundo com transparência sobre toda a tela
    draw.rectangle([(0, 0), frame_pil.size], fill=bg_color)

    # Aplicando transparência ao retângulo de fundo
    frame_with_bg = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
    cv2.addWeighted(frame, alpha, frame_with_bg, 1 - alpha, 0, frame)

    # Desenhando o texto
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)
    for i, line in enumerate(lines):
        width, _ = draw.textsize(line, font=font)
        text_x = (frame.shape[1] - width) // 2
        text_y = starting_y + i * (max_line_height + line_spacing)
        draw.text((text_x, text_y), line, font=font, fill=color)

    frame_with_text = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

    return frame_with_text


def add_text_to_video(input_video_path, output_video_path, text, font_path, color, line_spacing, bg_color, alpha, videos_created_folder, music_folder):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {input_video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    font_size, line_width = calculate_font_size_and_line_width(width)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with tqdm(total=total_frames) as barra_progresso:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Progresso finalizado!")
                break

            frame_with_text = draw_text_with_pil(frame, text, font_path, font_size, color, line_width, line_spacing, bg_color, alpha)
            out.write(frame_with_text)

            barra_progresso.update(1)

    cap.release()
    out.release()

    time.sleep(10)



    latest_video_path = get_latest_video(videos_created_folder)
    print('latest_video_path',latest_video_path)

    if latest_video_path:
        # Chama a função após a criação do vídeo
        actions_on_the_website(latest_video_path)
    else:
        print(f"Não foi possível encontrar o último vídeo em: {videos_created_folder}")
