#ARCHIVO PRINCIPAL CONTIENE LA BASE DEL PROGRAMA CON LA CLASE PRINCIPAL.
from kivy.lang import Builder
Builder.load_file("cargacontenedores.kv")
from kivy.config import Config
Config.set('kivy','keyboard_mode','systemanddock')
from kivy.app import App
from kivy.properties import StringProperty
#from kivy.lang import Builder    #contructor para los estilos
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
# Importar pantallas
from screens.pantalla_identificate import LoginScreen
from screens.pantalla_inicio import HomeScreen
from screens.pantalla_carga import CargaScreen
from screens.pantalla_admin import AdminScreen
from screens.pantalla_simulacion import SimuladorScreen

class LoginScreen(Screen):
    def validate_login(self, username, password):
        # Simulación: validación contra una base de datos o archivo
        if username == "admin" and password == "admin123":
            App.get_running_app().user_role = "admin"  # Asigna rol administrador
            self.manager.current = "admin"
        elif username == "user" and password == "user123":
            App.get_running_app().user_role = "user"  # Asigna rol usuario normal
            self.manager.current = "home"
        else:
            self.ids.error_label.text = "Credenciales inválidas"

class RoleScreenManager(ScreenManager):
    def switch_screen(self, screen_name ):
        user_role = App.get_running_app().user_role
        if screen_name == "admin" and user_role != "admin":
            print("Acceso denegado: No eres administrador")
        else:
            self.current = screen_name
class CargaContenedoresApp(App):
    user_role = StringProperty("user") 
    def build(self):
        self.title = "Carga de Contenedores"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))  # Pantalla de login
        sm.add_widget(HomeScreen(name="home"))    # Pantalla principal
        sm.add_widget(CargaScreen(name="carga")) # Pantalla de carga
        sm.add_widget(AdminScreen(name="admin")) # Pantalla de administrador
        sm.add_widget(SimuladorScreen(name="simulator"))    
        return sm
        

if __name__ == "__main__":
    CargaContenedoresApp().run()