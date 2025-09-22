# Description

This README is intended to guide users on how to rebuild synonyms dictionary by combining Sudachi synonyms dictionary and custom synonyms for use in OpenSearch in Solr format.

# Guidelines

## Synonyms Dictionary
Synonyms are used to expand search queries to include similar terms. The synonyms dictionary is a text file that contains a list of synonyms, with each line containing a list of equivalent terms separated by commas. The synonyms dictionary is used to expand search queries to include similar terms.
<br>
The synonyms dictionary is built by combining Sudachi synonyms dictionary with custom synonyms.

### Updating Sudachi Synonyms Dictionary
1. Download the latest version of Sudachi synonyms dictionary from the [SudachiDict Repository](https://github.com/WorksApplications/SudachiDict/tree/develop/src/main/text).
2. Replace the `sudachi_synonyms.txt` file located in `/dict/`.  
   *(Last updated: 2024-12-18)*

### Updating Custom Synonyms
1. Add new custom synonyms to the `custom_synonyms.txt` file in `/dict/`.

### Rebuilding Synonyms Dictionary
**Note:** Ensure Python 3 and pip3 are installed before running the script.

To rebuild the synonyms dictionary, use the following command:
```bash
python3 ssyn2es.py -s sudachi_synonyms.txt -c custom_synonyms.txt -o output_synonyms.txt
```

- **Inputs:** `sudachi_synonyms.txt` (Sudachi synonyms) and `custom_synonyms.txt` (custom synonyms).
- **Output:** `output_synonyms.txt` (reformatted synonyms for Solr).  

You can modify the input and output file paths as needed according to your deployment configuration.

## Morphological Dictionary
Morphological dictionaries are used to analyze and tokenize text data. The morphological dictionary is a text file that contains a list of words and their corresponding readings and parts of speech. The morphological dictionary is used to analyze and tokenize text data.
<br>
The morphological dictionary uses Kuromoji tokenizer for morphological analysis and is built based on the format 
that Kuromoji tokenizer can read.

### Updating Custom Morphological Dictionary
Custom morphological dictionaries can be maintained in separate files for different environments:
- `prod_morphological.txt`: for production environment
- `dev_morphological.txt`: for development and staging environment
### Deploying (TBD)
