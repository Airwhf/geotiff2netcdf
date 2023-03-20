#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2023/3/20 14:25
# @Author    :Haofan Wang
# @Email     :wanghf58@mail2.sysu.edu.cn
import glob
import os.path
import rioxarray
import xarray as xr

if __name__ == "__main__":
    print("This script is written by Haofan Wang.")
    dir = "/mnt/d/Wukai/20230320"  # 输入目录

    files = glob.glob(f"{dir}/*.tif")
    for fgeotiff in files:
        ds_geotiff = rioxarray.open_rasterio(fgeotiff)
        sub_name = os.path.basename(fgeotiff)
        lon = ds_geotiff.coords["x"].__array__()
        lat = ds_geotiff.coords["y"].__array__()
        data = ds_geotiff.__array__()[0,...]
        # 创建 xarray.DataArray
        data_array = xr.DataArray(
            data,
            coords=[('lat', lat, {'units': 'degrees_north'}),
                    ('lon', lon, {'units': 'degrees_east'})],
            attrs={'description': 'Example data'}
        )
        # 将 DataArray 转换为 xarray.Dataset
        dataset = xr.Dataset({'values': data_array})

        fnetcdf = f"{dir}/{sub_name}.nc"
        dataset.to_netcdf(fnetcdf)
        print(f"Finish: {fnetcdf}.")

