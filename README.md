# Human Detector

This tool has been updated to detect people using c++ which calls tensorflow nad then detects people.
To run this tool, go to the root directory of this repository and run:
```
cmake .
make
```
After this you will have a ```detector``` executable. Run it to see the results.
```
./detector persondetector.yml
```

You will then see a GUI which will show you live detections.
Also, don't forget to uncompress the model file in Net folder.

The Detector has also been updated to use a self trained model using Imagenet dataset from ILSVRC2014 challenge.
