"""
Constantes globales del proyecto: rutas, parámetros de display y configuración de gráficos.

PD: Si deseas correr el proyecto de otra manera, puedes modificar las LISTAS DE COLUMNAS.
"""

# CONFIGURACIÓN DE RUTAS
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent         # RAÍZ DEL PROYECTO
DATA   = ROOT / "data"                                  # CARPETA DE CSV's
GRAPHS = DATA / "output_graphs"                  # OUTPUT DE LOS GRÁFICOS

# CONFIGURACIÓN DEL DISPLAY
DISPLAY = {
    "display.max_columns": None,
    "display.width": None,
    "display.float_format": "{:.2f}".format,
}

# CONFIGURACIÓN DE GRÁFICOS
PLOT_THEME   = {"style": "white", "palette": "muted"}

PLOT_RCPARAMS = {
    "font.family": "arial",
    "font.size": 10,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.labelweight": "bold",
    "figure.dpi": 120,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": True,
}

# LISTAS DE COLUMNAS
DROP_COLS = ['Country', 'State', 'MeetState', 'MeetTown', 'MeetCountry', 'Federation','ParentFederation', 'MeetName', 'Division', 'Sanctioned', 'Tested', 'Wilks', 'Glossbrenner', 'Goodlift']

CAT_COLS  = ['Sex', 'Event', 'Equipment', 'Place']

NEG_COLS  = ['Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Bench4Kg', 'Squat1Kg', 'Squat2Kg', 'Squat3Kg', 'Squat4Kg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg', 'Deadlift4Kg']

REQUIRED_COLS = ['Name', 'Age', 'BodyweightKg', 'Dots'] + CAT_COLS + NEG_COLS + ['Best3BenchKg', 'Best3SquatKg', 'Best3DeadliftKg', 'TotalKg', 'Bench3bool',
                                                                                  'Squat3bool', 'Deadlift3bool', 'Bench4bool', 'Squat4bool', 'Deadlift4bool']

LIFT_COLS = [
        ('Best3BenchKg',    ['Bench1Kg',    'Bench2Kg',    'Bench3Kg']),
        ('Best3SquatKg',    ['Squat1Kg',    'Squat2Kg',    'Squat3Kg']),
        ('Best3DeadliftKg', ['Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg']),
    ]

BOOL_COLS = [
    ('Bench3Kg', 'Bench3bool'),
    ('Squat3Kg', 'Squat3bool'),
    ('Deadlift3Kg', 'Deadlift3bool'),
    ('Bench4Kg', 'Bench4bool'),
    ('Squat4Kg', 'Squat4bool'),
    ('Deadlift4Kg', 'Deadlift4bool'),
    ]

EXPECTED_TYPES = {
    'Name'            : 'str',
    'Age'             : 'float64',
    'BodyweightKg'    : 'float64',
    'Dots'            : 'float64',
    'Sex'             : 'category',
    'Event'           : 'category',
    'Equipment'       : 'category',
    'Place'           : 'category',
    'Best3BenchKg'    : 'float64',
    'Best3SquatKg'    : 'float64',
    'Best3DeadliftKg' : 'float64',
    'TotalKg'         : 'float64',
    'Bench3bool'      : 'boolean',
    'Squat3bool'      : 'boolean',
    'Deadlift3bool'   : 'boolean',
    'Bench4bool'      : 'boolean',
    'Squat4bool'      : 'boolean',
    'Deadlift4bool'   : 'boolean',
    'Bench1Kg'        : 'float64',
    'Bench2Kg'        : 'float64',
    'Bench3Kg'        : 'float64',
    'Bench4Kg'        : 'float64',
    'Squat1Kg'        : 'float64',
    'Squat2Kg'        : 'float64',
    'Squat3Kg'        : 'float64',
    'Squat4Kg'        : 'float64',
    'Deadlift1Kg'     : 'float64',
    'Deadlift2Kg'     : 'float64',
    'Deadlift3Kg'     : 'float64',
    'Deadlift4Kg'     : 'float64',
}