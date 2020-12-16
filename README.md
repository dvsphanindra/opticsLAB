# pyOptiCAD

3D-raytracing of optical systems. The aim of this package is to assist the optical designer in CAD design of optical
systems. vispy library is used for 3D visualization.

## Description

* Built around [vispy](https://vispy.org/) library, this is a Python-based package developed to assist the optical designer in CAD design of optical systems.
* Polarisation analysis can be performed with the Poincare sphere method. Poincare formalism is adopted as it is capable of visual representation of polarization vector as the radiation passes through the various components of the system.
* A quick overview of the capabilities of the package can be obtained from the screenshots located in the `gallery` and examples for quick evaluation of the package are available in `examples` in the repository.
* The capabilities of this package can be understood from the screenshots in the `gallery`. However, as this package is currently under active development, there can be errors in the code. Therefore, the package may not work as expected. The immediate target is to arrive at an error-free version where this package can be used for simple raytracing and polarization analysis by writing scripts in Python. In future, sophisticated analysis tools can be developed.
* A route map has been identified for developing GUI for the package based on the concept of _marshalling_. Having a GUI will help the designers with no knowledge of Python in building optical systems. Implementation of GUI will follow after the release of the error-free version.
* Contributions are welcome in various ways such as, and not limited to, making the package error-free, enhancing the functionality, development of GUI and so on.
* Current Version is 0.1

## How do I get set up?

This package has the following major dependencies: `vispy, pyquaternion, matplotlib, numpy, scipy`

The version information about these packages is provided in the file `requirements.txt`.

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

