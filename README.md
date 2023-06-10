[![PyPI](https://img.shields.io/pypi/v/simplesam.svg?)](https://pypi.org/project/henipipe/)
<!-- [![Build Status](https://travis-ci.org/mdshw5/simplesam.svg?branch=master)](https://travis-ci.org/mdshw5/simplesam) -->
[![Documentation Status](https://readthedocs.org/projects/henipipe/badge/?version=latest)](https://henipipe.readthedocs.io/en/latest/?badge=latest)


<p align="center"><img src="henipipe.png" alt="" width="250"></a></p>
<hr>


# henipipe
==========




Version 2.4.9

A python wrapper for processing of sequencing data generated using CutnRun or CutnTag (developed by the Henikoff lab FHCRC).  Now with a single-cell option ('SC') for processing CutnTag data generated using the iCell8 platform (Takara).

## New in version 2.4.x

1. Added a --version function
2. In version 2.4.9 - environs.json was properly configured for PBS; see below for using a project ID with PBS

## New in version 2.3

1. Henipipe adds a new function, DEDUP.  DEDUP will remove presumed PCR duplicates from the bed file but leave a record of how many were detected.  The DEDUP funciton is meant to be used after ALIGN and before other downstream functions.  It will replace the bed file with a collapsed bedfile with a new column that counts the number of presumed duplicates found.  Note that read pairs will be collapsed regardless of strand and all strand data will be changed to positive.  
2. Henipipe adds a new function, BLACKLIST.  BLACKLIST will remove bed entries that overlap with a user-specified blacklist file designated with the '-bl' flag.
2. Changes to MACS2 function were made in this version to allow custom parameters to be passed to MACS2 peak calling using the -M2p flag.
3. Fixed a bug in SCALE function

## New in version 2.2

Henipipe now will now make Bigwig files from bedgraphs

## New in version 2.0

Henipipe now will process single cell data generated by the Takara iCell8 platform (See instructions below).  The pipeline will output the following
1. A bigwig file of aggregated SC data
2. SEACR peak calls (v1.3 - v1.4 coming soon) using both the 'relaxed' and 'stringent' SEACR modes
3. A bedgraph file
4. A fragments.tsv.gz file for input into single cell software such as Signac and ArchR
5. A fragments.tsv.gz.tbi (Tabix indexed file of #4)

## Requirements

1. Python > 3.5 (henipipe uses the 'six' package but will attempt to install if not already installed)
2. Computing cluster with PBS or SLURM
3. Modules installed for python, bowtie2, samtools, bedtools, R
4. MACS2 is required for MACS2 function
5. Modules installed for kenttools and htslib are required for SC option

## Installation

Installation can probably be done correctly many different ways.  Here are the methods that have worked for us.  We recommend that henipipe be installed with pipx.

**At SCRI do the following**
```bash
module load python
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org' henipipe
```


**At the FHCRC do the following...**
```bash
module load Python/3.7.4-foss-2019b-fh1
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps henipipe
```

You should then be able to test installation by calling henipipe.  After running the folllowing, you should see the help screen displayed.

```bash
henipipe
```

## Help (-h)

```bash
usage: A wrapper for running henipipe [-h] [--sample_flag SAMPLE_FLAG]
                                      [--fastq_folder FASTQ_FOLDER]
                                      [--trim_folder TRIM_FOLDER]
                                      [--trim_args TRIM_ARGS]
                                      [--organized_by {folder,file}]
                                      [--genome_key GENOME_KEY]
                                      [--split_char SPLIT_CHAR]
                                      [--R1_char R1_CHAR] [--R2_char R2_CHAR]
                                      [--ext EXT] [--filter_high FILTER_HIGH]
                                      [--filter_low FILTER_LOW]
                                      [--output OUTPUT] [--runsheet RUNSHEET]
                                      [--log_prefix LOG_PREFIX]
                                      [--select SELECT] [--debug]
                                      [--bowtie_flags BOWTIE_FLAGS]
                                      [--cluster {PBS,SLURM,local}]
                                      [--threads THREADS] [--gb_ram GB_RAM]
                                      [--install INSTALL]
                                      [--norm_method {coverage,read_count,spike_in}]
                                      [--user USER] [--SEACR_norm {non,norm}]
                                      [--SEACR_fdr SEACR_FDR]
                                      [--SEACR_stringency {stringent,relaxed}]
                                      [--keep_files] [--verbose]
                                      {SC,MAKERUNSHEET,ALIGN,SCALE,MERGE,SEACR,MACS2,AUC,GENOMESFILE,FASTQC,TRIM}

positional arguments:
  {SC,MAKERUNSHEET,ALIGN,SCALE,MERGE,SEACR,MACS2,AUC,GENOMESFILE,FASTQC,TRIM}
                        a required string denoting segment of pipeline to run.
                        1) "MAKERUNSHEET" - to parse a folder of fastqs; 2)
                        "ALIGN" - to perform alignment using bowtie and output
                        bed files; 3) "SCALE" - to normalize data to reference
                        (spike in); 4) "MERGE" - to merge bedgraphs 5) "SEACR"
                        - to perform SEACR; 6) "MACS" - to perform MACS2; 7)
                        "AUC" - to calculate AUC between normalized bedgraph
                        using a peak file; 8) "GENOMESFILE" - print location
                        of genomes.json file; 9) "FASTQC" - run fastqc on
                        cluster; 10) run trimmotatic on cluster;

optional arguments:
  -h, --help            show this help message and exit
  --sample_flag SAMPLE_FLAG, -sf SAMPLE_FLAG
                        FOR MAKERUNSHEET only string to identify samples of
                        interest in a fastq folder
  --fastq_folder FASTQ_FOLDER, -fq FASTQ_FOLDER
                        For SC and MAKERUNSHEET only: Pathname of fastq folder
                        (files must be organized in folders named by sample)
  --trim_folder TRIM_FOLDER, -tf TRIM_FOLDER
                        REQURIED, For TRIM only: Pathname of output folder;
                        Note that all trimmed fastqs will be placed in the
                        same folder
  --trim_args TRIM_ARGS, -ta TRIM_ARGS
                        OPTIONAL, For TRIM only: Args to pass to trimmomatic
  --organized_by {folder,file}, -by {folder,file}
                        Option to specify how fastq or unbam folder is
                        organized
  --genome_key GENOME_KEY, -gk GENOME_KEY
                        For MAKERUNSHEET only: abbreviation to use "installed"
                        genomes in the runsheet (See README.md for more
                        details
  --split_char SPLIT_CHAR, -sc SPLIT_CHAR
                        Character by which to split the fastqfile name into
                        samples, OPTIONAL and for MAKERUNSHEET only
  --R1_char R1_CHAR, -r1c R1_CHAR
                        Character by which to split the fastqfile name into
                        read1, OPTIONAL and for MAKERUNSHEET only; default =
                        "_R1_"
  --R2_char R2_CHAR, -r2c R2_CHAR
                        Character by which to split the fastqfile name into
                        read2, OPTIONAL and for MAKERUNSHEET only; default =
                        "_R2_"
  --ext EXT, -e EXT     suffix of fastq files, OPTIONAL and for MAKERUNSHEET
                        only
  --filter_high FILTER_HIGH, -fh FILTER_HIGH
                        For ALIGN only: upper limit of fragment size to
                        exclude, defaults is no upper limit. OPTIONAL
  --filter_low FILTER_LOW, -fl FILTER_LOW
                        For ALIGN only: lower limit of fragment size to
                        exclude, defaults is no lower limit. OPTIONAL
  --output OUTPUT, -o OUTPUT
                        Pathname to output folder (note this folder must exist
                        already!!), Defaults to current directory
  --runsheet RUNSHEET, -r RUNSHEET
                        tab-delim file with sample fields as defined in the
                        script. - REQUIRED for all jobs except MAKERUNSHEET
  --log_prefix LOG_PREFIX, -l LOG_PREFIX
                        Prefix specifying log files for henipipe output from
                        henipipe calls. OPTIONAL
  --select SELECT, -s SELECT
                        To only run the selected row in the runsheet, OPTIONAL
  --debug, -d           To print commands (For testing flow). OPTIONAL
  --bowtie_flags BOWTIE_FLAGS, -b BOWTIE_FLAGS
                        For ALIGN: bowtie flags, OPTIONAL
  --cluster {PBS,SLURM,local}, -c {PBS,SLURM,local}
                        Cluster software. OPTIONAL Currently supported: PBS,
                        SLURM and local
  --threads THREADS, -t THREADS
                        number of threads; default: 8
  --gb_ram GB_RAM, -gb GB_RAM
                        gigabytes of RAM per thread
  --install INSTALL, -i INSTALL
                        FOR GENOMESFILE: location of file to install as a new
                        genomes.json file, existing genomes.json will be
                        erased
  --norm_method {coverage,read_count,spike_in}, -n {coverage,read_count,spike_in}
                        For ALIGN and SCALE: Normalization method, by
                        "read_count", "coverage", or "spike_in". If method is
                        "spike_in", HeniPipe will align to the spike_in
                        reference genome provided in runsheet. OPTIONAL
  --user USER, -u USER  user for submitting jobs - defaults to username.
                        OPTIONAL
  --SEACR_norm {non,norm}, -Sn {non,norm}
                        For SEACR: Normalization method; default is
                        "non"-normalized, select "norm" to normalize using
                        SEACR. OPTIONAL
  --SEACR_fdr SEACR_FDR, -Sf SEACR_FDR
                        For SEACR: Used to set FDR threshold when control is
                        not used. OPTIONAL
  --SEACR_stringency {stringent,relaxed}, -Ss {stringent,relaxed}
                        FOR SEACR: Default will run as "stringent", other
                        option is "relaxed". OPTIONAL
  --keep_files, -k      FOR ALIGN: use this flag to turn off piping (Will
                        generate all files).
  --verbose, -v         Run with some additional ouput - not much though...
                        OPTIONAL
```


## Runsheet (workflow for bulk processing only)

The runsheet is the brains of the henipipe workflow. You can make a runsheet using the MAKERUNSHEET command.  This command will parse a directory of fastq folder (specified using the -fq flag; fastq files should be organized in subfolders named by sample) and will find fastq mates (R1 and R2 - Currently only PE sequencing is supported).  Running henipipe MAKERUNSHEET will find and pair these fastqs for you and populate the runsheet with genome index locations (see below) and output filenames with locations as specified using the -o flag.  Note that thenipie output will default to the current working directory if no location is otherwise specified.  There is an option for selecting only folders that contain a specific string (using the -sf flag).  *After generation of a runsheet (csv file), you should take a look at it in Excel or Numbers to make sure things look okay...*  Here are the columns that you can include.  Order is irrelevant.  Column names (headers) exactly as written below are required.

### Example Runsheet 

**absolute pathnames are required for runsheets**

| sample | fasta | spikein_fasta | fastq1 | fastq2 | bed_out | spikein_bed_out | genome_sizes | bedgraph |  SEACR_key  | SEACR_out |
|--------|-------|---------------|--------|--------|---------|-----------------|--------------|----------|-------------|-----------|
|  mys1  |  path |      path     |  path  |  path  |   path  |       path      |     path     |   path   |     4JS     |   path    |
|  mys2  |  path |      path     |  path  |  path  |   path  |       path      |     path     |   path   | 4JS_CONTROL |   path    |


* 'sample' name of the sample REQUIRED.  
* 'fasta' location of the Bowtie2 indexed fasta file REQUIRED.  
* 'spikein_fasta' location of the Bowtie2 indexed fasta file for spike_in normalization OPTIONAL.  
* 'fastq1' a tab seperated string of filenames denoting location of all R1 files for a sample REQUIRED.  
* 'fastq2' a tab seperated string of filenames denoting location of all R2 files for a sample REQUIRED.  
* 'bed_out' name of the location for the aligned and sorted bam file REQUIRED.  
* 'spikein_bed_out' name of the location for the aligned and sorted bam file OPTIONAL.  
* 'genome_sizes' REQUIRED.  
* 'bedgraph' file name of normalized bedgraph REQUIRED.  
* 'SEACR_key' sample key corresponding to sample groups to be run against an IgG (or other) contol.  all samples to be run against a control are given the same name and the control is labeleled with the an additional string underscore + 'CONTROL' (i.e. 4JS_CONTROL) OPTIONAL.  
* 'SEACR_out' file name of SEACR output OPTIONAL.  

## Genomes and adding genome locations (required for bulk and SC)

Henipipe uses Bowtie2 for alignment.  As such, you should have a previously indexed location of your genome accessible to henipipe.  This location is referred to in henipipe as the 'fasta'.  Similarly, one should provide the location of the spike_in indexed reference genome in the 'spikein_fasta' field.  For bedgraph conversion, a text file of genome sizes text file is also needed.  See the following for a discussion on how to make a 'genome_sizes' file https://www.biostars.org/p/173963/.

Henipipe provides an easy way to add these locations to your system for repeated use using the --genome_key (-gk) option during MAKERUNSHEET commands.  A file called genomes.json can be found in the 'data' directory of the henipipe install folder.  This file can be edited to include those locations you want to regularly put in the runsheet.  The following shows an example of a genomes.json file.  The files "top level" is a name that can be used in the --genome_key field (-gk) during runsheet generation to populate the columns of the runsheet with fasta, spikein_fasta, and genome_sizes locations associated with that genome_key.  The 'default' key will be used when no genome_key is specified.

```json
{
    "default": {
        "fasta": "/path/path/hg38/bowtie2_index",
        "genome_sizes": "/path/path/hg38/genome_sizes.txt",
        "spikein_fasta": "/path/path/Ecoli/bowtie2_index"},
    "my_hg38": {
        "fasta": "/shared/biodata/ngs/Reference/iGenomes/Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome",
        "genome_sizes": "/shared/ngs/illumina/henikoff/solexa/databases/human/hg38/chr_lens.txt",
        "spikein_fasta": "/shared/ngs/illumina/henikoff/Bowtie2/Ecoli"
    }
```

## Doing a bulk henipipe run

Say your fastqs live within within subfolders of a folder 'fastq' in the folder 'data'.  So if you were to...
```bash
cd /data/fastq
ls
```
... you'd get a bunch of folders, each of which would be filled with fastqs.  Each folder name should correspond to a sample name.


**To run henipipe, do the following...**
1. Make a new output directory 'henipipe'.
2. Go into that directory and make a runsheet pointing to the fastq folder i.e. the folder level above.  (at the command line, henipipe is cool with either relative or absolute pathnames; but as stated earlier, absolute pathnames are required for the runsheet.)
3.  Optionally you can only select directories of fastq files that contain in their name the string denoted using the -sf flag.
4. After inspecting and completing the runsheet, run ALIGN, NORM, SEACR, and AUC.  


```bash
cd ..
mkdir henipipe
cd henipipe
henipipe MAKERUNSHEET -fq ../fastq -sf MySampleDirectoriesStartWithThisString -o .
henipipe ALIGN -r runsheet.csv
henipipe SCALE -r runsheet.csv
henipipe BIGWIG -r runsheet.csv
henipipe SEACR -r runsheet.csv
mkdir auc
henipipe AUC -r runsheet.csv -o auc
```


## Try our test bulk data


Clone this repo.  There you will find a folder called 'test_data'.  Our test fastq files are in a folder creatively named 'fastq'.  

Note that it is probably easier and faster to simply clone the henipipe repo than to find the data embedded the pipx install.  As such, I would encourage any user who would like to use these test data for troubleshooting purposes to install normally using pipx (as above), then separately clont the repo by invoking 'git clone' as below.  This obviously duplicates the repo, but I have made the test files pretty small (< 70 MB total).  I would then recommend that after all testing is complete, the user then delete the folder created using 'git clone'.


```bash

git clone https://github.com/scfurl/henipipe.git
cd ***Your specific location***/henipipe/test_data

ml Python # or otherwise load python
ml R # or otherwise load R

mkdir henipipe
cd henipipe

henipipe MAKERUNSHEET -fq ../fastq
#edit the resulting runsheet.csv file in Excel or Numbers - Numbers is better - export as CSV and rename (runsheet_fixed.csv)

#make sure it looks okay
awk -F ',' '{print $1, $2}' runsheet_fixed.csv

#proceed with henipipe steps
henipipe ALIGN -t 16 -r runsheet_fixed.csv -n spike_in
henipipe SCALE -r runsheet_fixed.csv -n spike_in
henipipe SEACR -r runsheet_fixed.csv

```

## Doing a SC henipipe run (New in >= Version 2.0)

Say your fastqs exist in a 'fastq' in a folder 'data'.
```bash
ls /data/fastq
```

For the current version of henipipe, these fastq files *must* be named such that each pair of fastqs (R1 and R2) has a unique name that contains the cell barcode in the name of the file.  This typically is the output for demuxed iCell8 Takara runs...  For example:

```bash
A2_1_TCTTATTACCTGCGGG_S221_R1_001.fastq.gz
A2_1_TCTTATTACCTGCGGG_S221_R2_001.fastq.gz
```


**To run henipipes sc, do the following...**
1. From within the 'data' directory (in the above example where the fastq files are located in data/fastq); Make a new output directory, say 'henipipe_sc'.
2. Run henipipe specifying the following: the location of the fastqs (here 'fastq') with the '-fq' flag and the location of the desired output (here 'henipipe_sc') with the '-o' flag.  Don't forget to add a genome key with the '-gk' flag!

```bash
mkdir henipipe_sc
henipipe SC -fq fastq -o henipipe_sc -gk FH_mm10_unmasked
```

### Henipipe SC options and disclaimers

Henipipe SC was written to accomodate iCell8 output.  As such, it should be able to parse the fastq folder and find paired fastq files.  That being said, it has not been exhaustively debugged.  Let us know if you have an issue using by submitting an issue through github.  Henipipe SC peak files will be generated using SEACR 1.3 (1.4 coming soon), but only by specifying an FDR value (See SEACR for more information).  The FDR is set using the '--SEACR_fdr' flag with a default of 0.05.  Future versions of henipipe will allow for use of this setting for bulk data but currently henipipe SEACR functionality in bulk still requires a control input file.

### Using a project code

Henipipe is not engineered to accept project IDs.  However for PBS job submission systems, our environs.json file will capture the global environmental variable PROJECT to run jobs with a specific project code.

For example (note this code is made up)

```sh
export PROJECT=e05c3b6h-5a82-4943-uj87-2659cea32a54
henipipe ALIGN -t 16 -r runsheet.csv -c PBS

```



## Acknowledgements

Written by Scott Furlan with code inspiration from Andrew Hill's cellwrapper; Henipipe includes a python script samTobed.py which takes code from a fantastic sam reader "simplesam" - https://github.com/mdshw5/simplesam.  samTobed.py uses specific sam-sorting parameters similar to those written in Jorja Henikoff's PERL script.
