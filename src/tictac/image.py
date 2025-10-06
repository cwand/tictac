import SimpleITK as sitk
from collections import defaultdict

import numpy as np
from tqdm import tqdm

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


def roi_volumes(roi_list: list[list[str]]) -> dict[str, float]:
    """Calculates the volumes of the ROIs in the list.
    The format of the input ROI-list is the same as in 'series_roi_calcs'.
    The output is a dict object with keys equal to the roi label (the
    third value in each roi tuple) and with values equal to the ROI volume in
    cm^3 (mL)

    Arguments:
        roi_list    --  The list of rois

    Return value:
    A dict object with the volume for each ROI indexed by the ROI label.
    """
    res = {}
    for roi in roi_list:
        # Read ROI image and threshold by the roi image value
        roi_image = sitk.ReadImage(roi[0])
        bin_image = sitk.BinaryThreshold(roi_image,
                                         lowerThreshold=int(roi[1]),
                                         upperThreshold=int(roi[1]),
                                         insideValue=1,
                                         outsideValue=0)

        # Count the number of voxels inside the threshold
        label_stats = sitk.LabelStatisticsImageFilter()
        label_stats.Execute(bin_image, roi_image)
        nvox = label_stats.GetCount(int(roi[1]))

        # Calculate volume as voxel size time voxel count and convert to cm3.
        spacings = roi_image.GetSpacing()
        volcm3 = nvox * spacings[0] * spacings[1] * spacings[2] / 1000.0
        res[roi[2]] = volcm3

    return res


def series_roi_calcs(series_path: str,
                     roi_list: list[list[str]],
                     progress: bool = True)\
        -> dict[str, npt.NDArray[np.float64]]:
    """Do a lazy calculation of mean image values in a ROI. Lazy in this
    context means that the images are loaded one at a time and the mean values
    computed, before the image is removed from memory and the next image is
    loaded. This saves some memory usage compared to loading all images in a
    list and then computing ROI-means, but on the other hand no manipulation
    of the images can be performed after the call of this function.
    The ROIs are given in a list. Each ROI in the list is another list of five
    string values:
     - roi[0] is the path to the ROI image file
     - roi[1] is the voxel value (label) of the ROI in the image file
     - roi[2] is the name the ROI-data should have in the output file
     - roi[3] is the computation type (mean or zmeanmax)
     - roi[4] defines the resampling strategy in case the ROI and dynamic
       images are not in the same physical space. This can be either "none"
       (no resampling, the images must be in identical physical space), "img"
       (the dynamic images should be resampled to the ROI image space), "roi"
       (the ROI image should be resampled to the dynamic image physical space).
       In either case the resampling is done using nearest-neighbour values.
    The function returns a dictionary object. The keys in the object are
    'tacq' which stores a list of acquisition times (relative to the first
    image) and the labels of the ROI.

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
        if roi[4] == 'roi':
            resampler = sitk.ResampleImageFilter()
            resampler.SetReferenceImage(sitk.ReadImage(dcm_names[0]))
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            roi_image = resampler.Execute(roi_image)

        rois.append(roi_image)

    # Prepare label statistics filter
    label_stats_filter = sitk.LabelStatisticsImageFilter()

    # Get acquisition time of first image
    acq0 = tictac.core.get_acq_datetime(dcm_names[0])

    for name in tqdm(dcm_names, disable=(not progress)):
        # Load images in order
        img = sitk.ReadImage(name)

        # Find acquisition time and store in list
        res['tacq'] = np.append(
            res['tacq'],
            (tictac.core.get_acq_datetime(name) - acq0).total_seconds())

        for i, roi in enumerate(roi_list):

            img_dup = img

            # Resample image if chosen
            if roi[4] == 'img':
                # Image needs to be resampled
                resampler = sitk.ResampleImageFilter()
                resampler.SetReferenceImage(rois[i])
                resampler.SetInterpolator(sitk.sitkNearestNeighbor)
                img_dup = resampler.Execute(img)

            if roi[3] == 'mean':
                # Apply label stats filter on resampled img and read ROI means
                label_stats_filter.Execute(img_dup, rois[i])

                # Append the mean value to the list for each label.
                res[roi[2]] = np.append(res[roi[2]],
                                        label_stats_filter.GetMean(int(roi[1])))

            if roi[3] == 'zmeanmax':

                # Iterate through all slices in the image
                n_slices = list(img_dup.GetSize())[2]
                slice_max = []

                for z in range(n_slices):
                    # Get current slice of image and roi
                    img_slice = img_dup[:, :, z]
                    lbl_slice = rois[i][:, :, z]

                    # Create mask
                    label_stats_filter.Execute(img_slice, lbl_slice)
                    if label_stats_filter.HasLabel(int(roi[1])):
                        # Append the maximum value in the ROI to the list
                        slice_max.append(label_stats_filter.GetMaximum(int(roi[1])))

                # The result is the mean of the maximum values
                res[roi[2]] = np.append(res[roi[2]], np.mean(slice_max))


    return res
