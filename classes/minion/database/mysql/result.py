from ..result import database_result
#/**
# * MySQL database result.   See [Results](/database/results) for usage and examples.
# */

class database_mysql_result(database_result):
    _internal_row = 0;

    def __init__(self, result, sql, as_object = False, params = None):
        new_result = []
        for r in  result.fetchall():
            new_r = dict()
            for key in r.keys():
                new_r[key] = r[key]
            new_result.append(new_r)

        database_result.__init__(self, new_result, sql, as_object=as_object, params=params)

        self._total_rows = int(result.rowcount)

        result.close()

    def __iter__(self):
        return self._result.__iter__()

    def next(self):
        return self._result.next()

