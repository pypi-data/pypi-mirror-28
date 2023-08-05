# -*- coding: utf-8 -*-


class SchemapyError(Exception):
    pass


class ActionError(SchemapyError):
    pass


class ResponseError(SchemapyError):
    pass
