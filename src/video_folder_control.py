import os

def get_next_video_path(folder_path, last_video_file):
    video_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.mp4'))])
    if not video_files:
        raise ValueError("Nenhum vídeo encontrado na pasta especificada.")

    if not os.path.exists(last_video_file):
        return os.path.join(folder_path, video_files[0])

    with open(last_video_file, 'r') as file:
        last_video = file.readline().strip()

    if last_video not in video_files:
        return os.path.join(folder_path, video_files[0])

    next_index = (video_files.index(last_video) + 1) % len(video_files)
    return os.path.join(folder_path, video_files[next_index])

def update_last_video_used(last_video_file, video_path):
    with open(last_video_file, 'w') as file:
        file.write(os.path.basename(video_path))


def get_output_video_path(output_folder, counter_file, text):
    if not os.path.exists(counter_file):
        counter = 1
    else:
        with open(counter_file, 'r') as file:
            counter = int(file.readline().strip()) + 1

    output_video_path = os.path.join(output_folder, f'{text[0:100]}... {counter}.mp4')

    with open(counter_file, 'w') as file:
        file.write(str(counter))

    return output_video_path

def get_latest_video(video_folder):
    # Lista todos os arquivos no diretório
    files = os.listdir(video_folder)

    # Filtra apenas os arquivos de vídeo
    video_files = [file for file in files if file.endswith('.mp4')]

    # Verifica se há vídeos na pasta
    if not video_files:
        return None

    # Ordena os vídeos pela data de modificação (o mais recente primeiro)
    latest_video = max(video_files, key=lambda x: os.path.getmtime(os.path.join(video_folder, x)))

    return os.path.join(video_folder, latest_video)

def remove_excess_videos_by_id(video_folder, max_videos):
    # Lista todos os arquivos no diretório
    files = os.listdir(video_folder)

    # Filtra apenas os arquivos de vídeo
    video_files = [file for file in files if file.endswith('.mp4')]

    # Verifica se o número de vídeos excede o limite
    if len(video_files) > max_videos:
        # Extrai os IDs dos vídeos e os ordena
        # Assume que o ID é um número no final do nome do arquivo, antes da extensão .mp4
        sorted_videos = sorted(video_files, key=lambda x: int(x.rsplit(' ', 1)[-1].split('.')[0]))

        # Remove os vídeos com menores IDs até atingir o limite
        for video in sorted_videos[:len(video_files) - max_videos]:
            os.remove(os.path.join(video_folder, video))
            print(f"Vídeo removido: {video}")
