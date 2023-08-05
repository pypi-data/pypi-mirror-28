import json
import os
import unittest

from seqrecord_expanded import SeqRecordExpanded

from dataset_creator import Dataset
from .data import test_data
from .generate_test_data import get_test_data


NEXUS_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Nexus')


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_sorting_seq_records(self):
        """Test SeqRecordExpanded objects are sorted by gene_code and then by
        voucher_code.
        """
        my_list = [
            {'seq': 'CTgCacGgTCaagacGTGCtGgaTgaggctGccGacTTttcggtCtGTAgGCGACGCCTTGAAGGACGGCTTCGACGGAGCGTCGCGGGTTATGATGCCCAATACGGAGTTGGAAGCACCAGCTCAGCGAAACGATGCCGCTCCGCACAGAGTCCCGCGACGAGACCGATACAGATTTCAACTwCGGCCGCACAATCCTGACCACAAAACACCCGGAGTCAAGGACCTAGTGTACTTGGAATCATCGCCGGGTTTCTGCGAAAAGAACCCGCGGCTGGGCATTCCAGGCACGCACGGGCGTTCCTGCAATGACACGAGTATCGGCGTCGACGGCTGCGACCTCATGTGCTGTGGCCGTGGCTACCGGACCGAGACAATGTTCGTTGTGGAGCGATGCAAC',
             'voucher_code': "CP100-11", 'taxonomy': {'genus': 'Aus', 'species': 'bus'}, 'gene_code': 'wingless', 'reading_frame': 2, 'table': 1},
            {'seq': '???????????????????????????????????????????TCTGTAGGCGATGCCTTGAAGGACGGCTTCGACGGAGCGTCGCGGGTCATGATGCCCAATACGGAGTTAGAAGCGCCTGCTCAGCGAAACGACGCCGCCCCGCACAGAGTCCCGCGACGAGACCGATACAGATTTCAACTTCGGCCGCACAATCCTGACCACAAAACACCCGGA?TCAAGGACCTAGTGTACTTGGAATCATCGCCGGGTTTCTGCGAAAAGAACCCGCGGCTGGGCATTCCCGGCACGCACGGGCGTGCCTGCAACGACACGAGTATCGGCGTCGACGGCTGCGACCTCATGTGCTGCGGCCGTGGCTACCGGACCGAGACAATGTTCGTCGTGGAGCGATGCAAC',
             'voucher_code': "CP100-10", 'taxonomy': {'genus': 'Aus', 'species': 'aus'}, 'gene_code': 'wingless', 'reading_frame': 2, 'table': 1},

            {'seq': '???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
             'voucher_code': "CP100-11", 'taxonomy': {'genus': 'Aus', 'species': 'bus'}, 'gene_code': 'RpS2', 'reading_frame': 3, 'table': 1},
            {'seq': '???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
             'voucher_code': "CP100-10", 'taxonomy': {'genus': 'Aus', 'species': 'aus'}, 'gene_code': 'RpS2', 'reading_frame': 3, 'table': 1},

            {'seq': '??????????????????????????????????????????????????????????????????????????AAAAAGAAACTTTTGGAAATTTaggtataATTTATGCTATATTAGCAATTGGATTATTAGGATTTATTGTGTGAGCTCATCATATATTTACTGTAGGTATAGATATTGATACTCGAGCTTATTTTACCTCTGCTACAATAATTATTGCAGTCCCAACAGGAATTAAAATTTTTAGTTGATTAGCAACTCTACATGGAACACAAATTAATTATAGTCCTTCCATACTTTGAAGACTAGGATTTATTTTTTTATTTACAGTAGGAGGATTAACTGGTGTAATTTTAGCTAATTCTTCAATTGATATTGCTCTTCATGATACTTATTATGTAgTAgCCCACTTTCATTATGTATTGTCTATAGGAGCAGTATTTGCTATTTTTGGAGGATTTGTCCATTGATATCCTTTATTTACAGGATTAATATTAAATCCATATTTATTAAAAATTCAATTTATTTCAATATTTATTGGAGTTAACTTAACTTTTTTCCCACAACATTTTTTAGGTTTAGCTGGTATACCTCGACGTTACTCAGATTACCCAGATAATTTTTTATCTTGAAATATTATTTCATCATTAGGATCTTATATTTCTCTATTTTCTATAATAATAATAaTTATTATTATATGAGAATCAATAACTTATCAACGTATAATTTTATTTTCATTAAATATACctTCTTCAATTGAGTGATATCAAAAaTTACCACCTGCCGAACATTCTTATAAtGAAC',
             'voucher_code': "CP100-10", 'taxonomy': {'genus': 'Aus', 'species': 'aus'}, 'gene_code': 'COI_end', 'reading_frame': 2, 'table': 5},
            {'seq': '?????????????????????????????????????????????????????????????????????????AAAAAAGAAACTTTCGGAAGCTTAGGTATAATTTACGCTATATTAGCTATTGGATTATTAGGATtTATTGTATGAGCTCATCATATATTTACAGTAGGAATAGATATTGATACCCGAGCTTATTTTACTTCTGCTACAATAATTATTGCCGTACCAACAGGAATTAAAATTTTTAGCTGATTAGCAACTCTTCACGGAACTCAAATCAATTATAGTCCTTCCATACTTTGAAGATTAGGATTTATTTTTTTATTTACAGTAGGAGGACTAACTGGTGTAATTTTAGCTAATTCTTCAATTGATATTACTCTCCATGATACTTATTATGTTGTAGCTCATTTTCATTATGTTCTATCTATAGGAGCAGTATTTGCTATTTTCGGAGGATTTATCCACTGATACCCCTTATTTACAGGATTAATATTAAACCCATATTTATTAAAAATTCAATTCATTTCAATATTTATTGGAGTTAATTTAACTTTTTTTCCACAACATTTTTTAGGGTTAGCTGGTATACCTCGTCGTTATTCAGATTACCCAGATAATTTTTTATCTTGAAATATTATTTCATCATTAGGATCTTATATTTCATTATTTTCTATAATAATAATAATTATTATTATTTGAGAATCAATAATTTATCAACGTATAATTTTATTTACATTAAATATACCCTCTTCAATTGAATGATATCAAAATTTACCTCCTGCCGAACATTCTTATAATGAAC',
             'voucher_code': "CP100-11", 'taxonomy': {'genus': 'Aus', 'species': 'bus'}, 'gene_code': 'COI_end', 'reading_frame': 2, 'table': 5},

            {'seq': '????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
             'voucher_code': "CP100-10", 'taxonomy': {'genus': 'Aus', 'species': 'aus'}, 'gene_code': 'ef1a', 'reading_frame': 2, 'table': 1},
            {'seq': '????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
             'voucher_code': "CP100-11", 'taxonomy': {'genus': 'Aus', 'species': 'bus'}, 'gene_code': 'ef1a', 'reading_frame': 2, 'table': 1},
        ]
        seq_records = []
        append = seq_records.append

        for i in my_list:
            seq_record = SeqRecordExpanded(
                i['seq'], voucher_code=i['voucher_code'],
                taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                reading_frame=i['reading_frame'], table=i['table'],
            )
            append(seq_record)

        expected = ['COI_end', 'COI_end', 'ef1a', 'ef1a', 'RpS2', 'RpS2', 'wingless', 'wingless']
        result = Dataset(seq_records).seq_records
        self.assertEqual(expected, [i.gene_code for i in result])

        expected = ['CP100_10', 'CP100_11', 'CP100_10', 'CP100_11',
                    'CP100_10', 'CP100_11', 'CP100_10', 'CP100_11']
        self.assertEqual(expected, [i.voucher_code for i in result])

    def test_extract_genes(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.gene_codes
        self.assertEqual(expected, result)

    def test_extract_number_of_chars(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '4739'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_wrong_argument(self):
        self.assertRaises(AttributeError,
                          Dataset, test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='5th position')

    def test_extract_number_of_chars_first_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st')
        expected = '1578'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='2nd')
        expected = '1577'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_third_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='3rd')
        expected = '1573'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_chars_first_and_second_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene',
                          codon_positions='1st-2nd')
        expected = '3155'
        result = dataset.number_chars
        self.assertEqual(expected, result)

    def test_extract_number_of_taxa(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = '10'
        result = dataset.number_taxa
        self.assertEqual(expected, result)

    def test_prepared_data(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        expected = ['ArgKin', 'COI-begin', 'COI_end', 'ef1a', 'RpS2', 'RpS5', 'wingless']
        result = dataset.data.gene_codes
        self.assertEqual(expected, result)

    def test_dataset_nexus(self):
        dataset = Dataset(test_data, format='NEXUS', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_using_default_parameters(self):
        dataset = Dataset(test_data, format='NEXUS')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_wrong_partitioning_parameter(self):
        self.assertRaises(AttributeError, Dataset, seq_records=test_data, format='NEXUS',
                          codon_positions='1st', partitioning='1st-2nd-3rd')

    def test_dataset_nexus_1st_codon_position(self):
        test_data = get_test_data("sample_data_numbers.txt")
        dataset = Dataset(test_data, format='NEXUS', codon_positions='1st', partitioning='by gene')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_1st_codon_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_3rd_codon_position(self):
        test_data = get_test_data("sample_data_numbers.txt")
        dataset = Dataset(test_data, format='NEXUS', codon_positions='3rd', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_3rd_codon_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_3rd_codon_position_partitioned_as_1st2nd_3rd(self):
        test_data = get_test_data("sample_data_numbers.txt")
        dataset = Dataset(test_data, format='NEXUS', codon_positions='3rd', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_3rd_codon_numbers.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_all_codon_positions_partitioned_by_codon_positions(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL', partitioning='by codon position')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_partitioned_as_each.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_nexus_all_codon_positions_partitioned_as_1st2nd_3rd(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL', partitioning='1st-2nd, 3rd')
        test_data_file = os.path.join(NEXUS_DATA_PATH, 'dataset_partitioned_as_1st2nd_3rd.nex')
        expected = open(test_data_file, 'r').read()
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_dataset_with_gene_missing_reading_frame(self):
        SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')
        with open(SAMPLE_DATA_PATH, 'r') as handle:
            sample_data = json.loads(handle.read())

        data = []
        append = data.append
        for i in sample_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            if i['gene_code'] == 'ArgKin':
                seq_record.reading_frame = None
            append(seq_record)

        self.assertRaises(ValueError, Dataset, data, format='NEXUS', codon_positions='ALL',
                          partitioning='1st-2nd, 3rd', aminoacids=True)

    def test_degenerate(self):
        SAMPLE_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data.txt')
        with open(SAMPLE_DATA_PATH, 'r') as handle:
            sample_data = json.loads(handle.read())

        data = []
        append = data.append
        for i in sample_data:
            seq_record = SeqRecordExpanded(i['seq'], voucher_code=i['voucher_code'],
                                           taxonomy=i['taxonomy'], gene_code=i['gene_code'],
                                           reading_frame=i['reading_frame'], table=i['table'])
            append(seq_record)

        with open(os.path.join(NEXUS_DATA_PATH, 'dataset_degenerated.nex'), 'r') as handle:
            expected = handle.read().strip()

        dataset = Dataset(data, format='NEXUS', codon_positions='ALL',
                          partitioning='by gene', degenerate='S')
        result = dataset.dataset_str
        self.assertEqual(expected, result)

    def test_using_outgroup(self):
        dataset = Dataset(test_data, format='NEXUS', codon_positions='ALL',
                          outgroup='CP100-19')
        expected = 'outgroup CP100_19_Aus_jus;'
        result = dataset.dataset_str
        self.assertTrue(expected in result)
