# bib-to-html

Translates bibtex files into an unordered HTML list and dumps them into an HTML template page

## Basic Usage

`python bib-to-html.py`

Reads bibliography entries from `summary.bib` in the current directory
and transforms them into a series of HTML files, one per year, based on
the format of `template.html` (also in the current directory). The
files will be named `LiteratureYEAR.html`.

## Moderately Less Basic Usage

`python bib-to-html.py BIBTEX_FILE TEMPLATE_FILE OUTPUT_FOLDER`

You can probably guess that:

* The bibliography is read from `BIBTEX_FILE`
* The template is located in `TEMPLATE_FILE`