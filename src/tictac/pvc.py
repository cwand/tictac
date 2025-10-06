from pandas import DataFrame
import numpy as np
import numpy.typing as npt
from scipy.interpolate import RegularGridInterpolator

def vdil_pvc(dyn: dict[str, npt.NDArray[np.float64]],
             vols: dict[str, float],
             label_main: str,
             label_dil: str,
             label_bkg: str) -> npt.NDArray[np.float64]:
    """
    Performs Partial Volume Correction on an ROI by volume dilation.
    This is done by using three ROI's:
      - The main ROI, which is the ROI of interest.
      - A dilated ROI, which is an ROI containing the spill-out signal
        from the main ROI as well as some background signal.
      - A background ROI, which contains only the backgrounf signal.
    From these the corrected signal is computed by subtracting the background
    signal from the dilated signal, and then adding the remaining signal
    into the main ROI, scaled by the volume:
        pvc_corr_signal = main_signal + (dil_signal - bkg_signal) * Vdil/Vmain
   The volumes should be given in the volume dict-object.
    """

    main_arr = dyn[label_main]
    main_vol = vols[label_main]
    dil_arr = dyn[label_dil]
    dil_vol = vols[label_dil]
    bkg_arr = dyn[label_bkg]

    return main_arr + (dil_arr - bkg_arr) * dil_vol / main_vol

def bard_pvc(aorta: npt.NDArray[np.float64],
             bkg: npt.NDArray[np.float64],
             diameter: float,
             table: DataFrame) -> npt.NDArray[np.float64]:
    """
    PVC routine designed to correct for partial volume effect of the
    aorta concentration. The correction takes into account the aorta
    diameter and the ratio of concentrations in the surrounding tissue
    (background) and the aorta.
    The correction uses a table of predetermined ratios between aorta and
    background given some known conditions. The columns in the table
    corresponds to a given aorta diameter. The rows of the table corresponds
    to a known aorta-to-background ratio, and the values in this row for each
    column is then the measured ratio for each diameter aorta.
    The routine returns the corrected aorta concentration curve.

    Arguments:
    aorta       --  The aorta concentrations to correct
    bkg         --  The background concentration
    diameter    --  Diameter of the aorta
    table       --  Table of predetermined ratios for interpolation

    Return value:
    The corrected aorta concentrations
    """

    # First convert the table to numpy arrays
    tab_diameters = np.array(table.columns.astype(float).tolist())
    tab_true_ratios = np.array(table.index.astype(float).tolist())
    tab_meas_ratios = table.to_numpy()

    # We create a 'new column', corresponding to the diameter of interest
    interp = RegularGridInterpolator((tab_true_ratios, tab_diameters),
                                     tab_meas_ratios, method='linear')
    pts = np.array([[r, diameter] for r in tab_true_ratios])
    tab_interp_ratios = interp(pts)

    # Compute measured ratios
    ratios = aorta / bkg

    # Interpolate the 'new column' to find true ratios
    true_ratios = np.interp(ratios, tab_interp_ratios, tab_true_ratios)

    # Return corrected aorta curve
    return np.array(true_ratios * bkg)


