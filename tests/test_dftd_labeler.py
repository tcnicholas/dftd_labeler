import os
import unittest
from dftd_labeler import (
    generate_index_filename,
    write_last_index,
)


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
EXAMPLE_XYZ_PATH = os.path.join(DATA_DIR, 'h.xyz')


class TestDFTDBProcessor(unittest.TestCase):

    def setUp(self):
        # Set up any pre-test conditions here
        pass

    def test_generate_index_filename(self):
        input_path = "input.extxyz"
        output_path = "output.extxyz"
        expected_filename = "last_processed_index_5c13d356b0f3a6df34797d55f88c168d.txt"
        self.assertEqual(generate_index_filename(input_path, output_path), expected_filename)

    def test_write_last_index(self):
        index_file = "test_index_file.txt"
        input_path = "input.extxyz"
        output_path = "output.extxyz"
        idx = 5
        write_last_index(index_file, input_path, output_path, idx)
        with open(index_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(lines[0].strip(), "Input: input.extxyz")
            self.assertEqual(lines[1].strip(), "Output: output.extxyz")
            self.assertEqual(lines[2].strip(), "5")

    # You can add more tests here for other utility functions, and logic checks

    def tearDown(self):
        # Clean up any post-test conditions here, like removing created files etc.
        pass


if __name__ == '__main__':
    unittest.main()
