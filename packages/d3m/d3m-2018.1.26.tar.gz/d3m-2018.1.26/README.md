# Python namespace for D3M project

This package provides a common Python namespace for D3M project and utility functions for searching of primitives
installed on the system, their discovery on PyPi, and generation of JSON descriptions of primitives.

## About Data Driven Discovery Program

DARPA Data Driven Discovery (D3M) Program is researching ways to get machines to build
machine learning pipelines automatically. It is split into three layers:
TA1 (primitives), TA2 (systems which combine primitives automatically into pipelines
and executes them), and TA3 (end-users interfaces).

## Installation

This package works with Python 3.6+.

You can install latest stable version from [PyPI](https://pypi.python.org/pypi):

```
$ pip install --process-dependency-links d3m
```

To install latest development version:

```
$ pip install --process-dependency-links git+https://gitlab.com/datadrivendiscovery/d3m.git@devel
```

`--process-dependency-links` argument is required for correct processing of dependencies.

## Changelog

See [HISTORY.md](./HISTORY.md) for summary of changes to this package.

## Repository structure

`master` branch contains latest stable release of the package.
`devel` branch is a staging branch for the next release.

Releases are [tagged](https://gitlab.com/datadrivendiscovery/d3m/tags).

## Primitives D3M namespace

The `d3m.primitives` module exposes all primitives under the same `d3m.primitives` namespace.

This is achieved using [Python entry points](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins).
Python packages containing primitives should register them and expose them under the common
namespace by adding an entry like the following to package's `setup.py`:

```python
entry_points = {
    'd3m.primitives': [
        'primitive_namespace.PrimitiveName = my_package.my_module:PrimitiveClassName',
    ],
},
```

The example above would expose the `my_package.my_module.PrimitiveClassName` primitive under
`d3m.primitives.primitive_namespace.PrimitiveName`.

Configuring `entry_points` in your `setup.py` does not just put primitives into a common namespace, but also
helps with discovery of your primitives on the system. Then your package with primitives just have to be
installed on the system and can be automatically discovered and used by any other Python code.

>**Note:**
Only primitive classes are available thorough  the `d3m.primitives` namespace, not other symbols
from a source module. In the example above, only `PrimitiveClassName` is available, not other
symbols inside `my_module` (except if they are other classes also added to entry points).

<!-- -->
>**Note:**
Modules under `d3m.primitives` are created dynamically at run-time based on information from
entry points. So some tools (IDEs, code inspectors, etc.) might not find them because there are
no corresponding files and directories under `d3m.primitives` module. You have to execute Python
code for modules to be available. Static analysis cannot find them.

## Primitives discovery on PyPi

To facilitate automatic discovery of primitives on PyPi (or any other compatible Python Package Index),
publish a package with a keyword `d3m_primitive` in its `setup.py` configuration:

```python
keywords='d3m_primitive'
```

>**Note:**
Be careful when automatically discovering, installing, and using primitives from unknown sources.
While primitives are designed to be bootstrapable and automatically installable without human
involvement, there are no isolation mechanisms yet in place for running potentially malicious
primitives. Currently recommended way is to use manually curated lists of known primitives.

## Python functions available

The `d3m.index` module exposes the following Python utility functions.

### `d3m.index.search`

Returns a map from primitive path (Python path inside the D3M namespace) to a primitive class,
for all known (discoverable through entry points) primitives, or limited by the
`primitive_path_prefix` search argument.

Example

```python
from d3m import index
for primitive_name, primitive in index.search().items():
    ...
```

### `d3m.index.discover`

Returns package names from PyPi which provide D3M primitives.

This is determined by them having a `d3m_primitive` among package keywords.

You can use `index` argument to set a base URL of Python Package Index to use.
Default is `https://pypi.python.org/pypi`.

### `d3m.index.register_primitive`

Registers a primitive under `d3m.primitives` namespace.

If `primitive_path_suffix` is equal to `foo.bar.Baz`, the primitive will be registered
under `d3m.primitives.foo.bar.Baz`.

This is useful to register primitives not necessary installed on the system
or which are generated at runtime. It is also useful for testing purposes.

## Command line

The `d3m.index` module also provides a command line interface by running
`python -m d3m.index`. The following commands are currently available.

Use `-h` or `--help` argument to obtain more information about each command
and its arguments.

### `python -m d3m.index search`

Searches locally available primitives. Lists registered Python paths to
primitive classes for primitives installed on the system.

### `python -m d3m.index discover`

Discovers primitives available on PyPi. Lists package names containing D3M
primitives on PyPi.

### `python -m d3m.index describe`

Generates a JSON description of a primitive.
