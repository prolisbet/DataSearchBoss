import csv
import json
import re
import os

# Путь к файлу CSV
csv_file_path = 'db_links/yappy_hackaton_2024_400k.csv'

# Путь к файлу JSON
json_file_path = 'db_links/hashtags_from_csv.json'

# Регулярное выражение для нахождения хештегов с русскими словами
hashtag_regex = re.compile(r'#([а-яА-ЯёЁ]+)')

# Множество для хранения уникальных хештегов
unique_hashtags = set()

# Чтение CSV файла и извлечение хештегов
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        description = row['description']
        hashtags = hashtag_regex.findall(description)
        unique_hashtags.update(hashtags)

# Сохранение уникальных хештегов в JSON файл
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(list(unique_hashtags), jsonfile, ensure_ascii=False, indent=4)

print(f"Уникальные хештеги сохранены в {json_file_path}")
print(f"Всего уникальных хештегов: {len(unique_hashtags)}")