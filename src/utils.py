import re

import matplotlib.pyplot as plt
import pandas as pd


def plot_barplot(col):
    counts = col.value_counts()

    _, ax = plt.subplots(figsize=(10, 5))
    ax.bar(counts.index, counts.values, edgecolor="k", linewidth=0.3)
    ax.set_xlabel(col.name)
    ax.set_ylabel("Count")
    ax.set_title(f"Distribution of {col.name}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def linreg(x_col, y_col):
    mask = x_col.notna() & y_col.notna()
    x = x_col[mask]
    y = y_col[mask]

    corr = x.corr(y)  # Pearson r

    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, alpha=0.5, edgecolors="k", linewidths=0.3)
    plt.xlabel(x_col.name)
    plt.ylabel(y_col.name)
    plt.title(f"{x_col.name} vs {y_col.name}")
    plt.text(
        0.05,
        0.95,
        f"r = {corr:.3f}",
        transform=plt.gca().transAxes,
        va="top",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    plt.tight_layout()
    plt.show()

    print(f"Pearson r : {corr:.4f}")


def parse_column(df, col, attrname, stringed=False):
    rows = []
    for idx, row in df.iterrows():
        cell = row[col]
        if pd.isna(cell) or cell == "":
            continue

        text = str(cell)
        seg_sep = "||" if "||" in text else "|"
        for part in text.split(seg_sep):
            if "::" in part:
                position, value = part.split("::", 1)
            elif ":" in part:
                position, value = part.split(":", 1)
            else:
                continue
            try:
                position = int(position)
            except ValueError:
                continue
            if stringed:
                rows.append(
                    {"original_index": idx, "position": position, attrname: str(value)}
                )
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue
                rows.append(
                    {"original_index": idx, "position": position, attrname: value}
                )

    return pd.DataFrame(rows)


def parse2(df, col):
    rows = []
    for idx, row in df.iterrows():
        cell = row[col]
        if pd.isna(cell) or cell == "":
            continue

        for value in re.split(r"\|\|?", str(cell)):
            rows.append({"original_index": idx, col: value.strip()})

    return pd.DataFrame(rows)


def index_preprocessing(df):
    df["id"] = df["original_index"].astype(str) + "p" + df["position"].astype(str)
