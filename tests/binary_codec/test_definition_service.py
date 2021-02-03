import unittest

import xrpl.binary_codec.definitions.definitions as definitions


class TestDefinitionService(unittest.TestCase):
    def setUp(self):
        self.test_field_name = "Sequence"

    def test_load_definitions(self):
        expected_keys = ["TYPES", "FIELDS", "TRANSACTION_RESULTS", "TRANSACTION_TYPES"]
        for key in expected_keys:
            self.assertIn(key, definitions.DEFINITIONS)

    def test_inverse_transaction_type_map(self):
        transaction_type_code = 8
        expected_transaction_type = "OfferCancel"
        transaction_type = definitions.TRANSACTION_TYPE_CODE_TO_STR_MAP[
            transaction_type_code
        ]
        self.assertEqual(expected_transaction_type, transaction_type)

    def test_inverse_transaction_result_map(self):
        transaction_result_code = 0
        expected_transaction_result = "tesSUCCESS"
        transaction_result = definitions.TRANSACTION_RESULTS_CODE_TO_STR_MAP[
            transaction_result_code
        ]
        self.assertEqual(expected_transaction_result, transaction_result)

    def test_get_field_type_name(self):
        expected_field_type_name = "UInt32"
        field_type_name = definitions.get_field_type_name(self.test_field_name)
        self.assertEqual(expected_field_type_name, field_type_name)

    def test_get_field_type_code(self):
        expected_field_type_code = 2
        field_type_code = definitions.get_field_type_code(self.test_field_name)
        self.assertEqual(expected_field_type_code, field_type_code)

    def test_get_field_code(self):
        expected_field_code = 4
        field_code = definitions.get_field_code(self.test_field_name)
        self.assertEqual(expected_field_code, field_code)

    def test_get_field_sort_key(self):
        expected_field_sort_key = (2, 4)
        field_sort_key = definitions.get_field_sort_key(self.test_field_name)
        self.assertEqual(expected_field_sort_key, field_sort_key)

    def test_get_field_header_from_name(self):
        expected_field_header = definitions.FieldHeader(2, 4)
        field_header = definitions.get_field_header_from_name(self.test_field_name)
        self.assertEqual(expected_field_header, field_header)

    def test_get_field_name_from_header(self):
        expected_field_name = self.test_field_name
        field_header = definitions.FieldHeader(2, 4)
        field_name = definitions.get_field_name_from_header(field_header)
        self.assertEqual(expected_field_name, field_name)
