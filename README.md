# tictac
Python code for extracting time-activity curves from dynamic SPECT or PET images

## Getting tictac
Clone the repository to your computer using git:
```
> git clone https://github.com/cwand/tictac
```

Enter the directory.
Make sure you are on the main branch:
```
> git checkout main
```

Create a new virtual python environment:
```
> python -m venv my_venv
```

Activate the virtual environment. Commands vary according to OS and shell (see [the venv documentation](https://docs.python.org/3/library/venv.html)), but in a Windows PowerShell:
```
> my_venv\Scripts\Activate.ps1
```

Install tictac and required dependencies
```
> pip install .
```

If everything has gone right, you should be able to run tictac
```
> python -m tictac
Starting TICTAC 2.0.1

...
__main__.py: error: the following arguments are required: -i, -o
```

## Using tictac

First and foremost: a help message is displayed when running tictac with the ```-h``` flag:
```
> python -m tictac -h
```


To use tictac you need
* A dynamic dicom image series in a directory, say ```img_dir```.
* Each ROI in a selection of files. The ROIs can be in one file or separate 
  files, and many formats are available, so long as thay can be read as an
  image by SimpleITK. For this example we say have one ROI in the file 
  ```roi1.nrrd``` with voxel value 1.

To get the mean voxel values in each ROI for each time frame, we run tictac:
```
> python -m tictac -i img_dir --roi roi1.nrrd 1 roi_name mean none -o tac.txt
```
The first argument ```-i img_dir``` specifies the path to the dynamic image
data. The second argument ```--roi roi1.nrrd 1 roi_name mean none``` specifies
the ROI, which is extracted with the following options:
* ```roi1.nrrd``` specifies the path to the ROI image file
* ```1``` specifies that the ROI voxel value is ```1```
* ```roi_name``` is the name the ROI will have in the output file
* ```mean``` specifies that we want the mean voxel value inside the ROI
* ```none``` specifies that no resampling should be done to the ROI image.

In case more than one ROI is wanted, each one gets its own ```--roi ...```.

The final argument to tictac (```-o```) is the path to the output file.

The output file is structured into columns:
* The first column has the header ```tacq``` and contains the time-stamps in seconds from
  the first image.
* Each ROI has a column, and for each time-stamp the corresponding
  mean voxel intensity value is calculated.

### ROI compuations

The ROI computation strategy is set by the fourth value in the ```--roi``` argument.
At this point, two different ROI comutations are implemented in tictac:
* ```mean```: Calculates the mean voxel value inside the ROI.
* ```zmeanmax```: Finds the maximum voxel intensity in each z-axis slice of the image,
  bounded by the ROI, and computes the mean of these maximum values.

### Resampling
If the dynamic images and the ROI are not in the same physical space (e.g. from different
examinations or different modalities), it is necessary to resample one or the other.
In the ```--roi``` argument the resampling strategy is set as the fifth value, and it can
be either
* ```none``` (no resampling, so images and ROI must be in the same physical space)
* ```roi``` (the ROI is resampled to the dynamic image space using nearest neighbour interpolation)
* ```img``` (the dynamic images are resampled to the ROI image space using nearest neighbour interpolation)

### Scale correction
To apply a scale factor to one of the labels, use the ```--scale``` option. This takes
three arguments: the label of the data to correct, the label to use as the corrected
data and the factor:
```
> python -m tictac -i img_dir --roi roi_blood.nrrd 1 blood mean none --roi roi_brain.nrrd 1 brain mean none -o tac.txt --scale blood blood2 1.5 --scale brain brain2 1000
```
In this example, one could imagine changing the unit from kBq/mL to Bq/mL on the ```brain``` label
and applying a (rather crude) partial volume correction to the ```blood``` label.

### Partial Volume Correction

The following partial volume correction routines are accessible in tictac:

#### VDIL

VDIL (Volume DILation) is the simple approach to PVC. We define three ROIs:
* The main ROI with a signal $x_{\mathrm{m}}$, which suffers from PVE.
* A dilated ROI surrounding the main ROI with signal $x_{\mathrm{d}}$, which
  captures the signal missing from the main ROI.
* A background ROI, which has the same signal, $x_{\mathrm{b}}$, that the 
  dilated ROI would have had if there had been no spill-in from the main ROI.
  This assures that the signal that belongs to the dilated volume is not being 
  used to correct the main volume.

Then a signal corrected for partial volume effects, $x_{\mathrm{pvc}}$, 
is calculated as:\
$$x_{\mathrm{pvc}} = x_{\mathrm{m}} + (x_{\mathrm{d}} - x_{\mathrm{b}})
\frac{V_\mathrm{d}}{V_\mathrm{m}},$$\
where $V_\mathrm{d}$ and $V_\mathrm{m}$ are the volumes of the main and dilated
ROIs respectively.

To use this routine in tictac, we use the ```--pvc_vdil``` option:
```
> python -m tictac -i img_dir --roi roi.nrrd 1 main mean none --roi roi.nrrd 2 dil mean none --roi roi.nrrd 3 bkg mean none -o tac.txt  --pvc_vdil main dil bkg main_pvc
```
The arguments to this option are (in order):
* The label of the main ROI
* The label of the dilated ROI
* The label of the background ROI
* The label to use for the corrected TAC

The volumes of the main and dilated ROIs will be calculated automatically.

#### BARD

BARD (Background-Aorta Ratio and Diameter) PVC is a routine for correcting
the signal in an Aorta ROI for Partial Volume Effects.
The assumption behind BARD is that the ratio of the aorta signal to the
background signal will be closer to unity than the true ratio, since the
partial volume effect will cause some of the aorta signal to spill out into
the background. This effect will be more severe the smaller the aorta.
If we measure a phantom with known activities which simulates an aorta in a 
background and compute the measured ratio, we can interpolate between measured
points to do the process in reverse: taking a measured ratio and find out what
the true ratio must have been given the diameter of the aorta.

To use this routine in tictac, we use the ```--pvc_bard``` option:
```
> python -m tictac -i img_dir --roi roi_aorta.nrrd 1 aorta mean none --roi roi_bkg.nrrd 1 bkg mean none -o tac.txt --pvc_bard aorta bkg 21 bard_table.txt aorta_bard
```
The arguments to this option are (in order):
* The label of the aorta ROI
* The label of the background ROI
* The diameter of the aorta
* A path to the file containing measured ratios
* The label to use for the corrected TAC

The file with measured ratios must be formatted with comma-separated values,
like this (```#``` indicates comments):
```
       10.0, 20.0, 30.0, 40.0   # First line is known diameters
0.0,    0.0,  0.0,  0.0,  0.0
1.0,    1.0,  1.0,  1.0,  1.0
2.0,    1.5,  1.7,  1.8,  1.9   # First value in following lines is known aorta:background ratio
5.0,    3.0,  4.0,  4.3,  4.5   # Following values are measured ratio for each diameter
10.0,   5.0,  6.5,  7.0,  7.5
100.0, 40.0, 80.0, 82.0, 85.0
```
In the example above, we have inserted two lines with a known ratio of 0 and 1
in the beginning and specified no correction. This can be necessary, since
there will be no extrapolation. If a ratio to correct falls outside the range
of measured ratios, an error will occur and the program will stop.

### Progress bar
As default tictac shows a progress bar. This behavoiur can be turned off (e.g. if
piping stdout to a file) by setting the argument ```--hideprogress```