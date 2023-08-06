from setuptools import setup

setup(
    name = "ga_dmp_hdf5",
    version = "0.1",
    py_modules = ["dmp_core"],
    description = "Tools for creating hdf5 files in GA's DMP format",
    author = "Richard Kalling",
    install_requires = ["numpy", "h5py"],
    license='MIT'
)
