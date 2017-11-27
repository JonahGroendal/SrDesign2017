#import ml
from bson.objectid import ObjectId
import db
import definitions

'''
linear_svm = ml.LinearSVM()
linear_svm.get_input_data()
linear_svm.fit()
print(linear_svm.evaluate())
'''

d = db.PeptideDB()
print(d.is_valid_data(definitions.valid_data_def, definitions.collection_defs["source"]))
