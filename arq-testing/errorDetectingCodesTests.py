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
        array = np.array([0])
        self.assertFalse(parity_check_decode(array))

class CyclicRedundancyCheckTest(unittest.TestCase):

    def test_packet_encoding(self):
        crc = CyclicRedundancyCheck()
        array = np.array([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0])
        array = crc.encode(array)
        correct_array = np.array([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1])
        self.assertTrue((array == correct_array).all())

    def test_packet_check(self):
        crc = CyclicRedundancyCheck()
        array = np.array([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1])
        self.assertTrue(crc.check(array))

        array[4] = 1
        self.assertFalse(crc.check(array))
        array[5] = 2
        array[6] = 2
        self.assertFalse(crc.check(array))

        array = np.array([1, 0, 1, 0, 1, 1])
        self.assertFalse(crc.check(array))




if __name__ == '__main__':
    unittest.main()
