import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns


custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)


def plot_period_precipitation(prec_data, save_to=None):
    fig, ax = plt.subplots()
    sns.barplot(prec_data, formatter=lambda x: x.month_name(), ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Precipitação mm")
    fig.tight_layout()
    if save_to:
        fig.savefig(
            save_to,
        )


def plot_month_precipitation(prec_data, save_to=None):
    fig, ax = plt.subplots()
    sns.barplot(prec_data, ax=ax)
    ax.set_ylim(0, 40)
    locator = mdates.DayLocator(interval=2)
    formatter = mdates.DateFormatter("%d")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlabel("")
    ax.set_ylabel("Precipitação mm")
    fig.tight_layout()
    if save_to:
        fig.savefig(
            save_to,
        )


def plot_period_temp(data, upper_lim=45, save_to=None):
    fig, ax = plt.subplots()
    ax.set_ylim(0, upper_lim)
    sns.lineplot(data, ax=ax)
    # ax.legend(["Média", "Max.", "Min."])
    locator = mdates.MonthLocator()
    formatter = mdates.DateFormatter(fmt="%b")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_ylabel("Temperatura °C")
    ax.set_xlabel("")
    fig.tight_layout()
    if save_to:
        fig.savefig(
            save_to,
        )
