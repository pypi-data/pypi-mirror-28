SIPSim
======

SIPSim is a toolset for simulating data from high resolution 
stable isotope probing (HR-SIP) experiments.

>Note: currently SIPSim is only Python 2.7 compatable, mainly because MFEprimer is used for simulating sequences from genomes.
We recommend using an anaconda environment, which will also help with installing the dependencies.


#### Sections

- [REFERENCE](#reference)
- [INSTALLATION](#installation)
- [TUTORIALS](#tutorials)
- [SIMULATION WORKFLOW](#simulation_workflow)
- [CHANGE LOG](#changelog)
- [LICENSE](#license)


# REFERENCE

[[top](#sections)]

If you use SIPSim, please cite:

> Youngblut, ND, Buckley DH. Evaluating the accuracy of DNA stable isotope probing. doi: https://doi.org/10.1101/138719


# INSTALLATION

[[top](#sections)]

## DEPENENCIES

### Python

See setup.py for a list of python package dependences.

#### Anaconda environment

You can use the `SIPSim_conda_env.yml` file to create an Anaconda environment for running `SIPSim`

> Note: this environment just helps with dependencies. You will still need to install other software into this environment (see below)

### Other

* [MFEprimer_linux](https://github.com/nick-youngblut/MFEprimer_linux)
  * This is a modified version of [MFEprimer-2.0](https://github.com/quwubin/MFEprimer)
    * It has been modified for installation into a linux environment via `python setup.py install`

### Dependency install issues (using Anaconda)

* boost-python
  * install via conda or see [boost.org](http://www.boost.org/doc/libs/1_64_0/libs/python/doc/html/index.html) on other methods to install
    * Note: there's currently no official conda channel for boost-python
* scipy libgrfortran issues
  * See https://github.com/ilastik/ilastik-build-conda/issues/17
* scipy MKL issues
  * See https://github.com/BVLC/caffe/issues/3884
  * MKL can be shut down. See [this blog post](https://www.continuum.io/blog/developer-blog/anaconda-25-release-now-mkl-optimizations)
    * This can be done by: `conda install nomkl`
    * NOTE: OpenBlas will try to use all threads. To limit threads, use `export OMP_NUM_THREADS=N`, where `N` is the number of threads to use.

## Installation of SIPSim

### Clone the repo

```
git clone https:github.com/nyoungb2/SIPSim.git
cd SIPSim
```

### Install the python package

```
python setup.py build
python setup.py install
```

## Installation of SIPSimR

[SIPSimR](https://github.com/nick-youngblut/SIPSimR) contains R scripts for data
analysis and plotting of data produced by SIPSim. See the SIPSimR README for more information.


# TUTORIALS

[[top](#sections)]

* [An example with 3 genomes](./ipynb/example/1_dataset.ipynb)
* [Recreating Fig 1 from Lueders et al., 2004](./ipynb/example/Lueders2004.ipynb)


# SIMULATION_WORKFLOW

[[top](#sections)]

![simulation pipeline](img/simulation_pipeline.png)


# CHANGELOG

[[top](#sections)]

## v0.2

* Restructered SIPSim to be fully installable via `setup.py`. This involved spliting the
software into 3 repositories (SIPSim, SIPSimR, and MFEprimer-linux).


# LICENSE

[[top](#sections)]

* Free software: MIT license