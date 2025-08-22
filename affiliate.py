#!/usr/bin/env python3
"""Number affiliations for each author, given an author list with affiliations
for each author."""

import argparse
from collections import OrderedDict

__author__ = 'Hayden Metsky <hayden@mit.edu>'


def read_authors(fn):
    """Read list of authors and shortcuts of their affiliations.

    Args:
        fn: path to file with two columns in which each line corresponds
            to an author; column 1 gives the author's name and column
            2 gives a comma-separated list of shorthand names of their
            affiliations

    Returns:
        ordered dict {author name: list of shorthands for affiliations},
        where the order of authors is the same as in the given file
    """
    authors = OrderedDict()
    with open(fn) as f:
        for line in f:
            author, affiliations = line.strip().split('\t')
            affiliations = [s.strip() for s in affiliations.split(',')]
            authors[author] = affiliations
    return authors


def read_affiliations(fn):
    """Read list of full names of affiliations.

    Args:
        fn: path to file with two columns in which each line corresponds
            to an affiliation; column 1 gives a shorthand name for the
            affiliation (assigned to authors) and column 2 gives the
            full name of the affiliation

    Returns:
        dict {shorthand for affiliation: full name of affiliation}
    """
    affiliations = {}
    attributes = OrderedDict()
    with open(fn) as f:
        for line in f:
            shorthand, fullname = line.rstrip().split('\t')
            if len(shorthand)>1:
                affiliations[shorthand] = fullname
            else:
                attributes[shorthand] = fullname
    return affiliations,attributes


def main(args):
    # Read input
    authors = read_authors(args.authors)
    affiliations,attributes = read_affiliations(args.affiliations)

    print(f"affiliations {affiliations}\n")
    print(f"attributes {attributes}\n")

    # unique affiliations, to later remove those not used for any authors
    affiliations_in_use = set()
    # Verify that each author's affiliation has a name
    for author in authors:
        for affiliation in authors[author]:
            if affiliation not in list(affiliations.keys())+list(attributes.keys()):
                raise Exception(("Author %s has affiliation %s but the "
                    "name of that affiliation was not given") % (author,
                    affiliation))
            else:
                affiliations_in_use |= set([affiliation])

    print(f"affiliations_in_use {affiliations_in_use}\n")

    affiliations_to_remove = set(list(affiliations.keys())) - affiliations_in_use
    for affiliation_to_remove in affiliations_to_remove:
        del affiliations[affiliation_to_remove]

    

    [authors[author]]

    # Order affiliations according to the author order
    affiliations_number = {}
    attributes_number = {}
    curr_num = 1
    attribute_num = 1
    for author_num,author in enumerate(authors):
        for affiliation in authors[author]:
            if affiliation not in affiliations_number:
                if len(affiliation)>1:
                    affiliations_number[affiliation] = curr_num
                    curr_num += 1
                else :
                    #affiliations_number[affiliation] = author_num
                    #attributes_number[affiliation] = author_num
                    attributes_number[affiliation] = attribute_num
                    attribute_num += 1
    #affiliations_ordered = sorted(list(affiliations.keys()),
    #    key=lambda x: affiliations_number[x])

    affiliations_ordered = sorted(list(affiliations.keys()),
        key=lambda x: affiliations_number[x])

    attributes_ordered = sorted(list(attributes.keys()),
        key=lambda x: attributes_number[x])

    attributes_ordered = list(attributes.keys())

    print(f"affiliations_ordered {affiliations_ordered}")
    print(f"attributes_ordered {attributes_ordered}")

    #affiliations_ordered = sorted(list(affiliations.keys()),
    #    key=lambda x: affiliations_number[x] if len(x)>1 else 1000+ord(x))

    # Generate HTML and LaTeX of authors with their affiliations numbered
    author_html = ''
    author_latex = ''
    for i, author in enumerate(authors):
        #numbers = [affiliations_number[x] for x in authors[author]]
        numbers = [affiliations_number[x] for x in [y for y in authors[author] if y not in attributes_number.keys()]]
        #numbers = [affiliations_number[x] for x in authors[author] if authors[author] in affiliations_number.keys() and type(affiliations_number[x])!=str]
        non_numbers = [x for x in [y for y in authors[author] if y in attributes_number.keys()]]
        #numbers_str = ','.join([str(x) for x in sorted(numbers)]+non_numbers)
        numbers_str = ','.join(
                                [str(x) for x in sorted(numbers)] + 
                                    [str(y) for y in sorted(non_numbers, key=lambda w: attributes_number[w])] )
        #print(f"numbers_str {numbers_str}")
        #print(f"non_numbers {non_numbers}")
        if i > 0:
            author_html += ', '
            author_latex += ',\n'

        author_html += author + '<sup>' + numbers_str + '</sup>'

        # For LaTeX, put an mbox around the last name and another around
        # everything before the last name, so that neither of these two
        # pieces are split with a line break
        author_split = author.split(' ')
        author_mbox = ('\mbox{' + ' '.join(author_split[:-1]) + '} ' +
            '\mbox{' + author_split[-1] + '}')
        author_latex += author_mbox + '$^{' + numbers_str + '}$'
    author_latex += '\n'

    # Generate HTML and LaTeX of affiliations with their full names
    affiliations_html = ''
    attributes_html = ''
    affiliations_latex = ''
    attributes_latex = ''
    for i, affiliation in enumerate(affiliations_ordered):
        number = str(affiliations_number[affiliation])
        fullname = affiliations[affiliation]
        if i > 0:
            affiliations_html += ' '

        affiliations_html += '<sup>' + number + '</sup>' + fullname + '.'
        affiliations_latex += '$^{' + number + '}$' + fullname + '.\n'

    for i, attribute in enumerate(attributes_ordered):
        symbol = attribute#str(attributes_number[attribute])
        fullname = attributes[attribute]
        if i > 0:
            attributes_html += ' '

        attributes_html += '<sup>' + symbol + '</sup>' + fullname + '.'
        attributes_latex += '$^{' + symbol + '}$' + fullname + '.\n'

        

    # Write HTML
    with open(args.out_html, 'w') as f:
        f.write(author_html)
        f.write('<br><br>')
        f.write(affiliations_html)
        f.write(attributes_html)

    # Write LaTeX if desired
    if args.out_latex:
        with open(args.out_latex, 'w') as f:
            f.write('%%%%%%%%%%%%%%%%%%%%%\n')
            f.write('%% LIST OF AUTHORS %%\n')
            f.write('%%%%%%%%%%%%%%%%%%%%%\n')
            f.write(author_latex)
            f.write('%%%%%%%%%%%%%%%%%%%%%\n')
            f.write('\n\n')
            f.write('%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
            f.write('%% LIST OF AFFILIATIONS %%\n')
            f.write('%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
            f.write(affiliations_latex)
            f.write(attributes_latex)
            f.write('%%%%%%%%%%%%%%%%%%%%%%%%%%\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('authors',
        help=("Path to file in which each line corresponds to an author "
              "(ordered as desired) and there are 2 columns: column 1 "
              "gives the full name of the author and column 2 gives a "
              "shorthand for the author's affiliation"))
    parser.add_argument('affiliations',
        help=("Path to file in which each line corresponds to an affiliation "
              "and there are 2 columns: column 1 gives a shorthand for an "
              "affiliation and column 2 gives the full name of the "
              "affiliation"))
    parser.add_argument('out_html',
        help=("Path to output HTML file that gives an author list with "
              "numbered affiliations"))
    parser.add_argument('--out-latex',
        help=("Path to output tex file that gives an author list with "
              "numbered affiliations"))

    args = parser.parse_args()
    main(args)
