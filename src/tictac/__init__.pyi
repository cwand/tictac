import SimpleITK as sitk
from datetime import datetime
import numpy.typing as npt
import numpy as np
from typing import Any
from pandas import DataFrame


# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...

def get_frame_duration(dicom_path:str) -> float: ...

def save_table(table: dict[str, npt.NDArray[np.float64]], path: str): ...


# From image.py

def load_dynamic_series(dicom_path: str) \
        -> dict[str, Any]: ...

def roi_volumes(roi_list: list[list[str]]) -> dict[str, float]: ...

def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]: ...

def series_roi_calcs(series_path: str,
                     roi_list: list[list[str]],
                     progress: bool = ...)\
        -> dict[str, npt.NDArray[np.float64]]: ...


# From pvc.py

def vdil_pvc(dyn: dict[str, npt.NDArray[np.float64]],
             vols: dict[str, float],
             label_main: str,
             label_dil: str,
             label_bkg: str) -> npt.NDArray[np.float64]: ...

def bard_pvc(aorta: npt.NDArray[np.float64],
             bkg: npt.NDArray[np.float64],
             diameter: float,
             table: DataFrame) -> npt.NDArray[np.float64]: ...
