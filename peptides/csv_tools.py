import definitions   # ./definitions.py
import urllib.request
import xlrd

class Dataset:
    # params (class attributes):
    #   - table - A 2D list with the first row being column names and the rest data
    def __init__(self, csv_filepath=None, table=None):
        self.table = table
        if csv_filepath is not None:
            self.import_csv(csv_filepath)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        unknown_count = 1
        doc = {}
        try:
            for col_index, value in enumerate(self.table[self.index + 1]):
                try:
                    col_name = self.table[0][col_index]
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

    # Reads csv_str into self.table
    def csv_into_table(self, csv_str, delimiter="|"):
        self.table = csv_str.split("\n")
        for i in range(len(self.table)):
            self.table[i] = self.table[i].split(delimiter)
        # remove trailing line if it's empty
        empty = True
        for value in self.table[len(self.table)-1]:
            if value != '' and value != None:
                empty = False
        if empty: del self.table[len(self.table)-1]

    def import_csv(self, filepath, delimiter="|"):
        with open(filepath) as f:
            file_str = f.read()
        self.csv_into_table(file_str, delimiter)

    # Exports to csv
    def export_csv(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.to_csv_string())

    # Returns a string representation of self.table in csv format
    def to_csv_string(self, delimiter="|"):
        csv_str = ""
        for row in self.table:
            for count, value in enumerate(row):
                if value == True:
                    csv_str += "1"
                elif value == False:
                    csv_str += "0"
                else:
                    csv_str += str(value)
                if count < len(row)-1:
                    csv_str += delimiter
            csv_str += "\n"
        return csv_str

    # Converts all field (column) names to lowercase
    # Optionally, rename can be set to replace field names.
    def conform_field_names(self, rename={}):
        for i in range(len(self.table[0])):
            if self.table[0][i] in rename:
                self.table[0][i] = rename[self.table[0][i]]
            else:
                self.table[0][i] = self.table[0][i].lower()

    def remove_duplicate_rows(self):
        self.table = [list(self.table[:1])].extend(list(set(tuple(i) for i in self.table[1:])))

    # Creates a new boolean field based on the value in another field.
    # Ex: An existing "toxicity" field contains the values "Toxic" or
    # "Immunogenic" or both. This fuction can create a new field named "Immunogenic"
    # and insert into it the value "True" in every record that contains the value
    # "Immunogenic" within the "toxicity" field.
    # params:
    #   file_list - a 2D list created from the csv
    #   source_field - the field in which the original value is located (Ex: toxicity)
    #   value - an existing value from within the field source_filed (Ex: Immunogenic)
    #   assume_false - assume the nonexistance of value to mean "False". If false, inserts "None"
    def create_bool_field_from_value(self, source_field, value, assume_false=False):
        # add value as new field
        self.table[0].append(value)
        index = self.table[0].index(source_field)

        for row in self.table[1:]:
            if row[index] == value:
                row.append(True)
            else:
                if assume_false:
                    row.append(False)
                else:
                    row.append(None)

    def remove_all_fields_except(self, keep_fields):
        fields = list(self.table[0])  # make a copy of field names
        for field in fields:
            if field not in keep_fields:
                self.remove_field(field)

    def remove_field(self, field):
        index = self.table[0].index(field)
        for row in self.table:
            del row[index]

    def remove_last_row(self):
        del self.table[len(self.table) - 1]

class Scrub:
    def __init__(self, delimiter="|"):
        self.delimiter = delimiter

    def read_from_file(self, filepath):
        with open(filepath) as f:
            file_str = f.read()
        return file_str

    def write_to_file(self, filepath, str_to_write):
        with open(filepath, "w") as f:
            f.write(str_to_write)

    def download_html_to_file(self, filepath, url):
        response = urllib.request.urlopen(url)
        data = response.read()          # bytes object
        html = data.decode('utf-8')     # str
        with open(filepath, "w") as f1:
            f1.write(html)
        return html

    def csv_str_from_quoted_csv_str(self, file_str, current_delimiter=","):
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
        if empty: del lines[len(lines) - 1]

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

    def list_from_quoted_csv_str(self, file_str):
        temp = self.delimiter
        self.delimiter = '","'
        file_list = self.list_from_csv_str(file_str)
        self.delimiter = temp
        file_list = self.remove_all(file_list, '"')
        # remove trailing line if it's empty
        empty = True
        for value in file_list[len(file_list) - 1]:
            if value != '' and value is not None:
                empty = False
        if empty: del file_list[len(file_list) - 1]
        return file_list

    # Converts all field names of a formatted csv to lower case
    # Optionally, replace can be set to replace a field name.
    # replace can be used to override the lowercase conversion of a field name.
    def conform_field_names(self, file_str, rename={}):
        split_str = file_str.split("\n", 2)
        for i in range(len(split_str)):
            # replace newline that split() removed
            if i != 2:
                split_str[i] = split_str[i] + '\n'
            if i == 1:
                # convert field names to lowercase
                split_str[i] = split_str[i].lower()
                # replace fields
                for key in replace:
                    split_str[i] = split_str[i].replace(key.lower(), replace[key])
        return ''.join(split_str)

    def remove_all(self, file_list, char):
        for row in file_list:
            for i in range(len(row)):
                row[i] = row[i].replace(char, '')
        return file_list

    def csv_from_excel(self, csv_file, workbook_filepath, sheet_name):
        wb = xlrd.open_workbook(workbook_filepath)
        sh = wb.sheet_by_name('Sheet1')
        sh.row_values(rownum)


class Inspect:
    def __init__(self):
        pass

    def get_excel_sheet_names(self, workbook_filepath):
        wb = xlrd.open_workbook(workbook_filepath)
        return wb.sheets()

    # Assumes field names are on second line of file
    def get_field_values(self, file_str, field_name, only_unique=False):
        field_index = self.get_field_index(file_str, field_name)
        lines = file_str.split("\n")
        values = []
        for line in lines[2:]:
            line_values = line.split(self.delimiter)
            if only_unique:
                if line_values[field_index] not in values:
                    values.append(line_values[field_index])
            else:
                values.append(line_values[field_index])
        return values

    # Assumes field names are on second line of file
    # substring of file can be given as arugment
    def get_field_index(self, file_str, field_name):
        lines = file_str.split("\n", 2)
        for line_count, line in enumerate(lines):
            if line_count == 1:
                fields = line.split(self.delimiter)
                for field_count, field in enumerate(fields):
                    if field == field_name:
                        return field_count

    def get_row_indexes_where_equals(self, file_list, field, value):
        field_index = file_list[1].index(field)
        indexes = []
        for count, row in enumerate(file_list):
            if count > 1:
                if row[field_index] == value:
                    indexes.append(count)
        return indexes
