import SimpleITK as sitk
from datetime import datetime
import numpy.typing as npt
import numpy as np
from typing import Any, Optional


# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...

def save_table(table: dict[str, npt.NDArray[np.float64]], path: str): ...


# From image.py

def load_dynamic_series(dicom_path: str) \
        -> dict[str, Any]: ...

def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]: ...

def series_roi_means(series_path: str,
                     roi_list: list[list[str]],
                     progress: bool = ...)\
        -> dict[str, npt.NDArray[np.float64]]: ...