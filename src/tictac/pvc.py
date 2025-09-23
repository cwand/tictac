from pandas import DataFrame
import numpy as np
import numpy.typing as npt
from scipy.interpolate import RegularGridInterpolator

def bard_pvc(aorta: npt.NDArray[np.float64],
             bkg: npt.NDArray[np.float64],
             diameter: float,
             table: DataFrame) -> npt.NDArray[np.float64]:

    ds = np.array(table.columns.astype(float).tolist())
    rs = np.array(table.index.astype(float).tolist())
    cs = table.to_numpy()
    interp = RegularGridInterpolator((rs, ds), cs, method='linear')
    pts = np.array([[r, diameter] for r in rs])

    tab_meas_ratios = interp(pts)
    tab_true_ratios = np.array(table.index.astype(float).tolist())

    ratios = aorta / bkg
    true_ratios = np.interp(ratios, tab_meas_ratios, tab_true_ratios)

    return true_ratios * bkg
