from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import asyncio
from threading import Lock

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

AUDIO_FILES = {
    "main": "static/radio.mp3",
    "alternative": "static/alternative.mp3"
}

current_track = "main"
lock = Lock()

async def audio_generator():
    global current_track
    chunk_size = 1024 * 16

    while True:
        path = Path(AUDIO_FILES.get(current_track, AUDIO_FILES["main"]))
        if not path.exists():
            current_track = "main"
            await asyncio.sleep(1)
            continue

        try:
            with path.open("rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    await asyncio.sleep(0.01)

            with lock:
                if current_track != "main":
                    current_track = "main"

        except Exception:
            current_track = "main"
            await asyncio.sleep(1)

@app.get("/radio")
async def stream_audio():
    return StreamingResponse(audio_generator(), media_type="audio/mpeg")

@app.get("/play-alternative")
async def play_alternative():
    global current_track
    if Path(AUDIO_FILES["alternative"]).exists():
        with lock:
            current_track = "alternative"
        return {"status": "ok"}
    return {"status": "error", "message": "alternative.mp3 not found"}

@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Radio</title>
        <style>
            body {
                font-family: sans-serif;
                text-align: center;
                padding: 60px;
            }
        </style>
    </head>
    <body>
        <h1>Radio</h1>
        <p>Нажмите клавишу <strong>J</strong> для воспроизведения джингла</p>
        <audio id="player" controls autoplay>
            <source src="/radio" type="audio/mpeg">
            Ваш браузер не поддерживает аудио.
        </audio>

        <script>
            const player = document.getElementById("player");

            document.addEventListener("keydown", async (e) => {
                if (e.key.toLowerCase() === "j") {
                    await fetch("/play-alternative");
                    player.pause();
                    player.currentTime = 0;
                    player.load();
                    await player.play();
                }
            });

            player.addEventListener("error", () => {
                setTimeout(() => {
                    player.load();
                    player.play();
                }, 1000);
            });
        </script>
    </body>
    </html>
    """
