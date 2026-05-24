"""
FastAPI-приложение для визуализации задачи распределения дизайнерских ресурсов
методом динамического программирования.
"""

import json
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from dp_solver import solve_dp, generate_example, generate_random


class SolveRequest(BaseModel):
    n_projects: int
    total_resources: int
    efficiency_table: List[List[float]]
    project_names: Optional[List[str]] = None

app = FastAPI(
    title="Оптимизация распределения дизайнерских ресурсов",
    description="Визуализация решения задачи распределения дизайнеров между проектами методом динамического программирования",
)

# Serve static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/solve")
async def solve(payload: SolveRequest):
    """
    Решает задачу распределения ресурсов методом динамического программирования.
    """
    if payload.n_projects <= 0 or payload.total_resources <= 0:
        return JSONResponse(
            status_code=400,
            content={"error": "Количество проектов и ресурсов должно быть положительным"},
        )

    # Проверка размерности таблицы эффективности
    if len(payload.efficiency_table) != payload.n_projects:
        return JSONResponse(
            status_code=400,
            content={"error": f"Таблица эффективности должна содержать {payload.n_projects} строк"},
        )

    for i, row in enumerate(payload.efficiency_table):
        if len(row) != payload.total_resources + 1:
            return JSONResponse(
                status_code=400,
                content={"error": f"Строка {i} таблицы должна содержать {payload.total_resources + 1} значений"},
            )

    result = solve_dp(payload.n_projects, payload.total_resources, payload.efficiency_table)
    result["project_names"] = payload.project_names or [
        f"Проект {i + 1}" for i in range(payload.n_projects)
    ]

    return result


@app.post("/example")
async def example():
    """Возвращает пример задачи из курсовой работы."""
    return generate_example()


@app.post("/random")
async def random_example():
    """Генерирует случайный пример задачи."""
    return generate_random(n_projects=4, total_resources=8)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
