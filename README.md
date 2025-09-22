# Description

This README is intended to guide users on how to rebuild synonyms dictionary by combining Sudachi synonyms dictionary and custom synonyms for use in OpenSearch in Solr format.

# Guidelines

## Synonyms Dictionary
Synonyms are used to expand search queries to include similar terms. The synonyms dictionary is a text file that contains a list of synonyms, with each line containing a list of equivalent terms separated by commas. The synonyms dictionary is used to expand search queries to include similar terms.
<br>

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
python3 ssyn2es.py -s sudachi_synonyms.txt -c custom_synonyms.txt -o custom_synonyms.txt
```

- **Inputs:** `sudachi_synonyms.txt` (Sudachi synonyms) and `custom_synonyms.txt` (custom synonyms).
- **Output:** `custom_synonyms.txt` (reformatted synonyms for Solr).  

You can modify the input and output file paths as needed. However, remember that these paths are configured in the `docker-compose.yml` file. If you change the file paths, be sure to update the `docker-compose.yml` file accordingly.

## Morphological Dictionary
Morphological dictionaries are used to analyze and tokenize text data. The morphological dictionary is a text file that contains a list of words and their corresponding readings and parts of speech. The morphological dictionary is used to analyze and tokenize text data.
<br>
Kuromoji tokenizer for morphological analysis. And morphological dictionary is built base on Solr format 
that Kuromoji tokenizer can read.
### Deploying (TBD)
