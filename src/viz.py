"""
Visualization functions: distribution and analylisis graphs.
"""

# IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from .config import GRAPHS, PLOT_THEME, PLOT_RCPARAMS


# GRAPHS CONFIG
sns.set_theme(**PLOT_THEME)
plt.rcParams.update(PLOT_RCPARAMS)
warnings.filterwarnings('ignore', category=FutureWarning)

# EXPLORATION GRAPHS: Each function shows a single variable

# AGE


def age_plotting(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # NAMING SET
    ax[0].set_title("AGE HISTOGRAM")
    ax[0].set_xlabel("AGE [YEARS]")
    ax[0].set_ylabel("FRECUENCY")

    ax[1].set_title("AGE BOXPLOT")
    ax[1].set_xlabel("SEX")
    ax[1].set_ylabel("AGE [YEARS]")

    # AX[0] ~ HISTOGRAM
    sns.histplot(data=df, x='Age', binwidth=3, kde=True, ax=ax[0])

    # AX[1] ~ BOXPLOT
    sns.boxplot(data=df, x='Sex', y='Age', palette={
                'F': 'pink', 'M': 'blue'}, ax=ax[1])

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "age_distribution.png", bbox_inches='tight')
    plt.close(fig)

# WEIGHT


def weight_plotting(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # NAMING SET
    ax[0].set_title("WEIGHT HISTOGRAM")
    ax[0].set_xlabel("WEIGHT [KG]")
    ax[0].set_ylabel("FRECUENCY")

    ax[1].set_title("WEIGHT BOXPLOT")
    ax[1].set_xlabel("SEX")
    ax[1].set_ylabel("WEIGHT [KG]")

    # AX[0] ~ HISTOGRAMA
    sns.histplot(data=df, x='BodyweightKg', binwidth=5, kde=True, ax=ax[0])

    # AX[1] ~ BOXPLOT
    sns.boxplot(data=df, x='Sex', y='BodyweightKg', palette={
                'F': 'pink', 'M': 'blue'}, ax=ax[1])

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "weight_distribution.png", bbox_inches='tight')
    plt.close(fig)

# EQUIPMENT


def equipment_plotting(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # NAMING SET
    ax[0].set_title("EQUIPMENT DISTRIBUTION")
    ax[0].set_xlabel("EQUIPMENT")
    ax[0].set_ylabel("FRECUENCY")

    ax[1].set_title("EQUIPMENT DISTRIBUTION BY SEX")
    ax[1].set_xlabel("EQUIPMENT")
    ax[1].set_ylabel("FRECUENCY")

    # AX[0] ~ COUNT
    sns.countplot(data=df, x='Equipment', ax=ax[0])

    # AX[1] ~ COUNT BY SEX
    sns.countplot(data=df, x='Equipment', hue='Sex', palette={
                  'F': 'pink', 'M': 'blue'}, ax=ax[1])

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "equipment_distribution.png", bbox_inches='tight')
    plt.close(fig)

# EVENT


def event_plotting(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # NAMING SET
    ax[0].set_title("EVENT DISTRIBUTION")
    ax[0].set_xlabel("EVENT")
    ax[0].set_ylabel("FRECUENCY")

    ax[1].set_title("EVENT DISTRIBUTION BY SEX")
    ax[1].set_xlabel("EVENT")
    ax[1].set_ylabel("FRECUENCY")

    # AX[0] ~ COUNT
    sns.countplot(data=df, x='Event', ax=ax[0])

    # AX[1] ~ COUNT BY SEX
    sns.countplot(data=df, x='Event', hue='Sex', palette={
                  'F': 'pink', 'M': 'blue'}, ax=ax[1])

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "event_distribution.png", bbox_inches='tight')
    plt.close(fig)

# FULL EXPLORATION FUNCTION [ITSELF]


def plot_full_explore(df: pd.DataFrame):
    """
    Executes every distribution visualization.
    """
    age_plotting(df)
    weight_plotting(df)
    equipment_plotting(df)
    event_plotting(df)

# GRAPHS FOR QUESTION ~ EACH FUNCTION CREATES THE GRAPHS FOR ITS QUESTION

# QUESTION 1


def graphs1(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # NAMING SET
    ax[0].set_title("Performance by Age & Sex")
    ax[0].set_xlabel("Age")
    ax[0].set_ylabel("Performance [DOTS]")

    ax[1].set_title("Performance by Age & Sex")
    ax[1].set_xlabel("Performance ")
    ax[1].set_ylabel("Performance [DOTS]")
    ax[1].set_xlim(16, 33)

    # AX[0] ~ GENERAL PLOT
    sns.lineplot(
        data=df,
        x='Age',
        y='Dots',
        hue='Sex',
        palette={
            'F': 'pink',
            'M': 'blue'
        },
        ax=ax[0]
    )

    # AX[1] ~ ZOOMED PLOT
    sns.lineplot(
        data=df,
        x='Age',
        y='Dots',
        hue='Sex',
        palette={
            'F': 'pink',
            'M': 'blue'
        },
        ax=ax[1]
    )

    # ZOOM's TAGS
    for line in ax[1].lines:
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax[1].annotate(f'{x:.0f}, {y: .0f}', (x, y), fontsize=10)

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "question1.png", bbox_inches='tight')
    plt.close(fig)

# QUESTION 2


def graphs2(bench_df: pd.DataFrame, squat_df: pd.DataFrame, deadlift_df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(10, 10))

    # BENCH
    # NAMING SET
    ax[0][0].set_title("BENCH PROGRESSION")
    ax[0][0].set_xlabel("ATTEMPT")
    ax[0][0].set_ylabel("LIFTED WEIGHT [KG]")

    ax[0][1].set_title("BENCH PROGRESSION BY SEX")
    ax[0][1].set_xlabel("ATTEMPT")
    ax[0][1].set_ylabel("LIFTED WEIGHT [KG]")

    # AX[0][0] ~ BENCH PROGRESSION
    sns.boxplot(data=bench_df, x='Intento', y='Peso', ax=ax[0][0])

    # AX[0][1] ~ BENCH PROGRESSION BY SEX
    sns.boxplot(data=bench_df, x='Intento', y='Peso', hue='Sex',
                palette={'F': 'pink', 'M': 'blue'}, ax=ax[0][1])

    # SQUAT
    # NAMING SET
    ax[1][0].set_title("SQUAT PROGRESSION")
    ax[1][0].set_xlabel("ATTEMPT")
    ax[1][0].set_ylabel("LIFTED WEIGHT [KG]")

    ax[1][1].set_title("SQUAT PROGRESSION BY SEX")
    ax[1][1].set_xlabel("ATTEMPT")
    ax[1][1].set_ylabel("LIFTED WEIGHT [KG]")

    # AX[1][0] ~ SQUAT PROGRESSION
    sns.boxplot(data=squat_df, x='Intento', y='Peso', ax=ax[1][0])

    # AX[1][1] ~ SQUAT PROGRESSION BY SEX
    sns.boxplot(data=squat_df, x='Intento', y='Peso', hue='Sex',
                palette={'F': 'pink', 'M': 'blue'}, ax=ax[1][1])

    # DEADLIFT
    # NAMING SET
    ax[2][0].set_title("DEADLIFT PROGRESSION")
    ax[2][0].set_xlabel("ATTEMPT")
    ax[2][0].set_ylabel("LIFTED WEIGHT [KG]")

    ax[2][1].set_title("DEADLIFT PROGRESSION BY SEX")
    ax[2][1].set_xlabel("ATTEMPT")
    ax[2][1].set_ylabel("LIFTED WEIGHT [KG]")

    # AX[2][0] ~ DEADLIFT PROGRESSION
    sns.boxplot(data=deadlift_df, x='Intento', y='Peso', ax=ax[2][0])

    # AX[2][1] ~ DEADLIFT PROGRESSION BY SEX
    sns.boxplot(data=deadlift_df, x='Intento', y='Peso', hue='Sex',
                palette={'F': 'pink', 'M': 'blue'}, ax=ax[2][1])

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "question2.png", bbox_inches='tight')
    plt.close(fig)

# PREGUNTA 3


def graphs3(fail_global: pd.DataFrame, fail_sex_df: pd.DataFrame, fail_equip_df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))

    # NAMING SET
    ax[0].set_title("FAILRATE BY EXERCISE")
    ax[0].set_xlabel("EXERCISE")
    ax[0].set_ylabel("FAILRATE")

    ax[1].set_title("FAILRATE BY EXERCISE BY SEX")
    ax[1].set_xlabel("EXERCISE")
    ax[1].set_ylabel("FAILRATE ")

    ax[2].set_title("FAILRATE BY EXERCISE BY EQUIPMENT")
    ax[2].set_xlabel("EXERCISE")
    ax[2].set_ylabel("FAILRATE")

    # AX[0] ~ GENERAL PLOT
    sns.barplot(
        data=fail_global,
        x='Levantamiento',
        y='FailRate',
        orient='v',
        errorbar=None,
        ax=ax[0]
    )

    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt='%.1f%%')

    # AX[1] ~ PLOT BY SEX
    sns.barplot(
        data=fail_sex_df,
        x='Levantamiento',
        y='FailRate',
        hue='Sex',
        palette={'F': 'pink', 'M': 'blue'},
        errorbar=None,
        ax=ax[1]
    )

    # TAGS
    for container in ax[1].containers:
        ax[1].bar_label(container, fmt='%.1f%%')

    # LEGEND
    sns.move_legend(ax[1], "upper right")

    # EJE AX[1] ~ PLOT BY EQUIPMENT
    sns.barplot(
        data=fail_equip_df,
        x='Levantamiento',
        y='FailRate',
        hue='Equipment',
        errorbar=None,
        ax=ax[2]
    )

    # TAGS
    for container in ax[2].containers:
        ax[2].bar_label(container, fmt='%.1f%%')

    # LEGEND
    sns.move_legend(ax[2], "lower right")

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "question3.png", bbox_inches='tight')
    plt.close(fig)

# QUESTION 4

# SUBGRAPH 1 ~ PERFORMANCE BY EXERCISE BY MODALITY


def plot_performance_modality(bench_only_df: pd.DataFrame, squat_only_df: pd.DataFrame, deadlift_only_df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

    # NAMING SET
    ax[0].set_title("PERFORMANCE BY BANCH")
    ax[0].set_xlabel("MODALITY")
    ax[0].set_ylabel("PERFORMANCE")

    ax[1].set_title("PERFORMANCE BY SQUAT")
    ax[1].set_xlabel("MODALITY")
    ax[1].set_ylabel("PERFORMANCE")

    ax[2].set_title("PERFORMANCE BY DEADLIFT")
    ax[2].set_xlabel("MODALITY")
    ax[2].set_ylabel("PERFORMANCE")

    # AX[0] ~ BENCH
    sns.barplot(
        data=bench_only_df,
        x='Event',
        y='Dot_Bench',
        orient='v',
        errorbar=None,
        ax=ax[0]
    )

    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt='%.2f')

    # AX[0] ~ SQUAT
    sns.barplot(
        data=squat_only_df,
        x='Event',
        y='Dot_Squat',
        orient='v',
        errorbar=None,
        ax=ax[1]
    )

    # TAGS
    ax[1].bar_label(ax[1].containers[0], fmt='%.2f')

    # AX[0] ~ DEADLIFT
    sns.barplot(
        data=deadlift_only_df,
        x='Event',
        y='Dot_Deadlift',
        orient='v',
        errorbar=None,
        ax=ax[2]
    )

    # TAGS
    ax[2].bar_label(ax[2].containers[0], fmt='%.2f')

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "performance_modalitiy4.png", bbox_inches='tight')
    plt.close(fig)

# SUBGRAPH 2 ~ FAIL RATE


def plot_fail_rate4(df4b: pd.DataFrame):

    fig, ax = plt.subplots(figsize=(24, 6))

    # NAMING SET
    ax.set_title("FAILRATE AT 3RD ATTEMPT POR MODALITY")
    ax.set_xlabel("LIFT")
    ax.set_ylabel("FAILRATE ")

    # PLOT
    sns.barplot(
        data=df4b,
        x='Levantamiento',
        y='FailRate',
        orient='v',
        hue='Event',
        errorbar=None,
        ax=ax
    )

    # LEGEND
    sns.move_legend(ax, "upper right")

    # TAGS
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "fail_rate4.png", bbox_inches='tight')
    plt.close(fig)

# GRÁFICO 4 ITSELF


def graphs4(bench_only_df: pd.DataFrame, squat_only_df: pd.DataFrame, deadlift_only_df: pd.DataFrame, df4b: pd.DataFrame):
    plot_performance_modality(bench_only_df, squat_only_df, deadlift_only_df)
    plot_fail_rate4(df4b)

# QUESTION 5


def graficos5(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    # NAMING SET
    ax[0].set_title("SUCCESS RATE AT 4TH ATTEMPT")
    ax[0].set_xlabel("EXERCISE")
    ax[0].set_ylabel("SUCCESS RATE")

    ax[1].set_title("SUCCESS RATE AT 4TH ATTEMPT BY SEX")
    ax[1].set_xlabel("EXERCISE")
    ax[1].set_ylabel("SUCCESS RATE")

    # AX[0] ~ GENERAL PLOT
    sns.barplot(
        data=df,
        x='Levantamiento',
        y='SuccessRate',
        orient='v',
        errorbar=None,
        ax=ax[0]
    )

    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt='%.1f%%')

    # AX[1] ~ PLOT BY SEX
    sns.barplot(
        data=df,
        x='Levantamiento',
        y='SuccessRate',
        orient='v',
        hue='Sex',
        errorbar=None,
        ax=ax[1]
    )

    # TAGS
    for container in ax[1].containers:
        ax[1].bar_label(container, fmt='%.1f%%')

    # OUTPUT SET
    plt.tight_layout()
    plt.savefig(GRAPHS / "question5.png", bbox_inches='tight')
    plt.close(fig)
