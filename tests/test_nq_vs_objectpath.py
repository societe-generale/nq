from objectpath import Tree as op_Tree
from nq import nested_query, get_range, when_attribute, recurse_until, Filter
from nq import Tree as nq_Tree
import time

data = {
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


def test_that_compares_objectpath_and_nq():
    op_tree = op_Tree(data)
    nq_tree = nq_Tree(data)
    # Simple example
    print("=== Simple example ===")
    print("  1 - ObjectPath version")
    print("    ", op_tree.execute("$.store.book"))
    print("  1 - nq version")
    print("    ", nq_tree.query("store", "book"))

    print("=== Indexes and ranges ===")
    # 1 - Get the second book
    print("  1 - ObjectPath version")
    x = op_tree.execute("$.store.book[1]")
    print("    ", x)
    print("  1 - nq version")
    y = nq_tree.query("store", "book", 1)
    print("    ", y)
    assert x == y
    # 2 - Get the last book
    print("  2 - ObjectPath version")
    x = op_tree.execute("$.store.book[-1]")
    print("    ", x)
    print("  2 - nq version")
    y = nq_tree.query("store", "book", -1)
    print("    ", y)
    assert x == y
    # 3 - Get the 3rd and 4th book
    print("  3 - ObjectPath version")
    x = "Not working"  # op_tree.execute("$.store.book[2:4]") # (Not working)
    print("    ", x)
    print("  3 - nq version")
    y = nq_tree.query("store", "book", get_range(2, 4))
    print("    ", y)
    # assert x == y (Not working)
    # 4 - Get all books where price is equal to 22.99
    print("  4 - ObjectPath version")
    x = list(op_tree.execute("$.store.book[@.price is 22.99]"))
    print("    ", x)
    print("  4 - nq version")
    y = nq_tree.query("store", "book", when_attribute("price", equals=22.99))
    print("    ", y)
    assert x[0] == y
    # 5 - Get all books where price is 22.99 and get only attributes price and isbn
    print("  5 - ObjectPath version")
    x = list(op_tree.execute("$.store.book[@.price is 22.99].(price, isbn)"))
    print("    ", x)
    print("  5 - nq version")
    y = {
        key: value
        for key, value in nested_query(
            data, "store", "book", when_attribute("price", equals=22.99)
        ).items()
        if key in ["price", "isbn"]
    }
    print("    ", y)
    assert x[0] == y
    # 6 - Get all attributes value named price
    print("  6 - ObjectPath version")
    x = list(op_tree.execute("$..price"))
    print("    ", x)
    print("  6 - nq version")
    y = nq_tree.query(recurse_until, "price")
    print("    ", y)
    assert x == y
    # Get all attributes value named price when its more than 9
    print("  7 - ObjectPath version")
    x = list(op_tree.execute("$..price[@ > 9]"))
    print("    ", x)
    print("  7 - nq version")
    y = nq_tree.query(recurse_until, when_attribute("price", greater_than=9), "price")
    print("    ", y)
    assert x == y
    moncustomfilter = Filter(
        lambda p: p.attribute in p.value and len(p.value[p.attribute]) > p.length,
        "moncustomfilter",
    )
    y = nq_tree.query(
        "store",
        "book",
        (
            moncustomfilter(attribute="title", length=16)
            | when_attribute("price", equals=8.99)
        )
        & when_attribute("price", lesser_than=22),
    )
    print(y)


def test_that_proves_nq_is_faster():
    op_start = time.time()
    for i in range(10000):
        op_tree = op_Tree(data)
        op_tree.execute("$.store.book")
        op_tree.execute("$.store.book[1]")
        op_tree.execute("$.store.book[-1]")
        op_tree.execute("$.store.book[@.price is 22.99]")
        op_tree.execute("$..price")
        op_tree.execute("$..price[@ > 9]")
    op_duration = time.time() - op_start
    nq_start = time.time()
    for i in range(10000):
        nq_tree = nq_Tree(data)
        nq_tree.query("store", "book")
        nq_tree.query("store", "book", 1)
        nq_tree.query("store", "book", -1)
        nq_tree.query("store", "book", when_attribute("price", equals=22.99))
        nq_tree.query(recurse_until, when_attribute("price", greater_than=9), "price")
    nq_duration = time.time() - nq_start
    print("NQ :", nq_duration, "VS OP :", op_duration)
    assert nq_duration < op_duration
