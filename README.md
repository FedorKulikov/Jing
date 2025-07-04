# Интернет-Радио с управлением горячими клавишами

## Описание
Это FastAPI-приложение для потоковой трансляции аудио с возможностью переключения треков по горячим клавишам. Основной трек воспроизводится в цикле, а по нажатию клавиши можно проиграть альтернативный трек. После завершения альтернативного трека автоматически возвращается основной поток.

## Возможности
- Потоковая трансляция аудио в реальном времени
- Переключение между треками по горячей клавише (по умолчанию 'J')
- Автоматическое зацикливание основного трека
- Простой и интуитивно понятный веб-интерфейс
- Поддержка различных аудиоформатов (MP3, WAV и др.)

## Требования
- Python 3.7+
- FastAPI (pip install fastapi)
- Uvicorn (pip install uvicorn)
- Аудиофайлы:
  - static/radio.mp3 (основной трек)
  - static/alternative.mp3 (альтернативный трек)

## Установка и запуск

1. Установите зависимости:
```bash
pip install fastapi uvicorn
```

2. Создайте папку для аудиофайлов:
```bash
mkdir static
```

3. Поместите ваши аудиофайлы в папку static/

4. Запустите приложение:
```bash
uvicorn main:app --reload
```

## Использование

### Веб-интерфейс
Откройте в браузере:
```bash
http://localhost:8000
```

### Управление
- Основной трек играет автоматически
- Нажмите клавишу **J** для воспроизведения альтернативного трека
- После завершения альтернативного трека автоматически вернется основной

### API Endpoints
- `GET /` - Веб-интерфейс
- `GET /radio` - Аудиопоток
- `GET /play-alternative` - Включить альтернативный трек

## Настройка
- Для смены горячей клавиши измените параметр в файле main.py:
```javascript
if (e.key.toLowerCase() === "j")
```

- Для замены аудиофайлов просто поместите новые файлы в папку static/:
  - radio.mp3 - основной трек
  - alternative.mp3 - альтернативный трек
