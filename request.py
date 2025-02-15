from fastapi import FastAPI, HTTPException, Response, Depends
from valid import NewCat, UserLoginSchema
from authorization import security,config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Cat


app = FastAPI()

@app.post("/login", tags=["Авторизация"])
async def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access token": token}
    raise HTTPException(status_code=401, detail="Неккоректное имя пользователя или пароль.")

@app.get("/protected",tags=["Авторизация"], dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "TOP SECRET"}
    #raise HTTPException(status_code=403, detail="Вы не вошли в систему.")

@app.get("/cats",
         tags=["Коты"],
         summary="Получить всех")
async def get_cats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cat))
    cats = result.scalars().all()
    return cats

@app.get("/cats/{cats_id}",
         tags=["Коты"],
         summary="Получить конкретного кота")
async def get_cat(id:int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cat).where(Cat.id == id))
    cat = result.scalars().first()

    if cat  is None:
        raise HTTPException(status_code=404, detail="Cat not found.")
    
    return cat

@app.post("/cats",
          tags=["Коты"],
          summary="Добавить кота"
          )
async def add_cat(name: str, color: str, age: int, db: AsyncSession = Depends(get_db)):
    new_cat = Cat(name=name, color=color, age=age)
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat

@app.delete("/cats/{cats_id}",
            tags=["Коты"],
            summary="Удалить кота")
async def delete_cat(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cat).where(Cat.id == id))
    cat = result.scalars().first()

    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found.")

    await db.delete(cat)
    await db.commit()
    
    return {"message": "Cat deleted successfully"}

@app.put("/cats/{cats_id}",
         tags=["Коты"],
         summary="Изменить кота")
async def update_cat(id: int, name: str = None, color: str = None, age: int = None, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cat).where(Cat.id == id))
    cat = result.scalars().first()

    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found.")

    if name:
        cat.name = name
    if color:
        cat.color = color
    if age is not None:
        cat.age = age

    await db.commit()
    await db.refresh(cat)
    
    return cat