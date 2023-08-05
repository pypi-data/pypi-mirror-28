# microcosm-resourcesync

Synchronize resources between endpoints

In non-trivial deployments of RESTful services, it is common to have multiple copies of the same service
running in different environments (development, testing, staging, production, etc). In many cases, it is
useful to synchronize some resource data between environments by first copying content to an intermediate
format and then copying that format to another environment.

This process is especially useful if the intermediate format lives in version control and supports diffs
and merging well.


## Installation

Install into a virtualenv:

    mkvirtualenv microcosm-resourcesync --python=python3
    pip install -e .


## Using libyaml

YAML performance is significantly better using `libyaml`. On OSX:

    brew install yaml-cpp libyaml
    pip uninstall PyYAML
    # installing with pip appears not to work
    python -m easy_install pyyaml


## Usage

The main usage is synchronizes from one or more `origin` endpoint to a `destination` endpoint:

    resource-sync [OPTIONS] [ORIGIN]... DESTINATION

Where endpoints may be any of the following:

 -  An HTTP(S) URL
 -  A YAML file
 -  A directory path
 -  The literal `-` (for `stdin`/`stdout`)


## Assumptions

Resources are assumed to adhere to certain REST conventions:

 -  Resources are formatted as either JSON or YAML;

    Origin endpoints define their own format whereas destination endpoints define a *default*
    format; the latter can be overridden on the command line using `--json` or `--yaml`.

    Additional formatters can be added with code changes.

 -  Resources define a few well-known attributes, including `id`, `type`, and `uri`.

    These attributes are derived from the parsed resource dictionary using a schema.

    The default behavior uses a schema based on the [HAL JSON](http://stateless.co/hal_specification.html)
    spec and includes additional processing for hypertext (HATEOAS).

    An alternate, simple schema can also be selected using `--simple` (vs `--hal`).

 -  Resources can be managed remotely over HTTP(S) using `GET` or `PUT` on the `uri`.

    Both operations are assumed to be idempotent. `PUT` operations will be retried a limited
    number of times in the event of connection-related errors.


## Capturing Data

A common use case is pull data from an HTTP endpoint to a local directory:

    resource-sync https://example.com/foo /path/to/local/data

The HTTP response may contain multiple resources (especially for endpoints implementing the microcosm
[Search](https://github.com/globality-corp/microcosm-flask/blob/develop/microcosm_flask/operations.py#L33)
convention or some other form of pagination). Similarly, the `--follow-xxx` flags can be used to
control how `resource-sync` traverses hypertext ("links") present in the HTTP response and pulls
further resources.

Each resource captured from the HTTP endpoint will be saved into its own file within the directory tree,
using type-specific sub-directories. By default, each resource will be stored as YAML (for better human
readability), though JSON may be used instead via the `--json` flag.


## Replaying Data

Another common use case is push data from a local directory to an HTTP endpoint:

    resource-sync /path/to/local/data https://example.com

In this case, `resource-sync` will push the local resource(s) to the remote server.

If the resources define dependency relationships, a *topological* sort will be used to ensure that resources
are pushed in the correct order (e.g. assuming a remote server with no prior content).


## Missing Features

 -  The `--rm` flag has no effect for directory trees or HTTP(S) endpoints.

    This means that there is currently now way to propage a removal from an origin to a destination,
    although a crude approximation can be achieved for a version-controlled directory by first removing
    **all** YAML/JSON files from the tree and then re-running the sychronization. The version control
    system should detect any files that were not restored by the re-run.

 -  The HTTP(S) endpoints should support batching to speed up writes.
