import os
import os.path

import json
import toml


class Environment:
    def __init__(self):
        self._project_path = os.path.abspath(".")

        self._config_path = os.path.join(self._project_path, "config.toml")
        self._config = (
            toml.load(open(self._config_path))
            if os.path.exists(self._config_path)
            else {}
        )
        self._urls = self._config.get("urls", [])
        self._translator = self._config.get("translator", {})

        self._data_path = os.path.join(self._project_path, "data.json")
        self._data = (
            json.load(open(self._data_path)) if os.path.exists(self._data_path) else {}
        )

        self._video_filename = "video.webm"
        self._audio_filename = "audio.mp4"
        self._audio_wav_filename = "audio.wav"
        self._audio_srt_filename = "audio.srt"
        self._trans_srt_filename = "audio_translate.srt"
        self._cover_image_filepath = "cover.png"
        self._final_filename = "final.mp4"

        self._videos = self._data.get("videos", {})

    @property
    def project_path(self):
        return self._project_path

    def project_subpath(self, subpath):
        return os.path.join(self._project_path, subpath)

    def set_urls(self, urls):
        self._urls = urls

    def set_translator(self, translator, from_lang, to_lang):
        self._translator = {
            "translator": translator,
            "from_lang": from_lang,
            "to_lang": to_lang,
        }

    def translator(self, translator):
        if translator:
            return translator
        return self._translator.get("transaltor")

    def translator_from_lang(self, from_lang):
        if from_lang:
            return from_lang
        return self._translator.get("from_lang")

    def translator_to_lang(self, to_lang):
        if to_lang:
            return to_lang
        return self._translator.get("to_lang")

    @property
    def videos(self):
        return self._videos

    def add_video(self, url, title, description):
        output_path = title.lower().replace(" ", "-")
        video_path = os.path.join(self._project_path, output_path)
        self._videos[output_path] = {
            "url": url,
            "title": title,
            "path": video_path,
            "description": description,
            "video_filepath": os.path.join(video_path, "video.wepm"),
            "audio_filepath": os.path.join(video_path, "audio.mp4"),
            "audio_wav_filepath": os.path.join(video_path, "audio.wav"),
            "audio_srt_filepath": os.path.join(video_path, self._audio_srt_filename),
            "trans_srt_filepath": os.path.join(video_path, self._trans_srt_filename),
            "cover_filepath": os.path.join(video_path, self._cover_image_filepath),
            "final_filepath": os.path.join(video_path, self._final_filename),
        }

        return output_path

    @property
    def video_filename(self):
        return self._video_filename

    @property
    def audio_filename(self):
        return self._audio_filename

    def video_filepath(self, output_path):
        return self._videos[output_path].get("video_filepath")

    def audio_filepath(self, output_path):
        return self._videos[output_path].get("audio_filepath")

    def audio_wav_filepath(self, output_path):
        return self._videos[output_path].get("video_filepath")

    def audio_srt_filepath(self, output_path):
        return self._videos[output_path].get("audio_srt_filepath")

    def trans_srt_filepath(self, output_path):
        return self._videos[output_path].get("trans_srt_filepath")

    def cover_filepath(self, output_path):
        return self._videos[output_path].get("cover_image_filepath")

    def final_filepath(self, output_path):
        return self._videos[output_path].get("final_filepath")

    def flush(self):
        self._config["urls"] = self._urls
        self._config["translator"] = self._translator
        toml.dump(self._config, open(self._config_path, "w"))

        self._data["videos"] = self._videos
        json.dump(self._data, open(self._data_path, "w"))
