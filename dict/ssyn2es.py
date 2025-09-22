#!/usr/bin/env python
# This file base on the original script from elasticsearch-sudachi repo: https://github.com/WorksApplications/elasticsearch-sudachi/blob/develop/docs/ssyn2es.py
# Which modified to remove punctuations and symbols from the output to be used in kuromoji plugin
# Along with combine with custom dictionary in Solr format
import argparse
import fileinput
import unicodedata

# Check if the string is a symbol or punctuation
def is_symbol_or_punctuation(s):
    return all(unicodedata.category(c).startswith(('S', 'P')) for c in s)

# read Sudachi synonyms and output them in solr format
def process_sudachi_synonyms(files, output_predicate):
    synonyms = {}
    with fileinput.input(files=files) as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            entry = line.split(",")[0:9]
            # entry[2] is the type of the word that used as a deletion history to prevent harmful words, etc)
            # entry[1] is the type of the word that used as a predicate(用言)
            # Skip if the entry is a deletion history or not allowed predicate
            if entry[2] == "2" or (not output_predicate and entry[1] == "2"):
                continue
            # Skip if the entry is a symbol or punctuation
            # This is to make sure the output is compatible with kuromoji plugin
            # entry[8] is the value of the word
            if is_symbol_or_punctuation(entry[8]):
                continue
            # entry[0] is the synonym group id
            group = synonyms.setdefault(entry[0], [[], []])
            # If the entry is a synonym word, add it to the second group
            # entry[2] is the type of the word
            # 0 is for determine that the word is a original word, 1 is for synonym word
            group[1 if entry[2] == "1" else 0].append(entry[8])

    output = []
    for groupid in sorted(synonyms):
        group = synonyms[groupid]
        if not group[1]:
            if len(group[0]) > 1:
                output.append(",".join(group[0]))
        else:
            # In case if the group has both original and synonym words
            # Its mean the group is a synonym group have explicit mappings
            if len(group[0]) > 0 and len(group[1]) > 0:
                output.append(",".join(group[0]) + "=>" + ",".join(group[0] + group[1]))
    return output

# read Solr dictionary and output them in solr format
def process_solr_dictionary(files):
    output = []
    with fileinput.input(files=files) as input:
        for line in input:
            line = line.strip()
            if line:
                output.append(line)
    return output

def main():
    parser = argparse.ArgumentParser(prog="ssyn2es.py", description="Convert and merge synonym files to desired format")
    parser.add_argument('files', metavar='FILE', nargs='*', help='Files to read, if empty, stdin is used')
    parser.add_argument('-p', '--output-predicate', action='store_true', help='Output predicates for Sudachi synonyms')
    parser.add_argument('-c', '--custom-dictionary', metavar='CUSTOM_DICT', help='Custom dictionary in Solr format')
    parser.add_argument('-s', '--sudachi-synonyms', metavar='SUDA_SYN', help='Sudachi synonym file')
    parser.add_argument('-o', '--output', metavar='OUTPUT', required=True, help='Output file to write the final combined dictionary')
    args = parser.parse_args()

    # Sudachi synnonym is the backbone of the dictionary
    # So it must be provided
    if not args.sudachi_synonyms:
        parser.error("You must specify a Sudachi synonym file with -s.")

    # Process Sudachi synonyms to Solr format
    print("Processing Sudachi synonyms...")
    sudachi_data = process_sudachi_synonyms([args.sudachi_synonyms], args.output_predicate)

    # Process custom dictionary if provided
    custom_data = []
    if args.custom_dictionary:
        print("Processing custom dictionary...")
        custom_data = process_solr_dictionary([args.custom_dictionary])

    # Combine both dictionaries
    final_data = sudachi_data + custom_data

    # Write to output
    with open(args.output, 'w', encoding='utf-8') as f:
        for line in final_data:
            f.write(line + "\n")

    print(f"Final dictionary written to {args.output}")

if __name__ == "__main__":
    main()
