from copytext import CopyException, Copy, Sheet
from openpyxl.reader.excel import load_workbook


def format_name(name):
    if not name:
        return None

    parts = name.split(', ')
    parts.reverse()
    _tmp_parts = []
    for part in parts:
        sub_parts = part.split()
        if len(sub_parts) > 1:
            for sub_part in sub_parts:
                _tmp_parts.append(sub_part)
        elif len(sub_parts) == 1:
            _tmp_parts.append(sub_parts[0])

    parts = _tmp_parts
    _tmp_parts = []
    _suffixes = []
    for part in parts:
        if len(part) == 1:
            _tmp_parts.append(part + '.')
        elif part in ['JR', 'SR', ]:
            _suffixes.append(part + '.')
        else:
            _tmp_parts.append(part)

    parts = _tmp_parts

    ret = ' '.join([part.capitalize() for part in parts])
    if len(_suffixes) > 0 :
        ret = ret + ', ' + ' '.join([suf.capitalize() for suf in _suffixes])

    return ret


def format_business_name(name):
    return capitalize(name)


def capitalize(text):
    if not text:
        return None
    parts = text.split()
    return ' '.join([part.capitalize() for part in parts])


FIELD_NAME_FILTERS = {
    'Donor Name': format_name,
    'Business Name': format_business_name,
    'Business Title': capitalize,
    'Powerplayer': format_name
}


class PlayersCopy(Copy):
    """
    Custom Copy object for Power Players project that makes sure text is formatted properly on load.
    """
    def load(self):
        """
        Parses the downloaded Excel file and writes it as JSON.
        """
        try:
            book = load_workbook(self._filename, data_only=True)
        except IOError:
            raise CopyException('"%s" does not exist. Have you run "fab update_copy"?' % self._filename)

        for sheet in book:
            columns = []
            rows = []

            for i, row in enumerate(sheet.rows):
                row_data = [c.internal_value for c in row]

                if i == 0:
                    columns = row_data
                    continue

                # If nothing in a row then it doesn't matter
                if all([c is None for c in row_data]):
                    continue

                data = dict(zip(columns, row_data))

                for field, func in FIELD_NAME_FILTERS.items():
                    try:
                        data[field] = func(data[field])
                    except KeyError:
                        pass

                rows.append(data)

            self._copy[sheet.title] = Sheet(sheet.title, rows, columns)
