# csv2py

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

csv2py is a Python package that simplifies the process of reading CSV files and loading them into Django models. It converts CSV data into Python objects, allowing you to easily manipulate and work with your data.

## Features

- Read CSV files and convert them into Python objects
- Load Python objects into Django models
- Supports different encodings and delimiters

## Installation

You can install csv2py using pip:

```bash
pip install csv2py
```

## How to use

Consider the scenario below:

```python
# my_project/my_app
from django.db import models


class Question(models.Model):
    number = models.IntegerField(...)

instance = Question(number=1)
```

1. Create a new file for your loaders classes. For example `loaders.py`

```python
# my_app/loaders.py
from csv2py import DjangoCSVLineLoader, Field
from . import models

class QuestionLoader(DjangoCSVLineLoader):
    model = models.Question
    context_name = "question"
    fields = [Field(column="NUMBER", target_attribute="number")]

```

2. Create a Django view to load the file into your loaders

```python
loader = QuestionLoader(file, encoding="UTF-8-sig", delimiter=",")
loader.run()
```


## Contributing

Contributions to csv2py are welcome and appreciated! Please see the CONTRIBUTING.md file for more information.

## License

csv2py is licensed under the MIT License. See the LICENSE file for more information.
