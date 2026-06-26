import os
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "outputs/eda"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_eda(df):

    numeric_columns = [
        col for col in df.columns
        if col != "CustomerID"
    ]

    # ---------- Histograms ----------
    hist_dir = os.path.join(OUTPUT_DIR, "histograms")
    os.makedirs(hist_dir, exist_ok=True)

    for column in numeric_columns:

        plt.figure(figsize=(6,4))

        sns.histplot(df[column], bins=30)

        plt.title(column)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                hist_dir,
                f"{column}.png"
            )
        )

        plt.close()

    # ---------- Boxplots ----------

    box_dir = os.path.join(OUTPUT_DIR, "boxplots")
    os.makedirs(box_dir, exist_ok=True)

    for column in numeric_columns:

        plt.figure(figsize=(6,2))

        sns.boxplot(
            x=df[column]
        )

        plt.title(column)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                box_dir,
                f"{column}.png"
            )
        )

        plt.close()

    # ---------- Correlation ----------

    plt.figure(figsize=(10,8))

    sns.heatmap(
        df[numeric_columns].corr(),
        annot=True,
        cmap="coolwarm"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "correlation_matrix.png"
        )
    )

    plt.close()