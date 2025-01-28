import json
from pathlib import Path
import aiofiles

CATS_FILE = Path("cats.json")

async def load_cats():
    if not CATS_FILE.exists():
        return []
    async with aiofiles.open(CATS_FILE, "r", encoding="utf-8") as file:
        content = await file.read()
        return json.loads(content)

async def save_cats(cats):
    async with aiofiles.open(CATS_FILE, "w", encoding="utf-8") as file:
        content = json.dumps(cats, ensure_ascii=False, indent=4)  
        await file.write(content)