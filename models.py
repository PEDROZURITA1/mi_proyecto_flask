# models.py
# ------------------------------------------------------------
# POO + Colecciones para el sistema de inventario.
# - Producto: entidad con validaciones en setters (@property)
# - Inventario: lógica en memoria con colecciones:
#   * dict[int, Producto]  -> acceso O(1) por ID
#   * set[str]             -> control/validación rápida por nombre
#   * list[Producto]       -> listados intermedios y filtrados
#   * tuple[Producto, ...] -> retornos inmutables en consultas
# ------------------------------------------------------------
from __future__ import annotations
from typing import Dict, List, Tuple


class Producto:
    """Entidad de dominio que representa un ítem del inventario."""

    def __init__(self, id_: int, nombre: str, cantidad: int, precio: float) -> None:
        self._id = int(id_)
        self.nombre = nombre         # usa setter (valida)
        self.cantidad = cantidad     # usa setter (valida)
        self.precio = precio         # usa setter (valida)

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = (valor or "").strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            valor = int(valor)
        except Exception:
            raise ValueError("La cantidad debe ser un entero.")
        if valor < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = valor

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            valor = float(valor)
        except Exception:
            raise ValueError("El precio debe ser numérico.")
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    def __repr__(self) -> str:
        return (f"Producto(id={self.id}, nombre='{self.nombre}', "
                f"cantidad={self.cantidad}, precio={self.precio:.2f})")


class Inventario:
    """Lógica de inventario en memoria."""

    def __init__(self) -> None:
        self._items: Dict[int, Producto] = {}
        self._nombres: set[str] = set()

    def agregar(self, p: Producto) -> None:
        if p.id in self._items:
            raise KeyError(f"Ya existe un producto con id {p.id}.")
        self._items[p.id] = p
        self._nombres.add(p.nombre.lower())

    def eliminar(self, id_: int) -> None:
        prod = self._items.pop(id_, None)
        if prod is None:
            raise KeyError(f"No existe un producto con id {id_}.")
        nombre = prod.nombre.lower()
        if not any(nombre == x.nombre.lower() for x in self._items.values()):
            self._nombres.discard(nombre)

    def actualizar_cantidad(self, id_: int, nueva: int) -> None:
        if id_ not in self._items:
            raise KeyError(f"No existe un producto con id {id_}.")
        self._items[id_].cantidad = nueva

    def actualizar_precio(self, id_: int, nuevo: float) -> None:
        if id_ not in self._items:
            raise KeyError(f"No existe un producto con id {id_}.")
        self._items[id_].precio = nuevo

    def buscar_por_nombre(self, patron: str) -> List[Producto]:
        patron