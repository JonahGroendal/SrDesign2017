import definitions

class Scrub:
    def __init__(self):
        pass

    # Converts all field names of a formatted csv to lower case
    # Optionally, replace can be set to replace a field name.
    # replace can be used to override the lowercase conversion of a field name.
    def conform_field_names(self, file_str, replace={}):
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

    def convert_quoted_csv(self, file_str, current_delimiter=",", output_delimiter="|"):
        # replace comma with |
        new_contents = file_str.replace(current_delimiter, output_delimiter)
        # remove all quotes
        new_contents = new_contents.replace('"', '')

        return new_contents

class Inspect:
    def __init__(self):
        pass

    # Assumes field names are on second line of file
    # substring of file can be given as arugment
    def get_field_values(self, file_str, field_name, only_unique=False, delimiter="|"):
        field_index = self.get_field_index(file_str, field_name)
        lines = file_str.split("\n")
        values = []
        for line in lines:
            line_values = line.split(delimiter)
            if only_unique:
                if line_values[field_index] not in values:
                    values.append(line_values[field_index])
            else:
                values.append(line_values[field_index])
        return values

    # Assumes field names are on second line of file
    # substring of file can be given as arugment
    def get_field_index(self, file_str, field_name, delimiter="|"):
        lines = file_str.split("\n", 2)
        for line_count, line in enumerate(lines):
            if line_count == 1:
                fields = line.split(delimiter)
                for field_count, field in enumerate(fields):
                    if field == field_name:
                        return field_count
