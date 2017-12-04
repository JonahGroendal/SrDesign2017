__author__ = "Jonah Groendal"

class PeptidesError(Exception):
    ''' base exception for this project '''
    pass

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
    ''' Raised when a document being inserted doesn't conform to its data schema. '''
    def __init__(self, definition, document):
        self.definition = definition
        self.document = document
        super().__init__(
            ("Document being inserted is invalid with respect to its data schema"
                ". Insert was aborted.\n    definition: {0}"
                "\n    document: {1}\n").format(self.definition, self.document)
        )
