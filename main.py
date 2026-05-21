"""
Gestor del proyecto. Lo corre end to end. La alternativa a este es chequear notebooks/eda.ipynb
"""

# IMPORTS
from src.config import DATA, GRAPHS
from src.io import load, save, pd_display
from src.features import bool_lift
from src.utils import global_assert
from src.cleaning import pre_filter, duplicates, fix_types, null_imputer, fix_data
from src.viz import plot_full_explore
from src.analysis import pregunta1, pregunta2, pregunta3, pregunta4, pregunta5



def main():
    """Orquesta todo el proceso."""

    # CONFIG DEL DISPLAY
    pd_display()

    # SET UP ~ CARGA DEL RAW_DF + PRE-FILTRADO
    print("Cargando el dataset...")
    df = load(DATA / "OPL_dataset.csv")
    df = pre_filter(df)

    # PRIMERA LIMPIEZA
    print("Eliminando duplicados...")
    df = duplicates(df)     # DUPLICADOS

    print("Arreglando tipos...")
    df = fix_types(df)      # TIPOS

    print("Imputando datos...")
    df = null_imputer(df)   # NULOS

    # PRIMERA FEATURE ~ SINO LLEVA ESTE ORDEN, LA FEATURE SE ROMPE
    print("Creando primera feature...")
    df = bool_lift(df)

    # TERMINAR LIMPIEZA
    print("Terminando la limpieza...")
    df = fix_data(df)

    # GUARDADO DEL CLEAN_DF
    print("Guardado el DF limpio...")
    save(df, DATA / "clean_dataset.csv")

    # ASSERTS
    print("Asegurando que la limpieza ha salido correctamente...")
    global_assert(df)

    # VISTAZO A LOS DATOS
    print("Creando gráficos para la exploración inicial...")
    GRAPHS.mkdir(parents = True, exist_ok = True)
    plot_full_explore(df)
    
    # PREGUNTA 1
    print("Resolviendo pregunta 1...")
    pregunta1(df)

    # PREGUNTA 2
    print("Resolviendo pregunta 2...")
    pregunta2(df)

    # PREGUNTA 3
    print("Resolviendo pregunta 3...")
    pregunta3(df)

    # PREGUNTA 4
    print("Resolviendo pregunta 4...")
    pregunta4(df)

    # PREGUNTA 5
    print("Resolviendo pregunta 5...")
    pregunta5(df)

# NO CALLABLE
if __name__ == "__main__":
    main()