# nq

Nested Queries, get items hidden far far away in your lists or dictionaries

## Description

nq is a Python library which can helps you fetching data deeply nested into Python structures (lists, dicts)
You just have to give a path to nq and it will be able to fetch the data you wanted.

## Installation

You just have to clone this repository and install it using the command
```bash
pip install .
```

Or you can also install it from PyPi
```bash
pip install nq
```

You can test the installation by running the following command :

```bash
python -c "import nq; print(nq.nested_query([00,[11,[22],33],44,[55]], 1, 1, 0))"
```

It should print the number 22

## Usage

Given the following JSON file

```json
{
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95,
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99,
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99,
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99,
            },
        ]
    }
}
```

Here is a few nq commands to get you started :

```python
>>> nq.nested_query(data, "store", "book", 1)
{'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}
>>> nq.nested_query(data, "store", "book", nq.get_range(2, 4))
[{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
>>> nq.nested_query(data, "store", "book", nq.when_attribute("price", equals=22.99))
{'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}
>>> nq.nested_query(data, nq.recurse_until, "price")
[8.95, 12.99, 8.99, 22.99]
>>> nq.nested_query(data, nq.recurse_until, nq.when_attribute("price", greater_than=9), "price")
[12.99, 22.99]
```

## Licensing

nq uses the MIT license, you can find more details about it [here](LICENSE)

## Contributing

You can find more details about contributions [here](CONTRIBUTING.md)