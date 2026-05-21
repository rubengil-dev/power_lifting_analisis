"""
Project manager that runs it end to end. You can check notebooks/eda.ipynb for an alternative look.
"""

# IMPORTS
from src.config import DATA, GRAPHS
from src.io import load, save, pd_display
from src.features import bool_lift
from src.utils import global_assert
from src.cleaning import pre_filter, duplicates, fix_types, null_imputer, fix_data
from src.viz import plot_full_explore
from src.analysis import question1, question2, question3, question4, question5


def main():
    """Manages whole project"""

    # CONFIG DISPLAY
    pd_display()

    # SET UP ~ DOWNLAD + PRE-FILTER
    print("Loading DataSet...")
    df = load(DATA / "OPL_dataset.csv")
    df = pre_filter(df)

    # FIRST CLEANING
    print("Deleting duplicates...")
    df = duplicates(df)

    print("Casting types...")
    df = fix_types(df)

    print("Imputing data...")
    df = null_imputer(df)

    # FEATURE
    print("Creating features...")
    df = bool_lift(df)

    # SECOND CLEANING
    print("Finish cleaning...")
    df = fix_data(df)

    # SAVING CLEANED DF
    print("Saving cleaned DataFrame...")
    save(df, DATA / "clean_dataset.csv")

    # ASSERTS
    print("Asserting cleaning was succesful...")
    global_assert(df)

    # DATA EXPLORATION
    print("Creating graphs for initial exploration...")
    GRAPHS.mkdir(parents=True, exist_ok=True)
    plot_full_explore(df)

    # QUESTION 1
    print("Answering question 1...")
    question1(df)

    # QUESTION 2
    print("Answering question 2...")
    question2(df)

    # QUESTION 3
    print("Answering question 3...")
    question3(df)

    # QUESTION 4
    print("Answering question 4...")
    question4(df)

    # QUESTION 5
    print("Answering question 5...")
    question5(df)


# NO CALLABLE
if __name__ == "__main__":
    main()
