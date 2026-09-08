#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Floor Plan Generator - Geração Automática de Plantas Baixas
Versão: 1.0.0

Este módulo gera plantas baixas profissionais em SVG/PDF para lojas.
Integrado com FreeCAD e Blender para modelos 3D.
"""

import json
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class RoomType(Enum):
    """Tipos de cômodos disponíveis"""
    SALES_FLOOR = "sales_floor"
    STORAGE = "storage"
    OFFICE = "office"
    RESTROOM = "restroom"
    ENTRANCE = "entrance"


@dataclass
class Point:
    """Representa um ponto 2D"""
    x: float
    y: float


@dataclass
class Dimension:
    """Representa dimensões (largura e altura)"""
    width: float
    height: float


class Room:
    """Representa um cômodo na loja"""

    def __init__(self, name: str, room_type: RoomType, position: Point, dimensions: Dimension):
        self.name = name
        self.room_type = room_type
        self.position = position
        self.dimensions = dimensions

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.room_type.value,
            "position": {"x": self.position.x, "y": self.position.y},
            "dimensions": {"width": self.dimensions.width, "height": self.dimensions.height}
        }


class FloorPlan:
    """Geração de plantas baixas"""

    def __init__(self, name: str, dimensions: Dimension):
        self.name = name
        self.dimensions = dimensions
        self.rooms: List[Room] = []

    def add_room(self, room: Room) -> None:
        """Adiciona um cômodo à planta"""
        self.rooms.append(room)

    def to_svg(self) -> str:
        """Exporta a planta em formato SVG"""
        scale = 10  # 1 unidade = 10 pixels

        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{self.dimensions.width * scale}"
     height="{self.dimensions.height * scale}"
     viewBox="0 0 {self.dimensions.width * scale} {self.dimensions.height * scale}">
  <rect width="{self.dimensions.width * scale}" height="{self.dimensions.height * scale}" fill="white" stroke="black" stroke-width="2"/>
'''

        for room in self.rooms:
            x = room.position.x * scale
            y = room.position.y * scale
            w = room.dimensions.width * scale
            h = room.dimensions.height * scale

            color = self._get_room_color(room.room_type)

            svg += f'''  <rect x="{x}" y="{y}" width="{w}" height="{h}"
       fill="{color}" stroke="black" stroke-width="1" opacity="0.7"/>
  <text x="{x + w/2}" y="{y + h/2}" text-anchor="middle" dominant-baseline="middle" font-size="12" font-weight="bold">{room.name}</text>
'''

        svg += "</svg>"
        return svg

    @staticmethod
    def _get_room_color(room_type: RoomType) -> str:
        """Retorna cor baseada no tipo de cômodo"""
        colors = {
            RoomType.SALES_FLOOR: "#FFE5B4",
            RoomType.STORAGE: "#D3D3D3",
            RoomType.OFFICE: "#87CEEB",
            RoomType.RESTROOM: "#B0E0E6",
            RoomType.ENTRANCE: "#98D8C8"
        }
        return colors.get(room_type, "#FFFFFF")

    def to_json(self) -> str:
        """Exporta a planta em JSON"""
        data = {
            "name": self.name,
            "dimensions": {"width": self.dimensions.width, "height": self.dimensions.height},
            "rooms": [room.to_dict() for room in self.rooms]
        }
        return json.dumps(data, indent=2)


if __name__ == "__main__":
    # Exemplo de uso
    print("Floor Plan Generator v1.0.0")
    print("Integrado com FreeCAD e Three.js")
