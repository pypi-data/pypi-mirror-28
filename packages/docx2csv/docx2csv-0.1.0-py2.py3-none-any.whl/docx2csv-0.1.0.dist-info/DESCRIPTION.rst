```
Usage: docx2csv [OPTIONS] FILENAME

  docx to csv convertor (http://github.com/ivbeg/docx2csv)
  Extracts tables from DOCX files as CSV or XLSX.

  Use command: "docx2csv convert <filename>" to run extraction. It will
  create files like filename_1.csv, filename_2.csv for each table found.

Options:
  --format TEXT         Output format: CSV, XLSX
  --singlefile TEXT     Outputs single XLS file with multiple sheets: True or False
  --sizefilter INTEGER  Filters table by size number of rows
  --help                Show this message and exit.
```
## Examples

docx2csv --format csv --sizefilter 3 CP_CONTRACT_160166.docx

Extracts tables from file CP_CONTRACT_160166.docx with number of rows > 3 and
saves results as CSV files.

##Requirements
* click https://github.com/pallets/click
* xlwt https://github.com/python-excel/xlwt
* python-docx https://github.com/python-openxml/python-docx
* openpyxl https://bitbucket.org/openpyxl/openpyxl/src


## Acknowledgements
Thanks to Vsevolod Oparin (https://www.facebook.com/vsevolod.oparin) for optimized "extract_table" code


.. :changelog:

History
=======


0.1.0 (2018-01-14)
------------------
* First public release on PyPI and updated github code


