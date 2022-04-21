"""Модуль содержит интерфейс для работы с видео."""
import subprocess
from multiprocessing import Process
from pathlib import Path
from typing import Optional

import ffmpeg_streaming
from ffmpeg_streaming import Formats


class MediaConverter:

    """Класс, реализующий работу с видео."""

    def make_container(self, video_track: str, audio_track: str, container: str) -> Optional[str]:

        """
        Функция преобразует файлы в контейнер.
        Дальше будет использовать его с разными протоколами потоковой передачи.

        Args:
            video_track: путь до видео трека
            audio_track: путь до аудио трека
            container: путь до контейнера, куда мы хотим положить

        Returns:
            Вернёт контейнер.
        """

        ffmpeg = subprocess.run(['which', 'ffmpeg'], capture_output=True).stdout.decode('utf-8').strip()
        command = [
            ffmpeg,
            '-i',
            video_track,
            '-i',
            audio_track,
            '-c:v',
            'copy',
            '-c:a',
            'aac',
            '-map',
            '0:v:0',
            '-map',
            '1:a:0',
            container,
        ]
        if subprocess.run(command).returncode == 0:
            return container
        return None

    def to_mpeg_dash(self, container: Path, output: str) -> None:

        """
        Функция, преобразующая в протокол MPEG-DASH.

        Подробнее см.
        https://ru.wikipedia.org/wiki/MPEG-DASH

        Args:
            container: путь до контейнера
            output: путь до манифеста
        """

        video = ffmpeg_streaming.input(str(container))
        dash = video.dash(Formats.h264())
        dash.auto_generate_representations()
        dash.output(output)

        container.unlink()

    def to_hls(self, container: str, output: str) -> None:

        """
        Функция, преобразующая в протокол hls.
        На данном этапе нам можно без неё обойтись.

        Подробнее см.
        https://ru.wikipedia.org/wiki/HLS

        Args:
            container: путь до контейнера
            output: путь до манифеста
        """
        pass


def main() -> None:

    """Функция иллюстрирует работу конвертора."""

    video = 'media/video/1.mp4'  # noqa: WPS114
    audio = 'media/audio/1.aac'
    mp_4 = 'media/av3.mp4'  # noqa: WPS114
    mpeg_dash_manifest = 'streams/dir_1/dash.mpd'

    mc = MediaConverter()
    container = mc.make_container(video, audio, mp_4)
    packaging = Process(target=mc.to_mpeg_dash, args=(container, mpeg_dash_manifest))
    packaging.start()


if __name__ == '__main__':
    main()
