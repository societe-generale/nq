from nq.filters import Filter
from nq.flags import Flags


class recurse_until:
    pass


def _common_iterable(obj):
    if isinstance(obj, dict):
        return obj
    else:
        return (index for index, value in enumerate(obj))


def _is_iterable(obj):
    return isinstance(obj, (list, tuple, set, dict))


def logger(enabled, depth):
    def log_wrapper(message, *args, **kwargs):
        if enabled:
            print(" " * depth * 2, "[nq]", message, *args, **kwargs)

    return log_wrapper


def nested_query(iterable, *path_parts, **kwargs):
    results = []
    if not _is_iterable(iterable):
        return results
    depth = kwargs["depth"] if "depth" in kwargs else 0
    verbose = kwargs["verbose"] if "verbose" in kwargs else False
    log = logger(verbose, depth)
    flags = []
    if "flags" in kwargs:
        flags = kwargs["flags"]
        if not isinstance(flags, list):
            flags = [flags]

    if len(path_parts) > 0:
        path_part = path_parts[0]
        log("Searching with path part", path_part, "on iterable", iterable)
        if isinstance(path_part, Filter):
            for key in _common_iterable(iterable):
                log("Applying filter", path_part, "on item", iterable[key])
                if path_part.check_filter(key, iterable[key], depth):
                    if len(path_parts) == 1:
                        results.append(iterable[key])
                    else:
                        results += nested_query(
                            iterable[key],
                            *path_parts[1::],
                            depth=depth + 1,
                            verbose=verbose
                        )
        elif path_part is recurse_until:
            if len(path_parts) > 1:
                test_next_part = nested_query(
                    iterable, *path_parts[1::], depth=depth + 1, verbose=verbose
                )
                if type(iterable) in (list, dict):
                    for key in _common_iterable(iterable):
                        if len(path_parts) == 1:
                            results.append(iterable[key])
                        else:
                            results += nested_query(
                                iterable[key],
                                *path_parts,
                                depth=depth + 1,
                                verbose=verbose
                            )
                if test_next_part:
                    results += test_next_part
        else:
            found_item = False
            try:
                iterable[path_part]
                found_item = True
            except Exception:
                pass
            if found_item:
                if len(path_parts) == 1:
                    results.append(iterable[path_part])
                elif type(iterable[path_part]) in (tuple, dict, list):
                    results += nested_query(
                        iterable[path_part],
                        *path_parts[1::],
                        depth=depth + 1,
                        verbose=verbose
                    )
        log("Found results", results)
        if depth == 0 and len(results) == 1:
            return results[0]
        else:
            if Flags.FIRST_RESULT in flags:
                return results[0]
            elif Flags.LAST_RESULT in flags:
                return results[-1]
            else:
                return results
    else:
        return iterable


class Tree:
    def __init__(self, data):
        self.data = data

    def query(self, *path_parts, **kwargs):
        return nested_query(self.data, *path_parts, **kwargs)
