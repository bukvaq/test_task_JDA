import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
import os


def text_cutter(text):
    """Разбивает входной текст на строки"""

    text_split = text.split()
    total_string = text_split[0]
    for i in text_split[1:]:
        if len(total_string.split("\n")[-1])+len(i)+1 >= 15:
            total_string = f"{total_string}\n{i}"
        else:
            total_string = f"{total_string} {i}"
    return total_string


def cleanFilename(sourcestring,  removestring=" %:/,.\\[]<>*?"):
    """Удаляет указанные символы из строки"""

    return ''.join([c for c in sourcestring if c not in removestring])


def main():
    """Создаёт графики по подготовленным данным"""

    path = "Output/Images"
    if not os.path.exists(path):
        os.makedirs(path)

    df2 = pd.read_csv("Output/Output.csv", delimiter=",")
    for area_iteration in df2.area.unique():
        fig, ax = plt.subplots()
        df_area = df2[df2.area == area_iteration]
        texts_to_adjust = []

        for cluster_iteration in df_area.cluster_name.unique():
            df_cluster = df_area[df_area.cluster_name == cluster_iteration]
            df_cluster.plot.scatter(
                x="x",
                y="y",
                ax=ax,
                c=df_cluster.colors.tolist(),
                label=cluster_iteration,
                marker="o",
                edgecolor="black",
                linewidths=0.5,
                s=df_cluster["count"]/10+6,
                alpha=0.8
            )

            for _, row_series in df_cluster.iterrows():
                texts_to_adjust.append(
                    ax.annotate(text=text_cutter(row_series.keyword),
                                xy=(row_series.x, row_series.y),
                                fontsize=8)
                )
            for texts in texts_to_adjust:
                texts.set_alpha(.8)

        ax.grid(False)
        ax.axis('off')
        ax.set_title(f"Area: {area_iteration}", y=-0.1)

        lgd = ax.legend(bbox_to_anchor=(-0.05, 0.5))

        for handle in lgd.legendHandles:
            handle.set_sizes([20.0])

        adjust_text(texts_to_adjust)

        plt.savefig(
            f"Output/Images/{cleanFilename(area_iteration)}.png",
            bbox_extra_artists=(lgd,),
            bbox_inches='tight',
            dpi=400
        )


if __name__ == "__main__":
    main()
