import pandas as pd
import random
import os


def main():
    """Подготавливает входные данные"""

    colors = [
        "#17becf",
        "#bcbd22",
        "#7f7f7f",
        "#e377c2",
        "#8c564b",
        "#9467bd",
        "#d62728",
        "#2ca02c",
        "#ff7f0e",
        "#1f77b4"
    ]

    path = "Output"
    if not os.path.exists(path):
        os.makedirs(path)

    df = pd.read_csv("tz_data.csv", delimiter=",")
    df2 = df.drop(df.columns[4], axis=1)
    df2.y = pd.to_numeric(df2["y"], errors="coerce")
    df2["count"] = pd.to_numeric(df2["count"], errors="coerce")
    df2 = df2.dropna()
    df2 = df2.drop_duplicates(subset=["area", "keyword"])

    dict_color_order = {}

    for cat in df2["area"].unique():
        dict_color_order[cat] = random.sample(colors, len(colors))

    df2["cluster"] = df2["cluster"].astype("int")
    df2["colors"] = df2.apply(
        lambda x: dict_color_order[x.area][x.cluster], axis=1)
    df2.sort_values(by=["area", "cluster", "cluster_name",
                    "count"], ascending=[True, True, True, False])
    df2.to_csv("Output/Output.csv", index=False)


if __name__ == "__main__":
    main()
