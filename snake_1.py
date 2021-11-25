#! /usr/bin/python3

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk # noqa

class GUI:
    def __init__(self, file):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(file)

        self.handlers = {
            'onDestroy': Gtk.main_quit,
            'onButtonC': self.on_button_clicked,
        }

        self.builder.connect_signals(self.handlers)

    def start(self):
        window = self.builder.get_object('main_window')
        window.show_all()
        Gtk.main()

    def on_button_clicked(self,button):
        id = Gtk.Buildable.get_name(button)
        print('ID asociado: {}'.format(id))


if __name__ == '__main__':
    gtk_object = GUI('/home/newjulis/Documents/LaboratoriosPython/Snake/interfaz.glade')

    gtk_object.start()
