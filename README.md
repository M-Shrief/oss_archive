# OSS Archive

## Overview
- [Setup](#setup)

## Setup

- Setup your virtual environment:
```sh
$ python -m venv .venv
```

- use the virtual environment with poetry
```sh
$ poetry env use .venv/bin/python3
```

- Install project packages:
```sh
$ poetry install 
```

- Run the app:
```sh
$ poetry run uvicorn oss_archive.main:app --reload
```
