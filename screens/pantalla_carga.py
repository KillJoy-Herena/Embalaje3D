from ortools.linear_solver import pywraplp
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class CargaScreen(Screen):
    def __init__(self, **kwargs):
        super(CargaScreen, self).__init__(**kwargs)
        self.paquetes = []
        self.contenedor_dim = None

        # Layout principal
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Título
        self.title_label = Label(
            text="Gestión para la Carga de Contenedores",
            font_size=24,
            size_hint=(1, 0.1),
        )
        layout.add_widget(self.title_label)

        # Entradas para dimensiones del contenedor
        layout.add_widget(Label(text="Dimensiones del Contenedor (en metros):"))
        self.contenedor_width = TextInput(hint_text="Ancho", multiline=False)
        self.contenedor_height = TextInput(hint_text="Altura", multiline=False)
        self.contenedor_depth = TextInput(hint_text="Profundidad", multiline=False)
        layout.add_widget(self.contenedor_width)
        layout.add_widget(self.contenedor_height)
        layout.add_widget(self.contenedor_depth)

        # Entradas para dimensiones de los paquetes
        layout.add_widget(Label(text="Dimensiones de Paquete (en cm):"))
        self.paquete_width = TextInput(hint_text="Ancho", multiline=False)
        self.paquete_height = TextInput(hint_text="Altura", multiline=False)
        self.paquete_depth = TextInput(hint_text="Profundidad", multiline=False)
        layout.add_widget(self.paquete_width)
        layout.add_widget(self.paquete_height)
        layout.add_widget(self.paquete_depth)

        # Botón para agregar paquete
        btn_agregar = Button(text="Agregar al Contenedor")
        btn_agregar.bind(on_press=self.agregar_paquete)
        layout.add_widget(btn_agregar)

        # Botones de menú
        button_layout = BoxLayout(size_hint=(1, 0.2))
        btn_inicio = Button(text="Salir", on_press=self.volver_a_home)
        btn_simulador = Button(text="VISUALIZAR", on_press=self.visualizar_carga)
        button_layout.add_widget(btn_inicio)
        button_layout.add_widget(btn_simulador)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def agregar_paquete(self, instance):
        """Agrega un paquete a la lista."""
        try:
            paquete_dim = [
                float(self.paquete_width.text) / 100,  # Convertir a metros
                float(self.paquete_height.text) / 100,
                float(self.paquete_depth.text) / 100,
            ]
           # Validar que todos los valores sean positivos
            if any(d <= 0 for d in paquete_dim):
                raise ValueError("Las dimensiones del paquete deben ser mayores a 0.")
        
            # Asegurarse de que el paquete tiene tres dimensiones
            if len(paquete_dim) != 3:
                raise ValueError("El paquete debe tener exactamente tres dimensiones.")
            self.paquetes.append(paquete_dim)
            self.paquete_width.text = self.paquete_height.text = self.paquete_depth.text = ""
            print(f"Paquete agregado: {paquete_dim}")
        
        except ValueError:
            self.title_label.text = "Error: Dimensiones inválidas para el paquete."

    def visualizar_carga(self, instance):
        """Optimiza la carga y pasa los datos al simulador."""
        try:
            self.contenedor_dim = (
                float(self.contenedor_width.text),
                float(self.contenedor_height.text),
                float(self.contenedor_depth.text),
            )
            if any(d <= 0 for d in self.contenedor_dim):
               raise ValueError("Las dimensiones deben ser mayores a 0.")
            
             # Validar paquetes
            for paquete in self.paquetes:
                if len(paquete) != 3:
                   raise ValueError(f"Paquete inválido encontrado: {paquete}")
        
        # Continuar con la optimización y pasar datos al simulador
            posiciones_optimizadas = self.optimizar_carga(self.contenedor_dim, self.paquetes)
            self.manager.get_screen("simulator").cargar_datos(
                self.contenedor_dim, posiciones_optimizadas
                
            )
            print("envio la data")
            self.manager.current = "simulator"
            print("Redirigiendo a Simulacion")
           
        except ValueError as e:
           self.title_label.text = f"Error: {str(e)}"

    def volver_a_home(self, instance):
        """Regresa a la pantalla principal."""
        self.manager.current = "home"

    def optimizar_carga(self, contenedor, paquetes):
        """Resuelve el problema de optimización usando OR-Tools."""
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            self.title_label.text = "Error al crear el solver"
            return []

        # Variables
        num_paquetes = len(paquetes)
        x = [solver.BoolVar(f"x_{i}") for i in range(num_paquetes)]

        # Restricción de volumen del contenedor
        contenedor_volumen = (
            contenedor[0] * contenedor[1] * contenedor[2]
        )
        solver.Add(
            sum(
                x[i] * paquetes[i][0] * paquetes[i][1] * paquetes[i][2]
                for i in range(num_paquetes)
            )
            <= contenedor_volumen
        )

        # Función objetivo: Maximizar el volumen utilizado
        solver.Maximize(
            sum(
                x[i] * paquetes[i][0] * paquetes[i][1] * paquetes[i][2]
                for i in range(num_paquetes)
            )
        )

        # Resolver
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            posiciones = [paquetes[i] for i in range(len(paquetes)) if x[i].solution_value() == 1]
            return posiciones
        else:
            self.title_label.text = "No se encontró una solución óptima."
            return []
    