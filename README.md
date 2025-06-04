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
> python -m tictac -i img_dir --roi roi1.nrrd 1 roi_name none -o tac.txt
```
The first argument ```-i img_dir``` specifies the path to the dynamic image
data. The second argument ```--roi roi1.nrrd 1 roi_name none``` specifies
the ROI, which is extracted with the following options:
* ```roi1.nrrd``` specifies the path to the ROI image file
* ```1``` specifies that the ROI voxel value is ```1```
* ```roi_name``` is the name the ROI will have in the output file
* ```none``` specifies that no resampling should be done to the ROI image.

In case more than one ROI is wanted, each one gets its own ```--roi ...```.

The final argument to tictac (```-o```) is the path to the output file.

The output file is structured into columns:
* The first column has the header ```tacq``` and contains the time-stamps in seconds from
  the first image.
* Each ROI has a column, and for each time-stamp the corresponding
  mean voxel intensity value is calculated.

### Resampling
If the dynamic images and the ROI are not in the same physical space (e.g. from different
examinations or different modalities), it is necessary to resample one or the other.
In the ```--roi``` argument the resampling strategy is set as the fourth value, and it can
be either
* ```none``` (no resampling, so images and ROI must be in the same physical space)
* ```roi``` (the ROI is resampled to the dynamic image space using nearest neighbour interpolation)
* ```img``` (the dynamic images are resampled to the ROI image space using nearest neighbour interpolation)

### Scale correction
To apply a scale factor to one of the labels, use the ```--scale``` option. This takes
three arguments: the label of the data to correct, the label to use as the corrected
data and the factor:
```
> python -m tictac -i img_dir --roi roi_blood.nrrd 1 blood none --roi roi_brain.nrrd 1 brain none -o tac.txt --scale blood blood2 1.5 --scale brain brain2 1000
```
In this example, one could imagine changing the unit from kBq/mL to Bq/mL on the ```brain``` label
and applying a (rather crude) partial volume correction to the ```blood``` label.

### Progress bar
As default tictac shows a progress bar. This behavoiur can be turned off (e.g. if
piping stdout to a file) by setting the argument ```--hideprogress```