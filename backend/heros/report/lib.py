import pandas as pd
from pathlib import Path

from heros.api.metereologico import get_data
from heros.report.period import period_of, period_of_yearsago
from heros.report.plots import plot_month_precipitation, plot_period_precipitation, plot_period_temp, plt


def month_stats(data_month):
    data = data_month.groupby(pd.Grouper(freq="d")).agg(
        {"temperatura": ["max", "min"], "precipitacao": "sum"}
    )

    no_rain = data["precipitacao"]["sum"] < 0.01

    return dict(
        temp_min=data.temperatura["min"].min(),
        temp_max=data.temperatura["max"].max(),
        precip_total=data.precipitacao["sum"].sum(),
        days_wo_rain=data.precipitacao["sum"][no_rain].count(),
    )


def year_stats(years_ago=0, dir: Path = Path("tmp/")):
    lastmonth = get_data(period_of_yearsago(months=1, years=years_ago))
    inputs = month_stats(lastmonth)
    inputs.update(
        temp_daily_5months=dir / f"temp_daily_5months_{years_ago}.png",
        preci_monthly_5months=dir / f"temp_monthly_5months_{years_ago}.png",
        preci_daily_lastmonth=dir / f"preci_daily_lastmonth_{years_ago}.png",
    )

    daily_prec_lastmonth = lastmonth.groupby(pd.Grouper(freq="d"))
    plot_month_precipitation(
        daily_prec_lastmonth["precipitacao"].sum(), inputs["preci_daily_lastmonth"]
    )

    fivemonths = get_data(period_of(months=5))
    fivemonths_daily = fivemonths.groupby(pd.Grouper(freq="d"))
    fivemonths_monthly = fivemonths.groupby(pd.Grouper(freq="ME"))
    plot_period_precipitation(
        fivemonths_monthly["precipitacao"].sum(), inputs["preci_monthly_5months"]
    )
    plot_period_temp(
        fivemonths_daily["temperatura"].agg(
            ["mean", "max", "min"],
        ),
        save_to=inputs["temp_daily_5months"],
    )
    plt.close()
    return inputs


def add_suffix_key(to_rename: dict, suffix: str):
    values = map(lambda k: k + suffix, to_rename.keys())
    keys = to_rename.values()
    return dict(zip(values, keys, strict=True))


