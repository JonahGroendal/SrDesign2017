__author__ = "Jonah Groendal"

class PeptidesError(Exception):
    ''' base exception for this project '''
    pass

class UndefinedFieldError(PeptidesError):
    ''' raised when a collections field value is reference but it isn't defined in definitions.py'''
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__("field '{0}' not defined".format(field_name))

class ConflictingUpdateError(PeptidesError):
    ''' Raised when updating a document reveals conflicing field values. '''
    def __init__(self, existing_document, conflicting_document):
        self.existing_document = existing_document
        self.conflicting_document = conflicting_document
        super().__init__(
            ("Field value of document in database conflicts with "
            "field value of document being inserted\n    existing document: {0}"
            "\n    conflicing document: {1}").format(existing_document, conflicting_document)
        )

class ViolationOfDefinedConstraintError(PeptidesError):
    ''' Raised when a document being inserted doesn't conform to its spec (in definitions.py). '''
    def __init__(self, invalid_value_definition, document):
        self.invalid_value_definition = invalid_value_definition
        self.document = document
        super().__init__(
            ("Document being inserted doesn't conform to its spec"
            " (in definitions.py). Insert was aborted.\n    invalid_value_definition: {0}"
            "\n    document: {1}\n").format(self.invalid_value_definition, self.document)
        )
