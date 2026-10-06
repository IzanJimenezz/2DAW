import tkinter as tk
from tkinter import font

class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e2e2e")

        self.expresion = ""
        self.entrada_var = tk.StringVar()

        self._crear_widgets()
        self._configurar_teclado()

    def _crear_widgets(self):
        # Pantalla de entrada
        pantalla = tk.Entry(
            self.root,
            textvariable=self.entrada_var,
            font=("Arial", 24),
            bg="#1e1e1e",
            fg="white",
            bd=0,
            justify="right",
            state="readonly"
        )
        pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Definición de botones: (texto, fila, columna, color_fondo, color_texto, colspan)
        botones = [
            ("C", 1, 0, "#ff6b6b", "white", 1),
            ("⌫", 1, 1, "#ff6b6b", "white", 1),
            ("%", 1, 2, "#4ecdc4", "white", 1),
            ("÷", 1, 3, "#4ecdc4", "white", 1),

            ("7", 2, 0, "#3d3d3d", "white", 1),
            ("8", 2, 1, "#3d3d3d", "white", 1),
            ("9", 2, 2, "#3d3d3d", "white", 1),
            ("×", 2, 3, "#4ecdc4", "white", 1),

            ("4", 3, 0, "#3d3d3d", "white", 1),
            ("5", 3, 1, "#3d3d3d", "white", 1),
            ("6", 3, 2, "#3d3d3d", "white", 1),
            ("-", 3, 3, "#4ecdc4", "white", 1),

            ("1", 4, 0, "#3d3d3d", "white", 1),
            ("2", 4, 1, "#3d3d3d", "white", 1),
            ("3", 4, 2, "#3d3d3d", "white", 1),
            ("+", 4, 3, "#4ecdc4", "white", 1),

            ("0", 5, 0, "#3d3d3d", "white", 2),
            (".", 5, 2, "#3d3d3d", "white", 1),
            ("=", 5, 3, "#45b7d1", "white", 1),
        ]

        for texto, fila, columna, bg, fg, colspan in botones:
            btn = tk.Button(
                self.root,
                text=texto,
                font=("Arial", 18),
                bg=bg,
                fg=fg,
                bd=0,
                activebackground="#555555",
                activeforeground="white",
                command=lambda t=texto: self._click_boton(t)
            )
            btn.grid(
                row=fila, column=columna, columnspan=colspan,
                padx=3, pady=3, sticky="nsew"
            )

        # Configurar expansión de filas y columnas
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _configurar_teclado(self):
        self.root.bind("<Key>", self._tecla_presionada)
        self.root.bind("<Return>", lambda e: self._click_boton("="))
        self.root.bind("<Escape>", lambda e: self._click_boton("C"))
        self.root.bind("<BackSpace>", lambda e: self._click_boton("⌫"))

    def _tecla_presionada(self, event):
        tecla = event.char
        if tecla.isdigit() or tecla in "+-*/.%":
            self._agregar_a_expresion(tecla)
        elif event.keysym == "Return":
            self._click_boton("=")
        elif event.keysym == "Escape":
            self._click_boton("C")
        elif event.keysym == "BackSpace":
            self._click_boton("⌫")

    def _click_boton(self, valor):
        if valor == "C":
            self._limpiar()
        elif valor == "⌫":
            self._borrar()
        elif valor == "=":
            self._calcular()
        else:
            self._agregar_a_expresion(valor)

    def _agregar_a_expresion(self, valor):
        # Convertir símbolos visuales a operadores Python
        reemplazos = {"×": "*", "÷": "/", "%": "/100"}
        valor_python = reemplazos.get(valor, valor)
        self.expresion += valor_python
        self.entrada_var.set(self.expresion)

    def _limpiar(self):
        self.expresion = ""
        self.entrada_var.set("")

    def _borrar(self):
        self.expresion = self.expresion[:-1]
        self.entrada_var.set(self.expresion)

    def _calcular(self):
        try:
            resultado = eval(self.expresion)
            # Formatear resultado para evitar decimales innecesarios
            if isinstance(resultado, float):
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 10)
            self.entrada_var.set(str(resultado))
            self.expresion = str(resultado)
        except ZeroDivisionError:
            self.entrada_var.set("Error: div/0")
            self.expresion = ""
        except Exception:
            self.entrada_var.set("Error")
            self.expresion = ""


def main():
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
