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
                     roi_list: list[list[str]])\
        -> dict[str, npt.NDArray[np.float64]]:
    """Do a lazy calculation of mean image values in a ROI. Lazy in this
    context means that the images are loaded one at a time and the mean values
    computed, before the image is removed from memory and the next image is
    loaded. This saves some memory usage compared to loading all images in a
    list and then computing ROI-means, but on the other hand no manipulation
    of the images can be performed after the call of this function.
    The ROIs are given in a list. Each ROI in the list is another list of four
    string values:
     - roi[0] is the path to the ROI image file
     - roi[1] is the voxel value (label) of the ROI in the image file
     - roi[2] is the name the ROI-data should have in the output file
     - roi[3] defines the resampling strategy in case the ROI and dynamic
       images are not in the same physical space. This can be either "none"
       (no resampling, the images must be in identical physical space), "img"
       (the dynamic images should be resampled to the ROI image space), "roi"
       (the ROI image should be resampled to the dynamic image physical space).
    In either case the resampling is done using nearest-neighbour values.
    The function returns a dictionary object. The keys in the object are
    'tacq' which stores a list of acquisition times (relative to the first
    image) and the labels of the ROI (integers) (see the keyword argument
    'labels' for options). Other keys are also available, see argument list
    below.

    Arguments:
    series_path --  The path to the images series dicom files
    roi_list    --  The lists of ROIs to compute

    Return value:
    A dict object with ROI labels as keys and a list with ROI mean values for
    every time point in the dynamic series as values. Furthermore, the
    acquisition times are stored in a list under the key 'tacq'.
    """

    res: dict[str, npt.NDArray[np.float64]] = defaultdict(
        lambda: np.ndarray(0))

    # Prepare series reader
    reader = sitk.ImageSeriesReader()

    # Get dicom file names in folder sorted according to acquisition time.
    dcm_names = reader.GetGDCMSeriesFileNames(series_path)

    # Read in all rois
    rois = []
    for roi in roi_list:
        roi_image = sitk.ReadImage(roi[0])

        # Resample ROI if chosen
        if roi[3] == 'roi':
            resampler = sitk.ResampleImageFilter()
            resampler.SetReferenceImage(sitk.ReadImage(dcm_names[0]))
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            roi_image = resampler.Execute(roi_image)

        rois.append(roi_image)

    # Prepare label statistics filter
    label_stats_filter = sitk.LabelStatisticsImageFilter()

    # Get acquisition time of first image
    acq0 = tictac.core.get_acq_datetime(dcm_names[0])

    for name in dcm_names:
        # Load images in order
        img = sitk.ReadImage(name)

        # Placeholder for resampled img if needed
        resampled_img: Optional[sitk.Image] = None

        # Find acquisition time and store in list
        res['tacq'] = np.append(
            res['tacq'],
            (tictac.core.get_acq_datetime(name) - acq0).total_seconds())

        for i, roi in enumerate(roi_list):

            # Resample image if chosen
            if roi[3] == 'img':
                if (resampled_img is None or
                        not rois[i].IsSameImageGeometryAs(resampled_img)):
                    # Image needs to be resampled
                    resampler = sitk.ResampleImageFilter()
                    resampler.SetReferenceImage(rois[i])
                    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
                    resampled_img = resampler.Execute(img)

                # Apply label stats filter on resampled img and read ROI means
                label_stats_filter.Execute(resampled_img, rois[i])

            else:

                # Apply label stats filter on original img and read ROI means
                label_stats_filter.Execute(img, rois[i])

            # Append the mean value to the list for each label.
            res[roi[2]] = np.append(res[roi[2]],
                                    label_stats_filter.GetMean(int(roi[1])))

    return res
