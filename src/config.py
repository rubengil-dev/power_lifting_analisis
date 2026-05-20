"""
Constantes globales del proyecto: rutas, parámetros de display y configuración de gráficos.

PD: Si deseas correr el proyecto de otra manera, puedes modificar las LISTAS DE COLUMNAS.
"""

# CONFIGURACIÓN DE RUTAS
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent         # RAÍZ DEL PROYECTO
DATA   = ROOT / "data"                                  # CARPETA DE CSV's
GRAPHS = DATA / "output_graphs"                         # OUTPUT DE LOS GRÁFICOS

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