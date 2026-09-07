#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Flask simples para servir o Floor Plan Generator.
"""

from flask import Flask, Response, jsonify, request

from floor_plan_generator import Dimension, FloorPlan, Point, Room, RoomType

app = Flask(__name__)

DEFAULT_ROOMS = [
    ("Área de Vendas", RoomType.SALES_FLOOR, 0, 0, 70, 60),
    ("Estoque", RoomType.STORAGE, 70, 0, 30, 40),
    ("Escritório", RoomType.OFFICE, 70, 40, 30, 20),
    ("Entrada", RoomType.ENTRANCE, 30, 60, 40, 20),
    ("Banheiro", RoomType.RESTROOM, 60, 60, 10, 10),
]


def build_default_plan() -> FloorPlan:
    plan = FloorPlan("Minha Loja Nova", Dimension(120, 100))
    for name, room_type, x, y, width, height in DEFAULT_ROOMS:
        plan.add_room(Room(name, room_type, Point(x, y), Dimension(width, height)))
    return plan


def plan_from_payload(data: dict) -> FloorPlan:
    dims = data["dimensions"]
    plan = FloorPlan(data["name"], Dimension(dims["width"], dims["height"]))
    for room in data.get("rooms", []):
        plan.add_room(
            Room(
                room["name"],
                RoomType(room["type"]),
                Point(room["x"], room["y"]),
                Dimension(room["width"], room["height"]),
            )
        )
    return plan


def plan_response(plan: FloorPlan) -> Response:
    if request.args.get("format") == "json":
        return Response(plan.to_json(), mimetype="application/json")
    return Response(plan.to_svg(), mimetype="image/svg+xml")


@app.get("/")
def index():
    return jsonify(
        {
            "service": "Floor Plan Generator API",
            "room_types": [t.value for t in RoomType],
            "endpoints": {
                "GET /api/plantas/exemplo": "Planta de exemplo (SVG; ?format=json para JSON)",
                "POST /api/plantas": "Gera uma planta a partir de JSON (SVG; ?format=json para JSON)",
            },
        }
    )


@app.get("/api/plantas/exemplo")
def planta_exemplo():
    return plan_response(build_default_plan())


@app.post("/api/plantas")
def criar_planta():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body é obrigatório"}), 400

    try:
        plan = plan_from_payload(data)
    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Dados inválidos: {exc}"}), 400

    return plan_response(plan)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
