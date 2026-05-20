"""
Gestor del proyecto. Lo corre end to end. La alternativa a este es chequear notebooks/eda.ipynb
"""

# IMPORTS
from src.io import load, save
from src import cleaning, features, viz, analysis
from src.config import PLOT_THEME, PLOT_RCPARAMS, DISPLAY, DATA


def main():
    """Orquesta todo el proceso."""
    
    # CARGA DEL RAW_DF
    df = load(DATA / "OPL_dataset.csv")

    # df = clean(df)
    # df = build_features(df)
    # # assert_columns(df, ['column_1', 'column_2'])

    # plot_graph(df)

    # GUARDADO DEL CLEAN_DF
    save(df, DATA / "clean_dataset.csv")


if __name__ == "__main__":
    main()
