from PySide6.QtCore import QCoreApplication, QDateTime, QTimer
from PySide6.QtWidgets import QMainWindow, QMessageBox
import re
import time
import traceback

from controllers.alta_controller import AltaController
from controllers.arduino_controller import ArduinoController
from models.alta_model import AltaModel
from models.recarga_model import RecargaModel
from views.administrador_view import AdminWindow
from views.dar_de_alta_view import AltaWindow
from views.login_view import LoginWindow
from views.recarga_view import RecargaWindow
from views.empleado_view import EmpleadoWindow


from views.cancelar_view import CancelarWindow
from views.sustituir_view import SustituirWindow

class AppController:
    """Controlador principal de ventanas."""

    UID_RE = re.compile(r"^[0-9A-F]{8,20}$")

    def __init__(self):
        self.current_window = None
        self.current_ui = None
        self.current_username = ""
        self.current_role = ""
        
        #recarga
        self.arduino = ArduinoController()
        self.recarga_model = RecargaModel()
        self.recarga_timer = None
        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0 
        
        #dar de alta
        self.alta_model = AltaModel()
        self.alta_timer = None
        self.uid_alta_actual = ""
        self.alta_pendiente = None

    def _normalizar_uid(self, uid: str) -> str:
        uid_limpia = uid.strip().upper()
        if len(uid_limpia) % 2 != 0:
            return ""
        if not self.UID_RE.fullmatch(uid_limpia):
            return ""
        return uid_limpia

    def show_login_window(self) -> None:
        self._close_current_window()
        self.current_window = LoginWindow(controller=self)
        self.current_window.show()

    def showLoginWindow(self) -> None:
        self.show_login_window()

    def show_window_by_role(self, username: str, role: str) -> None:
        self.current_username = username
        self.current_role = role.strip().lower()

        if self.current_role == "administrador":
            self.show_admin_window(username)
            return

        if self.current_role == "empleado":
            self.show_empleado_window(username)
            return

        self.show_login_window()

    def show_admin_window(self, username: str) -> None:
        self._close_current_window()
        self.current_window = QMainWindow()
        self.current_ui = AdminWindow()
        self.current_ui.setupUi(self.current_window)

        self.current_ui.botonalta.clicked.connect(self.show_alta_window)
        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)
        self.current_ui.botoncancelar.clicked.connect(self.show_cancelar_window)
        self.current_ui.botonsustituir.clicked.connect(self.show_sustituir_window)

        self.current_window.show()

    def show_empleado_window(self, username: str) -> None:
        self._close_current_window()
        self.current_window = QMainWindow()
        self.current_ui = EmpleadoWindow()
        self.current_ui.setupUi(self.current_window)

        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)

        self.current_window.show()

    def show_contador_window(self, username: str) -> None:
        self.show_admin_window(username)

    def showContadorWindow(self, username: str) -> None:
        self.show_contador_window(username)

    def show_alta_window(self) -> None:
        self._show_port_window(AltaWindow())
        self._configurar_alta_window()

    def show_recarga_window(self) -> None:
        self._show_port_window(RecargaWindow())
        self._configurar_recarga_window()
        
    def show_cancelar_window(self) -> None:
        self._show_port_window(CancelarWindow())
    
    def show_sustituir_window(self) -> None:
        self._show_port_window(SustituirWindow())

    def _show_port_window(self, ui) -> None:
        self._close_current_window()
        self.current_window = QMainWindow()
        self.current_ui = ui
        self.current_ui.setupUi(self.current_window)

        self._llenar_lista_puertos()

        if hasattr(self.current_ui, "botonregresar"):
            self.current_ui.botonregresar.clicked.connect(
                lambda: self.show_window_by_role(self.current_username, self.current_role)
            )

        self.current_window.show()

    def _llenar_lista_puertos(self) -> None:
        alta_controller = AltaController()
        puertos = alta_controller.obtener_puertos_combo()
        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is None:
            print(
                "[PUERTOS] La ventana actual no tiene combo de puertos "
                "llamado 'lista' ni 'comboBox'."
            )
            return

        lista_puertos.clear()

        if not puertos:
            lista_puertos.addItem("No hay puertos disponibles")
            return

        indice_detectado = 0

        for index, puerto in enumerate(puertos):
            lista_puertos.addItem(puerto["texto"], puerto["device"])
            if puerto["seleccionado"]:
                indice_detectado = index

        lista_puertos.setCurrentIndex(indice_detectado)

    def _combo_puertos_actual(self):
        if self.current_ui is None:
            return None

        return getattr(
            self.current_ui,
            "lista",
            getattr(self.current_ui, "comboBox", None)
        )
    
    def _close_current_window(self) -> None: 
        if isinstance(self.current_ui, RecargaWindow):
            if self.recarga_timer is not None:
                self.recarga_timer.stop()
            self.arduino.cerrar()

        if isinstance(self.current_ui, AltaWindow):
            if self.alta_timer is not None:
                self.alta_timer.stop()
            self.arduino.cerrar()

        if self.current_window is not None:
            self.current_window.close()
        
    def _configurar_recarga_window(self) -> None:
        ui = self.current_ui
        
        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        
        ui.texto4.setText("-")
        ui.texto5.setText("-")
        ui.texto6.setText("-")
        ui.texto1.setText("0.00")
        ui.texto2.setText("0.00")
        ui.texto7.setText("")
        
        monto = self._campo_monto_recarga()
        if monto is not None:
            monto.setReadOnly(False)
            monto.clear()
            monto.textChanged.connect(self._preview_saldo_nuevo)
        ui.botonrecargar.clicked.connect(self._ejecutar_recarga)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_recarga)
        
        if self.recarga_timer is None:
            self.recarga_timer = QTimer()
            self.recarga_timer.timeout.connect(self._leer_serial_recarga)
            
        self._conectar_puerto_recarga()
        self.recarga_timer.start(300)

    def _fallo_recarga(self, motivo: str, error: Exception | None = None) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self.current_ui.texto7.setText("Fallo recarga")

        if error is None:
            print(f"[RECARGA] Fallo recarga: {motivo}")
            return

        print(f"[RECARGA] Fallo recarga: {motivo}. Error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)
        
    def _conectar_puerto_recarga(self, *args) -> None:
        ui = self.current_ui
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None
        if not puerto:
            self._fallo_recarga("No hay puerto seleccionado")
            return
        
        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            self._fallo_recarga(f"No se pudo conectar al puerto {puerto}", e)
            
    def _leer_serial_recarga(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return
        
        ui = self.current_ui
        
        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            if linea.lower().startswith("sldo,"):
                self._procesar_saldo_recarga(linea)
            elif linea.startswith("ok,"):
                self._procesar_respuesta_recarga(linea)
            elif linea.lower().startswith("error"):
                self._fallo_recarga(f"Arduino reporto error: {linea}")

    def _procesar_saldo_recarga(self, linea: str) -> None:
        ui = self.current_ui

        try:
            _, uid, saldo_centavos, nombre = linea.split(",", 3)
            self.uid_actual = uid.strip()
            self.nombre_actual = nombre.strip()
            self.saldo_actual_centavos = int(saldo_centavos)

            ui.texto4.setText(self.uid_actual)
            ui.texto5.setText(self.nombre_actual)
            ui.texto1.setText(f"{self.saldo_actual_centavos / 100:.2f}")

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)
            if tarjeta_db:
                ui.texto6.setText(tarjeta_db["tipo_tarjeta"])
            else:
                ui.texto6.setText("No registrada")

            self._preview_saldo_nuevo()
        except Exception as e:
            self._fallo_recarga(f"No se pudo procesar la linea de saldo: {linea}", e)

    def _procesar_respuesta_recarga(self, linea: str) -> None:
        ui = self.current_ui

        try:
            partes = linea.split(",")
            if len(partes) < 4:
                self._fallo_recarga(f"Respuesta de recarga incompleta: {linea}")
                return

            _, uid, nuevo_saldo_centavos, folio = partes[:4]
            nuevo_saldo = int(nuevo_saldo_centavos) / 100
            monto = self.monto_pendiente_centavos / 100

            self.recarga_model.guardar_recarga_flexible(
                uid=uid,
                username=self.current_username,
                monto=monto,
                nuevo_saldo=nuevo_saldo,
                nombre_pasajero=self.nombre_actual,
                referencia=f"Folio: {folio}"
            )

            self.saldo_actual_centavos = int(nuevo_saldo_centavos)
            ui.texto1.setText(f"{nuevo_saldo:.2f}")
            ui.texto2.setText(f"{nuevo_saldo:.2f}")
            ui.texto7.setText("Recarga exitosa")
            monto = self._campo_monto_recarga()
            if monto is not None:
                monto.clear()
            self.monto_pendiente_centavos = 0
            
            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)
            if tarjeta_db:
                ui.texto6.setText(tarjeta_db["tipo_tarjeta"])
        except Exception as e:
            self._fallo_recarga(f"No se pudo procesar la respuesta de recarga: {linea}", e)

    def _campo_monto_recarga(self):
        if self.current_ui is None:
            return None

        return getattr(
            self.current_ui,
            "texto3",
            getattr(self.current_ui, "lineEdit", None)
        )

    def _texto_monto_recarga(self) -> str:
        monto = self._campo_monto_recarga()
        if monto is None:
            return ""

        if hasattr(monto, "toPlainText"):
            return monto.toPlainText().strip().replace(",", ".")

        return monto.text().strip().replace(",", ".")

    def _preview_saldo_nuevo(self, *args) -> None:
        ui = self.current_ui
        texto = self._texto_monto_recarga()

        if not texto:
            ui.texto2.setText(f"{self.saldo_actual_centavos / 100:.2f}")
            return

        try:
            monto = float(texto)
        except ValueError:
            ui.texto2.setText("Monto invalido")
            return

        nuevo = (self.saldo_actual_centavos / 100) + monto
        ui.texto2.setText(f"{nuevo:.2f}")
            
    def _ejecutar_recarga(self) -> None:
        ui = self.current_ui

        if not self.uid_actual:
            QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
            return

        texto_monto = self._texto_monto_recarga()
        if not texto_monto:
            QMessageBox.warning(self.current_window, "Error", "Captura el monto.")
            return

        try:
            monto = float(texto_monto)
        except ValueError:
            QMessageBox.warning(self.current_window, "Error", "Monto invalido.")
            return

        if monto <= 0:
            QMessageBox.warning(self.current_window, "Error", "El monto debe ser mayor a 0.")
            return

        self.monto_pendiente_centavos = round(monto * 100)

        try:
            comando = f"rc,{self.uid_actual},{self.monto_pendiente_centavos}"
            self.arduino.enviar_linea(comando)
            ui.texto7.setText("Enviando recarga...")
        except Exception as e:
            self._fallo_recarga("No se pudo enviar la recarga al Arduino", e)
            QMessageBox.critical(self.current_window, "Error", f"No se pudo enviar la recarga: {e}")
            
    def _configurar_alta_window(self) -> None:
        ui = self.current_ui

        self.uid_alta_actual = ""
        self.alta_pendiente = None

        ui.textonombre.clear()
        ui.textovigencia.clear()
        ui.textovigencia.setReadOnly(True)
        ui.normal.setChecked(True)

        self._actualizar_vigencia_desde_calendario()

        ui.calendario.selectionChanged.connect(self._actualizar_vigencia_desde_calendario)
        ui.botonguardar.clicked.connect(self._ejecutar_alta)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_alta)

        if self.alta_timer is None:
            self.alta_timer = QTimer()
            self.alta_timer.timeout.connect(self._leer_serial_alta)

        self._conectar_puerto_alta()
        self.alta_timer.start(300)
        
    def _actualizar_vigencia_desde_calendario(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui
        fecha = ui.calendario.selectedDate()

        ui.textovigencia.setPlainText(fecha.toString("dd-MM-yyyy"))
           
    def _conectar_puerto_alta(self, *args) -> None:
        ui = self.current_ui
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None

        if not puerto:
            return

        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f"[ALTA] Error al conectar al puerto {puerto}: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo conectar al puerto {puerto}: {e}"
            )
            
    def _leer_serial_alta(self, mostrar_errores: bool = True) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print("[ALTA]", linea)

            linea_minusculas = linea.lower()

            if linea_minusculas.startswith("sldo,"):
                try:
                    _, uid, saldo_centavos, nombre = linea.split(",", 3)
                    uid_detectada = self._normalizar_uid(uid)
                    if not uid_detectada:
                        print(f"[ALTA] UID invalida en trama sldo: {uid.strip()}")
                        continue

                    self.uid_alta_actual = uid_detectada
                    print(
                        "[ALTA] Tarjeta detectada "
                        f"UID={self.uid_alta_actual} "
                        f"saldo_centavos={saldo_centavos.strip()} "
                        f"nombre={nombre.strip()}"
                    )

                    if not ui.textonombre.toPlainText().strip() and nombre.strip():
                        ui.textonombre.setPlainText(nombre.strip())
                except Exception as e:
                    print(f"[ALTA] Error completo al procesar linea: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea_minusculas.startswith("uid,"):
                try:
                    _, uid = linea.split(",", 1)
                    uid_detectada = self._normalizar_uid(uid)
                    if not uid_detectada:
                        print(f"[ALTA] UID invalida: {uid.strip()}")
                        continue

                    self.uid_alta_actual = uid_detectada
                    print(f"[ALTA] Tarjeta detectada UID={self.uid_alta_actual}")
                except Exception as e:
                    print(f"[ALTA] Error completo al procesar UID: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea_minusculas.startswith("ok,"):
                try:
                    partes = linea.split(",")
                    if len(partes) >= 3:
                        uid_detectada = self._normalizar_uid(partes[2])
                        if not uid_detectada:
                            print(f"[ALTA] UID invalida en trama ok: {partes[2].strip()}")
                            continue

                        self.uid_alta_actual = uid_detectada
                        nombre = partes[3].strip() if len(partes) >= 4 else ""
                        print(
                            "[ALTA] Tarjeta detectada "
                            f"UID={self.uid_alta_actual} "
                            f"desde_trama={linea}"
                        )

                        if not ui.textonombre.toPlainText().strip() and nombre:
                            ui.textonombre.setPlainText(nombre)
                    else:
                        print(f"[ALTA] Trama ok incompleta: {linea}")
                except Exception as e:
                    print(f"[ALTA] Error completo al procesar ok: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea == "st":
                continue

            elif linea == "ok":
                if not self._guardar_alta_local_confirmada():
                    return

                QMessageBox.information(
                    self.current_window,
                    "Alta",
                    "Tarjeta dada de alta correctamente."
                )

            elif linea.lower().startswith("error"):
                # Error de lectura normal antes de enviar el alta
                if not self.alta_pendiente:
                    print(f"[ALTA] Error de lectura ignorado sin alta pendiente: {linea}")
                    continue

                self.alta_pendiente = None
                QMessageBox.warning(
                    self.current_window,
                    "Error",
                    f"El Arduino rechazo el alta: {linea}\n\n"
                    "No se guardo la tarjeta en la base local porque el alta "
                    "solo se persiste cuando Arduino confirma con 'ok'."
                )
                
    def _esperar_uid_alta_disponible(self) -> bool:
        print("[ALTA] No hay UID guardado. Solicitando UID real al Arduino con: uid")
        try:
            self.arduino.enviar_linea("uid")
        except Exception as e:
            print(f"[ALTA] No se pudo solicitar UID al Arduino: {e}")

        limite = time.monotonic() + 5.0
        while time.monotonic() < limite:
            self._leer_serial_alta(False)
            if self.uid_alta_actual:
                print(f"[ALTA] UID real detectada desde serial: {self.uid_alta_actual}")
                return True

            QCoreApplication.processEvents()
            time.sleep(0.05)

        print("[ALTA] No se recibió UID real desde serial.")
        return False

    def _guardar_alta_local_confirmada(self) -> bool:
        if not self.alta_pendiente:
            return True

        try:
            self.alta_model.guardar_alta_local(**self.alta_pendiente)
            print(
                "[ALTA] Alta guardada en DB local "
                f"UID={self.alta_pendiente['uid']}"
            )
            self.alta_pendiente = None
            return True
        except Exception as e:
            print(f"[ALTA] Error al guardar alta en DB local: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"El Arduino confirmo el alta, pero no se pudo guardar en la base local: {e}"
            )
            return False

    def _mostrar_error_uid_alta_no_disponible(self) -> None:
        QMessageBox.warning(
            self.current_window,
            "UID no disponible",
            "No hay una UID real disponible para dar de alta la tarjeta.\n\n"
            "La app no puede inventar una UID. Con el firmware actual no se "
            "puede obtener la UID de una tarjeta nueva si el Arduino no "
            "responde al comando 'uid' con una trama 'uid,<UID>'.\n\n"
            "Acerca o lee una tarjeta hasta que la app reciba una UID real "
            "por serial y vuelve a intentar."
        )

    def _ejecutar_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui

        self._leer_serial_alta(False)

        if not self.uid_alta_actual and not self._esperar_uid_alta_disponible():
            self._mostrar_error_uid_alta_no_disponible()
            return

        alias_tarjeta = ui.textonombre.toPlainText().strip().replace(",", " ")
        fecha = ui.calendario.selectedDate()

        # Formatos que ahora espera Arduino
        vigtarifa = fecha.toString("ddMMyy")          # 6 digitos
        vigencia12 = fecha.toString("ddMMyy") + "235959"   # 12 digitos

        if not alias_tarjeta:
            QMessageBox.warning(
                self.current_window,
                "Error",
                "Captura el nombre."
            )
            return

        if len(vigtarifa) != 6 or not vigtarifa.isdigit():
            QMessageBox.warning(
                self.current_window,
                "Error",
                "VIGTARIFA invalida."
            )
            return

        if len(vigencia12) != 12 or not vigencia12.isdigit():
            QMessageBox.warning(
                self.current_window,
                "Error",
                "VIGENCIA12 invalida."
            )
            return

        try:
            uid_alta = self._normalizar_uid(self.uid_alta_actual)
            if not uid_alta:
                self._mostrar_error_uid_alta_no_disponible()
                return

            # Mapeo segun el tipo seleccionado en la UI
            # Ajusta estos IDs si tu sistema usa otros valores
            if ui.preferencial.isChecked():
                no_tarjeta = "EU"   # Preferencial
                tipo_local = "EU"
            else:
                no_tarjeta = "NO"   # Normal
                tipo_local = "NO"

            id_tipo_tarjeta = "02"
            id_tarifa = "01"

            comando = (
                f"al,{uid_alta},{alias_tarjeta},{no_tarjeta},"
                f"{id_tipo_tarjeta},{id_tarifa},{vigtarifa},{vigencia12}"
            )

            print("[ALTA] Enviando:", comando)
            self.arduino.enviar_linea(comando)

            # Esto es para guardar en tu DB local cuando Arduino responda "ok"
            self.alta_pendiente = {
                "uid": uid_alta,
                "nombre_pasajero": alias_tarjeta,
                "tipo": tipo_local,
                "vigencia": vigencia12,
            }

        except Exception as e:
            print(f"[ALTA] Error completo al enviar alta: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo enviar el alta: {e}"
            )
