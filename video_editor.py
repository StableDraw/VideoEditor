from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips
from os import mkdir, remove
from os.path import isfile, exists
import string
import random
import filetype
 

class VideoEditor():
    def __init__(self):
        if not exists("input_temp"):
            mkdir("input_temp")

        if not exists("output_temp"):
            mkdir("output_temp")


    def get_random_path(self, dir_name: str = "", file_ext: str = "") -> str:
        '''
        Метод, генерирующий случайный путь к файлу в указанной папке
        '''

        if dir_name != "" and dir_name[:0] != "\\" or dir_name[:0] != "/":
            dir_name += "\\"

        n = 10 #Длина строки

        while True:
            filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k = n)) + file_ext #Генерируем случайную строку указанной длины
            if not isfile(dir_name + filename):
                break

        return filename


    def cut_video(self, video_path: bytes, cut_list: list) -> bytes:
        '''
        Обрезка видео
        '''

        video = VideoFileClip(video_path) #Открываем видеофайл
        fps = video.fps

        clips = [] #Создаём список клипов

        for clip_time in cut_list: #Нарезаем видео на клипы
            clips.append(video.subclip(clip_time["start"], clip_time["end"]))

        concat_clip = concatenate_videoclips(clips, method = "compose") #Объеденяем клипы воедино

        output_name = self.get_random_path(dir_name = "output_temp", file_ext = ".mp4") #Генерируем имя файла для временного размещения

        concat_clip.write_videofile("output_temp\\" + output_name, fps = fps) #Рендерим видеофайл

        video.close()

        return output_name


    def cut_audio(self, audio_path: bytes, cut_list: list) -> bytes:
        '''
        Обрезка аудио
        '''

        audio = AudioFileClip(audio_path) #Открываем аудиофайл
        fps = audio.fps

        clips = [] #Создаём список аудиофрагментов

        for clip_time in cut_list: #Нарезаем аудио на фрагменты
            clips.append(audio.subclip(clip_time["start"], clip_time["end"]))

        concat_clip = concatenate_audioclips(clips) #Объеденяем аудиофрагменты воедино

        output_name = self.get_random_path(dir_name = "output_temp", file_ext = ".wav") #Генерируем имя файла для временного размещения

        concat_clip.write_audiofile("output_temp\\" + output_name, fps = fps) #Рендерим аудиофайл

        audio.close()

        return output_name


    def cut_media(self, media: bytes, cut_list: list) -> bytes:
        '''
        Обрезка медиа (видео или аудио)
        Принимает медиа (видео или аудио) в виде строки байт, а также список словарей обрезки в формате [{"start": 0.0, "end": 0.0}, {"start": 0.0, "end": 0.0}, ]
        Возвращает обрезанное медиа (видео или аудио) в виде строки байт
        '''

        input_name = self.get_random_path("input_temp")

        with open("input_temp\\" + input_name, "wb") as f:
            f.write(media) #Записываем содержимое в файл

        kind = filetype.guess("input_temp\\" + input_name) #Определяем видео к нам пришло или аудио

        if "video" in kind.mime: #Если пришло видео
            output_name = self.cut_video(video_path = "input_temp\\" + input_name, cut_list = cut_list)
        elif "audio" in kind.mime: #Если пришло аудио
            output_name = self.cut_audio(audio_path = "input_temp\\" + input_name, cut_list = cut_list)
        else:
            raise Exception("Поддерживаются только видео и аудио")

        with open("output_temp\\" + output_name, "rb") as f:
            output = f.read()

        remove("input_temp\\" + input_name) #Удаляем временный входной файл
        remove("output_temp\\" + output_name) #Удаляем временный выходной файл

        return output



if __name__ == "__main__":

    ve = VideoEditor()

    cut_list = [{"start": 1.0, "end": 5.5}, {"start": 7.2, "end": 15.4}]

    with open("input.mp4", "rb") as f:
        video = f.read()

    video_output = ve.cut_media(media = video, cut_list = cut_list)

    with open("output.mp4", "wb") as f:
        f.write(video_output)


    with open("input.wav", "rb") as f:
        audio = f.read()

    audio_output = ve.cut_media(media = audio, cut_list = cut_list)

    with open("output.wav", "wb") as f:
        f.write(audio_output)