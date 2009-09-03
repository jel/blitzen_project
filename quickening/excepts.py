# -*- coding: utf-8 -*-
class DependencyLoop(RuntimeError):
    def __init__(self, deps_list, loaded_list):
        msg = u"\n\nCould not resolve:\n\n"

        for item, deps in deps_list.items():
            msg += u"    %r" % item
            if deps is not None:
                msg += u" which requires:"
                for d in deps:
                    msg += "\n        %r " % d
                    if (not d in loaded_list) and (not d in deps_list.keys()):
                        msg += u"(unavailable)"
                    elif d in loaded_list:
                        msg += u"(resolved)"
                msg += u"\n"
            msg += u"\n"

        msg += u"Resolved so far:\n"
        for l in loaded_list:
            msg += u"\n        %r" % l

        msg += u"\n"

        super(DependencyLoop, self).__init__(msg)
