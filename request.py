from fastapi import FastAPI, HTTPException, Response, Depends
from cats_data import load_cats, save_cats
from valid import NewCat, UserLoginSchema
from authorization import security,config

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
         summary="Получить всех котят")
async def read_cats():
    cats = await load_cats()
    return cats

@app.get("/cats/{cats_id}",
         tags=["Коты"],
         summary="Получить конкретного кота")
async def get_cats(cats_id: int):  
    cats = await load_cats() 
    for cat in cats:
        if cat["id"] == cats_id:
            return cat
    raise HTTPException(status_code=404, detail="Кот не найден.")

@app.post("/cats",
          tags=["Коты"],
          summary="Добавить нового кота")
async def add_cats(new_cat: NewCat):
    cats = await load_cats()
    new_id = max((cat["id"] for cat in cats), default=0) + 1
    new_cat_data = {
        "id": new_id,
        "nickname": new_cat.nickname,
        "color": new_cat.color,
        "age": new_cat.age,
    }
    cats.append(new_cat_data)
    await save_cats(cats)
    return {"success": True, "message": "Кот успешно добавлен"}

@app.delete("/cats/{cats_id}",
            tags=["Коты"],
            summary="Удалить кота")
async def delete_cat(cats_id: int):
    cats = await load_cats()
    cat_to_delete = next((cat for cat in cats if cat["id"] == cats_id), None)

    if not cat_to_delete:
        raise HTTPException(status_code=404, detail="Кот не найден.")
    
    cats = [cat for cat in cats if cat["id"] != cats_id]
    await save_cats(cats)

    return {"success": True, "message": f"Кот с ID {cats_id} успешно удален."}

# @app.put("/cats/{cats_id}",
#          tags=["Коты"],
#          summary="Изменить параметры кота")
# async def update_cat(cats_id: int, updated_cat: NewCat):
#     cats = await load_cats()
#     for cat in cats:
#         if cat["id"] == cats_id:
#             # Обновляем данные кота
#             cat["nickname"] = updated_cat.nickname
#             cat["color"] = updated_cat.color
#             cat["age"] = updated_cat.age
#             await save_cats(cats)
#             return {"success": True,}
