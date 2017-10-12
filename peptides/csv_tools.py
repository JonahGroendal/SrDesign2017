import definitions
import xlrd

class Scrub:
    def __init__(self, delimiter="|"):
        self.delimiter = delimiter

    def list_from_csv_str(self, file_str):
        lines = file_str.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].split(self.delimiter)
        # remove trailing line if it's empty
        empty = True
        for value in lines[len(lines)-1]:
            if value != '' and value != None:
                empty = False
        if empty: del lines[len(lines)-1]

        return lines

    def list_from_quoted_csv_str(self, file_str):
        temp = self.delimiter
        self.delimiter='","'
        file_list = self.list_from_csv_str(file_str)
        self.delimiter = temp
        file_list = self.remove_all(file_list, '"')
        # remove trailing line if it's empty
        empty = True
        for value in file_list[len(file_list)-1]:
            if value != '' and value != None:
                empty = False
        if empty: del file_list[len(file_list)-1]
        return file_list

    def csv_str_from_list(self, file_list):
        file_str = ""
        for row in file_list:
            for count, value in enumerate(row):
                if value == True:
                    file_str += "1"
                elif value == False:
                    file_str += "0"
                else:
                    file_str += str(value)
                if count < len(row)-1:
                    file_str += self.delimiter
            file_str += "\n"
        return file_str

    def prepend_list(self, file_list, values):
        return [list(values)] + file_list

    # Converts all field names of a formatted csv to lower case
    # Optionally, replace can be set to replace a field name.
    # replace can be used to override the lowercase conversion of a field name.
    def conform_field_names_csv(self, file_str, rename={}):
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

    # Converts all field names to lowercase
    # Optionally, rename can be set to replace a field names.
    def conform_field_names(self, file_list, rename={}):
        for i in range(len(file_list[1])):
            if file_list[1][i] in rename:
                file_list[1][i] = rename[file_list[1][i]]
            else:
                file_list[1][i] = file_list[1][i].lower()
        return file_list

    def csv_from_quoted_csv(self, file_str, current_delimiter=","):
        self.delimiter = ","
        file_list = self.list_from_csv_str(file_str)
        self.delimiter = '|'
        for row in file_list:
            for i in range(len(row)):
                row[i] = row[i].replace('"', '')
        return self.csv_str_from_list(file_list)

    # Creates a new, boolean field based on the value in another field.
    # Ex: An existing "toxicity" field can contain the values "Toxic" or
    # "Immunogenic". This fuction can create a new field named "Immunogenic"
    # and insert into it the value "True" in every record that contains the value
    # "Immunogenic" within the "toxicity" field.
    # params:
    #   file_list - a 2D list created from the csv
    #   source_field - the field in which the original value is located (Ex: toxicity)
    #   value - an existing value from within the field source_filed (Ex: Immunogenic)
    #   assume_false - assume the nonexistance of value to mean "False". If false, inserts "None"
    def create_bool_field_from_value(self, file_list, source_field, value, assume_false=False):
        # add value as new field
        file_list[1].append(value)
        index = file_list[1].index(source_field)

        for row in file_list[2:]:
            if row[index] == value:
                row.append(True)
            else:
                if assume_false:
                    row.append(False)
                else:
                    row.append(None)
        return file_list

    def remove_field(self, file_list, field):
        index = file_list[1].index(field)
        for row in file_list[1:]:
            del row[index]
        return file_list

    def remove_none_rows(self, file_list):
        for i in range(len(file_list)):
            if all(file_list[i]):
                del file_list[i]
        return file_list

    def remove_unwanted_fields(self, file_list, document_name):
        fields = list(file_list[1])
        for field in fields:
            if field not in definitions.collection_fields["peptide"]:
                file_list = self.remove_field(file_list, field)
        return file_list

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
