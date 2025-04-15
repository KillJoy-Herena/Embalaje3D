from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__( **kwargs)
        #grilla para stilos de la vista del login
        self.cols = 2
        # Etiqueta y campo de texto para el usuario
        self.add_widget(Label(text="Usuario:"))
        self.username_input = TextInput(multiline=False)
        self.add_widget(self.username_input)

        # Etiqueta y campo de texto para la contraseña
        self.add_widget(Label(text="Contraseña:"))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        # Botón para iniciar sesión
        self.login_button = Button(text="Iniciar Sesión")
        self.login_button.bind(on_press=self.verify_login)
        self.add_widget(self.login_button)

    def verify_login(self, instance):
        # Verificar las credenciales ingresadas
        username = self.username_input.text
        password = self.password_input.text

        # Validación básica
        if username == "admin" and password == "1234":
            self.show_popup("Éxito", "Inicio de sesión exitoso")
        else:
            self.show_popup("Error", "Credenciales incorrectas")

    def show_popup(self, title, message):
        # Mostrar un popup con un mensaje
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.5, 0.5))
        popup.open()


# Clase principal de la aplicación
""" class LoginApp(App):
    title = "Identificate"
    def build(self):
        return LoginScreen() """

""" 
# Ejecutar la aplicación
if __name__ == "__main__":
    LoginApp().run()
 """