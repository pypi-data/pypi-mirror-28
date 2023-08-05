# -*- coding: utf-8 -*-


class DotDict(dict):
    def __getattr__(self, attrname):
        try:
            attr = super(DotDict, self).__getattr__(attrname)

        except AttributeError as err:
            try:
                attr = self[attrname]

            except KeyError:
                raise err

        return attr

    def __setattr__(self, attrname, val):
        try:
            super(DotDict, self).__setattr__(attrname, val)

        except AttributeError:
            self[attrname] = val

    def __delattr__(self, attrname):
        try:
            super(DotDict, self).__delattr__(attrname)

        except AttributeError:
            del self[attrname]
