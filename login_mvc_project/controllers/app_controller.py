from pathlib import Path
import shutil

from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QSize, QTimer, Qt, QSettings, QRectF
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCalendarWidget,
    QDialog,
    QFileDialog,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QMenu,
    QToolButton,
    QLineEdit,

)
from datetime import datetime
from typing import Optional
import re
import time
import traceback
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QDoubleValidator

from core.sync_config import SYNC_INTERVAL_MS
from models.cancelar_model import CancelarModel
from models.sustituir_model import SustituirModel


from controllers.alta_controller import AltaController
from controllers.arduino_controller import ArduinoController
from controllers.login_controller import LoginController
from models.alta_model import AltaModel
from models.recarga_model import RecargaModel
from services.sync_service import SyncService
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
        
        #Login
        self.current_window = None
        self.current_ui = None
        self.current_username = ""
        self.current_role = ""
        
        self.settings = QSettings("RUMSA", "LoginMVC")

        # recarga
        self.arduino = ArduinoController()
        self.recarga_model = RecargaModel()
        self.recarga_timer = None
        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self.tarjeta_vencida = False

        # alta
        self.alta_model = AltaModel()
        self.alta_timer = None
        self.uid_alta_actual = ""
        self.alta_pendiente = None
        
        self.foto_alta_path = ""

        # sincronizacion
        self.sync_service = SyncService()
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self._sincronizar_pendientes)
        self.sync_timer.start(SYNC_INTERVAL_MS)
        
        # cancelar
        self.cancelar_model = CancelarModel()
        self.cancelar_timer = None
        self.uid_cancelar_actual = ""
        self.nombre_cancelar_actual = ""
        self.tarjeta_bloqueada = False
        
        #Sustituir
        self.sustituir_model = SustituirModel()
        self.sustituir_timer = None
        self.uid_sustituir_original = ""
        self.uid_sustituir_nueva = ""
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        self.popup_resultados_sustituir = None
        self.sustituir_pendiente = None
        
        
        
        
        

    def _normalizar_uid(self, uid: str) -> str:
        uid_limpia = uid.strip().upper()
        if len(uid_limpia) % 2 != 0:
            return ""
        if not self.UID_RE.fullmatch(uid_limpia):
            return ""
        return uid_limpia

    def _limpiar_alias_para_arduino(self, nombre: str, max_len: int = 24) -> str:
        import unicodedata
        import re as _re

        s = unicodedata.normalize("NFKD", nombre)
        s = s.encode("ascii", "ignore").decode("ascii")
        s = s.replace(",", " ")
        s = s.replace("\r", " ").replace("\n", " ")
        s = _re.sub(r"\s+", " ", s).strip()
        return s[:max_len]

    def _ajustar_alias_para_comando_alta(
        self,
        uid: str,
        alias: str,
        no_tarjeta: str,
        id_tipo_tarjeta: str,
        id_tarifa: str,
        vigtarifa: str,
        vigencia12: str,
    ) -> str:
        limite_serial_seguro = 60
        prefijo = f"al,{uid},"
        sufijo = f",{no_tarjeta},{id_tipo_tarjeta},{id_tarifa},{vigtarifa},{vigencia12}"
        max_alias = max(1, limite_serial_seguro - len(prefijo) - len(sufijo))
        return alias[:max_alias].strip()

    def _parsear_trama_saldo(self, linea: str):
        partes = linea.split(",")
        if len(partes) < 4 or partes[0].strip().lower() != "sldo":
            return None

        uid = partes[1].strip()
        saldo_centavos = partes[2].strip()
        campos_nombre = partes[3:]
        tipo_fisico = ""

        if len(campos_nombre) > 1 and campos_nombre[-1].strip().upper() in ("NO", "EU"):
            tipo_fisico = campos_nombre[-1].strip().upper()
            campos_nombre = campos_nombre[:-1]

        return {
            "uid": uid,
            "saldo_centavos": saldo_centavos,
            "nombre": ",".join(campos_nombre).strip(),
            "tipo_fisico": tipo_fisico,
        }

    def show_login_window(self) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = LoginWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_login_window()
        self.current_window.show()
        self._close_replaced_window(previous_window)
        QTimer.singleShot(500, self._sincronizar_pendientes)

    def showLoginWindow(self) -> None:
        self.show_login_window()
        
    def _cargar_recordarme_login(self)-> None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        recordarme = self.settings.value("login/recordarme", False, type=bool)
        usuario = self.settings.value("login/usuario","", type=str)
        
        self.current_ui.checkBoxRemember.setChecked(recordarme)
        
        if recordarme and usuario:
            self.current_ui.lineEditUser.setText(usuario)
            self.current_ui.lineEditPassword.setFocus()
        else:
            self.current_ui.lineEditUser.clear()
            self.current_ui.lineEditPassword.clear()
            self.current_ui.lineEditUser.setFocus()
            
    def _guardar_recordarme_login(self, username:str)->None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        if self.current_ui.checkBoxRemember.isChecked():
            self.settings.setValue("login/recordarme", True)
            self.settings.setValue("login/usuario", username)
        else:
            self.settings.setValue("login/recordarme", False)
            self.settings.remove("login/usuario")
        
        self.settings.sync()
        
    def _borrar_recordarme_si_desmarca(self, checked: bool) -> None:
        if checked:
            return
        
        self.settings.setValue("login/recordarme", False)
        self.settings.remove("login/usuario")
        self.settings.sync()
        

    def _configurar_login_window(self) -> None:
        ui = self.current_ui
        self.login_controller = LoginController()
        
        ui.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.accion_ver_password = ui.lineEditPassword.addAction(
            self._crear_icono_ojo(tachado=False),
            QLineEdit.ActionPosition.TrailingPosition
        )
        self.accion_ver_password.setToolTip("Mostrar Contraseña")
        self.accion_ver_password.triggered.connect(self._alternar_visibilidad_password)

        self._cargar_recordarme_login()

        ui.pushButtonLogin.clicked.connect(self._ejecutar_login)
        ui.pushButtonCancel.clicked.connect(self.current_window.close)
        ui.checkBoxRemember.toggled.connect(self._borrar_recordarme_si_desmarca)

        ui.pushButtonForgot.clicked.connect(
            lambda: QMessageBox.information(
                self.current_window,
                "Recuperar contrasena",
                "Contacta al administrador para recuperar tu contrasena.",
            )
        )
        ui.lineEditPassword.returnPressed.connect(self._ejecutar_login)
        ui.lineEditUser.returnPressed.connect(ui.lineEditPassword.setFocus)

    def _ejecutar_login(self) -> None:
        if not isinstance(self.current_ui, LoginWindow):
            return

        username = self.current_ui.lineEditUser.text().strip()
        password = self.current_ui.lineEditPassword.text().strip()

        ok, message = self.login_controller.authenticate(username, password)
        if not ok:
            QMessageBox.warning(self.current_window, "Login", message)
            return

        role = self.login_controller.get_role(username)
        if not role:
            QMessageBox.warning(
                self.current_window,
                "Login",
                "El usuario no tiene un rol asignado.",
            )
            return

        self._guardar_recordarme_login(username)

        self.show_window_by_role(username, role)


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
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = AdminWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_menu_usuario()

        self.current_ui.botonalta.clicked.connect(self.show_alta_window)
        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)
        self.current_ui.botoncancelar.clicked.connect(self.show_cancelar_window)
        self.current_ui.botonsustituir.clicked.connect(self.show_sustituir_window)

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def show_empleado_window(self, username: str) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = EmpleadoWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_menu_usuario()

        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

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
        self._configurar_cancelar_window()

    def show_sustituir_window(self) -> None:
        self._show_port_window(SustituirWindow())
        self._configurar_sustituir_window()

    def _show_port_window(self, ui) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = ui
        self.current_ui.setupUi(self.current_window)
        
        self._configurar_menu_usuario()

        self._llenar_lista_puertos()

        if hasattr(self.current_ui, "botonregresar"):
            self.current_ui.botonregresar.clicked.connect(
                lambda: self.show_window_by_role(self.current_username, self.current_role)
            )

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def _sincronizar_pendientes(self) -> None:
        if isinstance(self.current_ui, LoginWindow):
            return

        pendientes = self.sync_service.count_pending()
        if pendientes > 0:
            self._actualizar_estado_sync_ui("syncing", pendientes)

        resultado = self.sync_service.sync_pending_once()
        estado = resultado.get("state", "offline")
        pendientes_restantes = int(resultado.get("pending_after", 0) or 0)

        if estado == "connected":
            self._actualizar_estado_sync_ui("connected", pendientes_restantes)
            return

        if estado == "connected_with_errors":
            self._actualizar_estado_sync_ui("connected_with_errors", pendientes_restantes)
            return

        self._actualizar_estado_sync_ui("offline", pendientes_restantes)

    def _actualizar_estado_sync_ui(self, estado: str, pendientes: int = 0) -> None:
        if self.current_ui is None or not hasattr(self.current_ui, "labelEstadoConexion"):
            return

        if estado == "syncing":
            texto = f"● Sincronizando ({pendientes})" if pendientes else "● Sincronizando"
        elif estado == "connected":
            texto = f"● Conectado · Pendientes: {pendientes}" if pendientes else "● Conectado"
        elif estado == "connected_with_errors":
            texto = f"● Conectado · Pendientes: {pendientes}" if pendientes else "● Conectado"
        elif estado == "connecting":
            texto = "● Conectando"
        else:
            texto = f"● Sin conexión · Pendientes: {pendientes}" if pendientes else "● Sin conexión"

        self.current_ui.labelEstadoConexion.setText(texto)

        if isinstance(self.current_ui, AltaWindow):
            if estado == "offline":
                self._mostrar_error_alta_sin_internet()
            elif estado in ("connected", "connected_with_errors"):
                self.current_ui.labelEstadoConexion.setStyleSheet("color: green; font-weight: bold;")
                self._ocultar_error_alta_sin_internet()
                self._set_alta_inputs_enabled(True)
            else:
                self.current_ui.labelEstadoConexion.setStyleSheet("color: #245E91; font-weight: bold;")
                self._ocultar_error_alta_sin_internet()
                self._set_alta_inputs_enabled(False)

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

        return (
        getattr(self.current_ui, "lista", None)
        or getattr(self.current_ui, "comboBox", None)
        or getattr(self.current_ui, "puerto", None)
    )

    def _release_current_window(self):
        if isinstance(self.current_ui, RecargaWindow):
            if self.recarga_timer is not None:
                self.recarga_timer.stop()
            self.arduino.cerrar()

        if isinstance(self.current_ui, AltaWindow):
            if self.alta_timer is not None:
                self.alta_timer.stop()
            self.arduino.cerrar()
        
        if isinstance(self.current_ui, CancelarWindow):
            if self.cancelar_timer is not None:
                self.cancelar_timer.stop()
            self.arduino.cerrar()
            
        if isinstance(self.current_ui, SustituirWindow):
            if self.sustituir_timer is not None:
                self.sustituir_timer.stop()
            self.arduino.cerrar()
            self.popup_resultados_sustituir = None

        previous_window = self.current_window
        self.current_window = None
        self.current_ui = None
        return previous_window

    def _close_replaced_window(self, previous_window) -> None:
        if previous_window is not None:
            previous_window.close()

    def _close_current_window(self) -> None:
        previous_window = self._release_current_window()
        self._close_replaced_window(previous_window)

    # =========================
    # RECARGA
    # =========================

    def _configurar_recarga_window(self) -> None:
        ui = self.current_ui
        
        self._aplicar_estilos_sustituir()

        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self.tarjeta_vencida = False

        ui.texto4.setText("-")
        ui.texto5.setText("-")
        ui.texto6.setText("-")
        ui.texto1.setText("0.00")
        ui.texto2.setText("0.00")
        ui.texto7.setText("")
        ui.botonrecargar.setEnabled(True)
        
        self.oficina_recarga_actual = ""
        self._llenar_oficinas_recarga()
        

        monto = self._campo_monto_recarga()
        if monto is not None:
            monto.setReadOnly(False)
            monto.clear()
            validador_moto = QDoubleValidator(0.01, 99999.99, 2)
            validador_moto.setNotation(QDoubleValidator.StandardNotation)
            monto.setValidator(validador_moto)
            monto.setPlaceholderText("0.00")
            monto.setMaxLength(7)
            
            monto.textChanged.connect(self._preview_saldo_nuevo)
            monto.editingFinished.connect(self._formatear_monto_recarga)

        ui.botonrecargar.clicked.connect(self._ejecutar_recarga)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_recarga)

        if self.recarga_timer is None:
            self.recarga_timer = QTimer()
            self.recarga_timer.timeout.connect(self._leer_serial_recarga)

        self._conectar_puerto_recarga()
        self.recarga_timer.start(300)
        
    
   

    def _llenar_oficinas_recarga(self) -> None:
        ui = self.current_ui
        
        if ui is None or not hasattr(ui, "listaoficina"):
            return
        
        ui.listaoficina.clear()
        ui.listaoficina.addItem("Selecciona oficina", "")
        
        oficinas = [
            "Oficina Centro",
            "Oficina Terminal",
            "Oficina Norte",
        ]
        
        for oficina in oficinas:
            ui.listaoficina.addItem(oficina, oficina)
            
    
    def _oficina_seleccionada_recarga(self) -> str:
        ui = self.current_ui
        
        if ui is None or not hasattr(ui, "listaoficina"):
            return ""
        
        oficina = ui.listaoficina.currentData()
        
        if oficina is None:
            oficina = ui.listaoficina.currentText()
        
        return str(oficina).strip()        
        
    
    def _parsear_vigencia_tarjeta(self, vigencia_raw) -> Optional[datetime]:
        if vigencia_raw is None:
            return None

        texto_vigencia = str(vigencia_raw).strip()
        if not texto_vigencia:
            return None

        formatos = (
            "%d%m%y%H%M%S",
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        )

        for formato in formatos:
            try:
                return datetime.strptime(texto_vigencia, formato)
            except ValueError:
                continue

        return None

    def _actualizar_estado_vencimiento_tarjeta(self, tarjeta_db) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui
        monto = self._campo_monto_recarga()

        vigencia_raw = tarjeta_db["vigencia"] if tarjeta_db else None
        fecha_vigencia = self._parsear_vigencia_tarjeta(vigencia_raw)

        self.tarjeta_vencida = bool(
            fecha_vigencia and fecha_vigencia <= datetime.now()
        )

        if self.tarjeta_vencida:
            if monto is not None:
                monto.clear()
                monto.setEnabled(False)

            ui.texto2.setText(f"{self.saldo_actual_centavos / 100:.2f}")
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText(
                "Tarjeta vencida "
                f"({fecha_vigencia.strftime('%d-%m-%Y %H:%M:%S')})."
            )
            ui.texto7.setStyleSheet("color: red; font-weight: bold;")
            return

        if monto is not None and not getattr(self, "tarjeta_bloqueada", False):
            monto.setEnabled(True)

        if not getattr(self, "tarjeta_bloqueada", False):
            ui.botonrecargar.setEnabled(True)

        if "Tarjeta vencida" in ui.texto7.text():
            ui.texto7.setText("")
            ui.texto7.setStyleSheet("")
            
            

    def _fallo_recarga(self, motivo: str, error: Optional[Exception] = None) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self.current_ui.texto7.setText("Fallo recarga")
            self.current_ui.texto7.setMaximumHeight(50)
            self.current_ui.texto7.setStyleSheet("""
                color: red;
                font-size: 24px;
                font-weight: bold;
            """)
            

        if error is None:
            print(f"[RECARGA] Fallo recarga: {motivo}")
            return

        print(f"[RECARGA] Fallo recarga: {motivo}. Error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)

    def _conectar_puerto_recarga(self, *args) -> None:
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

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            if linea.lower().startswith("sldo,"):
                self._procesar_saldo_recarga(linea)
            elif linea.startswith("ok,"):
                self._procesar_respuesta_recarga(linea)
            elif linea == "st":
                self._limpiar_interfaz_por_retiro_tarjeta()
            elif linea.lower().startswith("error"):
                self._fallo_recarga(f"Arduino reporto error: {linea}")
                    
    def _procesar_saldo_recarga(self, linea: str) -> None:
        ui = self.current_ui

        try:
            saldo = self._parsear_trama_saldo(linea)
            if not saldo:
                self._fallo_recarga(f"Trama sldo incompleta: {linea}")
                return

            tipo_fisico = saldo["tipo_fisico"]
            self.uid_actual = saldo["uid"]
            self.nombre_actual = saldo["nombre"]
            self.saldo_actual_centavos = int(saldo["saldo_centavos"])

            ui.texto4.setText(self.uid_actual or "-")
            ui.texto5.setText(self.nombre_actual or "-")
            ui.texto1.setText(f"{self.saldo_actual_centavos / 100:.2f}")

            tipo_desde_tarjeta = ""

            if tipo_fisico == "NO":
                tipo_desde_tarjeta = "Normal"
            elif tipo_fisico == "EU":
                tipo_desde_tarjeta = "Preferencial"
            

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)

            if tarjeta_db:
                ui.texto6.setText(tipo_desde_tarjeta or tarjeta_db["tipo_tarjeta"])

                if int(tarjeta_db["en_lista_negra"]) == 1:
                    self._aplicar_bloqueo_lista_negra_recarga(True)
                    return
                else:
                    self._aplicar_bloqueo_lista_negra_recarga(False)

               
                self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)

            else:
                ui.texto6.setText(tipo_desde_tarjeta or "No registrada")
                self.tarjeta_vencida = False
                self._aplicar_bloqueo_lista_negra_recarga(False)

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
                oficina=self.oficina_recarga_actual,
                referencia=f"Folio: {folio}"
            )
            self._sincronizar_pendientes()

            self.saldo_actual_centavos = int(nuevo_saldo_centavos)
            ui.texto1.setText(f"{nuevo_saldo:.2f}")
            ui.texto2.setText(f"{nuevo_saldo:.2f}")
            
            ui.texto7.clear()
            ui.texto7.setMaximumHeight(80)
            
            if hasattr(ui.texto7, "setPlainText"):
                ui.texto7.setPlainText("Recarga Exitosa")
            else:
                ui.texto7.setText("Recarga Exitosa")
                
            ui.texto7.setStyleSheet("""
                color: #008000;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
                border: none;
                                    """)
            
            ui.texto7.repaint()
            QTimer.singleShot(2500, self._limpiar_mensaje_recarga_exitosa)
            

            monto = self._campo_monto_recarga()
            if monto is not None:
                monto.clear()

            self.monto_pendiente_centavos = 0

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)
            if tarjeta_db:
                ui.texto6.setText(tarjeta_db["tipo_tarjeta"])
            self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)

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

        tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)

        if tarjeta_db and int(tarjeta_db["en_lista_negra"]) == 1:
            self._aplicar_bloqueo_lista_negra_recarga(True)
            QMessageBox.warning(
                self.current_window,
                "Tarjeta en lista negra",
                "La tarjeta está en lista negra y no se puede recargar."
            )
            return
        else:
            self._aplicar_bloqueo_lista_negra_recarga(False)

    
        self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)
        if self.tarjeta_vencida:
            QMessageBox.warning(
                self.current_window,
                "Tarjeta vencida",
                "La tarjeta está vencida y no se puede recargar."
            )
            return
        
        oficina = self._oficina_seleccionada_recarga()
        
        if not oficina:
            QMessageBox.warning(
                self.current_window,
                "Oficina requerida",
                "Selecciona una oficina."
            )
            return
        self.oficina_recarga_actual = oficina

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
            ui.texto7.setMaximumHeight(40)
            ui.texto7.setStyleSheet("""
                color: #1f5fa8;
                font-size: 18px;
                font-weight: bold;
            """)
            
            
        except Exception as e:
            self._fallo_recarga("No se pudo enviar la recarga al Arduino", e)
            QMessageBox.critical(self.current_window, "Error", f"No se pudo enviar la recarga: {e}")
            
    # =========================
    #           ALTA
    # =========================
    def _hay_internet_para_alta(self) -> bool:
        try:
            return self.sync_service.ping()
        except Exception:
            return False


    def _mostrar_error_alta_sin_internet(self) -> None:
        ui = self.current_ui
        ui.labelEstadoConexion.setStyleSheet("color: red; font-weight: bold;")
        ui.labelEstadoConexion.setText(
            "Sin conexion"
        )
        if hasattr(ui, "mensajeInternet"):
            ui.mensajeInternet.setText("Sin conexion a internet, intente mas tarde.")
            ui.mensajeInternet.setVisible(True)
        self._set_alta_inputs_enabled(False)


    def _ocultar_error_alta_sin_internet(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        if hasattr(self.current_ui, "mensajeInternet"):
            self.current_ui.mensajeInternet.setText("")
            self.current_ui.mensajeInternet.setVisible(False)


    def _set_alta_inputs_enabled(self, enabled: bool) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui
        for nombre_widget in (
            "textonombre",
            "textocurp",
            "textofechanacimiento",
            "textovigencia",
            "pushButton",
            "normal",
            "preferencial",
            "calendario",
            "botonsubir",
            "botontomar",
            "botonguardar",
        ):
            if hasattr(ui, nombre_widget):
                getattr(ui, nombre_widget).setEnabled(enabled)
                
    
    def _limpiar_forulario_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return
        
        ui = self.current_ui
        
        self.uid_alta_actual = ""
        self.alta_pendiente = None
        self.foto_alta_path = ""
        
        widgets_con_senales = [
            ui.textonombre,
            ui.textocurp,
            ui.textofechanacimiento,
            ui.textovigencia,
            ui.calendario,
            ui.normal,
            ui.preferencial
        ]
        
        for widget in widgets_con_senales:
            widget.blockSignals(True)
            
        try:
            ui.textonombre.clear()
            ui.textocurp.clear()
            ui.textofechanacimiento.clear()
            
            if hasattr(ui, "curpstatus"):
                ui.curpstatus.clear()
                
            ui.normal.setChecked(True)
            ui.preferencial.setChecked(False)
            
            ui.calendario.setSelectedDate(QDate.currentDate())
            ui.textovigencia.setPlainText(
                ui.calendario.selectedDate().toString("dd-MM-yyyy")
            )
            
            ui.fotoimagen.clear()
            ui.fotoimagen.setText("Sin foto")
            
            ui.textonombre.setFocus()
            
        finally:
            for widget in widgets_con_senales:
                widget.blockSignals(False)
    
     

    def _seleccionar_foto_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui

        archivo, _ = QFileDialog.getOpenFileName(
            self.current_window,
            "Seleccionar foto",
            "",
            "Imagenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if not archivo:
            return

        carpeta_fotos = Path(__file__).resolve().parent.parent / "data" / "fotos"
        carpeta_fotos.mkdir(exist_ok=True)

        origen = Path(archivo)
        destino = carpeta_fotos / origen.name
        shutil.copy2(origen, destino)

        self.foto_alta_path = str(destino)

        pixmap = QPixmap(str(destino))
        ui.fotoimagen.setPixmap(
            pixmap.scaled(200, 200)
        )


    def _limpiar_foto_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        self.foto_alta_path = ""
        self.current_ui.fotoimagen.clear()
        self.current_ui.fotoimagen.setText("Sin foto")


    def _mostrar_calendario_nacimiento(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        dialog = QDialog(self.current_window)
        dialog.setWindowTitle("Seleccionar fecha")

        layout = QVBoxLayout(dialog)
        calendario = QCalendarWidget(dialog)
        layout.addWidget(calendario)

        def seleccionar_fecha():
            fecha = calendario.selectedDate()
            self.current_ui.textofechanacimiento.setPlainText(
                fecha.toString("dd-MM-yyyy")
            )
            dialog.accept()

        calendario.clicked.connect(seleccionar_fecha)

        dialog.exec()
        
    

    def _configurar_alta_window(self) -> None:
        ui = self.current_ui

        self.uid_alta_actual = ""
        self.alta_pendiente = None

        ui.textonombre.clear()
        ui.textovigencia.clear()
        
        ui.textocurp.textChanged.connect(self._limitar_curp_alta)
        ui.textonombre.textChanged.connect(self._solo_letras_espacios_nombre_alta)
        ui.textofechanacimiento.textChanged.connect(self._formatear_fecha_nacimiento_alta)
        
        if hasattr(ui, "curpstatus"):
            ui.curpstatus.setStyleSheet("color: red; font-weight: bold;")
            if hasattr(ui.curpstatus, "setPlainText"):
                ui.curpstatus.setPlainText("")
            else:
                ui.curpstatus.setText("")

        self._ocultar_error_alta_sin_internet()
        self._set_alta_inputs_enabled(False)

        ui.textovigencia.setReadOnly(True)
        ui.normal.setChecked(True)
        
        self.foto_alta_path = ""
        
        ui.fotoimagen.setText("Sin foto")
        ui.fotoimagen.setScaledContents(True)
  
        ui.botonsubir.clicked.connect(self._seleccionar_foto_alta)
        ui.botontomar.clicked.connect(self._limpiar_foto_alta)

        # ESTE ES EL QUE TE FALTA
        ui.pushButton.clicked.connect(self._mostrar_calendario_nacimiento)

        icono_calendario = Path(__file__).resolve().parent.parent / "assets" / "calendario.png"

        if icono_calendario.exists():
            ui.pushButton.setIcon(QIcon(str(icono_calendario)))
            ui.pushButton.setIconSize(QSize(24, 24))
            ui.pushButton.setText("")
        else:
            print(f"No se encontró el icono: {icono_calendario}")

        ui.labelEstadoConexion.setStyleSheet("color: #245E91; font-weight: bold;")
        ui.labelEstadoConexion.setText("● Listo")
        

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
        ui.textovigencia.setPlainText(f"{fecha.toString('dd-MM-yyyy')}")

    def _conectar_puerto_alta(self, *args) -> None:
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
                    saldo = self._parsear_trama_saldo(linea)
                    if not saldo:
                        print(f"[ALTA] Trama sldo incompleta: {linea}")
                        continue

                    uid = saldo["uid"]
                    saldo_centavos = saldo["saldo_centavos"]
                    nombre = saldo["nombre"]
                    uid_detectada = self._normalizar_uid(uid)
                    if not uid_detectada:
                        print(f"[ALTA] UID invalida en trama sldo: {uid}")
                        continue

                    self.uid_alta_actual = uid_detectada

                    print(
                        "[ALTA] Tarjeta detectada "
                        f"UID={self.uid_alta_actual} "
                        f"saldo_centavos={saldo_centavos} "
                        f"nombre={nombre}"
                    )

                    if not ui.textonombre.toPlainText().strip() and nombre.strip() and nombre.strip() != "-":
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

            elif linea_minusculas == "ok,alta":
                if not self.alta_pendiente:
                    print("[ALTA] Llego ok,alta pero no hay alta pendiente.")
                    continue

                try:
                    uid = self.alta_pendiente["uid"]
                    nombre = self.alta_pendiente.get(
                        "alias_tarjeta",
                        self.alta_pendiente["nombre_pasajero"],
                    )

                    comando_nombre = f"nm,{uid},{nombre}"
                    print("[ALTA] Enviando nombre:", comando_nombre)
                    self.arduino.enviar_linea(comando_nombre)

                    self.alta_pendiente["fase"] = "esperando_nombre"

                except Exception as e:
                    print(f"[ALTA] Error al enviar nombre: {e}")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self.alta_pendiente = None

                    if mostrar_errores:
                        QMessageBox.critical(
                            self.current_window,
                            "Error",
                            f"La tarjeta se dio de alta, pero no se pudo enviar el nombre: {e}"
                        )

            elif linea_minusculas == "ok,nombre":
                if not self.alta_pendiente:
                    print("[ALTA] Llego ok,nombre pero no hay alta pendiente.")
                    continue

                if not self._guardar_alta_local_confirmada():
                    return

                QMessageBox.information(
                    self.current_window,
                    "Alta",
                    "Tarjeta dada de alta correctamente."
                )

            elif linea_minusculas.startswith("ok,"):
                # compatibilidad para lecturas tipo:
                # ok,300426235959,0413243AC75A80,juan
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
                self._limpiar_interfaz_por_retiro_tarjeta()
                continue

            elif linea == "ok":
                # compatibilidad con firmware viejo
                if not self.alta_pendiente:
                    continue

                if not self._guardar_alta_local_confirmada():
                    return

                QMessageBox.information(
                    self.current_window,
                    "Alta",
                    "Tarjeta dada de alta correctamente."
                )

            elif linea_minusculas.startswith("error"):
                errores_de_lectura_automatica = {
                    "error,estado_tisc4",
                    "error,estado_tisc3",
                    "error,estado_tisc2",
                    "error,vigencia0",
                    "error,leer_saldo",
                    "error,leer_saldo2",
                }

                if linea_minusculas in errores_de_lectura_automatica:
                    print(f"[ALTA] Error automatico de verSaldo ignorado durante alta: {linea}")
                    continue

                if "error en las 3 aplicaciones" in linea_minusculas:
                    if self.alta_pendiente:
                        reintentos = self.alta_pendiente.get("reintentos_alta", 0)
                        comando = self.alta_pendiente.get("comando_alta")

                        if comando and reintentos < 2:
                            self.alta_pendiente["reintentos_alta"] = reintentos + 1

                            print(
                                "[ALTA] Reintentando alta por error en aplicaciones "
                                f"intento {reintentos + 1}: {comando}"
                            )

                            QTimer.singleShot(
                                1000,
                                lambda c=comando: self.arduino.enviar_linea(c)
                            )
                            continue
                    
                if not self.alta_pendiente:
                    print(f"[ALTA] Error de lectura ignorado sin alta pendiente: {linea}")
                    continue

                fase = self.alta_pendiente.get("fase", "desconocida")
                self.alta_pendiente = None

                if mostrar_errores:
                    QMessageBox.warning(
                        self.current_window,
                        "Error",
                        f"El Arduino rechazo la alta en fase '{fase}': {linea}\n\n"
                        "No se guardo la tarjeta en la base local porque el alta "
                        "solo se persiste cuando Arduino confirma completamente."
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

        print("[ALTA] No se recibio UID real desde serial.")
        return False

    def _guardar_alta_local_confirmada(self) -> bool:
        if not self.alta_pendiente:
            return True

        try:
            payload = {
                "uid": self.alta_pendiente["uid"],
                "nombre_pasajero": self.alta_pendiente["nombre_pasajero"],
                "tipo": self.alta_pendiente["tipo"],
                "vigencia": self.alta_pendiente["vigencia"],
                "curp": self.alta_pendiente.get("curp", ""),
                "fecha_nacimiento": self.alta_pendiente.get("fecha_nacimiento", ""),
                "foto": self.alta_pendiente.get("foto", ""),
            }

            self.alta_model.guardar_alta_local(**payload)

            print(
                "[ALTA] Alta guardada en DB local "
                f"UID={payload['uid']}"
            )

            self.alta_pendiente = None
            self._sincronizar_pendientes()
            self._limpiar_forulario_alta()
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

    def _set_curp_status_alta(self, mensaje: str, *, error: bool = False) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        if not hasattr(self.current_ui, "curpstatus"):
            return

        color = "#B42318" if error else "#137333"
        self.current_ui.curpstatus.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )
        self.current_ui.curpstatus.setText(mensaje)

    def _ejecutar_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        ui = self.current_ui

        self.alta_pendiente = None

        if not self._hay_internet_para_alta():
            self._mostrar_error_alta_sin_internet()
            return

        self._leer_serial_alta(False)

        if not self.uid_alta_actual and not self._esperar_uid_alta_disponible():
            self._mostrar_error_uid_alta_no_disponible()
            return

        nombre_pasajero_completo = re.sub(
            r"\s+",
            " ",
            ui.textonombre.toPlainText().strip(),
        )
        alias_tarjeta = self._limpiar_alias_para_arduino(nombre_pasajero_completo)

        if not nombre_pasajero_completo or not alias_tarjeta:
            QMessageBox.warning(
                self.current_window,
                "Error",
                "Captura el nombre."
            )
            return

        curp_alta = ui.textocurp.toPlainText().strip().upper()

        if not curp_alta or curp_alta == "-":
            QMessageBox.warning(
                self.current_window,
                "CURP requerida",
                "Captura la CURP."
            )
            return

        # 1. Validar primero en la base local
        try:
            curp_local = self.alta_model.buscar_curp_local(curp_alta)
        except Exception as e:
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo validar la CURP en la base local:\n\n{e}"
            )
            return

        if curp_local:
            self._set_curp_status_alta(
                f"La CURP {curp_alta} ya esta registrado.",
                error=True
            )
            return

        # 2. Validar también en el servidor
        try:
            curp_servidor = self.alta_model.buscar_curp_servidor(curp_alta)
        except Exception:
            self._mostrar_error_alta_sin_internet()
            return

        if curp_servidor:
            self._set_curp_status_alta(
                f"La CURP {curp_alta} ya esta registrado.",
                error=True
            )
            return


        fecha = ui.calendario.selectedDate()
        self._set_curp_status_alta(
            f"CURP {curp_alta} disponible.",
            error=False
        )
        vigtarifa = fecha.toString("ddMMyy")
        hora_actual = QDateTime.currentDateTime().toString("HHmmss")
        vigencia12 = vigtarifa + hora_actual

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

        uid_alta = self._normalizar_uid(self.uid_alta_actual)

        if not uid_alta:
            self._mostrar_error_uid_alta_no_disponible()
            return

        if ui.preferencial.isChecked():
            no_tarjeta = "EU"
            tipo_local = "EU"
        else:
            no_tarjeta = "NO"
            tipo_local = "NO"

        id_tipo_tarjeta = "02"
        id_tarifa = "01"
        alias_tarjeta = self._ajustar_alias_para_comando_alta(
            uid_alta,
            alias_tarjeta,
            no_tarjeta,
            id_tipo_tarjeta,
            id_tarifa,
            vigtarifa,
            vigencia12,
        )

        if not alias_tarjeta:
            QMessageBox.warning(
                self.current_window,
                "Error",
                "El nombre queda vacio al preparar el comando para Arduino."
            )
            return

        comando = (
            f"al,{uid_alta},{alias_tarjeta},{no_tarjeta},"
            f"{id_tipo_tarjeta},{id_tarifa},{vigtarifa},{vigencia12}"
        )

        self.alta_pendiente = {
            "uid": uid_alta,
            "nombre_pasajero": nombre_pasajero_completo,
            "alias_tarjeta": alias_tarjeta,
            "tipo": tipo_local,
            "vigencia": vigencia12,
            "curp": curp_alta,
            "fecha_nacimiento": ui.textofechanacimiento.toPlainText().strip(),
            "foto": self.foto_alta_path,
            "fase": "esperando_alta",
            "comando_alta": comando,
            "reintentos_alta": 0,
        }

        

        print("[ALTA] Enviando alta:", comando)
        self.arduino.enviar_linea(comando)
        
        
    # =========================
    # CANCELAR
    # =========================
            
    def _configurar_cancelar_window(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        self.uid_cancelar_actual = ""
        self.nombre_cancelar_actual = ""

        ui.textonombre.setPlainText("")
        
        ui.textonombre.textChanged.connect(self._solo_letras_espacios_nombre_cancelar)
        
        ui.textouid.setText("-")
        ui.listanegra.setChecked(False)
        ui.textomotivo.setPlainText("")

        ui.botoncancelar.clicked.connect(self._ejecutar_cancelar)
        ui.pushButton.clicked.connect(self._quitar_lista_negra)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_cancelar)

        if self.cancelar_timer is None:
            self.cancelar_timer = QTimer()
            self.cancelar_timer.timeout.connect(self._leer_serial_cancelar)

        self._conectar_puerto_cancelar()
        self.cancelar_timer.start(300)
    
    def _conectar_puerto_cancelar(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None

        if not puerto:
            return

        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f"[CANCELAR] Error al conectar al puerto {puerto}: {e}")
            
    def _leer_serial_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print("[CANCELAR]", linea)
            linea_minusculas = linea.lower()

            if linea_minusculas.startswith("sldo,"):
                try:
                    _, uid, saldo, nombre = linea.split(",", 3)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue

                    self.uid_cancelar_actual = uid
                    self.nombre_cancelar_actual = nombre.strip()

                    ui.textouid.setText(uid)
                    ui.textonombre.setPlainText(self.nombre_cancelar_actual)

                    try:
                        saldo_valor = int(str(saldo).strip()) / 100
                    except Exception:
                        saldo_valor = 0.0

                    tarjeta = self.cancelar_model.obtener_tarjeta_por_uid(uid)

                    if tarjeta:
                        self._mostrar_datos_tarjeta_cancelar(
                            tarjeta,
                            nombre_fallback=self.nombre_cancelar_actual,
                        )
                        #ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
                        #if bool(tarjeta["en_lista_negra"]):
                         #   ui.textomotivo.setPlainText(tarjeta["motivo_baja"] or "")
                        #else:
                        #    ui.textomotivo.setPlainText("")
                        #nombre_db = (tarjeta["nombre_pasajero"] or "").strip()
                        #if nombre_db:
                        #    self.nombre_cancelar_actual = nombre_db
                        #    ui.textonombre.setPlainText(nombre_db)
                    else:
                        ui.listanegra.setChecked(False)
                        ui.textomotivo.setPlainText("")

                except Exception as e:
                    print(f"[CANCELAR] Error al procesar saldo: {e}")

            elif linea_minusculas.startswith("uid,"):
                try:
                    _, uid = linea.split(",", 1)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue

                    self.uid_cancelar_actual = uid
                    ui.textouid.setText(uid)

                    tarjeta = self.cancelar_model.obtener_tarjeta_por_uid(uid)

                    if tarjeta:
                        self._mostrar_datos_tarjeta_cancelar(tarjeta)
                    else:
                        # No viene nombre desde serial, pero ya dejas la UID lista
                        self.nombre_cancelar_actual = ""
                        ui.textonombre.setPlainText("")
                        ui.listanegra.setChecked(False)
                        ui.textomotivo.setPlainText("")

                except Exception as e:
                    print(f"[CANCELAR] Error al procesar uid: {e}")
                    
            elif linea == "st":
                self._limpiar_interfaz_por_retiro_tarjeta()
                continue

    def _mostrar_datos_tarjeta_cancelar(self, tarjeta, nombre_fallback: str = "") -> None:
        if not isinstance(self.current_ui, CancelarWindow) or not tarjeta:
            return

        ui = self.current_ui
        nombre_db = (tarjeta["nombre_pasajero"] or "").strip()
        motivo_db = (tarjeta["motivo_baja"] or "").strip()

        self.nombre_cancelar_actual = nombre_db or nombre_fallback.strip()
        ui.textonombre.setPlainText(self.nombre_cancelar_actual)
        ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
        ui.textomotivo.setPlainText(motivo_db)
                    
    def _ejecutar_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        if not self.uid_cancelar_actual:
            QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
            return

        motivo = ui.textomotivo.toPlainText().strip()
        nombre_capturado = ui.textonombre.toPlainText().strip()

        if not motivo:
            QMessageBox.warning(self.current_window, "Error", "Captura el motivo de la baja.")
            return

        try:
            tarjeta_id = self.cancelar_model.cancelar_tarjeta_flexible(
                uid=self.uid_cancelar_actual,
                nombre_pasajero=nombre_capturado,
                saldo_actual=0.0,
                en_lista_negra=True,
                motivo_baja=motivo
            )

            ui.listanegra.setChecked(True)

            QMessageBox.information(
                self.current_window,
                "Cancelar",
                f"Tarjeta Cancelada correctamente."
            )

        except Exception as e:
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo cancelar la tarjeta: {e}"
            )
            
    # =========================
    # REACTIVAR TARJETA (LISTA NEGRA)
    # =========================
    
    def _quitar_lista_negra(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        if not self.uid_cancelar_actual:
            QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
            return
        
        nombre_capturado = ui.textonombre.toPlainText().strip()
        
        try:
            self.cancelar_model.cancelar_tarjeta_flexible(
                uid = self.uid_cancelar_actual,
                nombre_pasajero = nombre_capturado,
                saldo_actual = 0.0,
                en_lista_negra=False,
                motivo_baja = ""
            )
            
            ui.listanegra.setChecked(False)
            ui.textomotivo.setPlainText("")
            
            QMessageBox.information(
                self.current_window,
                "Lista negra",
                "La tarjeta fue reactivada correctamente."
            )
        
        except Exception as e:
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo reactivar la tarjeta: {e}"
            )


          
    def _aplicar_bloqueo_lista_negra_recarga(self, bloqueada: bool) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui
        self.tarjeta_bloqueada = bloqueada

        monto = self._campo_monto_recarga()
        
        if bloqueada:
            if monto is not None:
                monto.clear()
                monto.setEnabled(False)
                
            ui.texto2.setText(f"{self.saldo_actual_centavos / 100:.2f}")
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText("Tarjeta en lista negra.")
            ui.texto7.setStyleSheet("color: red; font-weight: bold;")
            return
        
        if monto is not None:
            monto.setEnabled(not self.tarjeta_vencida)
        
        ui.texto2.setText(f"{self.saldo_actual_centavos / 100:.2f}")
        ui.botonrecargar.setEnabled(not self.tarjeta_vencida)
        
        texto_actual = ""
        if hasattr(ui.texto7, "toPlainText"):
            texto_actual = ui.texto7.toPlainText().strip()
        elif hasattr(ui.texto7, "text"):
            texto_actual = ui.texto7.text().strip()
            
        if texto_actual == "Tarjeta en lista negra.":
            ui.texto7.clear()
            
        ui.texto7.setStyleSheet("")
        
        
    def _limpiar_interfaz_por_retiro_tarjeta(self) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self._limpiar_recarga_por_retiro()
            return

        if isinstance(self.current_ui, AltaWindow):
            self._limpiar_alta_por_retiro()
            return

        if isinstance(self.current_ui, CancelarWindow):
            self._limpiar_cancelar_por_retiro()
            return

        if isinstance(self.current_ui, SustituirWindow):
            self._limpiar_sustituir_por_retiro()
            return


    def _limpiar_recarga_por_retiro(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui

        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self.tarjeta_vencida = False
        self.tarjeta_bloqueada = False

        ui.texto4.setText("-")
        ui.texto5.setText("-")
        ui.texto6.setText("-")
        ui.texto1.setText("0.00")
        ui.texto2.setText("0.00")
        ui.texto7.clear()
        ui.texto7.setStyleSheet("")
        ui.botonrecargar.setEnabled(True)

        monto = self._campo_monto_recarga()
        if monto is not None:
            monto.clear()
            monto.setEnabled(True)


    def _limpiar_alta_por_retiro(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        if self.alta_pendiente:
            return

        self._limpiar_forulario_alta()


    def _limpiar_cancelar_por_retiro(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        self.uid_cancelar_actual = ""
        self.nombre_cancelar_actual = ""
        self.tarjeta_bloqueada = False

        ui.textouid.setText("-")
        ui.textonombre.setPlainText("")
        ui.listanegra.setChecked(False)
        ui.textomotivo.setPlainText("")


    def _limpiar_sustituir_por_retiro(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        if self.sustituir_pendiente:
            return

        ui = self.current_ui

        self.uid_sustituir_nueva = ""

        if hasattr(ui, "textouid"):
            ui.textouid.setText(self.uid_sustituir_original or "-")        
        
        
        
        
        
        
        
            
            
    #========================
    #   SUSTITUIR
    #========================
    
    
    
    def _configurar_sustituir_window(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        
        ui = self.current_ui
        
        self.uid_sustituir_original = ""
        self.uid_sustituir_nueva = ""
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        
        ui.buscador.clear()
        ui.buscador.setMaximumWidth(900)
        ui.textonombre.setPlainText("")
        ui.textocurp.setText("-")
        ui.textofecha.setText("-")
        ui.textouid.setText("-")
        ui.textotipo.setText("-")
        ui.textovigencia.clear()
        ui.textovigencia.setReadOnly(True)
        ui.botonsustituir.clicked.connect(self._ejecutar_sustitucion)
        
        self._crear_popup_resultados_sustituir()
        self._activar_busqueda_sustituir_al_presionar()
        ui.buscador.textChanged.connect(self._buscar_pasajeros_sustituir)
        ui.buscador.editingFinished.connect(self._ocultar_popup_sustituir)
        ui.calendario.selectionChanged.connect(self._actualizar_vigencia_sustituir_desde_calendario)
        
        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_sustituir)
            
        if self.sustituir_timer is None:
            self.sustituir_timer = QTimer()
            self.sustituir_timer.timeout.connect(self._leer_serial_sustituir)

        self._conectar_puerto_sustituir()
        self.sustituir_timer.start(300)
        self._actualizar_vigencia_sustituir_desde_calendario()
        
    def _activar_busqueda_sustituir_al_presionar(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        buscador = self.current_ui.buscador
        mouse_press_original = buscador.mousePressEvent
        focus_in_original = buscador.focusInEvent

        def mouse_press_event(event):
            mouse_press_original(event)
            self._buscar_pasajeros_sustituir(buscador.text())

        def focus_in_event(event):
            focus_in_original(event)
            self._buscar_pasajeros_sustituir(buscador.text())

        buscador.mousePressEvent = mouse_press_event
        buscador.focusInEvent = focus_in_event
        
    
    def _aplicar_estilos_sustituir(self)-> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        
        ui = self.current_ui
        ui.buscador.setPlaceholderText("Buscar por nombre, UID, o Curp...")
        
        ui.buscador.setStyleSheet(
            """
            QLineEdit#buscador {
            background-color: white;
            border: 2px solid #B7DDF5;
            color: #2e3a46;
            border-radius: 10px;
            padding: 5px 12px;
            font-size: 12px;
        }

        QLineEdit#buscador:focus {
            border: 2px solid #1E73BE;
            background-color: #F8FCFF;
        }
            """
            )
        
        ui.lista.setStyleSheet("""
        QComboBox#lista {
            background-color: white;
            border: 2px solid #B7DDF5;
            color: #2e3a46;
            border-radius: 10px;
            padding: 6px 12px;
            font-weight: bold;
        }

        QComboBox#lista:focus {
            border: 2px solid #1E73BE;
        }

        QComboBox#lista::drop-down {
            width: 32px;
            border-left: 1px solid #B7DDF5;
            background-color: #D9ECFF;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
        }

        QComboBox#lista QAbstractItemView {
            background-color: white;
            color: #2e3a46;
            border: 2px solid #7BB7F0;
            selection-background-color: #F4C430;
            selection-color: #3e3a32;
            padding: 4px;
            outline: 0;
        }
    """)
        
        
            
    
    def _crear_popup_resultados_sustituir(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui

        if self.popup_resultados_sustituir is None:
            self.popup_resultados_sustituir = QTableWidget(ui.centralwidget)
            self.popup_resultados_sustituir.setObjectName("tablaResultadosSustituir")

            self.popup_resultados_sustituir.setColumnCount(6)
            self.popup_resultados_sustituir.setHorizontalHeaderLabels([
                "Nombre", "UID", "Vigencia", "Tipo", "CURP", "Nacimiento"
            ])

            self.popup_resultados_sustituir.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.popup_resultados_sustituir.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.popup_resultados_sustituir.setSelectionMode(QAbstractItemView.SingleSelection)
            self.popup_resultados_sustituir.setAlternatingRowColors(True)
            self.popup_resultados_sustituir.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.popup_resultados_sustituir.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.popup_resultados_sustituir.setWordWrap(False)

            self.popup_resultados_sustituir.verticalHeader().setVisible(False)
            self.popup_resultados_sustituir.horizontalHeader().setStretchLastSection(False)

            self.popup_resultados_sustituir.itemClicked.connect(
                self._seleccionar_resultado_popup_sustituir
            )

            header = self.popup_resultados_sustituir.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Interactive)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

            self.popup_resultados_sustituir.setStyleSheet("""
                QTableWidget#tablaResultadosSustituir {
                    background-color: white;
                    alternate-background-color: #F8FCFF;
                    color: #2e3a46;
                    border: 2px solid #7BB7F0;
                    border-radius: 10px;
                    gridline-color: #D9ECFF;
                    font-size: 11px;
                    selection-background-color: #F4C430;
                    selection-color: #3e3a32;
                }

                QTableWidget#tablaResultadosSustituir::item {
                    padding: 6px;
                    border-bottom: 1px solid #EAF4FF;
                }

                QTableWidget#tablaResultadosSustituir::item:selected {
                    background-color: #F4C430;
                    color: #3e3a32;
                    font-weight: bold;
                }

                QHeaderView::section {
                    background-color: #D9ECFF;
                    color: #245e91;
                    font-weight: bold;
                    padding: 6px;
                    border: none;
                    border-bottom: 1px solid #7BB7F0;
                }

                QTableCornerButton::section {
                    background-color: #D9ECFF;
                    border: none;
                }
            """)

            self.popup_resultados_sustituir.hide()

        geo = ui.buscador.geometry()
        margen = 20
        ancho_disponible = max(650, ui.centralwidget.width() - (margen * 2))

        self.popup_resultados_sustituir.setGeometry(
            margen,
            geo.y() + geo.height() + 6,
            ancho_disponible,
            260,
        )    
   
    def _formatear_vigencia_sustituir(self, vigencia_raw) -> str:
        fecha = self._parsear_vigencia_tarjeta(vigencia_raw)
        if fecha:
            return fecha.strftime('%d-%m-%Y %H:%M:%S')
        return str(vigencia_raw or '-')

    def _formatear_fecha_simple_sustituir(self, fecha_raw) -> str:
        texto_fecha = str(fecha_raw or '').strip()
        if not texto_fecha:
            return '-'

        formatos = (
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y',
            '%d/%m/%Y',
        )

        for formato in formatos:
            try:
                return datetime.strptime(texto_fecha, formato).strftime('%d-%m-%Y')
            except ValueError:
                continue

        return texto_fecha
    
    def _actualizar_vigencia_sustituir_desde_calendario(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        fecha = self.current_ui.calendario.selectedDate()
        self.current_ui.textovigencia.setPlainText(fecha.toString('dd-MM-yyyy'))
        
    def _buscar_pasajeros_sustituir(self, texto: str) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        self._crear_popup_resultados_sustituir()
        termino = (texto or '').strip()

        try:
            self.resultados_sustituir = list(
                self.sustituir_model.buscar_tarjetas_por_nombre(termino)
            )
        except Exception as e:
            self.resultados_sustituir = []
            self.popup_resultados_sustituir.hide()
            print(f"[SUSTITUIR] Error al buscar en servidor: {e}")
            return

        tabla = self.popup_resultados_sustituir
        tabla.setRowCount(0)

        for fila, row in enumerate(self.resultados_sustituir):
            curp = str(row.get('curp') or '-')
            fecha_nacimiento = self._formatear_fecha_simple_sustituir(
                row.get('fecha_nacimiento')
            )

            valores = [
                row.get('nombre_pasajero') or '-',
                row.get('uid') or '-',
                self._formatear_vigencia_sustituir(row.get('vigencia')),
                row.get('tipo_tarjeta') or '-',
                curp,
                fecha_nacimiento,
            ]

            tabla.insertRow(fila)

            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                item.setData(Qt.UserRole, row.get('uid'))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                tabla.setItem(fila, columna, item)

        tabla.resizeColumnsToContents()
        tabla.setColumnWidth(0, max(tabla.columnWidth(0), 220))
        tabla.setColumnWidth(4, max(tabla.columnWidth(4), 160))

        if tabla.rowCount() > 0:
            tabla.show()
            tabla.raise_()
        else:
            tabla.hide()
            
            
    def _seleccionar_resultado_popup_sustituir(self, item) -> None:
        if item is None:
            return

        uid = item.data(Qt.UserRole)

        for row in self.resultados_sustituir:
            if row.get('uid') == uid:
                self._cargar_tarjeta_sustituir(row)
                break
        

    def _cargar_tarjeta_sustituir(self, row) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui
        self.tarjeta_sustituir_seleccionada = dict(row)
        self.uid_sustituir_original = self._normalizar_uid(str(row.get('uid') or ''))
        self.uid_sustituir_nueva = ''

        ui.buscador.blockSignals(True)
        ui.buscador.clear()
        ui.buscador.blockSignals(False)
        ui.textonombre.setPlainText(row['nombre_pasajero'] or '')
        ui.textocurp.setText(str(row.get('curp') or '-'))
        ui.textofecha.setText(
            self._formatear_fecha_simple_sustituir(row.get('fecha_nacimiento'))
        )
        ui.textouid.setText(self.uid_sustituir_original or '-')
        ui.textotipo.setText(row['tipo_tarjeta'] or '-')

        fecha_vigencia = self._parsear_vigencia_tarjeta(row['vigencia'])
        if fecha_vigencia:
            ui.calendario.setSelectedDate(QDate(fecha_vigencia.year, fecha_vigencia.month, fecha_vigencia.day))
        self._actualizar_vigencia_sustituir_desde_calendario()
        self._ocultar_popup_sustituir()

    def _ocultar_popup_sustituir(self) -> None:
        if self.popup_resultados_sustituir is not None:
            self.popup_resultados_sustituir.hide()

    def _conectar_puerto_sustituir(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None
        if not puerto:
            return
        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f'[SUSTITUIR] Error al conectar al puerto {puerto}: {e}')

    def _leer_serial_sustituir(self, mostrar_errores: bool = True) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print('[SUSTITUIR]', linea)
            linea_minusculas = linea.lower()

            try:
                if linea_minusculas.startswith('uid,'):
                    _, uid = linea.split(',', 1)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue
                    self._registrar_uid_sustituir_leida(uid)

                elif linea_minusculas.startswith('sldo,'):
                    _, uid, _saldo, _nombre = linea.split(',', 3)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue
                    self._registrar_uid_sustituir_leida(uid)
                
                elif linea == "st":
                    self._limpiar_interfaz_por_retiro_tarjeta()
                    continue

                elif linea_minusculas == 'ok,alta':
                    if not self.sustituir_pendiente:
                        print('[SUSTITUIR] Llego ok,alta pero no hay sustitucion pendiente.')
                        continue

                    uid = self.sustituir_pendiente['uid_nueva']
                    nombre = self.sustituir_pendiente['nombre_pasajero']
                    comando_nombre = f'nm,{uid},{nombre}'
                    print('[SUSTITUIR] Enviando nombre:', comando_nombre)
                    self.arduino.enviar_linea(comando_nombre)
                    self.sustituir_pendiente['fase'] = 'esperando_nombre'

                elif linea_minusculas == 'ok,nombre':
                    if not self.sustituir_pendiente:
                        print('[SUSTITUIR] Llego ok,nombre pero no hay sustitucion pendiente.')
                        continue

                    if not self._guardar_sustitucion_confirmada():
                        return

                    QMessageBox.information(
                        self.current_window,
                        'Sustituir',
                        f'Tarjeta sustituida.\nNueva: {self.uid_sustituir_nueva}'
                    )
                    self._limpiar_formulario_sustituir()

                elif linea == 'ok':
                    if not self.sustituir_pendiente:
                        continue

                    if not self._guardar_sustitucion_confirmada():
                        return

                    QMessageBox.information(
                        self.current_window,
                        'Sustituir',
                        f'Tarjeta sustituida.\nNueva: {self.uid_sustituir_nueva}'
                    )
                    self._limpiar_formulario_sustituir()

                elif linea_minusculas.startswith('error'):

                    errores_de_lectura_automatica = {
                        'error,estado_tisc4',
                        'error,estado_tisc3',
                        'error,estado_tisc2',
                        'error,vigencia0',
                        'error,leer_saldo',
                        'error,leer_saldo2',
                    }

                    if linea_minusculas in errores_de_lectura_automatica:
                        print(f'[SUSTITUIR] Error automatico de lectura ignorado: {linea}')
                        continue

                    if 'error en las 3 aplicaciones' in linea_minusculas:
                        if self.sustituir_pendiente:
                            reintentos = self.sustituir_pendiente.get('reintentos_alta', 0)
                            comando = self.sustituir_pendiente.get('comando_sustitucion')

                            if comando and reintentos < 2:
                                self.sustituir_pendiente['reintentos_alta'] = reintentos + 1

                                print(
                                    '[SUSTITUIR] Reintentando sustitucion por error en aplicaciones '
                                    f'intento {reintentos + 1}: {comando}'
                                )

                                QTimer.singleShot(
                                    1000,
                                    lambda c=comando: self.arduino.enviar_linea(c)
                                )
                                continue

                    if not self.sustituir_pendiente:
                        print(f'[SUSTITUIR] Error de lectura ignorado sin sustitucion pendiente: {linea}')
                        continue

                    self.sustituir_pendiente = None

                    if mostrar_errores:
                        QMessageBox.warning(
                            self.current_window,
                            'Sustituir',
                            'No se pudo preparar la tarjeta nueva. Intenta acercarla de nuevo y vuelve a presionar Sustituir.'
                        )
                    return
            except Exception as e:
                print(f'[SUSTITUIR] Error al procesar serial: {e}')
                traceback.print_exception(type(e), e, e.__traceback__)

    def _registrar_uid_sustituir_leida(self, uid: str) -> None:
        uid = self._normalizar_uid(uid)
        if not uid:
            return

        uid_original = self._normalizar_uid(self.uid_sustituir_original)
        if uid_original and uid == uid_original and not self.sustituir_pendiente:
            print(f'[SUSTITUIR] UID anterior ignorada como nueva: {uid}')
            return

        self.uid_sustituir_nueva = uid
        if isinstance(self.current_ui, SustituirWindow):
            self.current_ui.textouid.setText(uid)

    def _esperar_uid_sustituir_disponible(self) -> bool:
        try:
            self.arduino.enviar_linea('uid')
        except Exception:
            pass

        limite = time.monotonic() + 5.0
        while time.monotonic() < limite:
            self._leer_serial_sustituir()
            if self.uid_sustituir_nueva:
                return True
            QCoreApplication.processEvents()
            time.sleep(0.05)
        return False

    def _ejecutar_sustitucion(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        if not self.tarjeta_sustituir_seleccionada or not self.uid_sustituir_original:
            QMessageBox.warning(
                self.current_window,
                'Error',
                'Primero selecciona un pasajero del buscador.'
            )
            return

        self.uid_sustituir_original = self._normalizar_uid(self.uid_sustituir_original)
        self.uid_sustituir_nueva = ''
        self._leer_serial_sustituir(False)
        if not self.uid_sustituir_nueva and not self._esperar_uid_sustituir_disponible():
            QMessageBox.warning(
                self.current_window,
                'Error',
                'Acerca la tarjeta nueva al lector.'
            )
            return

        if self._normalizar_uid(self.uid_sustituir_nueva) == self.uid_sustituir_original:
            QMessageBox.warning(
                self.current_window,
                'Error',
                'La tarjeta nueva no puede ser la misma que la anterior.'
            )
            return

        fecha = self.current_ui.calendario.selectedDate()
        vigtarifa = fecha.toString('ddMMyy')
        hora_actual = QDateTime.currentDateTime().toString('HHmmss')
        nueva_vigencia = vigtarifa + hora_actual

        if len(vigtarifa) != 6 or not vigtarifa.isdigit():
            QMessageBox.warning(
                self.current_window,
                'Error',
                'VIGTARIFA invalida.'
            )
            return

        if len(nueva_vigencia) != 12 or not nueva_vigencia.isdigit():
            QMessageBox.warning(
                self.current_window,
                'Error',
                'VIGENCIA12 invalida.'
            )
            return

        row = dict(self.tarjeta_sustituir_seleccionada)
        nombre_tarjeta = self._limpiar_alias_para_arduino(row.get('nombre_pasajero') or '')

        if not nombre_tarjeta:
            QMessageBox.warning(
                self.current_window,
                'Error',
                'La tarjeta seleccionada no tiene nombre valido para copiar.'
            )
            return

        tipo_tarjeta_raw = str(row.get('tipo_tarjeta') or '').strip().lower()
        if 'prefer' in tipo_tarjeta_raw:
            no_tarjeta = 'EU'
            tipo_local = 'EU'
        else:
            no_tarjeta = 'NO'
            tipo_local = 'NO'

        try:
            nombre_tarjeta = self._ajustar_alias_para_comando_alta(
                self.uid_sustituir_nueva,
                nombre_tarjeta,
                no_tarjeta,
                '02',
                '01',
                vigtarifa,
                nueva_vigencia,
            )

            if not nombre_tarjeta:
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'El nombre queda vacio al preparar el comando para Arduino.'
                )
                return

            comando = (
                f'al,{self.uid_sustituir_nueva},{nombre_tarjeta},{no_tarjeta},'
                f'02,01,{vigtarifa},{nueva_vigencia}'
            )

            self.sustituir_pendiente = {
                'uid_anterior': self.uid_sustituir_original,
                'uid_nueva': self.uid_sustituir_nueva,
                'nombre_pasajero': nombre_tarjeta,
                'tipo_codigo_local': tipo_local,
                'nueva_vigencia': nueva_vigencia,
                'fase': 'esperando_alta',
                'comando_sustitucion': comando,
                'reintentos_alta': 0,
            }

            print('[SUSTITUIR] Enviando sustitucion:', comando)
            self.arduino.enviar_linea(comando)

        except Exception as e:
            self.sustituir_pendiente = None
            print(f'[SUSTITUIR] Error completo al enviar sustitucion: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                'Error',
                f'No se pudo enviar la sustitucion: {e}'
            )

    def _guardar_sustitucion_confirmada(self) -> bool:
        if not self.sustituir_pendiente:
            return True

        try:
            payload = {
                'uid_anterior': self.sustituir_pendiente['uid_anterior'],
                'uid_nueva': self.sustituir_pendiente['uid_nueva'],
                'nueva_vigencia': self.sustituir_pendiente['nueva_vigencia'],
                'nombre_pasajero': self.sustituir_pendiente['nombre_pasajero'],
                'tipo_codigo_local': self.sustituir_pendiente['tipo_codigo_local'],
            }

            self.sustituir_model.sustituir_tarjeta_servidor(**payload)

            print(
                '[SUSTITUIR] Sustitucion guardada en SERVIDOR '
                f"UID_ANTERIOR={payload['uid_anterior']} UID_NUEVA={payload['uid_nueva']}"
            )

            self.sustituir_pendiente = None
            return True

        except Exception as e:
            print(f'[SUSTITUIR] Error al guardar sustitucion en servidor: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                'Error',
                f'El Arduino confirmo la sustitucion, pero no se pudo guardar en el servidor: {e}'
            )
            return False

    def _limpiar_formulario_sustituir(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        self.uid_sustituir_original = ''
        self.uid_sustituir_nueva = ''
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        self.sustituir_pendiente = None

        self.current_ui.buscador.clear()
        self.current_ui.textonombre.setPlainText('')
        self.current_ui.textocurp.setText('-')
        self.current_ui.textofecha.setText('-')
        self.current_ui.textouid.setText('-')
        self.current_ui.textotipo.setText('-')
        self._actualizar_vigencia_sustituir_desde_calendario()
        self._ocultar_popup_sustituir()
        
    
    def _configurar_menu_usuario(self) -> None:
        ui = self.current_ui

        if ui is None or not hasattr(ui, "usuario"):
            return

        ui.usuario.setText(self.current_username or "Usuario")
        ui.usuario.setToolTip("Opciones de usuario")
        ui.usuario.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        ui.usuario.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        ui.usuario.setArrowType(Qt.ArrowType.NoArrow)

        menu = QMenu(self.current_window)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #D6E4F2;
                border-radius: 8px;
                padding: 6px;
            }

            QMenu::item {
                color: #245E91;
                padding: 8px 18px;
                border-radius: 6px;
                font: 700 9pt "Arial";
            }

            QMenu::item:selected {
                background-color: #F4C430;
                color: #245E91;
            }
        """)

        accion_cerrar = menu.addAction("Cerrar sesión")
        accion_cerrar.triggered.connect(self._cerrar_sesion)

        ui.usuario.setMenu(menu)

    def _cerrar_sesion(self) -> None:
        self.current_username = ""
        self.current_role = ""
        self.show_login_window()
        
    def _crear_icono_ojo(self, tachado: bool = False) -> QIcon:
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor("#245E91")
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        path = QPainterPath()
        path.moveTo(3, 12)
        path.cubicTo(7, 5, 17, 5, 21, 12)
        path.cubicTo(17, 19, 7, 19, 3, 12)
        
        painter.drawPath(path)
        
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QRectF(10, 10, 4, 4))
        
        if tachado:
            painter.setPen(QPen(color, 2))
            painter.drawLine(5, 20, 20, 5)
            
        painter.end()
        
        return QIcon(pixmap)
    
    
    def _alternar_visibilidad_password(self) -> None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        campo = self.current_ui.lineEditPassword
        
        if campo.echoMode() == QLineEdit.EchoMode.Password:
            campo.setEchoMode(QLineEdit.EchoMode.Normal)
            self.accion_ver_password.setIcon(self._crear_icono_ojo(tachado=True))
            self.accion_ver_password.setToolTip("Ocultar Contraseña")
        else:
            campo.setEchoMode(QLineEdit.EchoMode.Password)
            self.accion_ver_password.setIcon(self._crear_icono_ojo(tachado= False))
            self.accion_ver_password.setToolTip("Mostrar Contraseña")
            
            
    #----------------------------------------------
    #                     CURP
    #----------------------------------------------
    
    def _limitar_curp_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return

        campo = self.current_ui.textocurp
        texto_actual = campo.toPlainText()
        texto_limitado = texto_actual.strip().upper()[:18]

        if texto_actual != texto_limitado:
            campo.blockSignals(True)
            campo.setPlainText(texto_limitado)
            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)
            campo.blockSignals(False)
            
#---------------------------------------------------
#              NOMBRE Y ESPACIOS
#---------------------------------------------------

    def _solo_letras_espacios_nombre_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return
        
        campo = self.current_ui.textonombre
        texto = campo.toPlainText()
        
        texto_limpio = re.sub(
            r"[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]",
            "",
            texto
        )
        
        if campo.toPlainText() != texto_limpio:
            campo.blockSignals(True)
            campo.setPlainText(texto_limpio)
            
            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)
            
            campo.blockSignals(False)
            


#--------------------------------------------------
#               FECHA NACIMINETO(DD-MM-AAAA)
#--------------------------------------------------
    def _formatear_fecha_nacimiento_alta(self) -> None:
        if not isinstance(self.current_ui, AltaWindow):
            return
        
        campo = self.current_ui.textofechanacimiento
        texto_actual = campo.toPlainText()
        numeros = re.sub(r"\D", "", texto_actual)[:8]

        if len(numeros) <= 2:
            texto_formateado = numeros
            if len(numeros) == 2:
                texto_formateado += "-"
        elif len(numeros) <= 4:
            texto_formateado = numeros[:2] + "-" + numeros[2:]
            if len(numeros) == 4:
                texto_formateado += "-"
        else:
            texto_formateado = numeros[:2] + "-" + numeros[2:4] + "-" + numeros[4:]

        if texto_actual != texto_formateado:
            campo.blockSignals(True)
            campo.setPlainText(texto_formateado)

            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)

            campo.blockSignals(False)

#---------------------------------------------
#                MONTO DE RECARGA
#---------------------------------------------
    def _formatear_monto_recarga(self) -> None:
        monto = self._campo_monto_recarga()
        if monto is None:
            return
        texto = self._texto_monto_recarga()
        
        if not texto:
            return
        
        try:
            cantidad = float(texto)
        except ValueError:
            return
        monto.setText(f"{cantidad:.2f}")

    def _solo_letras_espacios_nombre_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        campo = self.current_ui.textonombre
        texto = campo.toPlainText()

        limpio = re.sub(
            "[^A-Za-z\\u00c1\\u00c9\\u00cd\\u00d3\\u00da\\u00dc\\u00d1"
            "\\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00fc\\u00f1\\s]",
            "",
            texto,
        )
        limpio = re.sub(r"\s+", " ", limpio)

        if texto == limpio:
            return

        campo.blockSignals(True)
        campo.setPlainText(limpio)

        cursor = campo.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        campo.setTextCursor(cursor)

        campo.blockSignals(False)
        
#----------------------------------------------------------
#                   TEXTO EN CANCELAR
#----------------------------------------------------------

    def _solo_letras_espacios_nombre_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return
        
        campo = self.current_ui.textonombre
        texto = campo.toPlainText()
        
        limpio = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]", "", texto)
        limpio = re.sub(r"\s+", " ", limpio)
        
        if texto == limpio:
            return
        
        campo.blockSignals(True)
        campo.setPlainText(limpio)

        cursor = campo.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        campo.setTextCursor(cursor)

        campo.blockSignals(False)
        
        
#-------------------------------------------------------
#       Borra "Recarga Exitosa" despues de recarga
#-------------------------------------------------------
    def _limpiar_mensaje_recarga_exitosa(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return
        
        ui = self.current_ui
        texto_actual = ""
        
        if hasattr(ui.texto7, "toPlainText"):
            texto_actual = ui.texto7.toPlainText().strip()
        elif hasattr(ui.texto7, "text"):
            texto_actual = ui.texto7.text().strip()
            
        if texto_actual == "Recarga Exitosa":
            ui.texto7.clear()
            ui.texto7.setStyleSheet("")
