"""Reutiliza bibliotecas ao invés de dar recal a cada import"""

import json

meses = [f'0{m}'[-2:] for m in range(1, 13)]
with open("configs.json", "r", encoding="utf-8") as file: configs = json.load(file)