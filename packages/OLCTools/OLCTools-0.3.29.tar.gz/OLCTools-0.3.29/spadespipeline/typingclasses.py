#!/usr/bin/env python 3
from accessoryFunctions.accessoryFunctions import combinetargets, filer, GenObject, MetadataObject, printtime, \
    make_path, write_to_logfile
from spadespipeline.GeneSeekr import GeneSeekr
from genesippr.genesippr import GeneSippr
import confindr.confindr as confinder
from biotools import bbtools
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio import SeqIO
from csv import DictReader
from glob import glob
import pandas
import shutil
import os

__author__ = 'adamkoziol'


class Quality(object):

    def contamination_finder(self):
        """
        Helper function to get confindr integrated into the assembly pipeline
        """
        printtime('Calculating contamination in reads', self.start)
        report = os.path.join(self.path, 'confinder', 'confindr_report.csv')
        if not os.path.isfile(report):
            # Create an object to store attributes to pass to confinder
            args = MetadataObject
            args.input_directory = self.path
            args.output_name = os.path.join(self.path, 'confinder')
            args.databases = os.path.join(self.reffilepath, 'ConFindr', 'databases')
            args.forward_id = '_R1'
            args.reverse_id = '_R2'
            args.threads = self.cpus
            args.kmer_size = 31
            args.number_subsamples = 5
            args.subsample_depth = 20
            args.kmer_cutoff = 2
            try:
                shutil.rmtree(args.output_name)
            except IOError:
                pass
            # Create a detector object
            confinder.run_mashsippr(args.input_directory,
                                    args.output_name,
                                    args.databases)
            # Open the output report file.
            with open(os.path.join(report), 'w') as f:
                f.write('Sample,Genus,NumContamSNVs,NumUniqueKmers,CrossContamination,ContamStatus\n')
            paired_reads = confinder.find_paired_reads(args.input_directory,
                                                       forward_id=args.forward_id,
                                                       reverse_id=args.reverse_id)
            # Perform contamination detection on each set of paired reads
            for pair in paired_reads:
                sample_name = os.path.basename(list(filer(pair))[0])
                printtime('Beginning analysis of sample {}...\n'.format(sample_name), self.start, '\033[1;34m')
                genus = confinder.read_mashsippr_output(os.path.join(args.output_name, 'reports', 'mash.csv'),
                                                        sample_name)
                confinder.find_contamination(pair, args, genus)
            printtime('Contamination detection complete!', self.start)
        # Load the confindr report into a dictionary using pandas
        # https://stackoverflow.com/questions/33620982/reading-csv-file-as-dictionary-using-pandas
        confindr_results = pandas.read_csv(report, index_col=0).T.to_dict()
        # Find the results for each of the samples
        for sample in self.metadata:
            # Create a GenObject to store the results
            sample.confinder = GenObject()
            # Iterate through the dictionary to find the outputs for each sample
            for line in confindr_results:
                # If the current line corresponds to the sample of interest
                if sample.name in line:
                    # Set the values using the appropriate keys as the attributes
                    sample.confinder.genus = confindr_results[line]['Genus']
                    sample.confinder.num_contaminated_snvs = confindr_results[line]['NumContamSNVs']
                    sample.confinder.unique_kmers = confindr_results[line]['NumUniqueKmers']
                    sample.confinder.cross_contamination = confindr_results[line]['CrossContamination']
                    sample.confinder.contam_status = confindr_results[line]['ContamStatus']
                    if sample.confinder.contam_status is True:
                        sample.confinder.contam_status = 'Contaminated'
                    elif sample.confinder.contam_status is False:
                        sample.confinder.contam_status = 'Clean'

    def estimate_genome_size(self):
        """
        Use kmercountexact from the bbmap suite of tools to estimate the size of the genome
        """
        printtime('Estimating genome size using kmercountexact', self.start)
        for sample in self.metadata:
            # Initialise the name of the output file
            sample[self.analysistype].peaksfile = os.path.join(sample[self.analysistype].outputdir, 'peaks.txt')
            # Run the kmer counting command
            out, err, cmd = bbtools.kmercountexact(forward_in=sorted(sample.general.fastqfiles)[0],
                                                   peaks=sample[self.analysistype].peaksfile,
                                                   returncmd=True,
                                                   threads=self.cpus)
            # Set the command in the object
            sample[self.analysistype].kmercountexactcmd = cmd
            # Extract the genome size from the peaks file
            sample[self.analysistype].genomesize = bbtools.genome_size(sample[self.analysistype].peaksfile)
            write_to_logfile(out, err, self.logfile, sample.general.logout, sample.general.logerr, None, None)

    def error_correction(self):
        """
        Use tadpole from the bbmap suite of tools to perform error correction of the reads
        """
        printtime('Error correcting reads', self.start)
        for sample in self.metadata:
            sample.general.trimmedcorrectedfastqfiles = [fastq.split('.fastq.gz')[0] + '_trimmed_corrected.fastq.gz'
                                                         for fastq in sorted(sample.general.fastqfiles)]
            out, err, cmd = bbtools.tadpole(forward_in=sorted(sample.general.trimmedfastqfiles)[0],
                                            forward_out=sample.general.trimmedcorrectedfastqfiles[0],
                                            returncmd=True,
                                            mode='correct',
                                            threads=self.cpus)
            # Set the command in the object
            sample[self.analysistype].errorcorrectcmd = cmd
            write_to_logfile(out, err, self.logfile, sample.general.logout, sample.general.logerr, None, None)

    def normalise_reads(self):
        """
        Use bbnorm from the bbmap suite of tools to perform read normalisation
        """
        printtime('Normalising reads to a kmer depth of 100', self.start)
        for sample in self.metadata:
            # Set the name of the normalised read files
            sample.general.normalisedreads = [fastq.split('.fastq.gz')[0] + '_normalised.fastq.gz'
                                              for fastq in sorted(sample.general.fastqfiles)]
            # Run the normalisation command
            out, err, cmd = bbtools.bbnorm(forward_in=sorted(sample.general.trimmedcorrectedfastqfiles)[0],
                                           forward_out=sample.general.normalisedreads[0],
                                           returncmd=True,
                                           threads=self.cpus)
            sample[self.analysistype].normalisecmd = cmd
            write_to_logfile(out, err, self.logfile, sample.general.logout, sample.general.logerr, None, None)

    def merge_pairs(self):
        """
        Use bbmerge from the bbmap suite of tools to merge paired-end reads
        """
        printtime('Merging paired reads', self.start)
        for sample in self.metadata:
            # Can only merge paired-end
            if len(sample.general.fastqfiles) == 2:
                # Set the name of the merged, and unmerged files
                sample.general.mergedreads = \
                    os.path.join(sample.general.outputdirectory, '{}_paired.fastq.gz'.format(sample.name))
                sample.general.unmergedforward = \
                    os.path.join(sample.general.outputdirectory, '{}_unpaired_R1.fastq.gz'.format(sample.name))
                sample.general.unmergedreverse = \
                    os.path.join(sample.general.outputdirectory, '{}_unpaired_R2.fastq.gz'.format(sample.name))
                # Run the merging command
                out, err, cmd = bbtools.bbmerge(forward_in=sample.general.normalisedreads[0],
                                                merged_reads=sample.general.mergedreads,
                                                returncmd=True,
                                                outu1=sample.general.unmergedforward,
                                                outu2=sample.general.unmergedreverse,
                                                threads=self.cpus)
                sample[self.analysistype].bbmergecmd = cmd
                write_to_logfile(out, err, self.logfile, sample.general.logout, sample.general.logerr, None, None)
            else:
                sample.general.mergedreads = sorted(sample.general.trimmedcorrectedfastqfiles)[0]

    def __init__(self, inputobject):
        self.metadata = inputobject.runmetadata.samples
        self.start = inputobject.starttime
        self.path = inputobject.path
        self.analysistype = 'quality'
        self.reffilepath = inputobject.reffilepath
        self.cpus = inputobject.cpus
        self.logfile = inputobject.logfile
        # Initialise the quality attribute in the metadata object
        for sample in self.metadata:
            setattr(sample, self.analysistype, GenObject())


class Plasmids(GeneSippr):

    def reporter(self):
        """
        Creates a report of the results
        """
        # Create the path in which the reports are stored
        make_path(self.reportpath)
        data = 'Strain,Gene,PercentIdentity,Length,FoldCoverage\n'
        with open(os.path.join(self.reportpath, self.analysistype + '.csv'), 'w') as report:
            for sample in self.runmetadata.samples:
                data += sample.name + ','
                try:
                    if sample[self.analysistype].results:
                        multiple = False
                        for name, identity in sample[self.analysistype].results.items():
                            if not multiple:
                                data += '{},{},{},{}\n'.format(name, identity,
                                                               len(sample[self.analysistype].sequences[name]),
                                                               sample[self.analysistype].avgdepth[name])
                            else:
                                data += ',{},{},{},{}\n'.format(name, identity,
                                                                len(sample[self.analysistype].sequences[name]),
                                                                sample[self.analysistype].avgdepth[name])
                            multiple = True
                    else:
                        data += '\n'
                except KeyError:
                    data += '\n'
            report.write(data)


class ResistanceNotes(object):

    @staticmethod
    def notes(targetpath):
        """
        Populates resistance dictionaries for different styles of gene:resistance entries
        :param targetpath: Directory in which the notes.txt file is located
        :return: the three resistance dictionaries
        """
        # Create a set of all the gene names without alleles or accessions e.g. sul1_18_AY260546 becomes sul1
        genedict = dict()
        altgenedict = dict()
        revaltgenedict = dict()
        # Load the notes file to a dictionary
        notefile = os.path.join(targetpath, 'notes.txt')
        with open(notefile, 'r') as notes:
            for line in notes:
                # Ignore comment lines - they will break the parsing
                if line.startswith('#'):
                    continue
                # Split the line on colons e.g. QnrB53:Quinolone resistance: has three variables after the split:
                # gene(QnrB53), resistance(Quinolone resistance), and _(\n) (unless there is an alternate name)
                gene, resistance, alternate = line.split(':')
                # Set up the resistance dictionary
                genedict[gene] = resistance
                # strA:Aminoglycoside resistance:Alternate name; aph(3'')-Ib - yields gene:resistance of aph(3'')-Ib
                # Aminoglycoside resistance
                if 'Alternate name' in line:
                    try:
                        altgene = alternate.split(';')[1].rstrip().lstrip()
                    except IndexError:
                        # blaGES-8:Beta-lactam resistance:Alternate name IBC-2
                        altgene = alternate.split()[-1].rstrip()
                    # Populate the dictionaries
                    genedict[altgene] = resistance
                    altgenedict[gene] = altgene
                    revaltgenedict[altgene] = gene
        return genedict, altgenedict, revaltgenedict

    @staticmethod
    def gene_name(name):
        """
        Split the FASTA header string into its components, including gene name, allele, and accession
        :param name: FASTA header
        :return:
        """
        # Allow for an additional part to the gene name aph(3'')_Ib_5_AF321551 yields gname: aph(3''), genename:
        # aph(3'')-Ib, allele: 5, accession AF321551
        if '_I' in name:
            pregene, postgene, allele, accession = name.split('_')
            genename = '{pre}-{post}'.format(pre=pregene,
                                             post=postgene)
            gname = pregene
        else:
            # Split the name on '_'s: ARR-2_1_HQ141279; gname, genename: ARR-2, allele: 1, accession: HQ141279
            try:
                genename, allele, accession = name.split('_')
                gname = genename
            # Some names have a slightly different naming scheme:
            except ValueError:
                try:
                    if 'bla' in name:
                        # >blaACC_1_2_AM939420 yields gname, genename: blaACC-1, allele: 2, accession: AM939420
                        genename, version, allele, accession = name.split('_')
                        gname = '{g}-{v}'.format(g=genename,
                                                 v=version)
                    else:
                        # tet(44)_1_NZ_ABDU01000081 yields gname, genename: tet(44), allele: 1,
                        # accession: NZ_ABDU01000081
                        genename, allele, preaccession, postaccession = name.split('_')
                        accession = '{preaccess}_{postaccess}'.format(preaccess=preaccession,
                                                                      postaccess=postaccession)
                        gname = genename
                except ValueError:
                    # Beta-lactamases have their own naming scheme
                    if name.split('_')[1].isdigit():
                        # blaOXY_1_1_1_Z30177 yields gname: blaOXY-1-1, genename: blaOXY, allele: 1, accession: Z30177
                        genename, version, allele, duplicate, accession = name.split('_')
                    else:
                        # blaOKP_B_15_1_AM850917 yields gname: blaOKP-B-15, genename: blaOKP, allele: 1,
                        # accession: AM850917
                        genename, version, allele, unknown, accession = name.split('_')
                    gname = '{g}-{ver}-{a}'.format(g=genename,
                                                   ver=version,
                                                   a=allele)
        return gname, genename, accession, allele

    @staticmethod
    def resistance(gname, genename, genedict, altgenedict, revaltgenedict):
        """
        Exxtracts the resistance phenotype from the dictionaries using the gene name
        :param gname: Name of gene. Often the same as genename, but for certain entries it is longer
        e.g. blaOKP-B-15 instead of blaOKP
        :param genename: Name of gene e.g. blaOKP
        :param genedict: Dictionary of gene:resistance
        :param altgenedict: Dictionary of gene alternate name:resistance
        :param revaltgenedict: Dictionary of gene alternate name: gene
        :return: finalgene: gene name to be used in the report, the resistance phenotype
        """
        # If the gene name is present in the altgenedict dictionary, adjust the string to output
        # to include the alternate name in parentheses e.g. strA (aph(3'')-Ib
        try:
            finalgene = '{namegene} ({genealt})'.format(namegene=genename,
                                                        genealt=altgenedict[genename])
        except KeyError:
            # Similar to above except with revaltdict
            try:
                finalgene = '{namegene} ({genealt})'.format(namegene=revaltgenedict[genename],
                                                            genealt=genename)
            except KeyError:
                finalgene = genename
        # Extract the resistance from the genedict dictionary
        try:
            res = genedict[genename]
        except KeyError:
            res = genedict[gname]
        return finalgene, res


class Resistance(GeneSippr):

    def reporter(self):
        """
        Creates a report of the results
        """
        genedict, altgenedict, revaltgenedict = ResistanceNotes.notes(self.targetpath)
        # Find unique gene names with the highest percent identity
        for sample in self.runmetadata.samples:
            try:
                if sample[self.analysistype].results:
                    # Initialise a dictionary to store the unique genes, and their percent identities
                    sample[self.analysistype].uniquegenes = dict()
                    for name, identity in sample[self.analysistype].results.items():
                        # Split the name of the gene from the string e.g. ARR-2_1_HQ141279 yields ARR-2
                        genename = name.split('_')[0]
                        # Set the best observed percent identity for each unique gene
                        try:
                            # Pull the previous best identity from the dictionary
                            bestidentity = sample[self.analysistype].uniquegenes[genename]
                            # If the current identity is better than the old identity, save it
                            if float(identity) > float(bestidentity):
                                sample[self.analysistype].uniquegenes[genename] = float(identity)
                        # Initialise the dictionary if necessary
                        except KeyError:
                            sample[self.analysistype].uniquegenes[genename] = float(identity)
            except KeyError:
                pass
        # Create the path in which the reports are stored
        make_path(self.reportpath)
        # Initialise strings to store the results
        data = 'Strain,Resistance,Gene,Allele,Accession,PercentIdentity,Length,FoldCoverage\n'
        with open(os.path.join(self.reportpath, self.analysistype + '.csv'), 'w') as report:
            for sample in self.runmetadata.samples:
                data += sample.name + ','
                if sample[self.analysistype].results:
                    # Create an attribute to store the string for the eventual pipeline report
                    sample[self.analysistype].pipelineresults = list()
                    # If there are multiple results for a sample, don't write the name in each line of the report
                    multiple = False
                    for name, identity in sorted(sample[self.analysistype].results.items()):
                        # Extract the necessary variables from the gene name string
                        gname, genename, accession, allele = ResistanceNotes.gene_name(name)
                        # Retrieve the best identity for each gene
                        try:
                            percentid = sample[self.analysistype].uniquegenes[gname]
                        # Beta-lactamases will not have the allele and version from the gene name defined above
                        except KeyError:
                            percentid = sample[self.analysistype].uniquegenes[gname.split('-')[0]]
                        # If the percent identity of the current gene matches the best percent identity, add it to
                        # the report - there can be multiple occurrences of genes e.g.
                        # sul1,1,AY224185,100.00,840 and sul1,2,CP002151,100.00,927 are both included because they
                        # have the same 100% percent identity
                        if float(identity) == percentid:
                            try:
                                # Determine the name of the gene to use in the report, as well as its associated
                                # resistance phenotype
                                finalgene, res = ResistanceNotes.resistance(gname, genename, genedict, altgenedict,
                                                                            revaltgenedict)
                                # Treat the initial vs subsequent results for each sample slightly differently - instead
                                # of including the sample name, use an empty cell instead
                                if multiple:
                                    data += ','
                                # Populate the results
                                data += '{},{},{},{},{},{},{}\n'.format(
                                    res,
                                    finalgene,
                                    allele,
                                    accession,
                                    identity,
                                    len(sample[self.analysistype].sequences[name]),
                                    sample[self.analysistype].avgdepth[name])
                                sample[self.analysistype].pipelineresults.append(
                                    '{rgene} ({pid}%) {rclass}'.format(rgene=finalgene,
                                                                       pid=identity,
                                                                       rclass=res)
                                )
                                multiple = True
                            except KeyError:
                                pass
                else:
                    data += '\n'
            # Write the strings to the file
            report.write(data)


class ResFinder(GeneSeekr):

    @staticmethod
    def sequencenames(contigsfile):
        """
        Takes a multifasta file and returns a list of sequence names
        :param contigsfile: multifasta of all sequences
        :return: list of all sequence names
        """
        sequences = list()
        for record in SeqIO.parse(open(contigsfile, "rU", encoding="iso-8859-15"), "fasta"):
            sequences.append(record.id)
        return sequences

    def strainer(self):
        for sample in self.metadata:
            if sample.general.bestassemblyfile != 'NA':
                setattr(sample, self.analysistype, GenObject())
                targets = glob(os.path.join(self.targetpath, '*.fsa'))
                targetcheck = glob(os.path.join(self.targetpath, '*.fsa'))
                if targetcheck:
                    try:
                        combinedtargets = glob(os.path.join(self.targetpath, '*.fasta'))[0]
                    except IndexError:
                        combinetargets(targets, self.targetpath)
                        combinedtargets = glob(os.path.join(self.targetpath, '*.fasta'))[0]
                    sample[self.analysistype].targets = targets
                    sample[self.analysistype].combinedtargets = combinedtargets
                    sample[self.analysistype].targetpath = self.targetpath
                    sample[self.analysistype].targetnames = self.sequencenames(combinedtargets)
                    sample[self.analysistype].reportdir = os.path.join(sample.general.outputdirectory,
                                                                       self.analysistype)
                else:
                    # Set the metadata file appropriately
                    sample[self.analysistype].targets = 'NA'
                    sample[self.analysistype].combinedtargets = 'NA'
                    sample[self.analysistype].targetpath = 'NA'
                    sample[self.analysistype].targetnames = 'NA'
                    sample[self.analysistype].reportdir = 'NA'
                    sample[self.analysistype].blastresults = 'NA'
            else:
                # Set the metadata file appropriately
                setattr(sample, self.analysistype, GenObject())
                sample[self.analysistype].targets = 'NA'
                sample[self.analysistype].combinedtargets = 'NA'
                sample[self.analysistype].targetpath = 'NA'
                sample[self.analysistype].targetnames = 'NA'
                sample[self.analysistype].reportdir = 'NA'
                sample[self.analysistype].blastresults = 'NA'

    def resfinderreporter(self):
        """
        Custom reports for ResFinder analyses. These reports link the gene(s) found to their resistance phenotypes
        """
        import xlsxwriter
        from Bio.SeqRecord import SeqRecord
        # Initialise resistance dictionaries from the notes.txt file
        genedict, altgenedict, revaltgenedict = ResistanceNotes.notes(self.targetpath)
        # Create a workbook to store the report. Using xlsxwriter rather than a simple csv format, as I want to be
        # able to have appropriately sized, multi-line cells
        workbook = xlsxwriter.Workbook(os.path.join(self.reportpath, '{}.xlsx'.format(self.analysistype)))
        # New worksheet to store the data
        worksheet = workbook.add_worksheet()
        # Add a bold format for header cells. Using a monotype font size 10
        bold = workbook.add_format({'bold': True, 'font_name': 'Courier New', 'font_size': 8})
        # Format for data cells. Monotype, size 10, top vertically justified
        courier = workbook.add_format({'font_name': 'Courier New', 'font_size': 8})
        courier.set_align('top')
        # Initialise the position within the worksheet to be (0,0)
        row = 0
        col = 0
        # A dictionary to store the column widths for every header
        columnwidth = dict()
        extended = False
        headers = ['Strain', 'Gene', 'Resistance', 'PercentIdentity', 'PercentCovered', 'Contig', 'Location',
                   'nt_sequence']
        for sample in self.metadata:
            sample[self.analysistype].sampledata = list()
            # Process the sample only if the script could find targets
            if sample[self.analysistype].blastresults != 'NA':
                for result in sample[self.analysistype].blastresults:
                    # Set the name to avoid writing out the dictionary[key] multiple times
                    name = result['subject_id']
                    # Use the ResistanceNotes gene name extraction method to get the necessary variables
                    gname, genename, accession, allele = ResistanceNotes.gene_name(name)
                    # Initialise a list to store all the data for each strain
                    data = list()
                    # Determine the name of the gene to use in the report and the resistance using the resistance
                    # method
                    finalgene, resistance = ResistanceNotes.resistance(gname, genename, genedict, altgenedict,
                                                                       revaltgenedict)
                    # Append the necessary values to the data list
                    data.append(finalgene)
                    data.append(resistance)
                    percentid = result['percentidentity']
                    data.append(percentid)
                    data.append(result['alignment_fraction'])
                    data.append(result['query_id'])
                    data.append('...'.join([str(result['low']), str(result['high'])]))
                    try:
                        # Only if the alignment option is selected, for inexact results, add alignments
                        if self.align and percentid != 100.00:

                            # Align the protein (and nucleotide) sequences to the reference
                            self.alignprotein(sample, name)
                            if not extended:
                                # Add the appropriate headers
                                headers.extend(['aa_Identity',
                                                'aa_Alignment',
                                                'aa_SNP_location',
                                                'nt_Alignment',
                                                'nt_SNP_location'
                                                ])
                                extended = True
                            # Create a FASTA-formatted sequence output of the query sequence
                            record = SeqRecord(sample[self.analysistype].dnaseq[name],
                                               id='{}_{}'.format(sample.name, name),
                                               description='')

                            # Add the alignment, and the location of mismatches for both nucleotide and amino
                            # acid sequences
                            data.extend([record.format('fasta'),
                                         sample[self.analysistype].aaidentity[name],
                                         sample[self.analysistype].aaalign[name],
                                         sample[self.analysistype].aaindex[name],
                                         sample[self.analysistype].ntalign[name],
                                         sample[self.analysistype].ntindex[name]
                                         ])
                        else:
                            record = SeqRecord(Seq(result['subject_sequence'], IUPAC.unambiguous_dna),
                                               id='{}_{}'.format(sample.name, name),
                                               description='')
                            data.append(record.format('fasta'))
                            if self.align:
                                # Add '-'s for the empty results, as there are no alignments for exact matches
                                data.extend(['-', '-', '-', '-', '-'])
                    # If there are no blast results for the target, add a '-'
                    except (KeyError, TypeError):
                        data.append('-')
                    sample[self.analysistype].sampledata.append(data)

        if 'nt_sequence' not in headers:
            headers.append('nt_sequence')
        # Write the header to the spreadsheet
        for header in headers:
            worksheet.write(row, col, header, bold)
            # Set the column width based on the longest header
            try:
                columnwidth[col] = len(header) if len(header) > columnwidth[col] else columnwidth[
                    col]
            except KeyError:
                columnwidth[col] = len(header)
            worksheet.set_column(col, col, columnwidth[col])
            col += 1
        # Increment the row and reset the column to zero in preparation of writing results
        row += 1
        col = 0
        # Write out the data to the spreadsheet
        for sample in self.metadata:
            worksheet.write(row, col, sample.name, courier)
            columnwidth[col] = len(sample.name)
            worksheet.set_column(col, col, columnwidth[col])
            col += 1
            multiple = False
            if not sample[self.analysistype].sampledata:
                # Increment the row and reset the column to zero in preparation of writing results
                row += 1
                col = 0
                # Set the width of the row to be the number of lines (number of newline characters) * 12
                worksheet.set_row(row)
                worksheet.set_column(col, col, columnwidth[col])
            for data in sample[self.analysistype].sampledata:
                if multiple:
                    col += 1
                # List of the number of lines for each result
                totallines = list()
                for results in data:
                    #
                    worksheet.write(row, col, results, courier)
                    try:
                        # Counting the length of multi-line strings yields columns that are far too wide, only count
                        # the length of the string up to the first line break
                        alignmentcorrect = len(str(results).split('\n')[1])
                        # Count the number of lines for the data
                        lines = results.count('\n') if results.count('\n') >= 1 else 1
                        # Add the number of lines to the list
                        totallines.append(lines)
                    except IndexError:
                        try:
                            # Counting the length of multi-line strings yields columns that are far too wide, only count
                            # the length of the string up to the first line break
                            alignmentcorrect = len(str(results).split('\n')[0])
                            # Count the number of lines for the data
                            lines = results.count('\n') if results.count('\n') >= 1 else 1
                            # Add the number of lines to the list
                            totallines.append(lines)
                        # If there are no newline characters, set the width to the length of the string
                        except AttributeError:
                            alignmentcorrect = len(str(results))
                            lines = 1
                            # Add the number of lines to the list
                            totallines.append(lines)
                    # Increase the width of the current column, if necessary
                    try:
                        columnwidth[col] = alignmentcorrect if alignmentcorrect > columnwidth[col] else \
                            columnwidth[col]
                    except KeyError:
                        columnwidth[col] = alignmentcorrect
                    worksheet.set_column(col, col, columnwidth[col])
                    col += 1
                    multiple = True
                # Set the width of the row to be the number of lines (number of newline characters) * 12
                worksheet.set_row(row, max(totallines) * 11)
                # Increase the row counter for the next strain's data
                row += 1
                col = 0
        # Close the workbook
        workbook.close()

    def object_clean(self):
        """

        """
        for sample in self.metadata:
            try:
                delattr(sample[self.analysistype], 'aaidentity')
                delattr(sample[self.analysistype], 'aaalign')
                delattr(sample[self.analysistype], 'aaindex')
                delattr(sample[self.analysistype], 'ntalign')
                delattr(sample[self.analysistype], 'ntindex')
                delattr(sample[self.analysistype], 'dnaseq')
                delattr(sample[self.analysistype], 'blastresults')
            except KeyError:
                pass

    def __init__(self, inputobject):
        # qseqid sacc stitle positive mismatch gaps evalue bitscore slen length
        self.resfinderfields = ['query_id', 'subject_id', 'positives', 'mismatches', 'gaps', 'evalue', 'bit_score',
                                'subject_length', 'alignment_length', 'query_start', 'query_end']
        self.analysistype = 'resfinder_assembled'
        self.metadata = inputobject.runmetadata.samples
        self.cutoff = 70
        self.start = inputobject.starttime
        self.reportdir = inputobject.reportpath
        self.pipeline = True
        self.referencefilepath = inputobject.reffilepath
        self.targetpath = os.path.join(self.referencefilepath, 'resfinder')
        self.threads = inputobject.cpus
        self.align = True
        self.logfile = inputobject.logfile
        self.unique = True
        self.strainer()
        self.runmetadata = MetadataObject()
        self.runmetadata.samples = self.metadata
        GeneSeekr.__init__(self, self)
        self.resfinderreporter()
        self.object_clean()


class Prophages(GeneSeekr):

    def reporter(self):
        with open(os.path.join(self.reportpath, 'prophages.csv'), 'w') as report:
            data = 'Strain,Gene,Host,PercentIdentity,PercentCovered,Contig,Location\n'
            # Set the required variables to load prophage data from a summary file
            targetpath = os.path.join(self.referencefilepath, self.analysistype)
            overview = glob(os.path.join(targetpath, '*.txt'))[0]
            fieldnames = ['id_prophage', 'file_name', 'host', 'host_id', 'number_of_prophages_in_host',
                          'start_position_of_prophage', 'end_position_of_prophage', 'length_of_prophage']
            for sample in self.metadata:
                # Create a set to ensure that genes are only entered into the report once
                genes = set()
                if sample.general.bestassemblyfile != 'NA':
                    # Open the prophage file as a dict - I do this here, as if I open it earlier, it looks like the
                    # file remains partially-read through for the next iteration. Something like prophagedata.seek(0)
                    # would probably work, but Dictreader objects don't have a .seek attribute
                    prophagedata = DictReader(open(overview), fieldnames=fieldnames, dialect='excel-tab')
                    try:
                        if sample[self.analysistype].blastresults:
                            data += '{},'.format(sample.name)
                            # Allow for formatting multiple hits for the same sample
                            multiple = False
                            for result in sample[self.analysistype].blastresults:
                                gene = result['subject_id']
                                if gene not in genes:
                                    if multiple:
                                        data += ','
                                    # Iterate through the phage data in the dictionary
                                    for phage in prophagedata:
                                        if phage['id_prophage'] == gene:
                                            # Add the data to the row
                                            data += '{},{},{},{},{},{}..{}\n' \
                                                .format(gene,
                                                        phage['host'],
                                                        result['percentidentity'],
                                                        result['alignment_fraction'] if float(
                                                            result['alignment_fraction']) <= 100 else '100.0',
                                                        result['query_id'],
                                                        result['low'],
                                                        result['high'])
                                    genes.add(gene)
                                    # Set multiple to true for any additional hits for this sample
                                    multiple = True
                        else:
                            data += '{}\n'.format(sample.name)
                    except KeyError:
                        data += '{}\n'.format(sample.name)
                else:
                    data += '{}\n'.format(sample.name)
            report.write(data)


class Univec(GeneSeekr):

    def reporter(self):
        from Bio import SeqIO
        import re
        with open(os.path.join(self.reportpath, 'univec.csv'), 'w') as report:
            data = 'Strain,Gene,Description,PercentIdentity,PercentCovered,Contig,Location\n'
            for sample in self.metadata:
                if sample.general.bestassemblyfile != 'NA':
                    # Create a set to ensure that genes are only entered into the report once
                    genes = set()
                    try:
                        if sample[self.analysistype].blastresults:
                            data += '{},'.format(sample.name)
                            # If multiple hits are returned for a sample, don't re-add the sample name on the next row
                            multiple = False
                            for result in sample[self.analysistype].blastresults:
                                gene = result['subject_id']
                                # Parse the reference file in order to extract the description of the BLAST hits
                                for entry in SeqIO.parse(sample[self.analysistype].combinedtargets, 'fasta'):
                                    # Find the corresponding entry for the gene
                                    if entry.id == gene:
                                        # Cut out the description from the entry.description using regex
                                        # e.g. for 'gnl|uv|X66730.1:1-2687-49 B.bronchiseptica plasmid pBBR1 genes for
                                        # mobilization and replication' only save the string after '2687-49'
                                        description = re.findall('\d+-\d+\s(.+)', entry.description)[0]
                                        # Don't add the same gene more than once to the report
                                        if gene not in genes:
                                            if multiple:
                                                data += ','
                                            data += '{},{},{},{},{},{}..{}\n' \
                                                .format(gene.split('|')[-1],
                                                        description,
                                                        result['percentidentity'],
                                                        result['alignment_fraction'] if float(
                                                            result['alignment_fraction'])
                                                        <= 100 else '100.0',
                                                        result['query_id'],
                                                        result['low'],
                                                        result['high'])
                                            # Allow for the proper formatting
                                            multiple = True
                                            genes.add(gene)
                        else:
                            data += '{}\n'.format(sample.name)
                    except KeyError:
                        data += '{}\n'.format(sample.name)
                else:
                    data += '{}\n'.format(sample.name)
            report.write(data)


class Virulence(GeneSippr):

    def reporter(self):
        """
        Creates a report of the results
        """
        # Create a set of all the gene names without alleles or accessions e.g. sul1_18_AY260546 becomes sul1
        genedict = dict()
        # Load the notes file to a dictionary
        notefile = os.path.join(self.targetpath, 'notes.txt')
        with open(notefile, 'r') as notes:
            for line in notes:
                # Ignore comment lines - they will break the parsing
                if line.startswith('#'):
                    continue
                # Split the line on colons e.g. stx1Aa:  Shiga toxin 1, subunit A, variant a: has three variables after
                # the split: gene(stx1Aa), description(Shiga toxin 1, subunit A, variant a), and _(\n)
                try:
                    gene, description, _ = line.split(':')
                # There are exceptions to the parsing. Some lines only have one :, while others have three. Allow for
                # these possibilities.
                except ValueError:
                    try:
                        gene, description = line.split(':')
                    except ValueError:
                        gene, description, _, _ = line.split(':')
                # Set up the description dictionary
                genedict[gene] = description.replace(', ', '_').strip()
        # Find unique gene names with the highest percent identity
        for sample in self.runmetadata.samples:
            try:
                if sample[self.analysistype].results:
                    # Initialise a dictionary to store the unique genes, and their percent identities
                    sample[self.analysistype].uniquegenes = dict()
                    for name, identity in sample[self.analysistype].results.items():
                        # Split the name of the gene from the string e.g. stx1:11:Z36899:11 yields stx1
                        genename = name.split(':')[0]
                        # Only allow matches of 100% identity for stx genes
                        if 'stx' in genename and float(identity) < 100.0:
                            pass
                        else:
                            # Set the best observed percent identity for each unique gene
                            try:
                                # Pull the previous best identity from the dictionary
                                bestidentity = sample[self.analysistype].uniquegenes[genename]
                                # If the current identity is better than the old identity, save it
                                if float(identity) > float(bestidentity):
                                    sample[self.analysistype].uniquegenes[genename] = float(identity)
                            # Initialise the dictionary if necessary
                            except KeyError:
                                sample[self.analysistype].uniquegenes[genename] = float(identity)
            except KeyError:
                pass
        # Create the path in which the reports are stored
        make_path(self.reportpath)
        # Initialise strings to store the results
        data = 'Strain,Gene,Subtype/Allele,Description,Accession,PercentIdentity,FoldCoverage\n'
        with open(os.path.join(self.reportpath, self.analysistype + '.csv'), 'w') as report:
            for sample in self.runmetadata.samples:
                data += sample.name + ','
                try:
                    if sample[self.analysistype].results:
                        # If there are many results for a sample, don't write the sample name in each line of the report
                        multiple = False
                        for name, identity in sorted(sample[self.analysistype].results.items()):
                            try:
                                # Split the name on colons: stx2A:63:AF500190:d; gene: stx2A, allele: 63, accession:
                                # AF500190, subtype: d
                                genename, allele, accession, subtype = name.split(':')
                            # Treat samples without a subtype e.g. icaC:intercellular adhesion protein C: differently.
                            # Extract the allele as the 'subtype', and the gene name, and accession as above
                            except ValueError:
                                genename, subtype, accession = name.split(':')
                            # Retrieve the best identity for each gene
                            percentid = sample[self.analysistype].uniquegenes[genename]
                            # If the percent identity of the current gene matches the best percent identity, add it to
                            # the report - there can be multiple occurrences of genes e.g.
                            # sul1,1,AY224185,100.00,840 and sul1,2,CP002151,100.00,927 are both included because they
                            # have the same 100% percent identity
                            if float(identity) == percentid:
                                # Treat the initial vs subsequent results for each sample slightly differently - instead
                                # of including the sample name, use an empty cell instead
                                if multiple:
                                    data += ','
                                try:
                                    description = genedict[genename]
                                except KeyError:
                                    description = 'na'
                                # Populate the results
                                data += '{},{},{},{},{},{}\n'.format(
                                    genename,
                                    subtype,
                                    description,
                                    accession,
                                    identity,
                                    sample[self.analysistype].avgdepth[name])
                                multiple = True
                    else:
                        data += '\n'
                except KeyError:
                    data += '\n'
            # Write the strings to the file
            report.write(data)
