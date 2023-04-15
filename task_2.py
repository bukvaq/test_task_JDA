import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
import os


def text_cutter(text):
    """Единожды разбивает входной текст на две строки
    если длина строки больше 15 символов"""

    text_split = text.split()
    total_string = ""
    check = False
    for i in text_split:
        if len(total_string)+len(i)+1 >= 15 and check is False:
            total_string = "\n"+total_string
            check = True
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
                x='x',
                y='y',
                ax=ax,
                c=df_cluster.colors.tolist(),
                label=cluster_iteration,
                marker="o",
                edgecolor="black",
                linewidths=0.5
            )

            for _, row_series in df_cluster.iterrows():
                texts_to_adjust.append(
                    ax.annotate(text=text_cutter(row_series.keyword),
                                xy=(row_series.x, row_series.y),
                                # arrowprops={"arrowstyle": "->"},
                                fontsize=7)
                )

        ax.grid(False)
        ax.axis('off')
        ax.set_title(f"Area: {area_iteration}", y=-0.1)

        lgd = ax.legend(bbox_to_anchor=(-0.05, 0.5))

        adjust_text(texts_to_adjust)

        plt.savefig(
            f"Output/Images/{cleanFilename(area_iteration)}.png",
            bbox_extra_artists=(lgd,),
            bbox_inches='tight'
        )


if __name__ == "__main__":
    main()
