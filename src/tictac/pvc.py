from pandas import DataFrame
import numpy as np
from scipy.interpolate import RegularGridInterpolator

def bard_pvc(aorta: float,
             bkg: float,
             diameter: float,
             table: DataFrame) -> float:

    # Convert to numpy arrays:
    ds = np.array(table.columns.astype(float).tolist())
    print(ds)
    rs = np.array(table.index.astype(float).tolist())
    print(rs)

    cs = table.to_numpy()
    print(cs)

    interp = RegularGridInterpolator((ds, rs), cs, method='linear')
    pt = np.array([diameter, aorta/bkg])
    c = interp(pt)

    return aorta / c[0]