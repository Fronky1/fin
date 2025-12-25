from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.recipes import router as recipes_router

app = FastAPI(
    title="Поварёшка",
    description="Каталог рецептов с поиском, оценками и комментариями",
    version="1.0.0"
)

# запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(recipes_router)

from app.routers.users import router as users_router

app.include_router(users_router)

from app.routers.comments import router as comments_router
from app.routers.ratings import router as ratings_router

app.include_router(comments_router)
app.include_router(ratings_router)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recipe/{id}", response_class=HTMLResponse)
def recipe_detail(request: Request, id: int):
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "recipe_id": id})


from app.routers.ratings import router as ratings_router

app.include_router(ratings_router)

#front

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, recipe_id: int):
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "recipe_id": recipe_id})


# Добавь роут для регистрации/входа, если есть страницы
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


from fastapi.responses import RedirectResponse


@app.get("/recipes/")
async def redirect_recipes():
    return RedirectResponse(url="/recipes")


from app.routers.users import router as users_router

app.include_router(users_router)

@app.get("/add-recipe", response_class=HTMLResponse)
async def add_recipe_page(request: Request):
    return templates.TemplateResponse("add_recipe.html", {"request": request})

