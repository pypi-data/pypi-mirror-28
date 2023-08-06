#!/usr/bin/env python
import os
import pickle
import argparse
import pandas as pd
from genomeqaml import extract_features


def classify_data(model, test_folder, refseq_database, report_file):
    # Extract features from the training folder.
    if not os.path.isfile(os.path.join(test_folder, 'extracted_features.csv')):
        print('Extracting features!')
        extract_features.main(sequencepath=test_folder,
                              report=True,
                              refseq_database=refseq_database)
    test_df = pd.read_csv(os.path.join(test_folder, 'extracted_features.csv'))
    dataframe = pd.get_dummies(test_df, columns=['Genus'], dummy_na=True)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    df = pickle.load(open(current_dir + '/../dataframe.p', 'rb'))
    training_dataframe = pd.get_dummies(df, columns=['Genus'], dummy_na=True)
    for column in dataframe:
        if column not in training_dataframe:
            dataframe.drop(column, axis=1, inplace=True)
    # Add any genera that weren't in our test set but were in the training set.
    for column in training_dataframe:
        if 'Genus' in column and column not in dataframe:
            not_present = [0] * len(dataframe)
            dataframe[column] = not_present
    # Then, add any features that were part of training data but not part of test data
    features = list(dataframe.columns[1:len(dataframe.columns)])
    x = dataframe[features]
    result = model.predict(x)
    probabilities = model.predict_proba(x)
    for i in range(len(result)):
        if result[i] == 0:
            output = 'Fail'
        elif result[i] == 1:
            output = 'Pass'
        elif result[i] == 2:
            output = 'Reference'
        fail_prob = '%.2f' % round(probabilities[i][0] * 100.0, 2)
        pass_prob = '%.2f' % round(probabilities[i][1] * 100.0, 2)
        ref_prob = '%.2f' % round(probabilities[i][2] * 100.0, 2)
        with open(report_file, 'a+') as f:
            f.write(test_df['SampleName'][i] + ',' + output + ',' + fail_prob + ',' + pass_prob + ',' + ref_prob + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test_folder',
                        type=str,
                        required=True,
                        help='Path to folder containing FASTA files you want to test.')
    parser.add_argument('-r', '--report_file',
                        type=str,
                        default='QAMLreport.csv',
                        help='Name of output file. Default is QAMLreport.csv.')
    args = parser.parse_args()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    model = pickle.load(open(current_dir + '/../model.p', 'rb'))
    with open(args.report_file, 'w') as f:
        f.write('Sample,Predicted_Class,Percent_Fail,Percent_Pass,Percent_Ref\n')
    classify_data(model, args.test_folder, current_dir + '/../refseq.msh', args.report_file)
    print('Classification complete! Results can be found in {}'.format(args.report_file))
