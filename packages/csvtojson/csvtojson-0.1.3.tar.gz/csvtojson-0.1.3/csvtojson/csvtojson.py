from typecheck import typecheck
import json


class csvtojson:
    def __init__(self, csv,
                 leading_row=True,
                 delimiter=',',
                 schema_fields=None,
                 remove_null=True):
        if not leading_row and not schema_fields:
            raise ValueError(('There should be either a leading row '
                              'or a defined schema'))
        self.delimiter = delimiter
        self.remove_null = remove_null
        self.header, self.body = self._read_csv(
            csv,
            leading_row=leading_row)
        if schema_fields:
            self.header = [s['name'] for s in schema_fields]
            self.schema = [s['type'].lower() for s in schema_fields]
        else:
            schema = ['none'] * len(self._split(self.body[0]))
            self.schema = self._analyze_schema(schema)

    def _read_csv(self, csv, leading_row=False):
        with open(csv, 'rb') as f:
            csv_list = f.read().splitlines()
            if leading_row:
                header = self._split(csv_list[0])
                body = csv_list[1:]
            else:
                header = []
                body = csv_list
        return header, body

    def _analyze_schema(self, schema):
        order = {
            'string': 0,
            'boolean': 1,
            'float': 2,
            'integer': 3,
            'none': 4
        }

        for row in self.body:
            fields = self._split(row)
            for index, field in enumerate(fields):
                t = typecheck(field.strip())
                if order[schema[index]] > order[t]:
                    schema[index] = t
        return [t if t != 'none' else 'string' for t in schema]

    def _split(self, row):
        nvals = []
        vals = row.replace('""', "_'_").split(self.delimiter)
        stack = []
        for val in vals:
            if not stack:
                if val.startswith('"'):
                    if val.endswith('"'):
                        nvals.append(val[1:-1].replace("_'_", '"'))
                    else:
                        stack.append(val)
                else:
                    nvals.append(val.replace("_'_", '"'))
            else:
                if val.endswith('"'):
                    stack.append(val)
                    nvals.append(','.join(stack)[1:-1].replace("_'_", '"'))
                    stack = []
                else:
                    stack.append(val)
        return nvals

    def convert(self):
        dtype = {
            'string': str,
            'boolean': bool,
            'float': float,
            'integer': int
        }
        for row in self.body:
            fields = self._split(row)
            res = {}
            for index, field in enumerate(fields):
                try:
                    t = dtype[self.schema[index]]
                    f = field.strip()
                    h = self.header[index].strip()
                    if f:
                        if t in [float, int]:
                            res[h] = t(f)
                        if t == bool:
                            if f.lower() == 'true':
                                res[h] = True
                            if f.lower() == 'false':
                                res[h] = False
                        if t == str:
                            if f.startswith('"') and f.endswith('"'):
                                res[h] = f[1:-1]
                            else:
                                res[h] = f
                    if h not in res and not self.remove_null:
                        res[h] = None
                except ValueError as err:
                    pass
            yield json.dumps(res, ensure_ascii=False)

    def write(self, output_file):
        for row in self.convert():
            output_file.write(row + '\n')
