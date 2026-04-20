from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QComboBox,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QStatusBar,
    )
from controllers.arduino_controller import ArduinoController
from core.ui_loader import load_ui


class ContadorWindow:
    def __init__(self, controller, username: str):
        self.controller = controller
        self.username = username
        self.window = load_ui("ui/contador.ui")

        if not isinstance(self.window, QMainWindow):
            raise RuntimeError("El archivo contador.ui no contiene un QMainWindow.")

        self.texto = self.window.findChild(QTextEdit, "texto")
        self.combo = self.window.findChild(QComboBox, "comboBox")
        self.contar_button = self.window.findChild(QPushButton, "contador")

        self._validate_widgets()
        
        self.arduino = ArduinoController()
        self.ultimo_valor_arduino = None
        self.puerto_actual = None
        self.contador_activo = False
        self.contador_Serial = 0
        
        self.statusbar = QStatusBar()
        self.window.setStatusBar(self.statusbar)
        
        self.label_puerto = QLabel("puerto: sin detectar")
        self.label_estado = QLabel("Arduino: --")
        self.label_valor = QLabel("Contador: 0")
        
        self.statusbar.addPermanentWidget(self.label_puerto)
        self.statusbar.addPermanentWidget(self.label_estado)
        self.statusbar.addPermanentWidget(self.label_valor)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.leer_arduino)
        
        self._setup_ui()
        self._connect_events()
        self.inicializar_arduino()

    def _validate_widgets(self) -> None:
        missing = []
        if self.texto is None:
            missing.append("texto")
        if self.combo is None:
            missing.append("comboBox")
        if self.contar_button is None:
            missing.append("contador")
        if missing:
            raise RuntimeError("Faltan objectName en contador.ui: " + ", ".join(missing))

    def _setup_ui(self) -> None:
        self.window.setWindowTitle(f"Contador - {self.username}")
        self.combo.addItems(["Caracteres", "Palabras", "Lineas", "Arduino"])
        
        self.texto.setReadOnly(True)

    def _connect_events(self) -> None:
        self.contar_button.clicked.connect(self.contar)
        
    def inicializar_arduino(self) -> None:
        puerto = self.arduino.detectar_puerto_arduino()
        
        if puerto is None:
            self.label_puerto.setText("Puerto: no se encontro Arduino")
            self.label_estado.setText("estado: sin conexion")
            return
        try:
            self.arduino.conectar(puerto,9600)
            self.puerto_actual = puerto
            self.label_puerto.setText("Estado: listo para contar")
        except Exception as e:
            self.puerto_actual = None
            self.label_puerto.setText("Puerto: error al abrir")
            self.label_estado.setText("Estado: sin conexion")
            QMessageBox.warning(
                self.window,
                "arduino",
                f"No se puede abrir el puerto {puerto},\n\nDetalle: {e}"
                                )
        
        
        
    def leer_arduino(self)->None:
        if not self.contador_activo:
            return     
        dato = self.arduino.leer_linea()       
        if not dato:
            return 
        dato_limpio = dato.strip()
        if dato_limpio.upper() == "PULSE" or dato_limpio == "1":
            self.contador_Serial += 1   
        else:
            try:
                self.contador_Serial = int(dato_limpio)
            except ValueError:
                return  
            self.label_valor.setText(f"Contador: {self.contador_Serial}")
            
            

    def show(self) -> None:
        self.window.show()

    def close(self) -> None:
        self.timer.stop()
        self.arduino.cerrar()
        self.window.close()

    def contar(self) -> None:
        option = self.combo.currentText()
        
        if option == "Arduino":
            if self.puerto_actual is None:
                QMessageBox.warning(
                    self.window,
                    "Arduino",
                    "No hay un Arduino detectado o conectado."
                )
                return
            
            if not self.contador_activo:
                self.contador_activo = True
                self.contador_Serial = 0
                self.label_estado.setText("Estado: contador...")
                self.label_valor.setText("contador: 0")
                self.contar_button.setText("detener conteo")
                self.timer.start(100)

            else:
                self.contador_actuvo = False
                self.time.stop()
                self.label_estado.setText(f"Estado: detenido en {self.contador_Serial}")
                self.contador_button("Contar")
                
            return
        
        text = self.texto.toPlainText()
                
                
           
        if option == "Caracteres":
            result = len(text)
        elif option == "Palabras":
            result = len([word for word in text.split() if word])
        else:
            result = len(text.splitlines()) if text else 0

        QMessageBox.information(self.window, "Resultado", f"{option}: {result}")
