# -*- coding: utf-8 -*-
from excepts import DependencyLoop

class DependencyResolver(object):
    """
    >>> dep = DependencyResolver({
    >>>     'a':        ('b', 'c'),
    >>>     'b':        ('c'),
    >>>     'c':        None,
    >>> })
    >>> resolved_deps = dep.resolve()
    >>> assert resolved_deps == ['c', 'b', 'a']
    'True'


    >>> try:
    >>>     dep = DependencyResolver({
    >>>         'a':        ('b'),
    >>>         'b':        ('a'),
    >>>     })
    >>> except DependencyError:
    >>>     print "error caught"
    >>> resolved_deps = dep.resolve()
    Error caught
    """
    def resolve(self, deps_dict):
        """Takes a dictionary of keys and their dependencies as values, and returns the keys in
        the order they should be loaded.  Raises DependencyLoop if dependencies cannot
        be resolved."""
        load_list = []
        remaining_deps = deps_dict

        # while any remaining deps need to be loaded,
        while remaining_deps:
            progress_made = False

            # check if all their dependencies are now met,
            for item, deps_required in remaining_deps.items():
                if deps_required is not None:
                    deps_met = True
                    for dep in deps_required:
                        if dep not in load_list:
                            deps_met = False
                else:
                    deps_met = True

                if deps_met:
                    load_list.append(item)
                    del remaining_deps[item]
                    progress_made = True

            # after examining all remaining_deps, see if we're still
            # making progress
            if not progress_made:
                raise DependencyLoop(remaining_deps, load_list)

        return load_list
