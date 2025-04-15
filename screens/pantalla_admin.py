from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functions_db import insertar_paquete, obtener_paquetes

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Formulario para agregar paquetes
        self.nombre_input = TextInput(hint_text="Nombre del paquete")
        self.peso_input = TextInput(hint_text="Peso (kg)")
        self.volumen_input = TextInput(hint_text="Volumen (m³)")
        btn_agregar = Button(text="Agregar Paquete")
        btn_agregar.bind(on_press=self.agregar_paquete)
        
        layout.add_widget(self.nombre_input)
        layout.add_widget(self.peso_input)
        layout.add_widget(self.volumen_input)
        layout.add_widget(btn_agregar)
        
        # Tabla para mostrar paquetes
        self.tabla = BoxLayout(orientation='vertical', size_hint_y=None)
        self.cargar_paquetes()
        layout.add_widget(self.tabla)
        
        self.add_widget(layout)

    def cargar_paquetes(self):
        self.tabla.clear_widgets()
        try:
           paquetes = obtener_paquetes()
           if not paquetes:
            self.tabla.add_widget(Button(text="No hay paquetes registrados."))
           else:
            for paquete in paquetes:
                self.tabla.add_widget(Button(text=f"{paquete[1]} - Peso: {paquete[2]}kg - Vol: {paquete[3]}m³"))
        except Exception as e:
            self.mostrar_error(f"Error al cargar paquetes: {str(e)}")

    def agregar_paquete(self, instance):
        nombre = self.nombre_input.text
        peso = float(self.peso_input.text)
        volumen = float(self.volumen_input.text)
        insertar_paquete(nombre, peso, volumen)
        self.cargar_paquetes()
