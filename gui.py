#!/usr/bin/python3

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa
# Constructor de objetos
'''
builder = Gtk.Builder()
# Archivo
glade_file = '/home/luisricardo/Gladetest/template.glade'
builder.add_from_file(glade_file)
# Obtener widgets por ID
win = builder.get_object("main_window")
boton1 = builder.get_object("boton1")
boton2 = builder.get_object("boton2")
boton3 = builder.get_object("boton3")
boton4 = builder.get_object("boton4")
label1 = builder.get_object("label1")

# Asociacion entre senal 'destroy' y la funcion Gtk.main_quit
win.connect('destroy', Gtk.main_quit)
boton1.connect('clicked',)
# Se muestran los widgets contenidos en la ventana (objeto win)
win.show_all()
# Se ejecuta el ciclo principal de GTK (Bloqueante)
Gtk.main()
'''


class GUI:  # Construye el GUI a base del archivo
    def __init__(self, file):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(file)
        self.handlers = {
            'onDestroy': Gtk.main_quit,
            'onButtonClicked': self.on_button_clicked,
                         }
        self.builder.connect_signals(self.handlers)

    def start(self):
        window = self.builder.get_object("main_window")
        window.show_all()
        Gtk.main()

    def on_button_clicked(self, button):
        id = Gtk.Buildable.get_name(button)
        image = self.builder.get_object('image')
        if id == 'instrucciones':
            pass
        elif id == 'iniciar':
            pass
        elif id == 'records':
            pass
        elif id == 'salir':
            pass


if __name__ == '__main__':
    gtk_object = GUI(
        '/home/luisricardo/Gladetest/template.glade'
    )
    gtk_object.start()
