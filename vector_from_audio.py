import os
import torch
from io import BytesIO
from typing import Optional, List
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from moviepy.editor import VideoFileClip
from scipy.io import wavfile
import numpy as np
from scipy.signal import resample

# Загрузка модели для аудио
audio_model_id = "facebook/wav2vec2-large-960h"
processor = Wav2Vec2Processor.from_pretrained(audio_model_id)
audio_model = Wav2Vec2Model.from_pretrained(audio_model_id)

app = FastAPI()


class AudioEncodeRequest(BaseModel):
    video_url: str


@app.post("/encode_audio")
async def encode_audio(request: AudioEncodeRequest):
    video_url = request.video_url
    if not video_url:
        raise HTTPException(status_code=400, detail="Please provide a video URL.")

    try:
        # Скачивание видеофайла
        response = requests.get(video_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Unable to fetch video from {video_url}")
        video_data = BytesIO(response.content)
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(video_data.getbuffer())

        # Извлечение аудиодорожки из видеофайла
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = "temp_audio.wav"
        audio.write_audiofile(audio_path)

        # Явное закрытие видео и аудио объектов
        audio.close()
        video.close()

        # Преобразование аудиофайла в массив numpy
        samplerate, data = wavfile.read(audio_path)
        if data.ndim > 1:
            # Если аудиодорожка имеет более одного канала, взять только первый канал
            data = data[:, 0]

        # Нормализация данных
        data = data.astype(np.float32) / 32768.0

        # Приведение частоты дискретизации к 16000 Гц
        target_samplerate = 16000
        if samplerate != target_samplerate:
            num_samples = int(len(data) * float(target_samplerate) / samplerate)
            data = resample(data, num_samples)

        # Создание тензора
        audio_tensor = torch.tensor(data)  # .unsqueeze(0)  # Добавление batch dimension - ломает программу

        # Преобразование аудио в вектора
        inputs = processor(audio_tensor, sampling_rate=samplerate, return_tensors="pt")
        input_values = inputs.input_values  # Получаем тензор входных значений
        with torch.no_grad():
            features = audio_model(input_values).last_hidden_state
        features /= features.norm(dim=-1, keepdim=True)

        return {"features": features.squeeze(0).tolist()}

    finally:
        # Удаление временных файлов
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)


# TODO:
# 1. Запустив такой код на сервере с поддержкой GPU, можно получать векторы по аудиодорожке из видеофайлов.
# 2. Сейчас такое приложение принимает URL-ссылки на видеофайлы и скачивает их самостоятельно.
#    Загружает временные файлы на диск и удаляет их в конце работы.