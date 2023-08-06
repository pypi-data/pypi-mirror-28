[![Build status](https://travis-ci.org/OLC-LOC-Bioinformatics/GenomeQAML.svg?master)](https://travis-ci.org/OLC-LOC-Bioinformatics)
# GenomeQAML: Genome Quality Assesment with Machine Learning

The GenomeQAML is a script that uses a pre-computed ExtraTreesClassifier model in order to 
classify FASTA-formatted _de novo_ assemblies as bad, good, or very good. It's easy to use,
and has minimal dependencies.

## External Dependencies

- [Mash (v2.0 or greater)](https://github.com/marbl/mash)
- [Prodigal (>=2.6.2)](https://github.com/hyattpd/Prodigal)

Both of these need to be downloaded and included on your $PATH.

## Installation

All you need to do is install with pip: `pip install genomeqaml`. 

Usage of a virtualenv
is highly recommended.

## Usage

GenomeQAML takes a directory containing uncompressed fasta files as input - these will be classified and a
 report written to a CSV-formatted file for your inspection.

To run, type `classify.py -t /path/to/fasta/folder`

This will create a report, by default called `QAMLreport.csv`. You can change the name 
of the report with the `-r` argument.

```
usage: classify.py [-h] -t TEST_FOLDER [-r REPORT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -t TEST_FOLDER, --test_folder TEST_FOLDER
                        Path to folder containing FASTA files you want to
                        test.
  -r REPORT_FILE, --report_file REPORT_FILE
                        Name of output file. Default is QAMLreport.csv.

```