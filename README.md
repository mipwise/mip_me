# Mip Me
This repository hosts the package that is built along the 
[Mip Go](https://www.mipwise.com/mip-go) program and solves the 
[Diet Problem](docs/diet_problem.ipynb) to illustrate the implementation of 
an optimization engine.

## Repository guide
- [docs](docs): Hosts documentation (in addition to readme files and docstrings)
  of the project.
- [mip_me](mip_me): Contains the Python package that solves the Diet Problem.
  It contains scripts that define the input and the output data schemas, the 
  solution engine, and other auxiliary modules.
- [test_mip_me](test_mip_me): Hosts testing suits and testing data sets used 
  for testing the solution throughout the development process.
- `pyproject.toml` and `setup.cfg` are used to build the distribution files 
  of the package (more information [here](https://github.com/mipwise/mip-go/blob/main/6_deploy/1_distribution_package/README.md)).