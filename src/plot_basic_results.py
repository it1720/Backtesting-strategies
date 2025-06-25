"""
	@file plot_basic_results.py
	@author Matěj Říčný
	@brief Visualizes portfolio size over time
	@details From JSON results generates plots to compare average
            and median portfolio sizes for each investment end date and saves the image.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting basic metrics for HODL, DCA and Rebalaned Portfolio.
def plot_basic_results():
    file = "results/portfolio_results.json"
    try:
        with open(file, "r") as f:
            data = pd.DataFrame(json.load(f))
    except FileNotFoundError:
        print("File:",file,"was not found")
        return
    # Getting data + setting order for plotting strategies
    strategies = ["HODL Portfolio", "DCA Portfolio", "Rebalanced Portfolio"]

    melted = data.melt(
        id_vars="End Date",
        value_vars=strategies,
        var_name="Strategy",
        value_name="Portfolio Value",
    )

    sns.set_style("whitegrid")
    # Average portfolio value for each strategy
    plot_bar(
        melted,
        strategies,
        "Average Portfolio Value of HODL, DCA, and Rebalancing Strategies",
        "img/basic/portfolio_average.png",
    )

    # Median portfolio value for each strategy
    median = melted.groupby(["End Date", "Strategy"]).median().reset_index()
    plot_bar(
        median,
        strategies,
        "Median Portfolio Value for HODL, DCA, and Rebalancing Strategies",
        "img/basic/portfolio_median.png",
    )


def plot_bar(data, strategies, title, path):
    palette = {
        "HODL Portfolio": "#587b7f",
        "DCA Portfolio": "#e76f51",
        "Rebalanced Portfolio": "#2a9d8f",
    }
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=data,
        x="End Date",
        y="Portfolio Value",
        hue="Strategy",
        hue_order=strategies,
        palette=palette,
        errorbar=None,
    )
    plt.title(title, fontsize=15, fontweight="bold")
    plt.xlabel("End Date", fontsize=13)
    plt.ylabel("Portfolio Value", fontsize=13)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.savefig(path)
    plt.show()


plot_basic_results()
