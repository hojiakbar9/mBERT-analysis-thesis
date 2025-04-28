import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Example Data (replace with your actual data)
data = {
    "Class": [
        "PosixParser",
        "OptionGroup",
        "HelpFormatter",
        "DefaultParser",
        "Caverphone, Codec 1",
        "Metaphone",
        "SoundexUtils",
        "Base64, Codec 4",
        "Base64, Codec 7",
        "Base64, Codec 8",
        "Base64, Codec 9",
        "Caverphone, Codec 10",
        "DoubleMetaphone",
        "StringUtils",
        "Lang",
        "PhoneticEngine",
        "Element, Jsoup 3",
        "Parser",
        "Entities, Jsoup 4",
        "Entities, Jsoup 6",
        "Node, Jsoup 8",
        "Element, Jsoup 22",
        "Elements",
        "Node, Jsoup 22",
    ],
    "LOC": [
        276,
        175,
        1042,
        707,
        183,
        405,
        123,
        1055,
        1071,
        1025,
        1061,
        185,
        1009,
        286,
        231,
        528,
        844,
        309,
        2245,
        2244,
        420,
        1119,
        536,
        615,
    ],
    "Cyclomatic Complexity": [
        28,
        15,
        103,
        101,
        9,
        110,
        12,
        123,
        118,
        112,
        115,
        9,
        255,
        31,
        20,
        37,
        120,
        62,
        15,
        15,
        60,
        92,
        101,
        92,
    ],
    "Mutation Time (seconds)": [
        1285,
        549,
        5426,
        5032,
        2939,
        4543,
        562,
        7035,
        7635,
        7413,
        7417,
        2987,
        13730,
        853,
        1327,
        3616,
        3789,
        3976,
        983,
        1179,
        2897,
        6968,
        2610,
        5729,
    ],
}

df = pd.DataFrame(data)

# Calculate Pearson Correlation
correlation_LOC_time, _ = pearsonr(df["LOC"], df["Mutation Time (seconds)"])
correlation_CC_time, _ = pearsonr(
    df["Cyclomatic Complexity"], df["Mutation Time (seconds)"]
)

print(f"Correlation between LOC and Mutation Time: {correlation_LOC_time}")
print(
    f"Correlation between Cyclomatic Complexity and Mutation Time: {correlation_CC_time}"
)

# Scatter plot for visualization
plt.scatter(df["LOC"], df["Mutation Time (seconds)"], label="LOC vs Mutation Time")
plt.scatter(
    df["Cyclomatic Complexity"],
    df["Mutation Time (seconds)"],
    label="Cyclomatic Complexity vs Mutation Time",
    color="r",
)
plt.xlabel("LOC and Cyclomatic Complexity")
plt.ylabel("Mutation Time (seconds)")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

plt.savefig("mutation_correlation_plot_customized.png", bbox_inches="tight")
