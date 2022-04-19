import unittest
from arq.errorDetectingCodes import *


class TestParityCheck(unittest.TestCase):

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


class TestCyclicRedundancyCheck(unittest.TestCase):

    def test_packet_encoding(self):
        crc = CyclicRedundancyCheck()
        array = np.array([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0])
        array = crc.encode(array)
        correct_array = np.array([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1])
        self.assertTrue((array == correct_array).all())

        array = np.array([0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1])
        correct_array = np.array([0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1])
        array = crc.encode(array)
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


class TestLongitudinalRedundancyCheck(unittest.TestCase):

    def test_packet_encoding(self):
        lrc = LongitudinalRedundancyCheck()
        array = np.array([1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1])
        encoded_correct_array = [
            np.array([1, 1, 1, 0, 0, 1, 1, 1]),
            np.array([1, 1, 0, 1, 1, 1, 0, 1]),
            np.array([0, 0, 1, 1, 1, 0, 0, 1]),
            np.array([1, 0, 1, 0, 1, 0, 0, 1]),
            np.array([1, 0, 1, 0, 1, 0, 1, 0])
        ]
        array = lrc.encode(array)
        for index in range(0, 5):
            self.assertTrue((array[index] == encoded_correct_array[index]).all())

    def test_packet_check(self):
        lrc = LongitudinalRedundancyCheck()
        array = [
            np.array([1, 1, 1, 0, 0, 1, 1, 1]),
            np.array([1, 1, 0, 1, 1, 1, 0, 1]),
            np.array([0, 0, 1, 1, 1, 0, 0, 1]),
            np.array([1, 0, 1, 0, 1, 0, 0, 1]),
            np.array([1, 0, 1, 0, 1, 0, 1, 0])]
        self.assertTrue(lrc.check(array))

        array[0][4] = 1
        array[3][2] = 1
        self.assertFalse(lrc.check(array))

        array = [
            np.array([0, 1, 1, 1, 1]),
            np.array([0, 1, 1, 1, 1, 0, 0]),
            np.array([0, 1, 0, 1, 0, 1, 0]),
            np.array([1, 0, 1, 0, 0, 0, 1]),
            np.array([1, 1, 1, 1, 0, 0])
        ]
        self.assertFalse(lrc.check(array))


class TestFletcherChecksum(unittest.TestCase):

    def test_packet_decoding(self):
        fch = FletcherChecksum()
        array = np.array([1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0])
        array = fch.encode(array)

        encoded_correct_array = [
            np.array([1, 0, 1, 0, 0, 0, 1, 1]),
            np.array([1, 1, 0, 0, 1, 0, 0, 0]),
            np.array([0, 0, 0, 1, 0, 0, 1, 1]),
            np.array([0, 1, 0, 0, 1, 0, 1, 0]),
            np.array([0, 1, 0, 1, 1, 0, 0, 0]),
            np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0])
        ]

        for index in range(0, 6):
            self.assertTrue((array[index] == encoded_correct_array[index]).all())

    def test_packet_check(self):
        fch = FletcherChecksum()
        array = [
            np.array([1, 0, 1, 0, 0, 0, 1, 1]),
            np.array([1, 1, 0, 0, 1, 0, 0, 0]),
            np.array([0, 0, 0, 1, 0, 0, 1, 1]),
            np.array([0, 1, 0, 0, 1, 0, 1, 0]),
            np.array([0, 1, 0, 1, 1, 0, 0, 0]),
            np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0])
        ]
        self.assertTrue(fch.check(array))

        array[0][1] = 1
        array[5][3] = 1
        self.assertFalse(fch.check(array))

        array = [
            np.array([1, 0, 1, 0, 0, 0, 1, 1]),
            np.array([1, 1, 0, 0, 1, 0, 0, 0]),
            np.array([0, 0, 0, 1, 0, 0]),
            np.array([0, 1, 0, 0]),
            np.array([0, 1, 0, 1, 0, 0]),
            np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1])
        ]
        self.assertFalse(fch.check(array))


if __name__ == '__main__':
    unittest.main()
