"""
	@file plot_dca_vs_improved.py
	@author Matěj Říčný
	@brief Visualizes multiple metrics of portfolio performance
	@details From JSON results generates plots to compare multiple metrics:
            - maximum loss, invested capital, ROI, and average portfolio value.
            for each investment end date and saves the image.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Plotting Portfolio Value, ROI, Capital Invested and MAX loss
# for HODL, DCA, and Improved DCA
def plot_results():
    file = "results/final.json"
    try:
        with open(file, "r") as f:
            data = pd.DataFrame(json.load(f))
    except FileNotFoundError:
        print("File:", file, "was not found")
        return
    # Columns we need for each metric to be melted
    portfolio = ["HODL Portfolio", "DCA Portfolio", "Improved DCA Portfolio"]
    roi = ["HODL ROI", "DCA ROI", "Improved DCA ROI"]
    invested = ["HODL Invested", "DCA Invested", "Improved DCA Invested"]
    loss = ["HODL Max Loss", "DCA Max Loss", "Improved DCA Max Loss"]

    # Portfolio Value
    melted_portfolio = data.melt(
        id_vars="End Date",
        value_vars=portfolio,
        var_name="Strategy",
        value_name="Portfolio Value",
    )
    plot_bar(
        melted_portfolio,
        portfolio,
        "Average Portfolio Value of HODL, DCA, and Improved DCA",
        "img/portfolio_value.png",
    )

    # ROI
    melted_roi = data.melt(
        id_vars="End Date",
        value_vars=roi,
        var_name="Strategy",
        value_name="ROI (%)",
    )
    plot_bar(
        melted_roi, roi, "Average ROI of HODL, DCA, and Improved DCA", "img/roi.png"
    )

    # Invested Capital
    melted_invested = data.melt(
        id_vars="End Date",
        value_vars=invested,
        var_name="Strategy",
        value_name="Invested",
    )
    plot_bar(
        melted_invested,
        invested,
        "Average Invested Capital of HODL, DCA, and Improved DCA",
        "img/invested.png",
    )

    # Max Loss
    melted_loss = data.melt(
        id_vars="End Date",
        value_vars=loss,
        var_name="Strategy",
        value_name="Max Loss (%)",
    )
    plot_bar(
        melted_loss,
        loss,
        "Average Max Loss of HODL, DCA, and Improved DCA",
        "img/max_loss.png",
    )


def plot_bar(data, strategy, title, path):
    # Last column of every melted data is the needed metric
    metric = data.columns[-1]
    colors = ["#587b7f", "#e76f51", "#2a9d8f"]
    # Keeping the same color for strategies
    palette = {strategy: color for strategy, color in zip(strategy, colors)}
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=data,
        x="End Date",
        y=metric,
        hue="Strategy",
        hue_order=strategy,
        palette=palette,
        errorbar=None,
    )
    plt.title(title, fontsize=19, fontweight="bold")
    plt.xlabel("End Date", fontsize=15)
    plt.ylabel(metric, fontsize=15)
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()
    plt.savefig(path)
    plt.show()


plot_results()
