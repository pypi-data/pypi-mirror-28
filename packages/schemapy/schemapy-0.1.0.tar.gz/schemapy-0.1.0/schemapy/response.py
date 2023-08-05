# -*- coding: utf-8 -*-

from schemapy.exceptions import ResponseError
from schemapy.utils import DotDict

from collections import Iterable
import six


class Response(object):
    def __init__(self, rows, fields=None, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)

        if isinstance(rows, six.string_types):
            raise ResponseError('rows cannot be a string')

        if not isinstance(rows, Iterable):
            rows = [rows]

        if fields is None:
            fields = []

        self._rows = rows
        self.fields = fields
        self._rowid = 0
        self._nrows = len(rows)

    def __repr__(self):
        return 'Response(count={0}, fields=[{1}])'.format(
            self._nrows,
            ', '.join([
                '{0}:{1}{2}'.format(
                    field.name,
                    field.type,
                    '*' if field.required else ''
                )
                for field in self.fields
            ])
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self._rowid < self._nrows:
            ret = self[self._rowid]
            self._rowid += 1
            return ret

        else:
            raise StopIteration

    def __getitem__(self, idx):
        if idx >= self._nrows:
            raise IndexError('list index out of range')

        row = self._rows[idx]

        record = DotDict()

        for field in self.fields:
            if field.required and field.name not in row:
                raise ResponseError(
                    'Missing required field: {0}'.format(field.name)
                )

            if field.name in row:
                validated = field.validate(row[field.name])

                if validated[1] is not None:
                    raise ResponseError(validated[1])

                else:
                    record[field.name] = validated[0]

        return record
