import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def plot_pairwise(trials_df, hyper_config, save_path):
    startup_cutoff = hyper_config["optuna"]["sampler"]["n_startup_trial"]
    metric_name = hyper_config["optuna"]["metric"]
    hyperparameters = hyper_config["optuna"]["parameters"]
    
    # select parameters that are optimized on a log basis
    temploghyperparams = [x for x in hyperparameters if "log" in hyperparameters[x]["type"]]
    loghyperparams = []
    for named_parameter, _ in temploghyperparams.items():
        if ":" in named_parameter:
            split_name = named_parameter.split(":")
            loghyperparams.append(f"params_{split_name[-1]}")

    # Change optimized variable name to be more meaningful
    trials_df.rename(columns={"value": metric_name})

    # Create a column for coloring that separates startup vs optimizing trials
    trials_df["hue"] = (["startup"] * startup_cutoff + 
                        ["optimize"] * (len(trials_df)-startup_cutoff)
    )

    pairplot = sns.pairplot(trials_df, hue="hue")
    for ax in pairplot.axes.flat:
        if ax.get_xlabel() in loghyperparams:
            ax.set(xscale="log")
        if ax.get_ylabel() in loghyperparams:
            ax.set(yscale="log")
    figure_save_path = os.path.join(save_path, "pairplot.png")
    plt.savefig(figure_save_path)
