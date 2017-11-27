'''
import ml

linear_svm = ml.LinearSVM()
linear_svm.get_input_data()
linear_svm.fit()
print(linear_svm.evaluate())
'''

import db
import definitions

d = db.PeptideDB()
a = d.peptides.find_one()
print(a["immunogenic"])
print(d.adheres_to_defined_constraints(definitions.collection_peptide["document_def"]["immunogenic"], a["immunogenic"]))
