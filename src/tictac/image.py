import SimpleITK as sitk
from collections import defaultdict

import numpy as np

import tictac.core
import numpy.typing as npt
from typing import Any, Optional


def load_dynamic_series(dicom_path: str) -> dict[str, Any]:
    """Loads a dynamic image series. The images and their relative acquisition
    times are stored in a dictionary object. The keys 'img' and 'acq' are
    available:
    Under the key 'img' the images are stored in a list in order of acquisition
    time. Each image is stored as a SimpleITK Image.
    Under the key 'acq' the relative acquisition times are stored in seconds.
    This means: result['img'][i] is acquired result['acq'][i] seconds after
    result['img'][0].

    Arguments:
    dicom_path  --  The path to the dicom files

    Return value:
    A dict-object with keys 'img' (SimpleITK Images in a list) and 'acq'
    (acquisition times in seconds in a list).
    """

    # Prepare reader
    reader = sitk.ImageSeriesReader()

    # Get dicom file names in folder sorted according to acquisition time.
    dcm_names = reader.GetGDCMSeriesFileNames(dicom_path)

    img_arr = []
    acq_arr = []

    # Get acquisition time of first image
    acq0 = tictac.core.get_acq_datetime(dcm_names[0])

    for name in dcm_names:
        # Load image and read acquisition time of each image and store in list
        img = sitk.ReadImage(name)
        img_arr.append(img)
        acq_arr.append(
            (tictac.core.get_acq_datetime(name)-acq0).total_seconds())

    return {'img': img_arr,
            'acq': acq_arr}


def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]:
    """Resample each image in an image series to the same physical space as
    a reference image. The pixel values in the resampled images will be
    interpolated according to the nearest-neighbour principle.

    Arguments:
    series  --  The image series.
    ref     --  The reference image.

    Return value:
    A list containing each resampled image in the same order.
    """

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(ref)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    return [resampler.Execute(img) for img in series]


def series_roi_means(series_path: str,
                     roi_path: list[list[str]])\
        -> dict[str, npt.NDArray[np.float64]]:
    """Do a lazy calculation of mean image values in a ROI. Lazy in this
    context means that the images are loaded one at a time and the mean values
    computed, before the image is removed from memory and the next image is
    loaded. This saves some memory usage compared to loading all images in a
    list and then computing ROI-means, but on the other hand no manipulation
    of the images can be performed after the call of this function.
    The images or the ROI can be resampled before calculation of the mean by
    using the resample argument. To resample the ROI to the size of the images
    set resample='roi', and to resample the images to the ROI space use
    resample='img'. In either case the resampling is done using
    nearest-neighbour values.
    The function returns a dictionary object. The keys in the object are
    'tacq' which stores a list of acquisition times (relative to the first
    image) and the labels of the ROI (integers) (see the keyword argument
    'labels' for options). Other keys are also available, see argument list
    below.

    Arguments:
    series_path --  The path to the images series dicom files
    roi_path    --  The path to the ROI dicom files
    resample    --  The resampling strategy. Allowed values are None (no
                    resampling, default value), 'roi' (resample ROI to image
                    space) or 'img' (resample images to ROI space).
    labels      --  Choose different labels for the resulting dict object. By
                    default, the label values in the ROI image is chosen. A
                    dictionary can be inserted here to replace those values. If
                    for example the ROI label value '1' should be replaced with
                    'left' and the value '2' should be replaced with 'right'
                    use the argument labels={'1': 'left', '2': 'right'}.
    ignore      --  List of labels to ignore when computing means. Default is
                    None, in which case all labels will be computed.

    Return value:
    A dict object with ROI labels as keys and a list with ROI mean values for
    every time point in the dynamic series as values. Furthermore, the
    acquisition times are stored in a list under the key 'tacq'.
    """

    # Input sanitation: if no label substitution is needed, the argument is
    # just an empty dict
    if labels is None:
        labels = {}

    # Input sanitation: if no ignoring is needed, the argument is
    # just an empty list
    if ignore is None:
        ignore = []

    res: dict[str, npt.NDArray[np.float64]] = defaultdict(
        lambda: np.ndarray(0))

    # Prepare series reader
    reader = sitk.ImageSeriesReader()

    # Get dicom file names in folder sorted according to acquisition time.
    dcm_names = reader.GetGDCMSeriesFileNames(series_path)

    # Read ROI image
    roi = sitk.ReadImage(roi_path)

    # Resample ROI if chosen
    if resample == 'roi':
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(sitk.ReadImage(dcm_names[0]))
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        roi = resampler.Execute(roi)

    # Prepare label statistics filter
    label_stats_filter = sitk.LabelStatisticsImageFilter()

    # Get acquisition time of first image
    acq0 = tictac.core.get_acq_datetime(dcm_names[0])

    for name in dcm_names:
        # Load images in order
        img = sitk.ReadImage(name)

        # Resample image if chosen
        if resample == 'img':
            resampler = sitk.ResampleImageFilter()
            resampler.SetReferenceImage(roi)
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            img = resampler.Execute(img)

        # Find acquisition time and store in list
        res['tacq'] = np.append(
            res['tacq'],
            (tictac.core.get_acq_datetime(name) - acq0).total_seconds())

        # Apply label stats filter and read ROI means
        label_stats_filter.Execute(img, roi)
        for label in label_stats_filter.GetLabels():
            if str(label) in ignore:
                continue
            # Append the mean value to the list for each label.
            res_key = labels.get(str(label), str(label))
            res[res_key] = np.append(res[res_key],
                                     label_stats_filter.GetMean(label))

    return res
