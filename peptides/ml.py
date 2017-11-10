import tensorflow as tf
import numpy as np
import db

class LinearSVM:
    def __init__(self):
        self.input_data = {}
        self.input_data["x"] = {}
        self.input_data["y"] = []

        sequence_letters = []
        for i in range(20):
            sequence_letters.append(
                tf.contrib.layers.feature_column.sparse_column_with_keys(
                    "protein_{0}".format(i),
                    (' ', 'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V')))

        self.estimator = tf.contrib.learn.SVM(
            example_id_column='example_id',
            feature_columns=sequence_letters,
            l2_regularization=10.0)

    def fit(self):
        return self.estimator.fit(input_fn=self.input_fn_train, steps=50)

    def evaluate(self):
        return self.estimator.evaluate(input_fn=self.input_fn_eval, steps=50)

    def predict(self):
        return self.estimator.predict(input_fn=self.input_fn_eval)

    # Input builders
    def input_fn_train(self):
        split_index = int(len(self.input_data["y"]) * .5)
        labels = tf.constant(self.input_data["y"][:split_index], dtype=tf.bool)
        feature_cols = {}
        for key in self.input_data["x"]:
            feature_cols[key] = tf.constant(self.input_data["x"][key][:split_index], dtype=tf.string)
        #print("train_data:\n", self.input_data["x"])
        return feature_cols, labels

    def input_fn_eval(self):
        split_index = int(len(self.input_data["y"]) * .5) + 1
        labels = tf.constant(self.input_data["y"][split_index:], dtype=tf.bool)
        feature_cols = {}
        for key in self.input_data["x"]:
            feature_cols[key] = tf.constant(self.input_data["x"][key][split_index:], dtype=tf.string)
        #print("eval_data\n:", self.input_data["x"])
        return feature_cols, labels

    def get_input_data(self):
        self.input_data["x"]["example_id"] = []
        for count in range(50):
            self.input_data["x"]["protein_{0}".format(count)] = []

        dbo = db.PeptideDB()
        input_cursor = dbo.peptides.find({"toxic": {"$exists": True}}, {"sequence": True, "toxic": True})
        for cursor_doc in input_cursor:
            sequence = list(cursor_doc["sequence"])
            sequence_len = len(sequence)
            if sequence_len <= 50:
                # Insert spaces to make sequnce 50 chars long
                # Spaces bisect existing string
                for _ in range(50 - sequence_len):
                    sequence.insert(int(sequence_len/2), " ")
                # Create ID for example data
                example_id = hash(cursor_doc["_id"]) % 1000000000
                if example_id < 0:
                    example_id *= -1
                example_id = str(example_id)
                self.input_data["y"].append(cursor_doc["toxic"]["value"])
                self.input_data["x"]["example_id"].append(example_id)
                for count, letter in enumerate(sequence):
                    self.input_data["x"]["protein_{0}".format(count)].append(letter)
        print("true:", len([a for a in self.input_data["y"] if a is True]))
        print("false:", len([a for a in self.input_data["y"] if a is False]))
