![example workflow](https://github.com/UofU-Cryosphere/spectro-dp/actions/workflows/pytest_flake8.yml/badge.svg)

# spectro-dp
Spectrometer data processing library from field devices.

## Current supported devices
* ASD field spectrometer

## Command Line Interfaces
After the environment is set up and the library installed, it provides the
below listed command line interfaces. 

A detailed help for each command is provided when giving the `--help` option.
All programs will prompt for required parameters if not given with the call.

### `asd_albedo`
Calculate the snow albedo from a sequence of ASD measurements.

### Sample call
```shell
asd_albedo -in /path/to/measurements/ -fp file_prefix -up 0 -down 10
```

### `asd_reflectatnce`
Calculate the reflectance from surface and white reference ASD measurements. 

### Sample call
```shell
asd_reflectatnce -in /path/to/measurements/ -fp file_prefix -rs 0 -wrs 10
```

## Installation
This library was developed with a `conda` environment,
using the supplied [environment.yml](./environment.yml) and 
[environment_dev.yml](./environment_dev.yml).

### Conda
Follow the instructions of the 
[official documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) 
to get started with `conda`.

### Create a `conda` environment
#### Command line interface execution
To use the command line interfaces, the execution environment needs to be set
up using the [environment.yml](./environment.yml):
```shell
conda create --file environment.yml
```

#### Library development
For development and running the tests, both `.yml` 
([environment.yml](./environment.yml) and [environment_dev.yml](./environment_dev.yml)) 
files need to be used for setup:
```shell
conda create --file environment.yml --file environment_dev.yml
```

#### Library installation
This step needs to be done for both, execution and development environment.

1. Clone the repository locally
2. Change path to inside the library
   ```shell
    cd spectrod-dp
   ```
3. Install the Library
    ```shell
    pip install -e .
   ```
   
## Development
All commands are covered by a test suite under the [test](./tests) directory.
Make sure that all tests pass once you completed code changes.

### Running tests
Running the test suite from inside the project root directory
```shell
pytest tests/
```