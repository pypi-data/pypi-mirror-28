################
bgparsers
################

Variants reader
---------------

BgParsers Variant Reader can read in an uniform way different variant input file formats. And you'll get,
if it's possible, always the same fields with the same syntax and format.

The processed fields are:

* **CHROMOSME**: Returns the chromosome as an uppercase string, always without "CHR" prefix. Ex: "X", "Y", "10"
* **POSITION**: The variant position as an **integer** value.
* **STRAND**: The strand. Possible values: **"-"**, **"+"** or **None** if unknown
* **REF**: The reference sequence.
* **ALT**: The alternate sequence.
* **SAMPLE**: Sample identifier.
* **DONOR**: Donor identifier.
* **ALT_TYPE**: Alteration type. Possible values: **snp**, **mnp**, **indel**

If the input file has the extension **gz**, **bgz** or **xz** it will be automatically uncompressed.

Usage example:

.. code-block:: python

   from bgparsers import readers

   for file in ['myvars.maf', 'myvars.vcf', 'myvars.vcf.gz', 'myvars.tsv.xz']:
       for r in readers.variants(file):
           chrom, ref, alt, pos = r['CHROMOSOME'], r['REF'], r['ALT'], r['POSITION']



License
-------

`LICENSE <LICENSE.txt>`_.