# For plotting.
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.mplot3d.proj3d import transform

from research.config.params import LAT_RANGE, LON_RANGE
from research.log import Log


# -------------------------- CADC 绘图 --------------------------
# 绘图的所有函数都返回一个figure和一个axes对象， 可用于将不同的图像绘制在同一个figure上

def plot_cdac_argo_data_one_day(one_day_data, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制一天的浮标位置分布图
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(10, 6))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111, projection = ccrs.PlateCarree())

    ax.set_extent([LON_RANGE[0], LON_RANGE[1], LAT_RANGE[0], LAT_RANGE[1]], crs=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()

    gl = ax.gridlines(draw_labels=True)
    gl.xlocator = plt.MaxNLocator(18)
    gl.ylocator = plt.MaxNLocator(18)
    ax.set_title('CDCA Argo Data One Day Float Position Distribution', pad=20)

    # 提取经纬度坐标
    lon = []
    lat = []

    for i, data in enumerate(one_day_data):
        pos = data['pos']
        lon.append(pos['lat'])
        lat.append(pos['lon'])

    ax.scatter(lat, lon, s=20, transform = ccrs.PlateCarree(), marker="*", color='#2ca02c')

    plt.show()

    return figure, ax


def plot_cdac_float_temperature_profile(float_data, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制单个浮标数据的剖面温度图
    :param float_data: Only part of the data is used
    :param figure:  If None, a new figure will be created
    :param ax:  If None, a new axes will be created
    :return: figure, ax
    """

    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(8, 10))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111)

    ax.set_title('CDCA Argo Data Profile')
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Pressure (dbar)')

    # 提取经纬度坐标
    pressures = -np.array(float_data['pres'][::-1])
    adjusted_pressures = -np.array(float_data['pres_adj'][::-1])
    temperatures = np.array(float_data['temp'][::-1])
    adjusted_temperatures = np.array(float_data['temp_adj'][::-1])

    ax.plot(temperatures, pressures, label='Temperature', color='#1f77b4')

    plt.show()

    return figure, ax


# 绘制一天的浮标数据温度剖面图
def plot_cdac_argo_data_one_day_temperature_profile(one_day_data, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制一天的浮标数据温度剖面图
    :param one_day_data: Only part of the data is used
    :param figure:  If None, a new figure will be created
    :param ax:  If None, a new axes will be created
    :return: figure, ax
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(8, 10))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111)

    ax.set_title('CDCA Argo Data One Day Profile')
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Pressure (dbar)')

    # 提取经纬度坐标
    for i, data in enumerate(one_day_data):
        pressures = -np.array(data['data']['pres'][::-1])
        adjusted_pressures = -np.array(data['data']['pres_adj'][::-1])
        temperatures = np.array(data['data']['temp'][::-1])
        adjusted_temperatures = np.array(data['data']['temp_adj'][::-1])

        ax.plot(temperatures, pressures, label='Temperature', color='#1f77b4')

    plt.show()

    return figure, ax


# 绘制一天的浮标数据盐度剖面图
def plot_cdac_argo_data_one_day_salinity_profile(one_day_data, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制一天的浮标数据盐度剖面图
    :param one_day_data: Only part of the data is used
    :param figure:  If None, a new figure will be created
    :param ax:  If None, a new axes will be created
    :return: figure, ax
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(8, 10))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111)

    ax.set_title('CDCA Argo Data One Day Profile')
    ax.set_xlabel('Salinity (PSU)')
    ax.set_ylabel('Pressure (dbar)')

    # 提取经纬度坐标
    for i, data in enumerate(one_day_data):
        pressures = -np.array(data['data']['pres'][::-1])
        salinities = np.array(data['data']['psal'][::-1])

        ax.plot(salinities, pressures, label='Salinity', color='#ff7f0e')

    plt.show()

    return figure, ax

# 绘制 CDAC 数据的混合层深度
def plot_cdac_mld_profile(mld, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制 CDAC 数据的混合层深度水平分布图
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111)

    ax.set_title('Argo Data MLD')

    mld = np.array(mld)
    mld_num = [i for i in range(len(mld))]
    ax.plot(mld_num, mld, label='MLD')
    ax.set_xlabel('Float Number')
    ax.set_ylabel('Depth (m)')

    plt.show()

    return figure, ax

def plot_cdac_mld_distribution(mld, positions, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制 CDAC 数据的混合层深度水平分布图
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(8, 10))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111, projection = ccrs.PlateCarree())

    ax.set_title('Argo Data MLD')
    ax.set_extent([LON_RANGE[0], LON_RANGE[1], LAT_RANGE[0], LAT_RANGE[1]], crs=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()
    # 设置地图刻度
    ax.set_xticks(np.arange(LON_RANGE[0], LON_RANGE[1], 10), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(LAT_RANGE[0], LAT_RANGE[1], 10), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    mld = np.array(mld)

    # 划分混合层深度
    # 0-100m
    mld_100 = []
    positions_100 = []
    # 100-300m
    mld_300 = []
    positions_300 = []
    # > 300m
    mld_300_plus = []
    positions_300_plus = []

    for i, mld_value in enumerate(mld):
        if mld_value <= 100:
            mld_100.append(mld_value)
            positions_100.append(positions[i])
        elif mld_value <= 300:
            mld_300.append(mld_value)
            positions_300.append(positions[i])
        else:
            mld_300_plus.append(mld_value)
            positions_300_plus.append(positions[i])

    # 不同深度绘制不同颜色和形状的点
    ax.scatter([pos['lon'] for pos in positions_100], [pos['lat'] for pos in positions_100], s=20, transform = ccrs.PlateCarree(), marker="*", color='#2ca02c')
    ax.scatter([pos['lon'] for pos in positions_300], [pos['lat'] for pos in positions_300], s=20, transform = ccrs.PlateCarree(), marker="o", color='#ff7f0e')
    ax.scatter([pos['lon'] for pos in positions_300_plus], [pos['lat'] for pos in positions_300_plus], s=20, transform = ccrs.PlateCarree(), marker="x", color='#1f77b4')
    plt.show()

    return figure, ax


# -------------------------- BOA Argo 绘图 --------------------------

# 绘制 Argo 在浮标位置的温度剖面图
def plot_argo_float_temperature_profile(temperatures, float_lon, float_lat, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制 Argo 在浮标位置的温度剖面图
    :param temperature: 3D array
    :param float_lon: Float position longitude
    :param float_lat: Float position latitude
    :param figure:  If None, a new figure will be created
    :param ax:  If None, a new axes will be created
    :return: figure, ax
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(8, 10))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111)

    ax.set_title('Argo Data Profile')
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Depth (m)')

    float_lon = int(float_lon)
    float_lat = int(float_lat)
    Log.d("Float Position ", float_lon, float_lat)

    temperature = temperatures[float_lon, float_lat]
    Log.d("Temperature ", temperature)
    deeps = -np.array([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 200,
         220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 500, 550, 600, 650, 700,
         750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 1975])
    Log.d("Deeps ", deeps)

    ax.plot(temperature, deeps, label='Temperature', color='#1f77b4')

    plt.show()

    return figure, ax

# 绘制 Argo 数据的混合层深度
def plot_argo_mld(mld, figure: plt.Figure = None, ax: plt.Axes = None):
    """
    绘制 Argo 数据的混合层深度水平分布图
    """
    plt.style.use('_mpl-gallery')
    if figure is None:
        figure = plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    if ax is None:
        ax = figure.add_subplot(111, projection = ccrs.PlateCarree())

    ax.set_title('Argo Data MLD')
    ax.set_extent([LON_RANGE[0], LON_RANGE[1], LAT_RANGE[0], LAT_RANGE[1]], crs=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()
    # 设置地图刻度
    ax.set_xticks(np.arange(LON_RANGE[0], LON_RANGE[1], 10), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(LAT_RANGE[0], LAT_RANGE[1], 10), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    mld = np.array(mld)

    # 划分混合层深度
    # 0-100m
    mld_100 = []
    positions_100 = []
    # 100-300m
    mld_300 = []
    positions_300 = []
    # > 300m
    mld_300_plus = []
    positions_300_plus = []

    for i in range(mld.shape[0]):
        for j in range(mld.shape[1]):
            if mld[i][j] <= 100:
                mld_100.append(mld[i][j])
                positions_100.append((i + LON_RANGE[0], j + LAT_RANGE[0]))
            elif mld[i][j] <= 300:
                mld_300.append(mld[i][j])
                positions_300.append((i + LON_RANGE[0], j + LAT_RANGE[0]))
            else:
                mld_300_plus.append(mld[i][j])
                positions_300_plus.append((i + LON_RANGE[0], j + LAT_RANGE[0]))

    # 不同深度绘制不同颜色和形状的点
    ax.scatter([pos[0] for pos in positions_100], [pos[1] for pos in positions_100], s=20, transform = ccrs.PlateCarree(), marker="*", color='#2ca02c')
    ax.scatter([pos[0] for pos in positions_300], [pos[1] for pos in positions_300], s=20, transform = ccrs.PlateCarree(), marker="o", color='#ff7f0e')
    ax.scatter([pos[0] for pos in positions_300_plus], [pos[1] for pos in positions_300_plus], s=20, transform = ccrs.PlateCarree(), marker="x", color='#1f77b4')
    plt.show()

    return figure, ax



