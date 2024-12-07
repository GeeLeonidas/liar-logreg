# SPDX-FileCopyrightText: 2024 Guilherme Leoi
#
# SPDX-License-Identifier: Apache-2.0

import traceback
from enum import IntEnum

import os
import pandas as pd
from zipfile import ZipFile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
    
from . import download_liar_dataset


class Status(IntEnum):
    OK = 0
    ERROR = 1


def main() -> Status:
    try:
        if not os.path.isfile("./liar_dataset.zip"):
            download_liar_dataset()
        zipped_dataset = ZipFile("./liar_dataset.zip")
        liar_column_names = [
            "statement id",
            "label",
            "statement",
            "subject",
            "speaker",
            "job title",
            "state info",
            "affiliation",
            "barely true count",
            "false count",
            "half true count",
            "mostly true count",
            "pants on fire count",
            "context"
        ]
        dataset = {
            zipped_file.filename:
                pd.read_csv(zipped_dataset.open(zipped_file.filename), names=liar_column_names, sep='\t')
            for zipped_file in zipped_dataset.infolist()
            if zipped_file.filename.endswith(".tsv")
        }
        
        train_df = dataset["train.tsv"]
        test_df = dataset["test.tsv"]
        valid_df = dataset["valid.tsv"]
                
        tf_idf = TfidfVectorizer() \
            .fit(train_df["statement"]) \
            .fit(test_df["statement"]) \
            .fit(valid_df["statement"])
        le = LabelEncoder() \
            .fit(train_df["label"]) \
            .fit(test_df["label"]) \
            .fit(valid_df["label"])
        
        X_train = tf_idf.transform(train_df["statement"])
        y_train = le.transform(train_df["label"])
        X_test = tf_idf.transform(test_df["statement"])
        y_test = le.transform(test_df["label"])
        X_valid = tf_idf.transform(valid_df["statement"])
        y_valid = le.transform(valid_df["label"])
        
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        y_train_pred = model.predict(X_train)
        train_score = accuracy_score(y_train, y_train_pred)
        print(f"Train score: {train_score*100:.1f}%")
        y_test_pred = model.predict(X_test)
        test_score = accuracy_score(y_test, y_test_pred)
        print(f"Test score: {test_score*100:.1f}%")
        y_valid_pred = model.predict(X_valid)
        valid_score = accuracy_score(y_valid, y_valid_pred)
        print(f"Validation score: {valid_score*100:.1f}%")
        
        labels = le.inverse_transform(list(range(6)))
        conf_matrix = pd.DataFrame(confusion_matrix(y_test, y_test_pred), columns=labels, index=labels)
        print(conf_matrix)
        
        for label in labels:
            correct = conf_matrix[label][label]
            predicted = sum(conf_matrix[label])
            print(f"'{label}' score: {100*correct/predicted:.1f}%")
        
        return Status.OK
    except:
        traceback.print_exc()
        return Status.ERROR


if __name__ == "__main__":
    import sys
    sys.exit(main())
