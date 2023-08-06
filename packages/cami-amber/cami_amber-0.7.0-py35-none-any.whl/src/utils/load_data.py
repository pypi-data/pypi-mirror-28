#!/usr/bin/env python

import os
import gzip
import mimetypes
import sys
from Bio import SeqIO
import numpy as np
import errno

try:
    import exclude_genomes
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    try:
        import exclude_genomes
    finally:
        sys.path.remove(os.path.dirname(__file__))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class GoldStandard:
    def __init__(self):
        pass


class Query:
    def __init__(self):
        pass


def load_unique_common(unique_common_file_path):
    genome_to_unique_common = {}
    with open(unique_common_file_path) as read_handler:
        for line in read_handler:
            genome_to_unique_common[line.split("\t")[0]] = line.split("\t")[1].strip('\n')
    return genome_to_unique_common


def load_tsv_table(stream):
    data = []
    next(stream)
    for line in stream:
        line = line.strip()
        if len(line) == 0 or line.startswith("@"):
            continue
        row_data = line.split('\t')

        mapped_genome = row_data[0]
        real_size = int(float(row_data[5]))
        predicted_size = int(float(row_data[3]))
        correctly_predicted = int(float(row_data[4]))

        if row_data[1] != "NA" and predicted_size > 0:
            precision = float(row_data[1])
        else:
            precision = np.nan
        data.append({'mapped_genome': mapped_genome, 'precision': precision, 'recall': float(row_data[2]),
                     'predicted_size': predicted_size, 'correctly_predicted': correctly_predicted, 'real_size': real_size})
    return data


def read_lengths_from_fastx_file(fastx_file):
    """

    @param fastx_file: file path
    @type fastx_file: str
    @rtype: dict[str, int]
    """
    file_type = mimetypes.guess_type(fastx_file)[1]
    if file_type == 'gzip':
        f = gzip.open(fastx_file, "rt")
    elif not file_type:
        f = open(fastx_file, "rt")
    else:
        raise RuntimeError("Unknown type of file: '{}".format(fastx_file))

    length = {}
    if os.path.getsize(fastx_file) == 0:
        return length

    file_format = None
    line = f.readline()
    if line.startswith('@'):
        file_format = "fastq"
    elif line.startswith(">"):
        file_format = "fasta"
    f.seek(0)

    if not file_format:
        raise RuntimeError("Invalid sequence file: '{}".format(fastx_file))

    for seq_record in SeqIO.parse(f, file_format):
        length[seq_record.id] = len(seq_record.seq)

    f.close()

    return length


def get_genome_mapping_without_lenghts(mapping_file, remove_genomes_file=None, keyword=None):
    gold_standard = GoldStandard()
    gold_standard.genome_id_to_list_of_contigs = {}
    gold_standard.sequence_id_to_genome_id = {}

    filtering_genomes_to_keyword = {}
    if remove_genomes_file:
        filtering_genomes_to_keyword = load_unique_common(remove_genomes_file)

    with open(mapping_file, 'r') as read_handler:
        for sequence_id, genome_id, length in read_binning_file(read_handler):
            if genome_id in filtering_genomes_to_keyword and (not keyword or filtering_genomes_to_keyword[genome_id] == keyword):
                continue
            gold_standard.sequence_id_to_genome_id[sequence_id] = genome_id
            if genome_id not in gold_standard.genome_id_to_list_of_contigs:
                gold_standard.genome_id_to_list_of_contigs[genome_id] = []
            gold_standard.genome_id_to_list_of_contigs[genome_id].append(sequence_id)

    if len(gold_standard.genome_id_to_list_of_contigs) == 0:
        sys.exit('All bins of the gold standard have been filtered out due to option --remove_genomes.')

    return gold_standard


def get_genome_mapping(mapping_file, fastx_file):
    """
    @param mapping_file:
    @type mapping_file: str | unicode

    @return:
    """
    gold_standard = GoldStandard()
    gold_standard.genome_id_to_total_length = {}
    gold_standard.genome_id_to_list_of_contigs = {}
    gold_standard.sequence_id_to_genome_id = {}
    gold_standard.sequence_id_to_lengths = {}

    with open(mapping_file, 'r') as read_handler:
        is_length_column_av = is_length_column_available(read_handler)
        sequence_length = {}
        if not is_length_column_av:
            if not fastx_file:
                exit("Sequences length could not be determined. Please provide a FASTA or FASTQ file using option -f or add column _LENGTH to gold standard.")
            sequence_length = read_lengths_from_fastx_file(fastx_file)
        for anonymous_contig_id, genome_id, length in read_binning_file(read_handler):
            total_length = length if is_length_column_av else sequence_length[anonymous_contig_id]
            gold_standard.sequence_id_to_lengths[anonymous_contig_id] = total_length
            gold_standard.sequence_id_to_genome_id[anonymous_contig_id] = genome_id
            if genome_id not in gold_standard.genome_id_to_total_length:
                gold_standard.genome_id_to_total_length[genome_id] = 0
                gold_standard.genome_id_to_list_of_contigs[genome_id] = []
            gold_standard.genome_id_to_total_length[genome_id] += total_length
            gold_standard.genome_id_to_list_of_contigs[genome_id].append(anonymous_contig_id)

    return gold_standard


def read_header(input_stream):
    """
    @Version:0.9.1
    @SampleID:RH_S1

    @@SEQUENCEID    BINID   TAXID
    """
    header = {}
    column_names = {}
    for line in input_stream:
        if len(line.strip()) == 0 or line.startswith("#"):
            continue
        line = line.rstrip('\n')
        if line.startswith("@@"):
            for index, column_name in enumerate(line[2:].split('\t')):
                column_names[column_name] = index
            return header, column_names
        if line.startswith("@"):
            key, value = line[1:].split(':', 1)
            header[key] = value.strip()


def read_rows(input_stream, index_key, index_value, index_length):
    for line in input_stream:
        if len(line.strip()) == 0 or line.startswith("#"):
            continue
        line = line.rstrip('\n')
        row_data = line.split('\t')
        key = row_data[index_key]
        value = row_data[index_value]
        if index_length is not None:
            length = row_data[index_length]
            yield key, value, int(length)
        else:
            yield key, value, int(0)


def is_length_column_available(input_stream):
    header, column_names = read_header(input_stream)
    input_stream.seek(0)
    return "_LENGTH" in column_names


def get_column_indices(input_stream):
    """

    :param input_stream: 
    :return: 
    """
    header, column_names = read_header(input_stream)
    if "SEQUENCEID" not in column_names:
        raise RuntimeError("Column not found: {}".format("SEQUENCEID"))
    index_key = column_names["SEQUENCEID"]
    if "BINID" in column_names:
        index_value = column_names["BINID"]
    elif "TAXID" in column_names:
        index_value = column_names["TAXID"]
    else:
        raise RuntimeError("Column not found: {}".format("BINID/TAXID"))
    index_length = None
    if "_LENGTH" in column_names:
        index_length = column_names["_LENGTH"]
    return index_key, index_value, index_length


def read_binning_file(input_stream):
    index_key, index_value, index_length = get_column_indices(input_stream)
    return read_rows(input_stream, index_key, index_value, index_length)


def open_query(file_path_query):
    query = Query()
    query.path = file_path_query
    query.bin_id_to_list_of_sequence_id = {}
    query.sequence_id_to_bin_id = {}
    with open(file_path_query) as read_handler:
        for sequence_id, predicted_bin, length in read_binning_file(read_handler):
            if predicted_bin not in query.bin_id_to_list_of_sequence_id:
                query.bin_id_to_list_of_sequence_id[predicted_bin] = []
            query.bin_id_to_list_of_sequence_id[predicted_bin].append(sequence_id)
            query.sequence_id_to_bin_id[sequence_id] = predicted_bin
    return query


def open_queries(file_path_queries):
    queries = []
    for file_path in file_path_queries:
        queries.append(open_query(file_path))
    return queries
