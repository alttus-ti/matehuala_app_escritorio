# Login MVC con flujo tipo AppController

Este proyecto ahora usa una estructura parecida al `urban_aeropuerto_app`:

- `AppController` controla que ventana se muestra.
- `LoginWindow` maneja la UI del login y valida credenciales.
- `LoginController` contiene la logica de autenticacion.
- `ContadorWindow` es la pantalla que abre despues de iniciar sesion.
- `AppController` incluye metodos estilo referencia: `showLoginWindow()` y `showContadorWindow()`.

## Estructura

```text
login_mvc_project/
|-- main.py
|-- controllers/
|   |-- app_controller.py
|   |-- auth_controller.py
|   |-- login_controller.py
|   `-- route_controller.py
|-- models/
|   `-- user_model.py
|-- views/
|   |-- login_view.py
|   `-- contador_view.py
|-- core/
|   `-- ui_loader.py
`-- ui/
    |-- login_qtdesigner.ui
    `-- contador.ui
```

## Ejecucion

```powershell
python main.py
```

Al iniciar, la app crea automaticamente la base local desde `sqlite_init.sql` en:

```text
data/matehuala.db
```

La carpeta `data/` no se sube al repositorio porque contiene la base generada en cada equipo.

Usuario de prueba:

- Usuario: `admin`
- Contrasena: `1234`

## Uso de SQLite

La conexion esta centralizada en `core/database.py`:

- `initialize_database()` crea la base y ejecuta `sqlite_init.sql`.
- `get_connection()` abre una conexion con `PRAGMA foreign_keys = ON`.

Ejemplo para consultar datos desde un modelo:

```python
from core.database import get_connection

with get_connection() as connection:
    usuarios = connection.execute("SELECT * FROM usuarios").fetchall()
```
