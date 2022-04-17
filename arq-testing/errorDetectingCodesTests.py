import unittest
from arq.errorDetectingCodes import *

class ParityCheckTest(unittest.TestCase):

    def test_packet_encoding(self):
        array = np.array([1, 0, 1, 0, 0, 0, 1])
        encoded_array = parity_check_encode(array)
        correct_array = np.array([1, 0, 1, 0, 0, 0, 1, 1])
        self.assertTrue((encoded_array == correct_array).all())

        array = np.array([1, 1, 0, 1, 0, 0, 1])
        encoded_array = parity_check_encode(array)
        correct_array = np.array([1, 1, 0, 1, 0, 0, 1, 0])
        self.assertTrue((encoded_array == correct_array).all())

    def test_packet_decoding(self):
        array = np.array([1, 0, 1, 0, 0, 0, 1, 1])
        self.assertTrue(parity_check_decode(array))

        array = np.array([1, 1, 0, 1, 0, 0, 1, 0])
        self.assertTrue(parity_check_decode(array))

        array[2] = 1
        self.assertFalse(parity_check_decode(array))

if __name__ == '__main__':
    unittest.main()
