import datetime
import os.path
from typing import Tuple, List, Optional

import numpy as np

import netCDF4
import matplotlib.dates


def read_0d_observations(path: str) -> np.ndarray:
    obs = []
    for l in open(os.path.join(path)):
        if not l.startswith("#"):
            dt, value, sd = l.rstrip().rsplit(maxsplit=2)
            mu = float(value)
            sigma = float(sd)
            p25 = mu - 0.67448 * sigma
            p75 = mu + 0.67448 * sigma
            obs.append(
                [datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"), mu, p25, p75]
            )
    return np.array(obs).reshape(-1, 4)


def read_result(
    path: str, name: str
) -> Tuple[List[datetime.datetime], np.ndarray, np.ndarray, str, str]:
    with netCDF4.Dataset(path) as nc:
        nctime = nc["time"]
        time = netCDF4.num2date(
            nctime,
            nctime.units,
            only_use_cftime_datetimes=False,
            only_use_python_datetimes=True,
        )
        z = -nc["z"][:, :, 0, 0]
        ncvar = nc[name]
        values = ncvar[..., 0, 0]
        return time, z, values, ncvar.long_name, ncvar.units


def read_ensemble_result(
    path: str, name: str, N: int
) -> Tuple[List[datetime.datetime], np.ndarray, np.ndarray, str, str]:
    pathname, pathext = os.path.splitext(path)
    results = []
    for i in range(1, N + 1):
        time, z, values, long_name, units = read_result(
            f"{pathname}_{i:04}{pathext}", name
        )
        results.append(values)
    return time, z, np.array(results), long_name, units


def plot_0d_timeseries(ax, time, values, obs, label: str = "model", extra_series=[]):
    low = obs[:, 1] - obs[:, 2]
    high = obs[:, 3] - obs[:, 1]
    ax.errorbar(
        obs[:, 0],
        obs[:, 1],
        yerr=[low, high],
        ecolor="k",
        elinewidth=1.0,
        fmt=".k",
        alpha=0.4,
        zorder=-1,
        label="observations",
    )
    icolor = 0
    for extra_label, extra_values in extra_series:
        ax.plot_date(time, extra_values, "-", color=f"C{icolor}", label=extra_label)
        icolor += 1
    (series,) = ax.plot_date(time, values, "-", color=f"C{icolor}", label=label)
    ax.set_xlim(time[0], time[-1])
    ax.xaxis.set_major_formatter(
        matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    )
    ax.grid()
    ax.legend()
    return series


def plot_1d_timeseries(ax, time, z, values, *args, cax=None, **kwargs):
    fig = ax.figure
    time_2d = np.broadcast_to(time[:, np.newaxis], z.shape)
    pc = ax.contourf(time_2d, z, values, *args, **kwargs)
    cb = fig.colorbar(pc, cax=cax)
    ax.set_ylabel("depth (m)")
    ax.xaxis.axis_date()
    ax.set_xlim(time[0], time[-1])
    ax.xaxis.set_major_formatter(
        matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    )
    ax.grid()
    ax.set_ylim(z.max(), z.min())
    return pc, cb


def plot_0d_ensemble_timeseries(
    ax,
    time,
    ens,
    ref={},
    obs=None,
    filter_period: int = 1,
    plot_spread: bool = True,
    label: Optional[str] = None,
):
    if filter_period != 1:
        import scipy.signal

        ens = scipy.signal.medfilt(ens, (1, filter_period))

    if obs is not None:
        low = obs[:, 1] - obs[:, 2]
        high = obs[:, 3] - obs[:, 1]
        # ax.plot_date(obs[:,0], obs[:,1], '.k', alpha=0.4, label='observations')
        ax.errorbar(
            obs[:, 0],
            obs[:, 1],
            yerr=[low, high],
            ecolor="k",
            elinewidth=1.0,
            fmt=".k",
            alpha=0.4,
            zorder=-1,
            label="observations",
        )
    label = label or "model"
    icolor = 0
    for reflabel, refvalues in ref:
        ax.plot_date(time, refvalues, "-", color=f"C{icolor}", label=reflabel)
        icolor += 1
    if plot_spread:
        p25 = np.percentile(ens, 25.0, axis=0)
        p75 = np.percentile(ens, 75.0, axis=0)
        pmin = np.min(ens, axis=0)
        pmax = np.max(ens, axis=0)
        ax.fill_between(
            time,
            pmin,
            pmax,
            alpha=0.2,
            label=f"{label}, ensemble min to max",
            fc=f"C{icolor}",
        )
        ax.fill_between(time, p25, p75, fc="w")
        ax.fill_between(
            time,
            p25,
            p75,
            alpha=0.5,
            label=f"{label}, 1st to 3rd ensemble quartile",
            fc=f"C{icolor}",
        )
        for p in (pmin, pmax, p25, p75):
            ax.plot_date(time, p, "-k", lw=0.2)
        label = f"{label}, ensemble median"

    median = np.median(ens, axis=0)
    ax.plot_date(time, median, "-", color=f"C{icolor}", label=label)
    ax.grid()
    ax.legend()
    ax.set_xlim(time[0], time[-1])
    ax.xaxis.set_major_formatter(
        matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    )


def plot_1d_ensemble_timeseries(ax, time, z, ens, *args, cax=None, **kwargs):
    fig = ax.figure
    time_2d = np.broadcast_to(time[:, np.newaxis], z.shape)
    pc = ax.contourf(time_2d, z, np.median(ens, axis=0), *args, **kwargs)
    cb = fig.colorbar(pc, cax=cax)
    ax.set_ylabel("depth (m)")
    ax.grid()
    ax.xaxis.axis_date()
    ax.set_xlim(time[0], time[-1])
    ax.xaxis.set_major_formatter(
        matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    )
    ax.set_ylim(z.max(), z.min())
    return pc, cb
