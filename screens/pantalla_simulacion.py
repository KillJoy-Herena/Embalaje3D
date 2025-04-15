from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Mesh, Color, Translate, Rotate, PushMatrix, PopMatrix, Scale
from kivy.clock import Clock


class SimuladorScreen(Screen):
    def __init__(self, **kwargs):
        super(SimuladorScreen, self).__init__(**kwargs)
        self.contenedor_dim = None
        self.paquete_posiciones = []

        # Layout principal
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Botón para volver a la pantalla de carga
        btn_volver = Button(text="Volver a Carga")
        btn_volver.bind(on_press=lambda x: setattr(self.manager, "current", "carga"))
        layout.add_widget(btn_volver)

        # Widget 3D para el simulador
        self.simulador_3d = Simulador3D()
        layout.add_widget(self.simulador_3d)

        self.add_widget(layout)

    def cargar_datos(self, contenedor_dim, posiciones_optimizadas):
        """Carga las dimensiones del contenedor y las posiciones de los paquetes."""
        self.contenedor_dim = contenedor_dim
        self.paquete_posiciones = posiciones_optimizadas
        self.simulador_3d.cargar_escena(contenedor_dim, posiciones_optimizadas)
        for  paquete in posiciones_optimizadas:
             if len(paquete) != 3:
                 raise ValueError(f"Paquete invalido{paquete}")
             print(f"Procesando paquete con dimensiones: {paquete}")

class Simulador3D(Widget):
    def __init__(self, **kwargs):
        super(Simulador3D, self).__init__(**kwargs)
        self.rotation = [0, 0, 0]  # Rotación [x, y, z]
        self.zoom = 1.0  # Zoom inicial
        self.contenedor_dim = None
        self.paquete_posiciones = []

        Clock.schedule_interval(self.update_canvas, 1 / 60)

    def cargar_escena(self, contenedor_dim, paquete_posiciones):
        """Carga el contenedor y los paquetes en la escena 3D."""
        self.canvas.clear()
        self.contenedor_dim = contenedor_dim
        self.paquete_posiciones = paquete_posiciones

        # Dibujar contenedor traslúcido
        vertices, indices, colors = self.create_cube_data(*contenedor_dim)
        with self.canvas:
            PushMatrix()
            Color(0, 0, 1, 0.3)  # Azul traslúcido
            Mesh(vertices=vertices, indices=indices, mode="lines")
            PopMatrix()

        # Dibujar paquetes
        for pos in paquete_posiciones:
            width, height, depth, offset = pos
            vertices, indices, colors = self.create_cube_data(width, height, depth, offset)
            with self.canvas:
                Color(1, 0, 0, 0.5)  # Rojo traslúcido
                Mesh(vertices=vertices, indices=indices, mode="lines")

    def create_cube_data(self, width, height, depth, offset=(0, 0, 0)):
        """Crea los datos de un cubo."""
        x, y, z = offset
        vertices = [
            x, y, z,  # 0
            x + width, y, z,  # 1
            x + width, y + height, z,  # 2
            x, y + height, z,  # 3
            x, y, z + depth,  # 4
            x + width, y, z + depth,  # 5
            x + width, y + height, z + depth,  # 6
            x, y + height, z + depth,  # 7
        ]
        indices = [
            0, 1, 1, 2, 2, 3, 3, 0,  # Front face
            4, 5, 5, 6, 6, 7, 7, 4,  # Back face
            0, 4, 1, 5, 2, 6, 3, 7,  # Connecting edges
        ]
        colors = [1, 1, 1, 1] * 8
        return vertices, indices, colors

    def update_canvas(self, dt):
        """Actualiza la cámara y renderiza la escena."""
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            Translate(0, 0, -5)
            Rotate(angle=self.rotation[1], axis=(0, 1, 0))
            Scale(self.zoom)
            PopMatrix()

    def on_touch_move(self, touch):
        """Control de rotación interactiva."""
        self.rotation[1] += touch.dx * 0.5  # Rotar sobre eje Y

    def on_touch_down(self, touch):
        """Control de zoom interactivo."""
        if touch.button == "scrolldown":
            self.zoom += 0.1
        elif touch.button == "scrollup":
            self.zoom -= 0.1
        self.zoom = max(0.1, min(self.zoom, 3))  # Limitar el rango de zoom
