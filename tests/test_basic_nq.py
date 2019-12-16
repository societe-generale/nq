from nq import nested_query, get_all, get_index, get_range


def test_get_nested():
    test_dict = {
        "bonjour": {
            "au revoir": {
                "thing": [
                    {
                        "truc": [
                            {"a": 5, "b": 4},
                            {"a": 6, "b": 7},
                            {"a": 8, "b": 9},
                            {"a": 43, "b": 11},
                            {"a": 54, "b": 422},
                            {"a": 51345, "b": 423},
                            {"a": 525, "b": 2111},
                            {"x": "abc", "y": "xyz"},
                        ]
                    },
                    {
                        "truc": [
                            {},
                            {},
                            {},
                            {},
                            {"x": "abcd"},
                            {"y": "efgh"},
                            {"z": "ijkl"},
                            {},
                        ]
                    },
                ],
                "thing2": 22,
            },
            "goodbye": {
                "thing": [
                    {},
                    {
                        "truc": [
                            {},
                            {},
                            {},
                            {},
                            {"x": "mnop"},
                            {"y": "qrst"},
                            {"z": "uvwx"},
                            {},
                        ]
                    },
                ],
                "thing2": 22,
            },
            "adieu": {"thing": [{}], "thing2": 22},
        }
    }
    assert nested_query(
        test_dict,
        "bonjour",
        get_all(),
        "thing",
        get_index(0),
        "truc",
        get_range(4, 6),
        get_all(),
    ) == [54, 422, 51345, 423]
