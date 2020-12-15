# pyOptiCAD

3D-raytracing of optical systems. The aim of this package is to assist the optical designer in CAD design of optical
systems. vispy library is used for 3D visualization.

## Description

* This is a Python-based package developed to assist the optical designer in CAD design of optical systems. It is built around [vispy](https://vispy.org/) library. Polarisation analysis can be performed with the Poincare sphere method. This methodology is adopted as it is capable of visual representation of the modification of polarization as the radiation passes through the various components of the system.
* Screenshots of the performance of the package are located in the `gallery` and examples for quick evaluation of the package are available in `examples` in the repository.
* The capabilities of this package can be understood from the screenshots in the `gallery`. However, as this package is currently under active development, there are errors in the present version. The immediate target is to arrive at an error-free version where this package can be used for simple raytracing and polarization analysis in optical systems development by writing scripts in Python. In future, sophisticated analysis tools can be developed. A route map for the creating GUI through _marshalling_ so that this package will be useful for designers with no knowledge of Python. Implementation of GUI will follow after the release of version 1.0.
* Contributions are welcome in various ways such as, not limited to, making the package error-free, enhancing the functionality, development of GUI and so on.
* Current Version is 0.1

## How do I get set up?

This package has the following major dependencies:
* `vispy`
* `pyquaternion`
* `matplotlib`
* `numpy`
* `scipy`

The version information for these packages is provided in the file `requirements.txt`.

### via pip

```sudo pip install vispy, pyquaternion```

In addition, `matplotlib`,`numpy`, and `scipy` are required

### via [Anaconda](https://www.continuum.io/what-is-anaconda) distribution
If you had installed Anaconda, you can install the above dependencies using the `conda` command.
```
conda install vispy, pyquaternion
```

## Contribution guidelines

This software is provided **AS IS**. Currently, there is no documentation available. We have not stuck to PEP8 guidelines.
You are free to contribute in whichever way you feel like such as, adding a feature, documentation, making the code compatible to PEP8 guidelines or anything else you can think of that will make the software useful to the community.

## Disclaimer

This software has been uploaded **AS IS**. Though it was used on Linux and Windows, there is no guarantee that this software is bug-free. Use with caution.

## License
![Alt text](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

