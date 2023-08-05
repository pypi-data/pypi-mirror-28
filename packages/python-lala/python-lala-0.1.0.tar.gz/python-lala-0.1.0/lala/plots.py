from datetime import datetime

import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')
reader = shpreader.Reader(shpfilename)
countries = list(reader.records())
name_to_geometry = {
    country.attributes[e]: country.geometry
    for country in countries
    for e in ('ADM0_A3', 'BRK_NAME')
}
name_to_extent = {
    name: geometry.bounds
    for name, geometry in name_to_geometry.items()
}


def init_map(figsize=(12, 8),  extent=(-150, 60, -25, 60)):
    """Initialize a world map with the given dimensions."""
    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)

    ax.set_extent(extent)
    ax.figure.set_size_inches(figsize)
    return ax


def countries_colormap(country_values, figsize=(12, 8), mini='auto',
                       maxi='auto', extent=(-150, 60, -25, 60)):
    countries, values = zip(*country_values)
    values = np.array(values)
    if mini == 'auto':
        mini = values.min()
    if maxi == 'auto':
        maxi = values.max()
    values = (values - mini) / (maxi - mini)
    country_values = zip(countries, values)

    ax = init_map(figsize=figsize, extent=extent)
    for (country_name, value) in country_values:
        if country_name not in name_to_geometry:
            continue
        color = cm.YlOrBr(value)
        ax.add_geometries(name_to_geometry[country_name], ccrs.PlateCarree(),
                          facecolor=color)
    return ax


def plot_geo_positions(dataframe, ax):
    counts = [
        (len(dataframe_), ll)
        for (ll, dataframe_) in dataframe.groupby(['longitude', 'latitude'])
    ]
    counts, xy = zip(*(sorted(counts)[::-1]))
    counts = 1.0 * np.array(counts)
    counts = np.maximum(5, 600 * counts / counts.max())
    xx, yy = [list(e) for e in zip(*xy)]
    ax.scatter(xx, yy, c='w', s=counts, zorder=2000, linewidths=2,
               edgecolor='k', transform=ccrs.Geodetic())


def plot_piechart(dataframe, column, ax=None):
    count = dataframe[column].value_counts()
    ax = count.plot(kind='pie', ax=ax)
    ax.set_aspect('equal')
    ax.set_ylabel('')
    return ax, count


def plot_entries_in_time(dataframe, bins_per_day=4, ax=None):
    mini, maxi = dataframe['timestamp'].min(), dataframe['timestamp'].max()
    seconds_in_a_day = 24 * 60 * 60
    bins = int(bins_per_day * (maxi - mini) / seconds_in_a_day)
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(12, 3))
    dataframe['timestamp'].plot(kind='hist', bins=bins, alpha=0.6)
    x_ticks = ax.get_xticks()
    xlabels = [datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d')
               for x in x_ticks]
    ax.set_xticklabels(xlabels, rotation=45)
    ax.set_xlim(mini, maxi)
    ax.set_ylabel('occurences')
    return ax
