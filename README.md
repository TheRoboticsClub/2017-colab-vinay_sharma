### Update
Also Contains code for parsing json files, primarily to add dataset support for more datasets in DetectionSuite.
Uses standard C++ library boost/property_tree for the same.
Link to [Documnetation](https://www.boost.org/doc/libs/1_67_0/doc/html/property_tree/accessing.html)
### Human Detector

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
