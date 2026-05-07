import reflex as rx
import httpx
from typing import List, Dict

API_URL = "http://127.0.0.1:8000"


class State(rx.State):
    metodo: str = "biseccion"
    menu_abierto: bool = False

    a_val: str = "0"
    b_val: str = "3"

    x0: str = "0"
    x1: str = "1"

    resultado: str = "Esperando..."
    iteraciones: List[Dict] = []

    def toggle_menu(self):
        self.menu_abierto = not self.menu_abierto

    def set_metodo(self, metodo):
        self.metodo = metodo
        self.menu_abierto = False

    def set_a_val(self, v): self.a_val = v
    def set_b_val(self, v): self.b_val = v
    def set_x0(self, v): self.x0 = v
    def set_x1(self, v): self.x1 = v

    def calcular(self):
        with httpx.Client() as client:

            if self.metodo == "biseccion":
                payload = {
                    "a": float(self.a_val),
                    "b": float(self.b_val)
                }
                data = client.post(f"{API_URL}/biseccion", json=payload).json()

            else:
                payload = {
                    "x0": float(self.x0),
                    "x1": float(self.x1)
                }
                data = client.post(f"{API_URL}/secante", json=payload).json()

            if "error" in data:
                self.resultado = data["error"]
                self.iteraciones = []
            else:
                self.resultado = (
                    f"Raíz aproximada: {data['resultado_final']['raiz']}"
                )
                self.iteraciones = data["iteraciones"]


def boton_verde(texto, **kwargs):
    return rx.button(
        texto,
        bg="green",
        color="white",
        width="220px",
        height="60px",
        font_size="22px",
        **kwargs
    )


def campo(label, value, setter):
    return rx.vstack(
        rx.text(
            label,
            color="white",
            font_size="18px",
            font_weight="bold"
        ),
        rx.input(
            value=value,
            on_change=setter,
            width="300px",
            height="55px",
            text_align="center"
        ),
        spacing="2",
        align="center"
    )


def tabla_biseccion():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Iteración"),
                rx.table.column_header_cell("a"),
                rx.table.column_header_cell("b"),
                rx.table.column_header_cell("c"),
                rx.table.column_header_cell("f(c)"),
                rx.table.column_header_cell("Error"),
            )
        ),
        rx.table.body(
            rx.foreach(
                State.iteraciones,
                lambda i: rx.table.row(
                    rx.table.cell(i["iteracion"]),
                    rx.table.cell(i["a"]),
                    rx.table.cell(i["b"]),
                    rx.table.cell(i["c"]),
                    rx.table.cell(i["fc"]),
                    rx.table.cell(i["error"]),
                )
            )
        ),
        width="100%"
    )


def tabla_secante():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Iteración"),
                rx.table.column_header_cell("x0"),
                rx.table.column_header_cell("x1"),
                rx.table.column_header_cell("x2"),
                rx.table.column_header_cell("Error"),
            )
        ),
        rx.table.body(
            rx.foreach(
                State.iteraciones,
                lambda i: rx.table.row(
                    rx.table.cell(i["iteracion"]),
                    rx.table.cell(i["x0"]),
                    rx.table.cell(i["x1"]),
                    rx.table.cell(i["x2"]),
                    rx.table.cell(i["error"]),
                )
            )
        ),
        width="100%"
    )


def index():
    return rx.box(

        rx.image(
            src="/logo.png",
            position="absolute",
            top="20px",
            right="30px",
            width="130px",
            z_index="10"
        ),

        rx.vstack(

            rx.box(
                rx.heading(
                    "MÉTODOS NUMÉRICOS",
                    color="white",
                    font_size="40px",
                    text_align="center",
                    width="100%"
                ),
                bg="rgba(10,20,70,0.85)",
                width="100%",
                padding="20px"
            ),

            # MENU CENTRADO
            rx.center(
                rx.box(
                    boton_verde("Menú", on_click=State.toggle_menu),

                    rx.cond(
                        State.menu_abierto,
                        rx.vstack(
                            boton_verde(
                                "Bisección",
                                on_click=lambda: State.set_metodo("biseccion")
                            ),
                            boton_verde(
                                "Secante",
                                on_click=lambda: State.set_metodo("secante")
                            ),
                            align="center"
                        )
                    )
                ),
                width="100%"
            ),

            rx.hstack(

                rx.box(
                    rx.vstack(
                        rx.heading(
                            rx.cond(
                                State.metodo == "biseccion",
                                "Método de Bisección",
                                "Método de Secante"
                            ),
                            color="white",
                            font_size="32px"
                        ),

                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Aplicación del método de bisección",
                                    color="white",
                                    font_size="24px"
                                ),
                                rx.text(
                                    "El método de bisección es un método numérico "
                                    "para encontrar raíces de funciones continuas "
                                    "dentro de un intervalo [a,b].",
                                    color="white",
                                    font_size="18px"
                                ),
                            ),
                            bg="rgba(0,80,50,0.6)",
                            padding="20px",
                            border_radius="12px",
                            width="100%"
                        ),

                        rx.cond(
                            State.metodo == "biseccion",
                            rx.vstack(
                                campo("Extremo inferior (a)", State.a_val, State.set_a_val),
                                campo("Extremo superior (b)", State.b_val, State.set_b_val),
                            ),
                            rx.vstack(
                                campo("Valor inicial (x0)", State.x0, State.set_x0),
                                campo("Valor inicial (x1)", State.x1, State.set_x1),
                            )
                        ),

                        boton_verde("Calcular", on_click=State.calcular),

                        rx.box(
                            rx.text(
                                State.resultado,
                                font_size="22px",
                                font_weight="bold",
                                text_align="center"
                            ),
                            bg="white",
                            padding="20px",
                            border_radius="12px",
                            width="100%"
                        ),

                        spacing="5",
                        align="center"
                    ),
                    bg="rgba(0,100,180,0.55)",
                    padding="25px",
                    border_radius="15px",
                    width="42%"
                ),

                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Tabla de Iteraciones",
                            font_size="34px",
                            text_align="center",
                            width="100%"
                        ),

                        rx.cond(
                            State.metodo == "biseccion",
                            tabla_biseccion(),
                            tabla_secante()
                        ),
                    ),
                    width="58%",
                    padding="20px"
                ),

                width="100%",
                spacing="5"
            ),

            width="100%"
        ),

        background_image="url('/fondo.png')",
        background_size="cover",
        min_height="100vh",
        padding="20px",
        position="relative"
    )


app = rx.App()
app.add_page(index)
