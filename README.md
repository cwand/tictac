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
__main__.py: error: the following arguments are required: img_dir, roi_path, out_path
```

## Using tictac

First and foremost: a help message is displayed when running tictac with the ```-h``` flag:
```
> python -m tictac -h
```


To use tictac you need
* A dynamic dicom image series in a directory, say ```img_dir```.
* An ROI-file containing the label-map ROI image. Formats can vary, but for this example we say the ROI has been saved
  in the file ```roi.nrrd```.

To get the mean voxel values in each ROI for each time frame, we run tictac:
```
> python -m tictac img_dir roi.nrrd tac.txt
```
The final argument to tictac is the path to the output file.

The output file is structured into columns:
* The first column has the header ```tacq``` and contains the time-stamps in seconds from
  the first image.
* Each label in the ROI labelmap file has a column, and for each time-stamp the corresponding
  mean voxel intensity value is calculated.

### Custom labels
Perhaps the labels in the ROI image file are not very descriptive, if for example they are
simply numbered from 0, 1, ... In that case it might be desired to substitute the labels with
more descriptive values. To do this, use the ```--labels``` argument:
```
> python -m tictac img_dir roi.nrrd tac.txt --labels 0,bkg 1,brain
```
The example above uses the label ```bkg``` instead of ```0``` and ```brain``` instead of ```1```.
Any remaining labels in the ROI file will be kept as they are.

### Ignore certain labels
If there are labels in the ROI file that should be ignored, use the ```--ignore``` argument:
```
> python -m tictac img_dir roi.nrrd tac.txt --labels 1,brain --ignore 0
```
This example replaces the label ```1``` with ```brain```, and will ignore the label ```0```, which will not be
output to the resulting file.

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