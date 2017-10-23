class PeptidesError(Exception):
    ''' base exception for this project '''
    pass

class UndefinedFieldError(PeptidesError):
    ''' raised when a collections field value is reference but it isn't defined in definitions.py'''
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__("field '{0}' not defined".format(field_name))

class ConflictingUpdateError(PeptidesError):
    ''' raised when updating a document reveals conflicing field values '''
    def __init__(self, existing_document, conflicting_document):
        self.existing_document = existing_document
        self.conflicting_document = conflicting_document
        super().__init__(("Field value of document in database conflicts with "
                "field value of document being inserted. existing document: {0}"
                " conflicing document: {1}").format(existing_document, conflicting_document))
