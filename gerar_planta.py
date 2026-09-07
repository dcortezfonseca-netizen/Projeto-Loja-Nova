#!/usr/bin/env python3
# Gerador de Plantas Profissionais - Simples e Prático

import math

def gerar_planta(nome_loja, comodos):
    """
    Gera planta SVG profissional
    comodos = lista de (nome, x, y, largura, altura, tipo)
    """

    cores = {
        "vendas": "#FFE5B4",
        "estoque": "#D3D3D3",
        "escritorio": "#87CEEB",
        "entrada": "#98D8C8",
        "banheiro": "#B0E0E6"
    }

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1000">
  <rect width="1200" height="1000" fill="white" stroke="black" stroke-width="3"/>
  <text x="600" y="40" font-size="32" font-weight="bold" text-anchor="middle">{nome_loja}</text>
'''

    for comodo in comodos:
        nome, x, y, larg, alt, tipo = comodo
        cor = cores.get(tipo, "#FFFFFF")
        x_svg, y_svg = x * 5 + 50, y * 5 + 100
        w_svg, h_svg = larg * 5, alt * 5

        svg += f'''  <rect x="{x_svg}" y="{y_svg}" width="{w_svg}" height="{h_svg}" fill="{cor}" stroke="#333" stroke-width="2" opacity="0.8"/>
  <text x="{x_svg + w_svg/2}" y="{y_svg + h_svg/2}" text-anchor="middle" font-size="14" font-weight="bold">{nome}</text>
  <text x="{x_svg + w_svg/2}" y="{y_svg + h_svg/2 + 20}" text-anchor="middle" font-size="11" fill="gray">{larg}m x {alt}m</text>
'''

    svg += '''</svg>'''
    return svg

if __name__ == "__main__":
    comodos = [
        ("Área de Vendas",  0,  0,  70,  60, "vendas"),
        ("Estoque",        70,  0,  30,  40, "estoque"),
        ("Escritório",     70, 40,  30,  20, "escritorio"),
        ("Entrada",        30, 60,  40,  20, "entrada"),
        ("Banheiro",       60, 60,  10,  10, "banheiro"),
    ]

    svg = gerar_planta("Minha Loja Nova", comodos)

    with open("planta_loja.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("✅ Planta gerada: planta_loja.svg")
    print("   Abra no navegador para visualizar!")
