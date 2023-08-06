tool-aws
========

[![Build Status](https://travis-ci.org/geoadmin/tool-aws.svg?branch=master)](https://travis-ci.org/geoadmin/tool-aws)

### Macro CMDs for managing AWS resources

## Installation

`$ pip install tool_aws`

## Usage

Batch delete files in S3 by listing content iteratively with a prefix.

`$ s3rm --bucket-name ${BUCKET_NAME} --prefix ${PATH}`

Batch delete tiles in S3 using a bbox in LV95:

`$ s3rm --bucket-name ${BUCKET_NAME} --prefix /1.0.0/ch.swisstopo.fixpunkte-agnes/default/current/2056/* --bbox 2671000,1139000,2712250,1158500 --image-format png`


You can always use the help function:

```
$ s3rm --help
usage: s3rm [-h] -b BUCKETNAME -p PREFIX [--profile PROFILENAME] [--bbox BBOX]
            [-n NBTHREADS] [-s CHUNKSIZE] [-i IMAGEFORMAT] [-lr LOWRES]
            [-hr HIGHRES] [-f]

Purpose:
    This script is intended for efficient and MASSIVE RECURSIVE
    DELETION of S3 'folders'. This mean that any resource matching with
    the PREFIX variable, will be DELETED IRREVERSIVELY.

    Use this script CAREFULLY.

optional arguments:
  -h, --help            show this help message and exit

Mandatory arguments:
  -b BUCKETNAME, --bucket-name BUCKETNAME
                        bucket name
  -p PREFIX, --prefix PREFIX
                        Prefix (string) relative to the bucket base path.

Program options:
  --profile PROFILENAME
                        AWS profile
  --bbox BBOX           a bounding box in lv95
  -n NBTHREADS, --threads-number NBTHREADS
                        Number of threads (subprocess), default: machine
                        number of CPUs
  -s CHUNKSIZE, --chunk-size CHUNKSIZE
                        Chunk size for S3 batch deletion, default is set to
                        1000 (maximal value for S3)
  -i IMAGEFORMAT, --image-format IMAGEFORMAT
                        The image format
  -lr LOWRES, --lowest-resolution LOWRES
                        The lowest resolution in meters
  -hr HIGHRES, --highest-resolution HIGHRES
                        The highest resolution in meters
  -f, --force           force the removal, i.e. no prompt for confirmation.

Disclaimer:
    This software is provided "as is" and
    is not granted to work in particular cases or without bugs.
    The author disclaims any responsability in case of data loss,
    computer damage or any other bad issue that could arise
    using this software.
```

## Setup in dev mode

`$ virtualenv .venv`
`$ source .venv/bin/activate`
`$ pip install -e .`
`$ pip install -r dev-requirements.txt`


To launch the tests:

`$ nosetests tests/`

### Style

Control styling:

`$ flake8 tool_aws/ tests/`

Autofix mistakes:

`$ find tool_aws/* tests/* -type f -name '*.py' -print | xargs autopep8 --in-place --aggressive --aggressive --verbose`

