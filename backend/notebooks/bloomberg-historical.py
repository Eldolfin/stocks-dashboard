import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from glob import glob
    import marimo as mo

    return glob, mo, pd


@app.cell
def _(glob):
    all_files = glob("./historical-data/history*.xlsx")
    files_multi = glob("./historical-data/history*10 stocks*.xlsx")
    files_single = list(set(all_files) - set(files_multi))
    return (files_multi,)


@app.cell
def _(files_multi, mo, pd):
    for file in mo.status.progress_bar(files_multi, title="reading multi file"):
        multi = pd.read_excel(
            file,
            header=1,
        )
        reshaped_columns = multi.columns[1:-27].to_numpy().reshape(-1, 29)

        for sub_cols in reshaped_columns:
            sub_df = multi[sub_cols]
            ticker = sub_df.columns[0].split(" ")[0].replace("/", "-")
            sub_df = sub_df.iloc[:, 1:]
            sub_df.to_csv(f"./historical-data/cleaned/{ticker}.csv")

    return


if __name__ == "__main__":
    app.run()
