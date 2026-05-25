# 1. Objective
Analyze the performance of powerlifting athletes in official, drug-tested competitions to answer 5 specific questions regarding age, progression, failed attempts, and specialization. The goal is to extract clear insights to support athletes' strategies during competition.

## 1.1. Questions
The questions I aimed to answer were:

1. At what age do athletes reach their peak performance? Does it differ between men and women?
2. How do athletes progress within a competition? Do they increase the weight between attempts 1 → 2 → 3, or do they tend to repeat/decrease it?
3. In which lift (squat, bench press, deadlift) do most failed attempts occur on the 3rd attempt?
4. Do athletes who compete in more full-lifting events perform better or worse than those who specialize in a single lift?
5. What is the success rate of the 4th attempt? Do they actually manage to outperform themselves?

## 1.2. Dataset
For this project, I used the open-source CSV from **Open Powerlifting**. The raw dataset contains ~3.9M rows and 42 columns. Every single variable is defined in `OPL_guide.txt`, which is attached to the project (acting as their project's `README.md`). I downloaded it directly into the `data` directory as `OPL_dataset.csv`. You can download it at: [Open Powerlifting](https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html).

The file used is `openpowerlifting-latest.zip`, with a size of 158MB and 3,925,888 rows (at the time of download [05/2026]).

# 2. Procedure

## 2.1. Pipeline

The pipeline is clearly structured in `main.py` and detailed in the notebook, but it essentially followed these steps:

1. **DataFrame Loading and Pre-filtering**: Before starting the exploration, and after reviewing `OPL_guide.txt`, I reduced the DataFrame's dimensions. I filtered the data to keep only the columns I would actually use and restricted the records to athletes in official, drug-tested competitions.
2. **Cleaning**: This involved removing absolute duplicates, fixing data types, and imputing as many missing values (nulls) as possible instead of simply dropping them.
3. **Feature Engineering**: Before finishing the cleaning process, I had to create the boolean indicator columns; doing it later would have been impossible.
4. **Finalizing Cleaning**: I handled the negative values in the attempt columns and removed rows corresponding to the mixed-sex category due to the lack of sufficient data (~100 rows) and to streamline the analysis.
5. **Asserts**: I implemented assertions to verify that the entire cleaning process executed correctly (checking negative values, deleted columns, newly created columns, etc).
6. **Saving and Exploration**: The goal was to save the clean dataset and observe the 4 main "_tag_" variables: Age, Sex, Event Type (SBD), and Equipment allowed (Section 6 of `notebooks/eda.ipynb`).
7. **Analysis**: This is the most extensive part. It consists of 5 sub-sections where I answer each of the initial questions and display their respective plots (Sections 7 and 8 of `notebooks/eda.ipynb`).

## 2.2. Data Issues & Fixes
The main challenge with this dataset is the high volume of null values across most columns, though many of these nulls are logically valid. For instance, if an athlete did not perform a specific lift, that column is naturally null. To bypass this initial issue, I made a strict decision: using the available columns, I imputed the maximum possible values for all relevant variables, but I chose not to artificially fill data with means or medians to preserve the integrity of the original dataset. After this baseline cleaning, the DataFrame is pre-filtered dynamically for each specific question to remove only the relevant NaNs. This approach prevented the massive data loss that a global row-dropping strategy would have caused.

Another major issue in the raw dataset is that failed attempts are recorded as negative values. These negative numbers distort statistical metrics like the mean and offer little utility beyond indicating that the attempt occurred and failed. To resolve this, the cleaning pipeline applied the following logic:

1. I generated boolean columns (configured to handle NaNs) to record whether a lift was successful (`True`), failed (`False`), or not attempted (`NaN`). I only did this for the 3rd and 4th attempts of each lift, as these were the only ones required for the analysis.
2. Once these boolean indicators were established (and not before), all values in the original attempt columns that were 0 or negative were converted to `NaN`. This ensured they would be cleanly filtered out during question-specific analysis.

Additionally, the original dataset included 4 different performance coefficients: Dots, Wilks, Glossbrenner, and Goodlift. I decided to stick exclusively with Dots, as it is the most up-to-date metric. I attempted to impute missing Dots values using the other coefficients, but whenever Dots was `NaN`, the others were missing as well. Ultimately, to answer Question 4, I engineered a simple, custom metric to evaluate standardized performance regardless of whether athletes competed in full-power or single-lift events. I verified its validity by checking that it correlated strongly with Dots (r > 0.85).

Finally, as with any real-world "dirty" dataset, I had to cast data types, filter data (strictly for official and tested ("natty") competitions), and reshape the dataframes to meet the statistical assumptions required for tests like **ANOVA** or **POST-HOC** in Question 2.

The entire preprocessing workflow is documented in `src/cleaning.py`, while the question-specific filtering is located in `src/analysis.py`. You can also review the exploratory data analysis and cleaning steps in sections 3-6 of the notebook `notebooks/eda.ipynb`.

# 3. Results

## 3.1. Insights

- The peak performance window for a powerlifting athlete occurs around age 22 and sustains until age 24, after which performance begins to decline at an accelerating rate.

- The bench press is notably different from the deadlift and the squat. It is the only lift where specialization yields a clear performance improvement, and it is the only one with a failure rate higher than 50% on the third attempt. For the squat and deadlift, the strength developed in the other disciplines appears to be highly transferable, resulting in a much lower failure rate (~30%). 
[This conclusion should be taken with caution due to data asymmetry].

- The universal tendency for athletes to attempt a heavier weight on each subsequent lift suggests that the final attempt is the most critical in competition. Concurrently, the failure rate on this final attempt is high, particularly in the bench press. Combined, these findings suggest a competitive strategy: taking greater risks on the second attempt to apply pressure on other lifters.

- It is highly recommended that athletes take a fourth attempt when permitted. Since this attempt is free from competition pressure, it boasts a success rate of ~80% (pending verification to rule out publication bias). This is extremely valuable data for planning future competitions.

- **Additional Note**: No significant differences between sexes were observed in any of the analyzed trends, except for the obvious variance in absolute loads, which disappears once normalized for body weight.

## 3.2. Future Perspectives and Analysis

- Develop a predictive model to estimate the maximum weight an athlete can successfully lift on their next attempt, thereby optimizing competition attempts in real-time.

- Incorporate biological variables such as sleep duration, diet, and recovery metrics prior to competitions to perform a more robust analysis.

- Replicate this study exclusively using the SBD (full-power) category, as it is the predominant division. This would make the insights even more directly transferable to the standard competitive field.

# 4. Project Information

## 4.1 Project Structure

```
project/
├── .venv/                          # VIRTUAL ENVIRONMENT
├── data/                           # DATASETS & GRAPHS
│   ├── output_graphs/                  # GRAPHS OUTPUT
│   ├── clean_dataset.csv               # CLEAN
│   └── OPL_dataset.csv                 # RAW
├── notebooks/
│   └── eda.ipynb                   # FULL-PIPELINE INDEPENDENT NOTEBOOK
├── src/                            # PIPELINE MODULARIZATION
│   ├── __init__.py
│   ├── analysis.py                 # FUNCTIONS TO ANSWERS Q1-Q5
│   ├── cleaning.py                 # CLEANING FUNCTIONS
│   ├── config.py                   # CONFIGURATION
│   ├── features.py                 # NEW COLUMNS
│   ├── io.py                       # UPLOAD AND DOWNLOAD SETUP
│   ├── utils.py                    # HELPER FUNCTIONS & ASSERTS
│   └── viz.py                      # GRAPHS CREATOR
├── .gitignore
├── OPL_guide.txt                   # OPEN POWERLIFTING GUIDE FOR BETTER UNDERSTANDING
├── main.py                         # MANAGER FILE
├── README.md                       # THE GUIDE YOU ARE READING RIGHT NOW :)
└── requirements.txt                # PROJECT's REQUIREMENTS TO WORK
```

## 4.2. How to execute it yourself

### STEP 1 ~ Download the dataset

  I. Go to [Open Powerlifting](https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html) and download the FULL DATASET.
 II. Place it inside the `data` folder.
III. **[Option A ~ Recommended]** Rename the file to `OPL_dataset.csv` (copy-paste).
 IV. [Option B] **If you decide not to rename it**, you must:
- In the `main.py` file, modify line 23:
```python
# LINEA ACTUAL
df = load(DATA / "OPL_dataset.csv")

# TU LINEA
df = load(DATA / "tu_nombre_archivo.csv")
```

In notebooks/eda.ipynb, modify the LOADING section:
```python
# LINEA ACTUAL
        opl_df = pd.read_csv('../data/OPL_dataset.csv', low_memory = False)

# TU LINEA
        opl_df = pd.read_csv('../data/tu_nombre_archivo.csv', low_memory = False)
```

### STEP 2 ~ Create, Activate & Prepare the Virtual Environment

Run the following blocks of code step-by-step (line by line) in your computer's terminal.

**MAC/LINUX**
```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

**WINDOWS**
```powershell
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```
### STEP 3 ~ Execution
```PowerShell
python main.py
```

PS1: You can also run and review the notebook for further clarity and detailed explanations :)

PS2: Execution might take a little while since the operations are not fully optimized :)