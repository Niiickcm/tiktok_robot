import time

from google_ia import message_ia
from generate_video import add_text_to_video
from video_folder_control import update_last_video_used,get_next_video_path,get_output_video_path,remove_excess_videos_by_id

# CRIA UM TEXTO MOTIVADOR
message = message_ia()
print("Iniciando...",message)
time.sleep(10)

# FAZ A JUNÇÃO DO TEXTO COM O VIDEO
base_videos_folder = 'base_videos'
videos_created_folder = 'videos_created'
last_video_file = 'last_video_used.txt'
counter_file = 'video_counter.txt'
text = message
input_video_path = get_next_video_path(base_videos_folder, last_video_file)
output_video_path = get_output_video_path(videos_created_folder, counter_file, text)


max_videos = 10
remove_excess_videos_by_id(videos_created_folder, max_videos)


# CONFIGURAÇOES DO TEXTO
font_path = 'arial.ttf'
color = (255, 255, 255)
line_spacing = 15
bg_color = (0, 0, 0)
alpha = 0.6
music_folder = 'songs_video'

add_text_to_video(input_video_path, output_video_path, text, font_path, color, line_spacing, bg_color, alpha, videos_created_folder, music_folder)
update_last_video_used(last_video_file, input_video_path)



