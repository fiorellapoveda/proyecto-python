#!/usr/bin/python3

# Puede ser necesario colocar el "/local/" entre usr y bin

"""
Proyecto de Python - Código de menú principal.
En este se encuentra la lógica referente al menú mostrado al ejecutar .py.

Este código fue realizado en máquinas virtuales con instalaciones de Ubuntu
version 20.04 y un repositorio en github.
Para ejecutarlo es necesario tener instalada pygame (sudo pip3 install pygame).

Estudiantes:
- Fiorella Poveda Chaves (B86145).
- Luis Ricardo Carmona Mora (B91646).
- Julián Zamora Villalobos (B07025).
"""

import gi
import snake
import instructions
import records

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa

class GUI:
# Construye el GUI a base del archivo de glade

    def __init__(self, file):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(file)
        self.handlers = {
            "onDestroy": Gtk.main_quit,
            "onButtonClicked": self.on_button_clicked,
        }
        self.builder.connect_signals(self.handlers)

    def start(self):
        window = self.builder.get_object("main_window")
        window.show_all()
        Gtk.main()

    def on_button_clicked(self, button):
        id = Gtk.Buildable.get_name(button)

        if id == "button_1":
            snake.runGame()
        elif id == "button_2":
            instructions.runInst()
        elif id == "button_3":
            records.runRecords()
        elif id == "button_4":
            window.destroy()

if __name__ == "__main__":
    gtk_object = GUI("archivos_glade/GUI.glade")
    gtk_object.start()
