# plot_watcher
A simple script that can watch a list of directories and does some action when a specific kind of change happens

In its current implementation, this script polls the directories listed as an argument (see plot_watcher.bat) for any changes. Once it finds a new .plot file created or added, it will look in the directory "../Plots" relative to the one where the change happened (so it goes back one level then enters "Plots" dir, where old plots supposedly reside, you can change this to suit your need) and if it finds any .plot files it will delete one.
This will let you keep your plotter working (against your new NFT contract address) and one by one your old plots will be replaced with the newer portable ones.

Example directory structure based on the default arguments in plot_watcher.bat:

E:

|---Plots

|---Portable_Plots


F:

|---Plots

|---Portable_Plots


G:

|---Plots

|---Portable_Plots


The script will look inside the "Portable_Plots" directories and once a new .plot file is added the script will delete one .plot file from the old ones in "Plots".

DICLAIMER: This script is given AS-IS and was made for my own case, if you need an update to suit your setup you can fork it and add to it yourself. I'm not liable to any damage done from losing your 5489743159 plots, if you need to do any tests for yourself you can comment out or remove the line "os.remove(...." until your changes are tested and you're satisfied with the result.

## Installation:

We make use of the module pywin32 so it needs to be installed by running the command: **python -m pip install pywin32**

After checking the list of portable plot directories in the .bat file, you need to make sure that either the old Plots follow the same directory structure as described above or you can edit the script to point to the right directory. This following line can be edited to point to the relative path starting from the location of the newly created plot:

```python
oldPlotDir = os.path.abspath(os.path.join(os.path.dirname(filename), "..", "Plots"))
```

## Usage:

Run the bat file and leave it open to track the new plots.

![plot_watcher screenshot](plot_watcher.png?raw=true "plot_watcher screenshot")
