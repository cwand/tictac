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
Starting TICTAC 1.0.1

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
The final argument to tictac (```-o```) is the path to the output file.

The output file is structured into columns:
* The first column has the header ```tacq``` and contains the time-stamps in seconds from
  the first image.
* Each label in the ROI labelmap file has a column, and for each time-stamp the corresponding
  mean voxel intensity value is calculated.

### Resampling
If the dynamic images and the ROI are not in the same physical space (e.g. from different
examinations or different modalities), it is necessary to resample one or the other. This can
be done with the ```--resample``` argument.
To resample the ROI to the dynamic image space use:
```
> python -m tictac img_dir roi.nrrd tac.txt --resample roi
```
Conversely, to resample each of the dynamic images to the ROI space use:
```
> python -m tictac img_dir roi.nrrd tac.txt --resample img
```
Either way, the resampling is done by a simple nearest-neighbour interpolator.

### Scale correction
To apply a scale factor to one of the labels, use the ```--scale``` option. This takes
three arguments: the label of the data to correct, the label to use as the corrected
data and the factor:
```
> python -m tictac img_dir roi.nrrd tac.txt --scale blood blood2 1.5 --scale brain brain2 1000
```
In this example, one could imagine changing the unit from kBq/mL to Bq/mL on the ```brain``` label
and applying a (rather crude) partial volume correction to the ```blood``` label.