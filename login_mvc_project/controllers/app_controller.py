from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QTimer
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QMainWindow, QMessageBox
from datetime import datetime
from typing import Optional
import re
import time
import traceback

from core.sync_config import SYNC_INTERVAL_MS
from models.cancelar_model import CancelarModel
from models.sustituir_model import SustituirModel
from services.sync_service import SyncService

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

    def show_login_window(self) -> None:
        self._close_current_window()
        self.current_window = LoginWindow(controller=self)
        self.current_ui = None
        self.current_window.show()
        QTimer.singleShot(500, self._sincronizar_pendientes)

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
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def show_empleado_window(self, username: str) -> None:
        self._close_current_window()
        self.current_window = QMainWindow()
        self.current_ui = EmpleadoWindow()
        self.current_ui.setupUi(self.current_window)

        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)

        self.current_window.show()
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
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def _sincronizar_pendientes(self) -> None:
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

    def _close_current_window(self) -> None:
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

        if self.current_window is not None:
            self.current_window.close()

    # =========================
    # RECARGA
    # =========================

    def _configurar_recarga_window(self) -> None:
        ui = self.current_ui

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
        vigencia_raw = tarjeta_db["vigencia"] if tarjeta_db else None
        fecha_vigencia = self._parsear_vigencia_tarjeta(vigencia_raw)

        self.tarjeta_vencida = bool(
            fecha_vigencia and fecha_vigencia <= datetime.now()
        )

        if self.tarjeta_vencida:
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText(
                "Tarjeta vencida "
                f"({fecha_vigencia.strftime('%d-%m-%Y %H:%M:%S')})."
            )
            return

        ui.botonrecargar.setEnabled(True)
        if "Tarjeta vencida" in ui.texto7.text():
            ui.texto7.setText("")

    def _fallo_recarga(self, motivo: str, error: Optional[Exception] = None) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self.current_ui.texto7.setText("Fallo recarga")

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

                if int(tarjeta_db["en_lista_negra"]) == 1:
                    self._aplicar_bloqueo_lista_negra_recarga(True)
                    return
                else:
                    self._aplicar_bloqueo_lista_negra_recarga(False)

                # ESTA LINEA FALTABA
                self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)

            else:
                ui.texto6.setText("No registrada")
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
                referencia=f"Folio: {folio}"
            )
            self._sincronizar_pendientes()

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

        # ESTA PARTE FALTABA
        self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)
        if self.tarjeta_vencida:
            QMessageBox.warning(
                self.current_window,
                "Tarjeta vencida",
                "La tarjeta está vencida y no se puede recargar."
            )
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
            
    # =========================
    # ALTA
    # =========================

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

            elif linea_minusculas == "ok,alta":
                if not self.alta_pendiente:
                    print("[ALTA] Llego ok,alta pero no hay alta pendiente.")
                    continue

                try:
                    uid = self.alta_pendiente["uid"]
                    nombre = self.alta_pendiente["nombre_pasajero"]

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

            elif linea.lower().startswith("error"):
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
            }

            self.alta_model.guardar_alta_local(**payload)

            print(
                "[ALTA] Alta guardada en DB local "
                f"UID={payload['uid']}"
            )

            self.alta_pendiente = None
            self._sincronizar_pendientes()
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

        alias_tarjeta = self._limpiar_alias_para_arduino(
            ui.textonombre.toPlainText().strip()
        )

        fecha = ui.calendario.selectedDate()

        # Fecha seleccionada + hora actual real de la PC
        vigtarifa = fecha.toString("ddMMyy")
        hora_actual = QDateTime.currentDateTime().toString("HHmmss")
        vigencia12 = vigtarifa + hora_actual

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

            if ui.preferencial.isChecked():
                no_tarjeta = "EU"
                tipo_local = "EU"
            else:
                no_tarjeta = "NO"
                tipo_local = "NO"

            id_tipo_tarjeta = "02"
            id_tarifa = "01"

            # Guardar primero el estado pendiente para evitar carreras
            self.alta_pendiente = {
                "uid": uid_alta,
                "nombre_pasajero": alias_tarjeta,
                "tipo": tipo_local,
                "vigencia": vigencia12,
                "fase": "esperando_alta",
            }

            # PASO 1: alta sin nombre
            comando = (
                f"al,{uid_alta},{no_tarjeta},"
                f"{id_tipo_tarjeta},{id_tarifa},{vigtarifa},{vigencia12}"
            )

            print("[ALTA] Enviando alta:", comando)
            self.arduino.enviar_linea(comando)

        except Exception as e:
            self.alta_pendiente = None
            print(f"[ALTA] Error completo al enviar alta: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo enviar el alta: {e}"
            )
            
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

                    # SI NO EXISTE EN BD, LO CREA
                    self.cancelar_model.guardar_lectura_si_no_existe(
                        uid=uid,
                        nombre_pasajero=self.nombre_cancelar_actual,
                        saldo_actual=saldo_valor,
                    )

                    tarjeta = self.cancelar_model.obtener_tarjeta_por_uid(uid)
                    if tarjeta:
                        ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
                        nombre_db = (tarjeta["nombre_pasajero"] or "").strip()
                        if nombre_db:
                            self.nombre_cancelar_actual = nombre_db
                            ui.textonombre.setPlainText(nombre_db)
                    else:
                        ui.listanegra.setChecked(False)

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
                        self.nombre_cancelar_actual = tarjeta["nombre_pasajero"] or ""
                        ui.textonombre.setPlainText(self.nombre_cancelar_actual)
                        ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
                    else:
                        # No viene nombre desde serial, pero ya dejas la UID lista
                        self.nombre_cancelar_actual = ""
                        ui.textonombre.setPlainText("")
                        ui.listanegra.setChecked(False)

                except Exception as e:
                    print(f"[CANCELAR] Error al procesar uid: {e}")
                    
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
        if monto is not None:
            if bloqueada:
                monto.clear()
                monto.setEnabled(False)
            else:
                monto.setEnabled(True)

        ui.texto2.setText(f"{self.saldo_actual_centavos / 100:.2f}")

        if bloqueada:
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText("Tarjeta en lista negra.")
            ui.texto7.setStyleSheet("color: red; font-weight: bold;")
        else:
            if ui.texto7.text() == "Tarjeta en lista negra.":
                ui.texto7.clear()
            ui.texto7.setStyleSheet("")
            ui.botonrecargar.setEnabled(not self.tarjeta_vencida)       
            
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
        ui.textonombre.setPlainText("")
        ui.textouid.setText("-")
        ui.tipotarjeta.setText("-")
        ui.textovigencia.clear()
        ui.textovigencia.setReadOnly(True)
        ui.botonsustituir.clicked.connect(self._ejecutar_sustitucion)
        
        self._crear_popup_resultados_sustituir()
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
            
    
    def _crear_popup_resultados_sustituir(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        
        ui = self.current_ui
        if self.popup_resultados_sustituir is None:
            self.popup_resultados_sustituir = QListWidget(ui.centralwidget)
            self.popup_resultados_sustituir.hide()
            self.popup_resultados_sustituir.itemClicked.connect(self._seleccionar_resultado_popup_sustituir)
            
        
        geo = ui.buscador.geometry()
        self.popup_resultados_sustituir.setGeometry(
            geo.x(),
            geo.y() + geo.height() + 2,
            geo.width(),
            160,
        )
        
    def _formatear_vigencia_sustituir(self, vigencia_raw) -> str:
        fecha = self._parsear_vigencia_tarjeta(vigencia_raw)
        if fecha:
            return fecha.strftime('%d-%m-%Y %H:%M:%S')
        return str(vigencia_raw or '-')
    
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

        if len(termino) < 2:
            self.resultados_sustituir = []
            self.popup_resultados_sustituir.hide()
            return

        try:
            self.resultados_sustituir = list(
                self.sustituir_model.buscar_tarjetas_por_nombre(termino)
            )
        except Exception as e:
            self.resultados_sustituir = []
            self.popup_resultados_sustituir.hide()
            print(f"[SUSTITUIR] Error al buscar en servidor: {e}")
            return

        self.popup_resultados_sustituir.clear()

        for row in self.resultados_sustituir:
            descripcion = (
                f"{row['nombre_pasajero']} | {row['uid']} | "
                f"{self._formatear_vigencia_sustituir(row['vigencia'])} | {row['tipo_tarjeta']}"
            )
            item = QListWidgetItem(descripcion)
            item.setData(256, row['uid'])
            self.popup_resultados_sustituir.addItem(item)

        if self.popup_resultados_sustituir.count() > 0:
            self.popup_resultados_sustituir.show()
        else:
            self.popup_resultados_sustituir.hide()
            
            
    def _seleccionar_resultado_popup_sustituir(self, item) -> None:
        uid = item.data(256)
        for row in self.resultados_sustituir:
            if row['uid'] == uid:
                self._cargar_tarjeta_sustituir(row)
                break

    def _cargar_tarjeta_sustituir(self, row) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui
        self.tarjeta_sustituir_seleccionada = dict(row)
        self.uid_sustituir_original = row['uid']
        self.uid_sustituir_nueva = ''

        ui.buscador.setText(row['nombre_pasajero'])
        ui.textonombre.setPlainText(row['nombre_pasajero'] or '')
        ui.textouid.setText('Acerca la tarjeta nueva al lector')
        ui.tipotarjeta.setText(row['tipo_tarjeta'] or '-')

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

    def _leer_serial_sustituir(self) -> None:
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
                    self.uid_sustituir_nueva = uid
                    ui.textouid.setText(uid)

                elif linea_minusculas.startswith('sldo,'):
                    _, uid, _saldo, _nombre = linea.split(',', 3)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue
                    self.uid_sustituir_nueva = uid
                    ui.textouid.setText(uid)
            except Exception as e:
                print(f'[SUSTITUIR] Error al procesar serial: {e}')

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

        self._leer_serial_sustituir()
        if not self.uid_sustituir_nueva and not self._esperar_uid_sustituir_disponible():
            QMessageBox.warning(
                self.current_window,
                'Error',
                'Acerca la tarjeta nueva al lector.'
            )
            return

        if self.uid_sustituir_nueva == self.uid_sustituir_original:
            QMessageBox.warning(
                self.current_window,
                'Error',
                'La tarjeta nueva no puede ser la misma que la anterior.'
            )
            return

        fecha = self.current_ui.calendario.selectedDate()
        nueva_vigencia = fecha.toString('ddMMyy') + QDateTime.currentDateTime().toString('HHmmss')

        try:
            self.sustituir_model.sustituir_tarjeta(
                uid_anterior=self.uid_sustituir_original,
                uid_nueva=self.uid_sustituir_nueva,
                nueva_vigencia=nueva_vigencia,
            )

            QMessageBox.information(
                self.current_window,
                'Sustituir',
                f'Tarjeta sustituida.\nNueva: {self.uid_sustituir_nueva}'
            )

            self.uid_sustituir_original = ""
            self.uid_sustituir_nueva = ""
            self.tarjeta_sustituir_seleccionada = None
            self.resultados_sustituir = []

            self.current_ui.buscador.clear()
            self.current_ui.textonombre.setPlainText("")
            self.current_ui.textouid.setText("-")
            self.current_ui.tipotarjeta.setText("-")
            self._actualizar_vigencia_sustituir_desde_calendario()
            self._ocultar_popup_sustituir()

        except Exception as e:
            QMessageBox.critical(
                self.current_window,
                'Error',
                f'No se pudo sustituir la tarjeta: {e}'
            )          