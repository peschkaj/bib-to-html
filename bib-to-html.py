# bib-to-html - transforms a BibTex file into an HTML file using a 
# template and simple string replacement
# Copyright (C) 2017 Jeremiah Peschka <jpeschka@pdx.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import bibtexparser
import sys


def load_records(filename):
    """Loads BibTex records from filename and puts them into a common format 
    as a Python dict"""
    with open(filename) as summary:
        bibtex_str = summary.read()

    db = bibtexparser.loads(bibtex_str)

    years = {}

    for e in db.entries:
        y = e['year']
        if y not in years:
            years[y] = list()

        # Construct a dictionary item
        link = {'author': e['author'],
                'title': e['title']
                }

        if 'journal' in e:
            link['publication'] = e['journal']
        elif 'booktitle' in e:
            link['publication'] = e['booktitle']

        if 'url' in e:
            link['url'] = e['url']
        else:
            link['url'] = "https://dx.doi.org/%s" % (e['doi'])

        years[y].append(link)

    return years


def lists_to_html(lists, template_file, output_directory):
    """Converts a list of dictionary entries to a valid HTML page
    It's assumed that the template file will contain $THE_YEAR$ and $THE_LIST$ as strings to be replaced.
    """

    sorted_keys = sorted(lists.keys())

    with open(template_file) as template:
        template_str = template.read()

    for year in sorted_keys:
        contents = template_str.replace("$THE_YEAR$", year)
        html_list = "<ul>"

        sorted_entries = sorted(lists[year], key=lambda e: e['author'])

        for entry in sorted_entries:
            html_list += "<li><a href='%s'>%s</a> (%s) <i>%s</i></a></li>\n" % (
                entry['url'], entry['title'], entry['author'], entry['publication'])

        contents = contents.replace("$THE_LIST$", html_list)

        output_file_name = os.path.join(output_directory, "Literature%s.html" % year)
        print("Writing to " + output_file_name)

        with open(output_file_name, 'w') as f:
            f.write(contents)


def main(summary_file, template_file, output_directory):
    """The main method"""
    years = load_records(summary_file)
    lists_to_html(years, template_file, output_directory)


if __name__ == '__main__':
    argc = len(sys.argv)

    try:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "/?":
            print("Usage: python bib-to-html.py references.bib template.html /output/directory")
            exit(0)
    except IndexError:
        pass

    try:
        BIBTEX_LOCATION = sys.argv[1]
    except IndexError:
        BIBTEX_LOCATION = "summary.bib"

    try:
        TEMPLATE_FILE = sys.argv[2]
    except IndexError:
        TEMPLATE_FILE = "template.html"

    try:
        OUTPUT_FOLDER = sys.argv[3]
    except IndexError:
        OUTPUT_FOLDER = "."

    main(BIBTEX_LOCATION, TEMPLATE_FILE, OUTPUT_FOLDER)
