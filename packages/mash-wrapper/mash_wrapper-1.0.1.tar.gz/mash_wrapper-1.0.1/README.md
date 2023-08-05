# mash_wrapper.py

## About

mash_wrapper.py is a script that is intended to allow users to use mash plasmid 
database (provided in indexes folder) . It provides options to run mash dist 
as well as mash screen with different purposes. While `mash dist` is 
used to calculate the similarities of any sequence with the existing plasmids
 in database, `mash screen` is used to check if any of the existing plasmid 
 might be present in the provided reads. So, basically, this script features 
 two different ways to check the presence of plasmids both in sequences (Fasta) 
 and in reads (FastQ). Then, the resulting `*.json` files can be imported in 
 [pATLAS](http://www.patlas.site).

## Installation

* Download [release 1.0.0 - popcorns & unicorns](https://github.com/tiagofilipe12/mash_wrapper/releases/tag/v1.0.0)
(don't forget to download [index file](https://github.com/tiagofilipe12/mash_wrapper/releases/download/v1.0.0/assembly_reference.msh), 
that is used to run this script).

* Download [mash 2.0.0](https://github.com/marbl/Mash/releases/tag/v2.0)

* `pip3 install -r requirements.txt`

## How to run

### Assembly or fasta comparison

`mash_wrapper.py -rs <assembly_reference.msh> -a <your_fasta> -j -o 
<tyour_output_folder>`

### Mash screen for read samples

`mash_wrapper.py -rs assembly_reference.msh -r <read(s)> -o <output_name> 
-t <number_of_threads> -j -ms`

## What is mash_wrapper.py

This script runs MASH in plasmid databases, using `mash dist` and `mash screen`

Note: each header in fasta is considered a reference ('-i' option of mash).

### Options:

```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE [INPUTFILE ...], --input_references INPUTFILE [INPUTFILE ...]
                        Provide the input fasta files to parse. Not required
                        for multiple comparisons between assemblies.
  -rs REF_SKETCH, --reference_sketch REF_SKETCH
                        If you have a reference sketch for references provide
                        it with this option.
  -r READS [READS ...], --reads READS [READS ...]
                        Provide the input read files to parse. Usually fastq 1
                        or 2 files. This option is mutually with "-f".
  -f SEQUENCES [SEQUENCES ...], --sequences SEQUENCES [SEQUENCES ...]
                        Provide the input sequence files to parse. Usually
                        fasta files. This option is mutually exclusive with
                        "-r".
  -o OUTPUT_TAG, --output OUTPUT_TAG
                        Provide an output tag
  -t THREADS, --threads THREADS
                        Provide the number of threads to be used. Default: 1
  -no_rm, --no-remove   Specify if you do not want to remove the output
                        concatenated fasta.
  -j, --json            If you desire to export a json file with all
                        significant entries use this options.
  -m, --mashix          Perform a matrix of all mash distance, taking all
                        files.

MASH related options:
  -k KMER_SIZE, --kmers KMER_SIZE
                        Provide the number of k-mers to be provided to mash
                        sketch. Default: 21
  -p PVALUE, --pvalue PVALUE
                        Provide the p-value to consider a distance
                        significant. Default: 0.05.
  -md MASHDISTANCE, --mashdist MASHDISTANCE
                        Provide the maximum mash distance to be parsed to the
                        matrix. Default: 0.1.
  -ms, --mashscreen     Runs mash screen. This will prevent mash dist to run.
  -w, --winner_takes_it_all
                        Uses the winner takes it all function to remove
                        redundancy from mash screen results. NOTE: DO NOT USE
                        FOR PLASMID ID!
  -id MIN_IDENTITY, --min_identity MIN_IDENTITY
                        Provide the minimum identity for mash screen run.
                        Default is 0, reporting all values
```

---

#### Outputs:


* A **text** file with MASH distance outputs as well as .msh files for each input read file.

* A **html** file with a bar plot graphical visualization, with each input read file as a series of data.

* A **json** file that can be imported in [pATLAS](www.patlas.site).

