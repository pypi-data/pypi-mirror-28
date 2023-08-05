## plait.py

plait.py is a program for generating fake data from composable yaml templates.

The idea behind plait.py is that it should be easy to model fake data that
looks real. Currently, many fake data generators model their data as a
collection of
[IID](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables)
variables; with plait.py we can stitch together those variables into a more
coherent model.

### features

* declarative syntax
* use basic [faker.rb](https://github.com/stympy/faker) fields with #{} interpolators
* sample and join data from CSV files
* lambda expressions, case and mixture fields
* nested and composable templates
* static variables and hidden fields

### how its different

some specific examples of what plait.py can do:

* model realistic populations using census data
* create a taxi trip dataset with a cost model based on geodistance
* add seasonal patterns (daily, weekly, etc) to data
* create realistic zipcodes by state, city or region

### future direction

Currently, plait.py models independent markov processes - future investigation
into modeling processes that can interact with each other is needed.

If you have ideas on features to add, open an issue - Feedback is appreciated!

## usage

### installation

    # install with python
    pip install plaitpy

    # or with pypy
    pypy-pip install plaitpy

### generating records

specify a template as a yaml file, then generate records from that yaml file.

    # a simple example (if cloning plait.py repo)
    python main.py templates/timestamp/uniform.yaml

    # if plait.py is installed via pip
    plait.py templates/timestamp/uniform.yaml

### looking up faker fields

plait.py also simplifies looking up faker fields:

    # list faker namespaces
    plait.py --list
    # lookup faker namespaces
    plait.py --lookup name

    # lookup faker keys
    # (-ll is short for --lookup)
    plait.py --ll name.suffix

## documentation

### yaml file commands

* see docs/FORMAT.md

### datasets

* see docs/EXAMPLES.md
* also see templates/ dir

