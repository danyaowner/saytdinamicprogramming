"""
Модуль решения задачи распределения ресурсов
методом динамического программирования.
"""

from typing import List, Dict, Any
import random


def solve_dp(
    n_projects: int,
    total_resources: int,
    efficiency_table: List[List[float]],
) -> Dict[str, Any]:
    """
    Решает задачу распределения ресурсов методом динамического программирования.

    Аргументы:
        n_projects: количество проектов
        total_resources: общее количество доступных ресурсов (дизайнеров)
        efficiency_table: таблица эффективности, где
            efficiency_table[i][x] — эффективность проекта i при выделении x ресурсов

    Возвращает:
        словарь с результатами:
            - distribution: список [x1, x2, ..., xn]
            - total_efficiency: суммарная эффективность
            - efficiencies: список эффективностей по проектам
            - bellman_table: таблица значений функций Беллмана
            - optimal_actions: таблица оптимальных решений по шагам
    """
    N = n_projects
    R = total_resources

    F = [[0.0] * (R + 1) for _ in range(N + 2)]
    x_opt = [[0] * (R + 1) for _ in range(N + 2)]

    # Прямой ход (от последнего проекта к первому)
    for k in range(N, 0, -1):
        for s in range(R + 1):
            best_value = -1.0
            best_x = 0
            for x in range(s + 1):
                value = efficiency_table[k - 1][x] + F[k + 1][s - x]
                if value > best_value:
                    best_value = value
                    best_x = x
            F[k][s] = best_value
            x_opt[k][s] = best_x

    # Обратный ход (восстановление оптимального решения)
    distribution = []
    s = R
    for k in range(1, N + 1):
        x = x_opt[k][s]
        distribution.append(x)
        s -= x

    efficiencies = [float(efficiency_table[i][distribution[i]]) for i in range(N)]

    bellman_table = []
    for s in range(R + 1):
        row: Dict[str, Any] = {"s": s}
        for k in range(1, N + 1):
            row[f"F{k}"] = float(F[k][s])
            row[f"x{k}"] = int(x_opt[k][s])
        bellman_table.append(row)

    optimal_actions = []
    s = R
    for k in range(1, N + 1):
        x = x_opt[k][s]
        optimal_actions.append({
            "step": k,
            "state_before": s,
            "action": x,
            "efficiency": float(efficiency_table[k - 1][x]),
            "state_after": s - x,
        })
        s -= x

    total_eff = float(F[1][R])
    calc_sum = sum(efficiencies)
    if abs(total_eff - calc_sum) > 0.001:
        total_eff = calc_sum

    return {
        "distribution": distribution,
        "total_efficiency": total_eff,
        "efficiencies": efficiencies,
        "bellman_table": bellman_table,
        "optimal_actions": optimal_actions,
        "n_projects": N,
        "total_resources": R,
    }


def generate_example() -> Dict[str, Any]:
    """Генерирует пример задачи из курсовой работы. 3 проекта, 5 дизайнеров."""
    return {
        "n_projects": 3,
        "total_resources": 5,
        "efficiency_table": [
            [0, 120, 210, 280, 340, 390],
            [0, 100, 190, 265, 330, 380],
            [0, 90, 170, 240, 300, 350],
        ],
        "project_names": ["Брендбук", "Веб-сайт", "Полиграфия"],
    }


def generate_random(n_projects: int = 4, total_resources: int = 8) -> Dict[str, Any]:
    """Генерирует случайный пример задачи."""
    project_types = [
        "Брендбук", "Веб-сайт", "Полиграфия", "Логотип",
        "Соцсети", "Упаковка", "Презентация", "Приложение",
        "Иллюстрация", "Анимация", "Инфографика", "Баннер",
    ]

    efficiency_table = []
    project_names = []

    for i in range(n_projects):
        base = random.randint(70, 130)
        name = project_types[i % len(project_types)]
        if i >= len(project_types):
            name = f"Проект {i + 1}"
        project_names.append(name)

        row = [0]
        for x in range(1, total_resources + 1):
            eff = int(base * (x ** 0.7) + random.randint(-5, 5))
            if x > 3:
                eff = int(eff * (1 - 0.05 * (x - 3)))
            eff = max(eff, row[-1])
            row.append(eff)
        efficiency_table.append(row)

    return {
        "n_projects": n_projects,
        "total_resources": total_resources,
        "efficiency_table": efficiency_table,
        "project_names": project_names,
    }
