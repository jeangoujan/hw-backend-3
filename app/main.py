from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from attrs import define
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@define
class Car:
    id: int
    name: str
    year: int


class CarRepository:
    def __init__(self):
        self.cars = []

    def get_all_cars(self):
        return self.cars

    def save_car(self, car: Car):
        car.id = len(self.cars) + 1
        self.cars.append(car)

repo = CarRepository()



@app.get("/")
def index():
    return RedirectResponse(url='/cars', status_code=303)


@app.get("/cars")
def get_cars(request: Request):
    cars = repo.get_all_cars()
    return templates.TemplateResponse("index.html", {"request": request, "cars": cars})

@app.get("/cars/new")
def get_new_car_form(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})


@app.post("/cars/new")
def post_car(
        name: str = Form(),
        year: int = Form()
):
    tmp = Car(id=0, name=name, year=year)
    repo.save_car(tmp)
    return RedirectResponse(url="/cars", status_code=303)

@app.get("/cars/search")
def search_car(request: Request, q: str =""):
    cars = repo.get_all_cars()
    filtered_cars = []
    for car in cars:
        if q.lower() in car.name.lower():
            filtered_cars.append(car)


    return templates.TemplateResponse("search.html",{"request": request, "cars": filtered_cars, "q":q})
