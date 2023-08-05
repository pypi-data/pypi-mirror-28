#!/usr/bin/env python3

## Last update: 22/12/2017
## Author: T.F. Jesus
## This script runs MASH in plasmid databases.
## Note: each header in fasta is considered a reference

import argparse
import os
import operator
from subprocess import Popen, PIPE
import plotly
import plotly.graph_objs as go
import json
from multiprocessing import Pool
from functools import partial
import tqdm
try:
    from utils.args_limit import required_length
    from utils.mashscreen2json import mashscreen, sort_mash_screen, \
        screen2json
except ImportError:
    from mashwrapper.utils.args_limit import required_length
    from mashwrapper.utils.mashscreen2json import mashscreen, sort_mash_screen, \
        screen2json

## Checks if a directory exists and if not creates one.
def folderexist(directory):
    '''
    Checks if a folder exists or not and if it doesn't creates a new one.
    Parameters
    ----------
    directory: str
        A string with the path to the directory

    '''
    if not directory.endswith("/"):
        directory = directory + "/"
    if not os.path.exists(os.path.join(directory)):
        os.makedirs(os.path.join(directory))
        print(os.path.join(directory) + " does not exist. One will be "
                                        "created...")
    else:
        print(os.path.join(directory) + " exists!")


## Function to fix several issues that fasta header names can have with some
# programs
def header_fix(input_header):
    '''
    A function to fix Fasta headers for unwanted characters
    Parameters
    ----------
    input_header: str
        the actual string of the header to be fixed

    Returns
    -------
    input_header: str
        returns the fixed string with problematic characters replaced by "_"

    '''
    problematic_characters = ["|", " ", ",", ".", "(", ")", "'", "/", "[", "]",
                              ":", "{", "}"]
    for char in problematic_characters:
        input_header = input_header.replace(char, '_')
    return input_header


## Function to create a master fasta file from several fasta databases. One
# fasta is enought though
def master_fasta(fastas, output_tag):
    '''
    A function to concatenate all fastas to a main_fasta
    Parameters
    ----------
    fastas: list
        A list of all fasta files given as inputs to argparser
    output_tag: str
        The tag of the output file, used in many instances to attribute
        common names to files from the same run

    Returns
    -------
    : str
        A string with the full name of the file with all concatenated fastas

    '''
    master_fasta = open("master_fasta_" + output_tag + ".fas", "w")
    for filename in fastas:
        fasta = open(filename, "r")
        for line in fasta:
            if line.startswith(">"):
                line = header_fix(line)
            master_fasta.write(line)

    master_fasta.close()
    return "master_fasta_" + output_tag + ".fas"


## Makes the sketch command of mash for the reference
def sketch_references(inputfile, output_tag, threads, kmer_size):
    '''
    Function to make mash sketch for the references. This function is only
    executed when a new reference index is necessary. Usually users will
    provide a .msh file that already contains this index and this function
    will be skipped.
    Parameters
    ----------
    inputfile: str
        The name of the main fasta file
    output_tag: str
        The tag of the output file, used in many instances to attribute
        common names to files from the same run
    threads: str
        The number of threads to be used by mash
    kmer_size: str
        The kmer size to be used by mash

    Returns
    -------
    : str
        A string with the path to the index file .msh

    '''
    out_folder = os.path.join(os.path.dirname(os.path.abspath(inputfile)),
                              output_tag)
    out_file = os.path.join(out_folder, output_tag + "_reference")
    folderexist(out_folder)
    sketcher_command = ["mash",
                        "sketch",
                        "-o",
                        out_file,
                        "-k",
                        kmer_size,
                        "-p",
                        threads,
                        "-i",
                        inputfile]
    print("\nRunning mash sketch for references...\n")
    p = Popen(sketcher_command, stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    print(stderr)
    return out_file + ".msh"


## Makes the sketch command of mash for the reads to be compare to the reference.
## According to mash turorial it is useful to provide the -m 2 option in order
# to remove single-copy k-mers
def sketch_reads(read, mainpath, output_tag, threads, kmer_size):
    '''
    A function to make sketches of the reads provided before executing mash
    screen. Mash dist is not recommended to find existing plasmids contained in
    read files.
    This function will be run as many times as the input reads.
    Parameters
    ----------
    read: str
        the name of the read files
    mainpath: str
        The name of the main fasta file
    output_tag: str
        The tag of the output file, used in many instances to attribute
        common names to files from the same run
    threads: str
        The number of threads to be used by mash
    kmer_size: str
        The kmer size to be used by mash

    Returns
    -------
    : str
        The path to the .msh sketch file. Note that this function will be
        ran many times and many .msh files will be generated.

    '''
    out_file = os.path.join(mainpath, output_tag + "_" +
                            os.path.basename(read).split(".")[0])
    folderexist(output_tag)
    sketcher_command = ["mash",
                        "sketch",
                        "-o",
                        out_file,
                        "-k",
                        kmer_size,
                        "-p",
                        threads,
                        "-m",
                        "2",
                        "-r",
                        read]
    print
    print("Running mash sketch for reads...")
    print
    p = Popen(sketcher_command, stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    print(stderr)
    return out_file + ".msh"


## Makes the sketch command of mash for the reads to be compare to the reference.
## According to mash turorial it is useful to provide the -m 2 option in order
# to remove single-copy k-mers
def sketch_sequences(sequence, mainpath, output_tag, threads, kmer_size):
    '''
    Requires testing...
    Parameters
    ----------
    sequence
    mainpath
    output_tag
    threads
    kmer_size

    Returns
    -------

    '''
    out_file = os.path.join(mainpath, output_tag + "_" +
                            os.path.basename(sequence).split(".")[0])
    folderexist(mainpath)
    sketcher_command = ["mash",
                        "sketch",
                        "-o",
                        out_file,
                        "-k",
                        kmer_size,
                        "-p",
                        threads,
                        "-r",
                        sequence]
    print("\nRunning mash sketch for sequences...\n")
    p = Popen(sketcher_command, stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    print(stderr)
    return out_file + ".msh"


## Executes mash dist
def masher(ref_sketch, read_sketch, threads):
    '''
    Function that executes mash dist both for fastas and for reads. However,
    this is not really recommended for reads
    Parameters
    ----------
    ref_sketch: str
        The name of the reference sketch to be user in mash dist
    read_sketch: str
        The sketch of a read or sequence (Fasta) file name
    threads: str
        The number of threads to be used by mash dist

    Returns
    -------
    out_file_path: str
        The path to the output file

    '''
    out_folder = os.path.join(os.path.dirname(os.path.abspath(ref_sketch)))
    out_file = os.path.basename(read_sketch).split(".")[0] + "_distances.txt"
    out_file_path = os.path.join(out_folder, out_file)
    mash_command = "mash dist -p {} {} {} > {}".format(threads, ref_sketch,
                                                       read_sketch,
                                                       out_file_path)
    print("\n{}\n".format(mash_command))
    p = Popen(mash_command, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    stdout, stderr = p.communicate()
    print(stderr)
    return out_file_path

def masher_direct(ref_sketch, assembly, output_tag, threads):
    '''
    This function takes an assembly without sketching it a priori. Given that
    this is extremely fast, there is no need to sketch before running mash dist
    Parameters
    ----------
    ref_sketch: str
        file name for the reference sketch
    assembly: str
        file name for the fasta to be read
    output_tag: str
        The tag of the output file, used in many instances to attribute
        common names to files from the same run
    threads: str
        The number of threads to be used by mash dist

    Returns
    -------

    '''
    out_folder = os.path.join(os.path.dirname(os.path.abspath(assembly)),
                              output_tag)
    folderexist(out_folder)
    out_file = "{}_{}".format(os.path.basename(assembly),
                                 "_distances.txt")
    out_file_path = os.path.join(out_folder, out_file)
    mash_command = "mash dist -p {} {} {} > {}".format(threads, ref_sketch,
                                                       assembly,
                                                       out_file_path)

    print
    print(mash_command)
    print
    p = Popen(mash_command, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    stdout, stderr = p.communicate()
    print(stderr)
    return out_file_path

## Reads the output of mash dist and performes a barplot for each reads
def mashdist2graph(list_mash_files, tag):
    dist_dict = {}
    trace_list = []
    ## First reads mash output files and creates a sorted dictionary for each
    # file by mash distance (from highest to lowest values)
    for in_file in list_mash_files:
        dist_file = open(in_file, "r")
        for line in dist_file:
            tab_split = line.split("\t")
            reference_id = tab_split[0]
            query_id = tab_split[1].split("/")[-1].split(".")[0]
            mash_distance = tab_split[2]
            p_value = tab_split[3]
            if float(
                    p_value) < 0.05:  ## filters distances with no significant
                # p-values
                dist_dict[reference_id] = mash_distance
        ## Orders the dictionary from the minor distances to the major
        sorted_dist_dict = sorted(dist_dict.items(),
                                  key=operator.itemgetter(1))
        ## creates two lists to be given as the x and y for the bar plot
        global_reference = []
        global_values = []
        for k, v in sorted_dist_dict:
            if k not in global_reference:
                global_reference.append(k)
            global_values.append(1 - float(
                v))  # converts mash distances to mash "similarities", i.e.,
            # inverts the scale.
        trace = go.Bar(x=global_reference, y=global_values, name=query_id)
        trace_list.append(trace)

    ## Creates the plot itself
    layout = go.Layout(barmode="group", yaxis=dict(
        title="Mash distances (mutation rate between pairwise comparisons)"))
    fig = go.Figure(data=trace_list, layout=layout)
    plotly.offline.plot(fig, filename=tag + ".html",
                                   auto_open=False)

def json_dumping(mash_output, pvalue, mashdist, output_tag):
    out_file = open(
        os.path.join(output_tag, os.path.basename(mash_output) + ".json"),
        "w")
    input_f = open(mash_output, 'r')
    #temporary_list = []
    master_dict = {}
    for line in input_f:
        tab_split = line.split("\t")
        ref_accession = "_".join(tab_split[0].strip().split("_")[0:3])
        #seq_string = tab_split[1].split(".")[0].strip()
        mash_dist = tab_split[2].strip()
        p_value = tab_split[3].strip()
        ## there is no need to store all values since we are only interested in
        # representing the significant ones
        ## and those that correlate well with ANI (mashdist<=0.1)
        if float(p_value) < float(pvalue) and float(mash_dist) < float(mashdist):
            # temporary_list.append([ref_accession, mash_dist])
            master_dict[ref_accession] = 1 - float(mash_dist)
    # if temporary_list:
    #     master_dict[ref_accession] = temporary_list
        ## writes output json

    out_file.write(json.dumps(master_dict))
    out_file.close()

## calculates ths distances between pairwise genomes
## This function should be multiprocessed in order to retrieve several output
# files (as many as the specified cores specified?)
def mash_distance_matrix(list_mash_files, pvalue, mashdist, threads,
                         output_tag):
    # new mp module
    pool = Pool(int(threads))  # Create a multiprocessing Pool
    mp2 = pool.map(partial(multiprocess_mash_file, pvalue, mashdist),
                   list_mash_files)
    # process list_mash_files iterable with pool
    ## loop to print a nice progress bar
    try:
        for _ in tqdm.tqdm(mp2, total=len(list_mash_files)):
            pass
    except:
        print("progress will not be tracked because of 'reasons'... check if "
              "you have tqdm package installed.")
    pool.close()
    pool.join()  ## needed in order for the process to end before the remaining
    # options are triggered

    ## parse to output file the list
    output_file = open(output_tag + "mash_wrapper_results.txt", 'w')
    output_file.write("sequence\treference\tdistance\n")
    for sequence_list in mp2:
        output_file.write(sequence_list[-1])
        output_file.write("\t{}\t{}\n".format(sequence_list[0][0], sequence_list[0][1]))

    output_file.close()


def multiprocess_mash_file(pvalue, mashdist, in_folder):
    input_f = open(os.path.join(in_folder), 'r')
    temporary_list = []

    #  mash dist specified in each sequence/genome
    for line in input_f:
        tab_split = line.split("\t")
        ref = tab_split[0].strip()
        seq = tab_split[1].strip()
        mash_dist = tab_split[2].strip()
        p_value = tab_split[3].strip()

        if float(p_value) < float(pvalue) and ref != seq and float(
                mash_dist) < float(mashdist):
            temporary_list.append([ref, mash_dist])
    #print temporary_list
    temporary_list.append(seq)
    return temporary_list

def main():
    parser = argparse.ArgumentParser(
        description="Runs MASH using a database against sets of reads")
    mutual_parser = parser.add_mutually_exclusive_group()
    mutual_parser_2 = parser.add_mutually_exclusive_group()

    mutual_parser_2.add_argument("-i", "--input_references", dest="inputfile",
                                 nargs="+",
                                 help="Provide the input fasta files to "
                                      "parse. Not required for multiple "
                                      "comparisons between assemblies.")
    mutual_parser_2.add_argument("-rs", "--reference_sketch",
                                 dest="ref_sketch",
                                 help="If you have a reference sketch for "
                                      "references "
                                      "provide it with this option.")

    mutual_parser_2.add_argument("-rf", "--reference_fasta",
                                 dest="ref_fasta",
                                 help="If you have a reference fasta "
                                      "provide it with this option.")

    mutual_parser.add_argument("-r", "--reads", dest="reads", nargs="+",
                               action=required_length(1,2),
                               help="Provide the input read files to parse. "
                                    "Usually fastq 1 or 2 files. This option "
                                    "is mutually with '-f'.")  ## should implement a parser for a given directory with reads or a list file with all full path to each read library
    mutual_parser.add_argument("-f", "--sequences", dest="sequences",
                               nargs="+",
                               help="Provide the input sequence files to parse. "
                                    "Usually fasta files. This option is "
                                    "mutually exclusive with '-r'.")  ## should implement a parser for a given directory with reads or a list file with all full path to each read library
    mutual_parser.add_argument("-a", "--assemblies", dest="assemblies",
                               nargs="+",
                               help="Provide the input assemblies files to "
                                    "parse. "
                                    "Usually fasta files. This option is "
                                    "mutually exclusive with '-r'.")

    parser.add_argument("-o", "--output", dest="output_tag", required=True,
                        help="Provide an output tag")
    parser.add_argument("-t", "--threads", dest="threads",
                        help="Provide the number of threads to be used. "
                             "Default: 1")
    parser.add_argument("-no_rm", "--no-remove", dest="no_remove",
                        action="store_true",
                        help="Specify if you do not want to remove the output"
                             " concatenated fasta.")
    parser.add_argument("-j", "--json", dest="json", action="store_true",
                        help="If you desire to export a json file with all "
                             "significant entries use this options.")
    parser.add_argument("-m", "--mashix", dest="mashix", action="store_true",
                        help="Perform a matrix of all mash distance, taking "
                             "all files.")

    mash_options = parser.add_argument_group("MASH related options")
    mash_options.add_argument("-k", "--kmers", dest="kmer_size",
                              help="Provide the number of k-mers to be provided"
                                   " to mash sketch. Default: 21")
    mash_options.add_argument("-p", "--pvalue", dest="pvalue", default="0.05",
                              help="Provide the p-value to consider a distance"
                                   " significant. Default: 0.05.")
    mash_options.add_argument("-md", "--mashdist", dest="mashdistance",
                              default="0.1",
                              help="Provide the maximum mash distance to be"
                                   " parsed to the matrix. Default: 0.1.")
    ## mash screen related options
    mash_options.add_argument("-ms", "--mashscreen", dest="mashscreen",
                              action="store_true",
                              help="Runs mash screen. This will prevent mash "
                                   "dist to run.")
    mash_options.add_argument("-w", "--winner_takes_it_all", dest="winner",
                              action="store_true",
                              help="Uses the winner takes it all function to "
                                   "remove redundancy from mash screen "
                                   "results. NOTE: DO NOT USE FOR PLASMID ID!")
    mash_options.add_argument("-id", "--min_identity", dest="min_identity",
                              default="0.9", help="Provide the minimum "
                                                  "identity "
                                                "for mash screen run. Default "
                                                "is 0, reporting all values")

    args = parser.parse_args()

    pvalue = args.pvalue
    mashdist = args.mashdistance

    if args.threads is None:
        threads = "1"
    else:
        threads = args.threads
    if args.kmer_size is None:
        kmer_size = "21"
    else:
        kmer_size = args.kmer_size

    if args.inputfile:
        fastas = []
        for filename in args.inputfile:
            if any(x in filename for x in
                   [".fas", ".fasta", ".fna", ".fsa", ".fa"]):
                fastas.append(filename)

        main_fasta = master_fasta(fastas, args.output_tag)
        ref_sketch = sketch_references(main_fasta, args.output_tag, threads,
                                       kmer_size)
        mainpath = os.path.join(os.path.dirname(os.path.abspath(main_fasta)),
                                args.output_tag)
    elif args.ref_sketch:
        ref_sketch = args.ref_sketch
        mainpath = os.path.dirname(os.path.abspath(ref_sketch))

    elif args.ref_fasta:
        # TODO this is a wrapper to fix a problem with using msh file in
        # different machines, now it has to generate a sketch each time mach
        # runs for the input fastas
        ref_sketch = sketch_references(args.ref_fasta, args.output_tag,
                                       threads, kmer_size)
        mainpath = os.path.dirname(os.path.abspath(ref_sketch))

    else:
        print("Error no reference sketch or fasta was provided")

    list_mash_files = []

    ## checks if there are reads or sequences since different commands will be
    # parsed to mash depending on it
    if args.reads:
        ## used for reads
        if not args.mashscreen:
            for read in args.reads:
                read_sketch = sketch_reads(read, mainpath, args.output_tag,
                                           threads, kmer_size)
                mash_output = masher(ref_sketch, read_sketch, threads)
                ## parses distances.txt to json file
                if args.json:
                    json_dumping(mash_output, pvalue, mashdist, args.output_tag)

                list_mash_files.append(mash_output)
            mashdist2graph(list_mash_files, args.output_tag)
        else:
            #folderexist(mainpath) # checks main path
            screen_out_file = mashscreen(ref_sketch, args.output_tag,
                threads, pvalue, args.winner, args.min_identity, args.reads)
            mash_output = sort_mash_screen(screen_out_file)
            if args.json:
                screen2json(mash_output)
    ## TODO test if this code is still used
    elif args.sequences:
        ## used for sequences
        for sequence in args.sequences:
            if any(x in sequence for x in
                   [".fas", ".fasta", ".fna", ".fsa", ".fa"]):
                fastas.append(sequence)

            sequence_sketch = sketch_sequences(sequence, mainpath,
                                               args.output_tag, threads,
                                               kmer_size)
            mash_output = masher(ref_sketch, sequence_sketch, threads)
            ## parses distances.txt to json file
            if args.json:
                json_dumping(mash_output, pvalue, mashdist, args.output_tag)

            list_mash_files.append(mash_output)
        mashdist2graph(list_mash_files, args.output_tag)
    ## this is the statement executed to run fastas or plasmid assemblies in
    # mash dist
    elif args.assemblies:
        list_mash_files = []
        for assembly in args.assemblies:
            mash_output = masher_direct(ref_sketch, assembly, args.output_tag, threads)
            list_mash_files += mash_output
            if args.json:
                json_dumping(mash_output, pvalue, mashdist, args.output_tag)
    else:
        print("Error: Please provide a reads file (-r option) or a sequences "
              "file (-f option)")

    if args.mashix:
        mash_distance_matrix(list_mash_files, pvalue, mashdist, threads,
                             args.output_tag)

    ## remove master_fasta
    if not args.no_remove:
        try:
            os.remove(main_fasta)
        except:
            pass

if __name__ == "__main__":
    main()
