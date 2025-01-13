# Safe Pickle to JSON Converter

A secure Python utility for converting pickle files to JSON format with two security modes: strict and permissive.

## Features

- **Two Security Modes**:
  - **Strict Mode** (default): Whitelist-based approach that only allows basic data types and common safe objects
  - **Permissive Mode**: Blacklist-based approach that blocks known dangerous operations while allowing more complex types

- **Supported Types**:
  - Basic: dict, list, tuple, str, int, float, bool, None
  - Date/Time: datetime, date, time, timedelta
  - Numbers: Decimal
  - Collections: set, frozenset
  - Additional types in permissive mode: OrderedDict, defaultdict, and more

- **Security Features**:
  - Protection against code execution
  - Prevention of system access
  - Blocking of dangerous modules and operations

## Installation

pip install safe-pickle-to-json

## Usage

### Command Line Interface

Convert a pickle file to JSON using strict mode (default):

