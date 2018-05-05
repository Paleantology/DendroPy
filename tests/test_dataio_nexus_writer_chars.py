#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2010-2015 Jeet Sukumaran and Mark T. Holder.
##  All rights reserved.
##
##  See "LICENSE.rst" for terms and conditions of usage.
##
##  If you use this work or any portion thereof in published work,
##  please cite it as:
##
##     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
##     for phylogenetic computing. Bioinformatics 26: 1569-1571.
##
##############################################################################

"""
Tests for NEXUS tree list writing.
"""

import unittest
import dendropy
import os
import sys
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
from support import dendropytest
from support import compare_and_validate
from support import pathmap
from support import standard_file_test_chars

class NexusWriterCharactersTestCase(
        compare_and_validate.ValidateWriteable,
        dendropytest.ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.check_taxon_annotations = False
        cls.check_matrix_annotations = False
        cls.check_sequence_annotations = False
        cls.check_column_annotations = False
        cls.check_cell_annotations = False
        standard_file_test_chars.DnaTestChecker.build()
        standard_file_test_chars.RnaTestChecker.build()
        standard_file_test_chars.ProteinTestChecker.build()
        standard_file_test_chars.Standard01234TestChecker.build()
        standard_file_test_chars.ContinuousTestChecker.build()
        cls.srcs = (
                ("standard-test-chars-dna.multi.nexus", dendropy.DnaCharacterMatrix, standard_file_test_chars.DnaTestChecker),
                ("standard-test-chars-rna.multi.nexus", dendropy.RnaCharacterMatrix, standard_file_test_chars.RnaTestChecker),
                ("standard-test-chars-protein.multi.nexus", dendropy.ProteinCharacterMatrix, standard_file_test_chars.ProteinTestChecker),
                ("standard-test-chars-generic.interleaved.nexus", dendropy.StandardCharacterMatrix, standard_file_test_chars.Standard01234TestChecker),
                ("standard-test-chars-continuous.mesquite.nexus", dendropy.ContinuousCharacterMatrix, standard_file_test_chars.ContinuousTestChecker),
                )

    def verify_char_matrix(self, char_matrix, src_matrix_checker_type):
        self.assertEqual(type(char_matrix), src_matrix_checker_type.matrix_type)
        if src_matrix_checker_type.matrix_type is dendropy.StandardCharacterMatrix:
            src_matrix_checker_type.create_class_fixtures_label_sequence_map_based_on_state_alphabet(src_matrix_checker_type,
                    char_matrix.default_state_alphabet)
        standard_file_test_chars.general_char_matrix_checker(
                self,
                char_matrix,
                src_matrix_checker_type,
                check_taxon_annotations=self.check_taxon_annotations,
                check_matrix_annotations=self.check_matrix_annotations,
                check_sequence_annotations=self.check_sequence_annotations,
                check_column_annotations=self.check_column_annotations,
                check_cell_annotations=self.check_cell_annotations,)

    def test_basic_nexus_chars(self):
        for src_filename, matrix_type, src_matrix_checker_type in self.__class__.srcs:
            src_path = pathmap.char_source_path(src_filename)
            d1 = matrix_type.get_from_path(src_path, "nexus")
            s = self.write_out_validate_equal_and_return(
                    d1, "nexus", {})
            d2 = matrix_type.get_from_string(s, "nexus")
            self.verify_char_matrix(d2, src_matrix_checker_type)

if __name__ == "__main__":
    unittest.main()
