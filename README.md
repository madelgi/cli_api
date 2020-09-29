# CLI API


A small API for executing arbitrary scripts in the cloud.


## Set up and installation

I currently don't have this hosted anywhere, so you will need to run the
code locally to experiment with it.


## Run locally

To run the API locally, fill out a `.env` file (you can basically use the `.env.sample` file verbatim),
and run the following:

```bash
$ make dev
```

You should now be able to access the API at `0.0.0.0:5000`.


## Run tests

To run tests, you must have the development container already running. If you do not, please execute `make dev`
first. After this, you can execute the following to run the test suite:

```bash
$ make pytest
```

If you would like to run a specific test, or subset of tests, pass the location to the `test_loc`
argument:

```bash
$ make pytest test_loc=tests/script/test_controller.py
```

