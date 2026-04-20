from controllers.arduino_controller import ArduinoController

class AltaController:
    def __init__(self):
        self.arduino = ArduinoController()
        
    def obtener_puertos_combo(self):
        puertos = self.arduino.listar_puertos()
        puerto_detectado = self.arduino.detectar_puerto_arduino()
        
        items = []
        
        for puerto in puertos:
            texto = f"{puerto['device']} - {puerto['description']}"
            items.append({
                "texto": texto,
                "device":puerto["device"],
                "seleccionado": puerto["device"] == puerto_detectado
            })
        return items