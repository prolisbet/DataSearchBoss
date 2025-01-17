# Документация для Программы Обработки Аудио

## Описание

Модуль `vector_from_audio.py` предназначен для автоматизированного извлечения 
и обработки аудио-дорожек из видеороликов, а также для их последующего анализа 
с использованием модели Wav2Vec2. Он включает в себя функции для загрузки модели, 
обработки видеофайлов, логирования, а также сохранения и обновления результатов 
обработки в JSON-файлах.

## Структура Программы

### Импорт и настройка библиотек

Программа начинается с импорта необходимых библиотек, таких как `os`, `torch`, 
`requests`, `fastapi`, `pydantic`, `transformers`, `moviepy`, `scipy`, `numpy`, 
`sklearn`, `logging`, `json`, и `asyncio`. Эти библиотеки обеспечивают 
функционал для работы с аудио и видео, машинного обучения, логирования, 
асинхронного программирования, и веб-приложений.

### Логирование

Для отслеживания работы программы и выявления потенциальных проблем используется 
модуль `logging`. Логирование настроено на уровень `INFO`.

### Загрузка модели

Модель Wav2Vec2 от Hugging Face используется для обработки аудио. 
Модель и процессор загружаются из предварительно обученного репозитория 
`jonatasgrosman/wav2vec2-large-xlsr-53-russian`.

### Создание папки для результатов

Программа создает папку `audio_processing` для сохранения результатов обработки. 
Это помогает организовать результаты и избежать их потери.

### Чтение данных

Программа читает данные из JSON-файла `all_videos.json`, содержащего информацию 
о видеороликах. Из файла выбираются 100 записей для обработки, начиная с заданного 
индекса (в данном случае, с 900 по 1000).

### Обработка записей

Асинхронная функция `process_records` обрабатывает выбранные видеозаписи. 
Для каждой записи извлекается URL видео, который затем передается в функцию 
`encode_audio` для извлечения и обработки аудио-дорожки. Результаты успешной 
обработки сохраняются в словари `new_audio_vectors` и `new_audio_process`, 
а информация о неудачных попытках — в словарь `new_audio_fail`.

### Обработка аудио

#### `@app.post("/encode_audio")`

Эта функция выполняет следующие задачи:

1. **Проверка и получение URL видео**: Функция проверяет наличие URL видео в запросе. Если URL отсутствует, возвращается ошибка.
2. **Скачивание видеофайла**: Видео скачивается по указанному URL и сохраняется во временный файл `temp_video.mp4`.
3. **Извлечение аудио из видео**: С помощью библиотеки `moviepy` извлекается аудиодорожка из видео и сохраняется в файл `temp_audio.wav`.
4. **Обработка аудиофайла**:
    - Чтение аудиофайла и преобразование его в массив numpy.
    - Нормализация данных и приведение частоты дискретизации к 16000 Гц.
    - Создание тензора и преобразование аудио в вектора с помощью модели Wav2Vec2.
    - Преобразование вектора в формат 1x1024 с использованием PCA.
5. **Возвращение результатов**: Возвращаются извлеченные признаки, время обработки, длина видео и количество каналов.
6. **Очистка временных файлов**: Удаление временных файлов после завершения обработки.

Пример использования:

```python
@app.post("/encode_audio")
async def encode_audio(request: AudioEncodeRequest):
    # Код функции
```
### Обновление и сохранение результатов

Программа читает существующие данные из файлов `audio_vectors.json`, 
`audio_process.json` и `audio_fail.json`. Затем она дополняет эти данные 
новыми записями и сохраняет их обратно в соответствующие файлы.

### Логирование времени выполнения

Время выполнения программы измеряется и логируется для оценки производительности.

## Используемые Библиотеки

- **os**: Работа с файловой системой. (Встроенная библиотека Python)
- **torch 1.9.0**: Работа с тензорами и моделями глубокого обучения. (https://pytorch.org/)
- **requests 2.26.0**: Отправка HTTP-запросов. (https://docs.python-requests.org/)
- **fastapi 0.68.1**: Создание веб-приложений. (https://fastapi.tiangolo.com/)
- **pydantic 1.8.2**: Валидация данных. (https://pydantic-docs.helpmanual.io/)
- **transformers 4.11.3**: Работа с моделями трансформеров. (https://huggingface.co/transformers/)
- **moviepy 1.0.3**: Работа с видеофайлами. (https://zulko.github.io/moviepy/)
- **scipy 1.7.1**: Научные вычисления. (https://www.scipy.org/)
- **numpy 1.21.2**: Работа с массивами данных. (https://numpy.org/)
- **sklearn ~ scikit-learn 1.5.0**: Машинное обучение и анализ данных. (https://scikit-learn.org/)
- **logging**: Логирование событий. (Встроенная библиотека Python)
- **json**: Работа с JSON-файлами. (Встроенная библиотека Python)
- **asyncio**: Асинхронное программирование. (Встроенная библиотека Python)

## Примечания

- На момент написания документации, программа обработала видеофайлы с 0 по 999 включительно.
- Для дальнейшей работы необходимо изменить начальный и конечный индексы в переменных `start_video` и `end_video`.

## Заключение

Этот скрипт представляет собой мощный инструмент для извлечения аудио из видео и их последующего анализа с использованием современных моделей машинного обучения. Благодаря использованию FastAPI и асинхронного программирования, программа легко интегрируется в веб-сервисы и может быть использована для обработки данных в реальном времени.