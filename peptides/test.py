#import ml
from bson.objectid import ObjectId
import db

'''
linear_svm = ml.LinearSVM()
linear_svm.get_input_data()
linear_svm.fit()
print(linear_svm.evaluate())
'''

d = db.PeptideDB()
p = d.peptides.find({"sequence": "GLGSLLGKAFKFGLKTVGKMMGGAPREE"})

for s in p:
    print(s)
