import os

from enum import Enum

import numpy as np
from torch.utils.data import Dataset, DataLoader

from src.config.params import BASE_BOA_ARGO_DATA_PATH, BASE_ERA5_DATA_PATH
from src.utils.util import resource_argo_monthly_data, import_era5_sst


class FrameType(Enum):
    surface = 0
    mld = 1


class Argo3DTemperatureDataset(Dataset):
    """
    Argo 三维温度数据集
    """

    def __init__(self, step=1, lon=(0, 0), lat=(0, 0), depth=(0, 0), dtype=FrameType.surface, *args):
        super().__init__(*args)
        self.step = step
        self.lon = lon
        self.lat = lat
        self.depth = depth
        self.dtype = dtype
        self.data = resource_argo_monthly_data(BASE_BOA_ARGO_DATA_PATH)

    def __len__(self):
        return len(self.data) / self.step

    def __getitem__(self, index):
        cur = index * self.step
        match self.dtype:
            case FrameType.surface:
                return self.data[cur:cur + self.step]['temp'][self.lon[0]:self.lon[1], self.lat[0]:self.lat[1],
                       self.depth[0]:self.depth[1]]
            case FrameType.mld:
                return self.data[cur:cur + self.step]['mld'][self.lon[0]:self.lon[1], self.lat[0]:self.lat[1],
                       self.depth[0]:self.depth[1]]


# ERA5 三维数据集
class ERA5SstDataset(Dataset):
    """
    ERA5 SST 数据集

    :arg  width: 序列长度宽度
    :arg  step: 时间平移步长
    :arg  lon: 经度范围
    :arg  lat: 纬度范围
    """

    def __init__(self, width=10, step=10, lon=None, lat=None, *args):
        super().__init__(*args)
        if lat is None:
            lat = np.array([0, 0])
        if lon is None:
            lon = np.array([0, 0])

        self.precision = 4

        self.width = width
        self.step = step
        self.lon = np.array(lon) * self.precision
        self.lat = np.array(lat) * self.precision

        first_file = None

        with os.scandir(BASE_ERA5_DATA_PATH) as files:
            for entry in files:
                if entry.is_file() and entry.name.endswith('.nc'):
                    first_file = entry.path
                    break
        if first_file is not None:
            self.file = first_file
            sst, shape, time = import_era5_sst(self.file)
            self.shape = shape
            self.time = time
        else:
            self.file = None

    def __len__(self):
        return int(self.shape[0] / self.step)

    def __getitem__(self, index):
        cur = index * self.step
        sst, shape, time = import_era5_sst(self.file, cur, cur + self.width)
        return sst[:, self.lon[0]:self.lon[1], self.lat[0]:self.lat[1]] - 273.15, time
