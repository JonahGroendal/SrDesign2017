__author__ = "Jonah Groendal"

import urllib.request
import xlrd

class Dataset:
    """
    This class is primarily used to clean csv files. A csv can be read into memory
    with import_csv(), cleaned using the other functions, and exported to file with
    export_csv().

    This class has two attributes: a 2D list named self.table and
    a list named column_names. self.table contains the data of the dataset.
    self.column_names IS self.table[0], it is the header for the table
    (self.column_names and self.table[0] can be used interchangeably).

    Instances of this class are iterable. When iterated over, a dictionary
    representing each row in self.table is returned. The dictionary is a COPY
    of what's in self.table, so changing values in the returned dictionary does
    not effect the data in self.table.
    """

    def __init__(self, csv_filepath=None, column_names=[None]):

        self.table = [[]]
        column_names = column_names
        if csv_filepath is not None:
            self.import_csv(csv_filepath)

    @property
    def column_names(self):
        return self.table[0]

    @column_names.setter
    def column_names(self, v):
        self.table[0] = v

    @column_names.deleter
    def column_names(self):
        self.table[0] = [None]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        unknown_count = 1
        doc = {}
        try:
            for col_index, value in enumerate(self.table[self.index + 1]):
                try:
                    col_name = self.column_names[col_index]
                    if col_name in doc:
                        if type(doc[col_name]) is not list:
                            doc[col_name] = list((doc[col_name],))
                        doc[col_name].append(value)
                    else:
                        doc[col_name] = value
                except IndexError:
                    # label for this col doesn't exist, use "unknown_n" as substitute
                    doc["unknown_{0}".format(unknown_count)] = value
                    unknown_count += 1
        except IndexError:
            raise StopIteration
        else:
            self.index += 1
        return doc

    ##########################
    # IMPORT / EXPORT
    ##########################
    def import_csv(self, filepath, delimiter="|", encoding="utf-8"):
        """ Imports csv into self.table """
        with open(filepath, encoding=encoding) as f:
            file_str = f.read()
        self.csv_into_table(file_str, delimiter)

    def export_csv(self, filepath, pretty=False):
        """ Exports to csv """
        with open(filepath, "w") as f:
            f.write(self.to_csv_string(pad_values=pretty))

    ##########################
    # ROW OPERATIONS
    ##########################
    def append_row(self, row_dict):
        """ Appends a row of data to self.table """
        row = [None] * len(self.column_names)
        for key in row_dict:
            row[self.column_names.index(key)] = row_dict[key]
        self.table.append(row)

    def remove_last_row(self):
        """ Removes last row in self.table """
        del self.table[len(self.table) - 1]

    def remove_rows_where_equals(self, column_name, value):
        """ Removes all rows where value of column == value """
        index = self.column_names.index(column_name)
        indices_to_delete = []
        for count, row in enumerate(self.table):
            if row[index] == value:
                indices_to_delete.append(count)
        for i in range(len(indices_to_delete)):
            del self.table[indices_to_delete[len(indices_to_delete) - 1 - i]]

    def remove_rows_where(self, column_name, function):
        """
        Removes rows where function returns False when passed the value of
        column column_name. function must take only that one parameter.
        """
        column_index = self.column_names.index(column_name)
        data_rows = filter(lambda row: not function(row[column_index]), self.table[1:])
        self.table = [self.column_names]
        self.table.extend(data_rows)

    def combine_rows(self, row_indices):
        """
        Combines values from all specified row_indices in self.table into
        self.table[row_indices[0]]
        """
        new_row_index = row_indices[0]
        for index in row_indices[1:]:
            self.table[new_row_index].extend(self.table[index])
        for index in row_indices[1:]:
            del self.table[index]

    def remove_duplicate_rows(self):
        """ Removes any rows that contain all the same data as another row """
        self.table = [list(self.table[:1])].extend(list(set(tuple(i) for i in self.table[1:])))

    ##########################
    # COLUMN OPERATIONS
    ##########################
    def conform_column_names(self, rename={}):
        """
        Converts all column names to lowercase.
        Optionally, rename can be set to replace column names.
        """
        for i in range(len(self.column_names)):
            if self.column_names[i] in rename:
                self.column_names[i] = rename[self.column_names[i]]
            else:
                self.column_names[i] = self.column_names[i].lower()

    def create_bool_column_from_value(self, source_column, value, assume_false=False):
        """
        Creates a new boolean column based on the value in another column.

        Ex: An existing "toxicity" column contains the values "Toxic" or
        "Immunogenic" or both. This fuction can create a new column named "Immunogenic"
        and insert into it the value "True" in every record that contains the value
        "Immunogenic" within the "toxicity" column.

        params:
            source_column - the column in which the original value is located (Ex: toxicity)
            value - an existing value from within the column source_filed (Ex: Immunogenic)
            assume_false - assume the nonexistance of value to mean "False". If false, inserts "None"
        """
        # add value as new column
        self.column_names.append(value)
        index = self.column_names.index(source_column)

        for row in self.table[1:]:
            if value in row[index]:
                row.append(True)
            else:
                if assume_false:
                    row.append(False)
                else:
                    row.append(None)

    def remove_all_columns_except(self, keep_column_names):
        """ Removes all columns in self.table besides those specified. """
        columns = list(self.column_names)  # make a copy of column names
        for column in columns:
            if column not in keep_column_names:
                self.remove_column(column)

    def remove_column(self, column_name):
        """ Remove column from self.table whose column name is column_name. """
        index = self.column_names.index(column_name)
        for row in self.table:
            del row[index]

    def unique_values_of_column(self, column_name):
        """ Returns list of all unique values for a column. """
        index = self.column_names.index(column_name)
        return list(set([v[index] for v in self.table[1:]]))

    ##########################
    # HELPER METHODS
    ##########################
    def csv_into_table(self, csv_str, delimiter="|"):
        """ Reads csv_str into self.table. """
        self.table = csv_str.split("\n")
        for i in range(len(self.table)):
            self.table[i] = self.table[i].split(delimiter)
        # remove trailing line if it's empty
        empty = True
        for value in self.table[len(self.table) - 1]:
            if value != '' and value is not None:
                empty = False
        if empty:
            del self.table[len(self.table) - 1]

    def to_csv_string(self, delimiter="|", pad_values=False):
        """
        Returns a string representation of self.table in csv format.
        If pad_values, each string in a column will be the same length (padded
        with spaces).
        """
        def pad(value, index):
            if pad_values:
                format_str = "{{:<{}}}".format(col_lengths[index])
                return format_str.format(value)
            else:
                return value

        if pad_values:
            col_lengths = [None] * len(self.column_names)
            for i, v in enumerate(col_lengths):
                column_values = [c[i] for c in self.table]
                col_lengths[i] = max([len(str(x)) for x in column_values])

        csv_str = ""
        for row in self.table:
            for count, value in enumerate(row):
                if value is True:
                    csv_str += pad("1", count)
                elif value is False:
                    csv_str += pad("0", count)
                else:
                    csv_str += pad(str(value), count)
                if count < len(row) - 1:
                    csv_str += delimiter
            csv_str += "\n"
        return csv_str

class Scrub:
    """
    Misc methods for common scrubbing operations.
    Attribute self.delimiter is the default delimiter used in the methods.
    """
    def __init__(self, delimiter="|"):
        self.delimiter = delimiter

    def read_from_file(self, filepath, encoding="utf-8"):
        with open(filepath, encoding=encoding) as f:
            file_str = f.read()
        return file_str

    def write_to_file(self, filepath, str_to_write):
        with open(filepath, "w") as f:
            f.write(str_to_write)

    def download_html_to_file(self, filepath, url, encoding="utf-8"):
        response = urllib.request.urlopen(url)
        data = response.read()          # bytes object
        html = data.decode(encoding)     # str
        with open(filepath, "w") as f1:
            f1.write(html)
        return html

    def csv_str_from_quoted_csv_str(self, file_str, current_delimiter=","):
        """
        Takes the contents of a csv file with values quoted as a string and
        returns the contents of the csv string without quotes around values.
        """
        temp = self.delimiter
        self.delimiter = '","'
        file_list = self.list_from_csv_str(file_str)
        self.delimiter = temp
        for row in file_list:
            for i in range(len(row)):
                row[i] = row[i].replace('"', '')
        return self.csv_str_from_list(file_list)

    def list_from_csv_str(self, file_str):
        lines = file_str.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].split(self.delimiter)
        # remove trailing line if it's empty
        empty = True
        for value in lines[len(lines) - 1]:
            if value != '' and value is not None:
                empty = False
        if empty:
            del lines[len(lines) - 1]

        return lines

    def csv_str_from_list(self, file_list):
        file_str = ""
        for row in file_list:
            for count, value in enumerate(row):
                if value is True:
                    file_str += "1"
                elif value is False:
                    file_str += "0"
                else:
                    file_str += str(value)
                if count < len(row) - 1:
                    file_str += self.delimiter
            file_str += "\n"
        return file_str

    def prepend_list(self, file_list, values):
        return [list(values)] + file_list

    def remove_all(self, file_list, char):
        for row in file_list:
            for i in range(len(row)):
                row[i] = row[i].replace(char, '')
        return file_list


class Inspect:
    """
    Methods useful for inspecting csv files. Not used in any scubbing scripts
    but sometimes handy when making the scripts.
    """
    def __init__(self):
        pass

    def get_column_values(self, file_str, column_name, only_unique=False):
        """
        Returns list of all values from within column column_name.

        params:
            file_str - the contents of the file in a string
            column_name - name of column
            only_unique - return only unique values
        """
        column_index = self.get_column_index(file_str, column_name)
        lines = file_str.split("\n")
        values = []
        for line in lines:
            line_values = line.split(self.delimiter)
            if only_unique:
                if line_values[column_index] not in values:
                    values.append(line_values[column_index])
            else:
                values.append(line_values[column_index])
        return values

    def get_row_indexes_where_equals(self, file_list, column, value):
        """
        params:
            file_list - contents of file as a string
        """
        column_index = file_list[1].index(column)
        indexes = []
        for count, row in enumerate(file_list):
            if count > 1:
                if row[column_index] == value:
                    indexes.append(count)
        return indexes
