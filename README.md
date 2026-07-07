# Proyecto Final - Framework de Automatización QA - Maria Lujan Alderete

## Descripción

Framework de automatización de pruebas end-to-end que combina:
- **Pruebas de UI** sobre [SauceDemo](https://www.saucedemo.com) con Selenium WebDriver + Page Object Model
- **Pruebas de API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com) con la librería `requests`
- **Reportes HTML** con capturas de pantalla automáticas en fallos
- **Logging centralizado** con rotación de archivos
- **CI/CD** con GitHub Actions

Este proyecto extiende la pre-entrega original (`preentrega_alderete`), manteniendo
compatibilidad con las fixtures y tests previos, y sumando todo lo requerido en la
consigna del Trabajo Final Integrador.

## Tecnologías usadas

- Python 3.x
- Selenium WebDriver
- Pytest + pytest-html + pytest-rerunfailures
- Requests
- Git / GitHub Actions

## Estructura del proyecto

```
proyecto_final_alderete/
├── pages/                      # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── test/                       # Pruebas de UI (SauceDemo)
│   ├── test_login.py           # Incluye parametrización con data externa
│   ├── test_inventory.py
│   └── test_cart.py
├── tests_api/                  # Pruebas de API (JSONPlaceholder)
│   ├── conftest.py             # Fixtures de URLs
│   ├── test_users_api.py       # GET (status, headers, estructura, negativo)
│   ├── test_create_post_api.py # POST parametrizado
│   ├── test_post_lifecycle.py  # Ciclo de vida: POST → PATCH → DELETE (e2e)
│   └── test_login_api.py       # Opcional: login reqres.in (requiere API key)
├── utils/
│   ├── LoginPage.py             # Se mantiene por compatibilidad, delega al POM
│   ├── logger.py                # Logger centralizado (logs/suite.log)
│   └── data/
│       └── login_data.json      # Datos externos parametrizados
├── reports/                    # Reportes HTML + capturas (se generan, no se versionan)
├── logs/                       # Logs de ejecución (se generan, no se versionan)
├── .github/workflows/tests.yml # Pipeline de CI/CD
├── conftest.py                 # Fixtures raíz (driver, login_in_driver) + hooks
├── pytest.ini
├── requirements.txt
└── README.md
```

## Instalación

```bash
git clone https://github.com/marialde93/preentrega_alderete
cd preentrega_alderete
pip install -r requirements.txt
```

## Cómo ejecutar las pruebas

```bash
# Todo (UI + API)
pytest

# Solo API
pytest -m api -v

# Solo UI
pytest -m ui -v

# Solo smoke tests (críticos)
pytest -m smoke -v

# Un archivo específico
pytest test/test_login.py -v
pytest tests_api/test_post_lifecycle.py -v
```

Cada ejecución genera automáticamente `reports/report.html` (autocontenido, con
capturas de pantalla embebidas en los fallos de UI) y agrega entradas en `logs/suite.log`.

### Nota sobre reqres.in

`test_login_api.py` usa la API pública reqres.in, que **ahora exige una API key**
en todos sus endpoints (cambio posterior a los apuntes del curso). El test se
saltea automáticamente si no configurás la variable de entorno `REQRES_API_KEY`.
Para activarlo:
1. Creá una cuenta gratis en https://app.reqres.in
2. `export REQRES_API_KEY=tu_key` (o configurala como secret en GitHub Actions)

El resto de la suite de API corre sin necesidad de ninguna key, contra JSONPlaceholder.

## Cómo interpretar los reportes

- Abrí `reports/report.html` en el navegador: vas a ver una tabla con cada test,
  su estado (passed/failed), duración y una columna extra con la URL en la que
  ocurrió el fallo (para tests UI).
- Si un test de UI falla, el reporte incluye automáticamente una captura de
  pantalla del momento exacto del error (`reports/screens/`).
- `logs/suite.log` tiene el detalle cronológico paso a paso de cada test
  (útil para debugging sin necesidad de reproducir el escenario).

## Funcionamiento de las pruebas

### UI (`test/`)

- **test_login.py** — login válido, login con password inválida, y dos suites
  parametrizadas (usuarios válidos e inválidos) leyendo datos desde
  `utils/data/login_data.json`
- **test_inventory.py** — título de página, productos visibles, elementos de UI,
  nombre/precio del primer producto
- **test_cart.py** — agregar producto al carrito y verificar que coincide en la
  vista de carrito

### API (`tests_api/`)

- **test_users_api.py** — GET con validación de 5 niveles (status, headers,
  estructura, contenido, performance), GET parametrizado por id, y escenario
  negativo (404)
- **test_create_post_api.py** — POST parametrizado con distintos payloads
- **test_post_lifecycle.py** — fixture que crea un recurso real (POST), luego
  lo actualiza (PATCH) y lo elimina (DELETE), validando que el flujo completo
  corra en menos de 3 segundos. También incluye PUT con reemplazo completo.
- **test_login_api.py** — opcional, login contra reqres.in (ver nota arriba)

## CI/CD

El workflow `.github/workflows/tests.yml` corre automáticamente en cada push a
`main`: ejecuta primero los tests de API (rápidos, sin navegador) y luego los
de UI con Chrome headless, subiendo los reportes como artefactos descargables
desde la pestaña Actions.

## Notas

- Los tests son independientes entre sí; la falla de uno no afecta a los demás
- Los tests UI usan esperas explícitas (`WebDriverWait`) para mayor estabilidad
- El driver se inicializa en modo incógnito para evitar cache entre ejecuciones
- La lógica de página está encapsulada en `pages/` (Page Object Model)
