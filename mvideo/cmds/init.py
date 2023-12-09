import click

from pytube import Playlist, YouTube
from pytube.cli import on_progress

from mvideo.environment import Environment


def extract_videos(urls, playlist, playlist_start, playlist_end):
    video_urls = None
    if playlist:
        playlist = Playlist(playlist)
        if playlist_start < playlist_end and playlist_end <= playlist.count:
            video_urls = playlist.video_urls[
                playlist_start:playlist_end
            ]  # pyright: ignore
        else:
            video_urls = playlist.video_urls
    else:
        video_urls = urls.split(",")

    videos = {}
    for url in video_urls:
        videos[url] = YouTube(url, on_progress_callback=on_progress)

    return videos


def download_streams(env: Environment, video: YouTube, output_path: str):
    print("Downloading Video...")
    stream = (
        video.streams.filter(type="video", is_dash=True).order_by("resolution").last()
    )
    stream.download(  # pyright: ignore
        filename=env.video_filename, output_path=output_path
    )

    print("Downloading Audio...")
    stream = video.streams.filter(type="audio").first()
    stream.download(  # pyright: ignore
        filename=env.audio_filename, output_path=output_path
    )


@click.command("init")
@click.option("--urls", type=click.STRING, help="The list of video URL")
@click.option("--playlist", type=click.STRING, help="Playlist URL")
@click.option("--playlist-start", type=click.INT, help="Playlist start index")
@click.option("--playlist-end", type=click.INT, help="Playlist end index")
@click.option("--translator", type=click.STRING, help="Translator")
@click.option("--translator-from-lang", type=click.STRING, help="Translator from lang")
@click.option("--translator-to-lang", type=click.STRING, help="Translator to lang")
def init(
    urls,
    playlist,
    playlist_start,
    playlist_end,
    translator,
    translator_from_lang,
    translator_to_lang,
):
    env = Environment()

    try:
        # 1. Set translator and urls to config
        env.set_translator(translator, translator_from_lang, translator_to_lang)

        # 2. extract YouTubes from playlist or urls
        videos = extract_videos(urls, playlist, playlist_start, playlist_end)
        if not videos:
            raise RuntimeError("No videos found!")
        env.set_urls([url for url in videos])

        # 3. Download YouTubes
        for url, video in videos.items():
            output_path = env.add_video(
                url,
                video.title,
                video.description,
            )
            download_streams(env, video, output_path=output_path)
    except Exception as e:
        print(e)
    finally:
        # 4. Write config and data
        env.flush()
