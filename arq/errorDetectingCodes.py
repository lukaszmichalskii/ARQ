import numpy as np


def parity_check_encode(array: np.ndarray) -> np.ndarray:
    number_of_ones = 0
    for element in array:
        if element:
            number_of_ones += 1
    if number_of_ones % 2 == 0:
        return np.append(array, 0)
    else:
        return np.append(array, 1)


def parity_check_decode(array: np.ndarray) -> bool:
    if array.size > 1:
        number_of_ones = 0
        for element in array:
            if element:
                number_of_ones += 1
        if number_of_ones % 2 == 0:
            return True
        else:
            return False


class CyclicRedundancyCheck:
    def __init__(self):
        self.__polynomial = np.array([1, 1, 0, 0, 1, 1, 0, 0, 1])
        self.__number_of_bits = 8

    def encode(self, array: np.ndarray) -> np.ndarray:
        data_array = np.append(array, np.full(self.__number_of_bits, 0))
        integer_value_of_array = data_array.dot(2 ** np.arange(data_array.size)[::-1])
        divisor = np.append(self.__polynomial, np.full(data_array.size - self.__polynomial.size, 0))
        integer_value_of_divisor = divisor.dot(2**np.arange(divisor.size)[::-1])

        while integer_value_of_array > (2 ** self.__number_of_bits - 1):
            if integer_value_of_divisor <= ((2 ** (np.floor(np.log2(integer_value_of_array))+1)) - 1):
                integer_value_of_array = integer_value_of_array ^ integer_value_of_divisor
            integer_value_of_divisor = integer_value_of_divisor >> 1

        crc_code = np.fromstring(np.binary_repr(integer_value_of_array).zfill(self.__number_of_bits), dtype='S1').astype(int)
        return np.append(array, crc_code)

    def check(self, array: np.ndarray) -> bool:
        if array.size > self.__number_of_bits:
            integer_value_of_array = (array.dot(2 ** np.arange(array.size)[::-1]))
            divisor = np.append(self.__polynomial, np.full(array.size - self.__polynomial.size, 0))
            integer_value_of_divisor = divisor.dot(2 ** np.arange(divisor.size)[::-1])

            while integer_value_of_array > (2 ** self.__number_of_bits - 1):
                if integer_value_of_divisor <= ((2 ** (np.floor(np.log2(integer_value_of_array)) + 1)) - 1):
                    integer_value_of_array = integer_value_of_array ^ integer_value_of_divisor
                integer_value_of_divisor = integer_value_of_divisor >> 1

            if integer_value_of_array == 0:
                return True
            else:
                return False
        else:
            return False


class LongitudinalRedundancyCheck:
    def __init__(self):
        self.__block_size = 8

    def encode(self, array: np.ndarray) -> list:
        if array.size % self.__block_size != 0:
            missing_elements_to_valid_block_size = self.__block_size - array.size % self.__block_size
            for element in range(0, missing_elements_to_valid_block_size):
                array = np.insert(array, 0, 0)

        array = np.split(array, array.size/self.__block_size)
        rows_of_array = len(array)
        parity_row = np.zeros(self.__block_size, dtype=int)
        for column in range(0, self.__block_size):
            number_of_ones = 0
            for row in range(0, rows_of_array):
                if array[row][column]:
                    number_of_ones += 1

            if number_of_ones % 2 != 0:
                parity_row[column] = 1
        array.append(parity_row)
        return array

    def check(self, array: list) -> bool:
        for ndarray in array:
            if ndarray.size != self.__block_size:
                return False

        rows_of_array = len(array)
        for column in range(0, self.__block_size):
            number_of_ones = 0
            for row in range(0, rows_of_array):
                if array[row][column]:
                    number_of_ones += 1

            if number_of_ones % 2 != 0:
                return False

        return True


class FletcherChecksum:

    def __init__(self):
        self.__data_block_size = 8

    def encode(self, array: np.ndarray) -> list:
        checksum1, checksum2 = 0, 0
        if array.size % self.__data_block_size != 0:
            missing_elements_to_valid_block_size = self.__data_block_size - array.size % self.__data_block_size
            for element in range(0, missing_elements_to_valid_block_size):
                array = np.insert(array, 0, 0)

        array = np.split(array, array.size/self.__data_block_size)
        for ndarray in array:
            integer_value_of_data_block = ndarray.dot(2 ** np.arange(ndarray.size)[::-1])
            checksum1 += integer_value_of_data_block
            checksum2 += checksum1
        checksum1 = checksum1 % (2 ** self.__data_block_size)
        checksum2 = checksum2 % (2 ** self.__data_block_size)
        checksum1 = np.fromstring(np.binary_repr(checksum1).zfill(8), dtype='S1').astype(int)
        checksum2 = np.fromstring(np.binary_repr(checksum2).zfill(8), dtype='S1').astype(int)
        checksum = np.concatenate((checksum1, checksum2))
        array.append(checksum)
        return array

    def check(self, array: list) -> bool:
        checksum1, checksum2 = 0, 0
        rows_of_array = len(array) - 1
        for ndarray in array[:rows_of_array]:
            integer_value_of_data_block = ndarray.dot(2 ** np.arange(ndarray.size)[::-1])
            checksum1 += integer_value_of_data_block
            checksum2 += checksum1

        correct_checksum = array[rows_of_array]
        correct_checksum = np.split(correct_checksum, 2)

        correct_checksum1 = correct_checksum[0].dot(2 ** np.arange(correct_checksum[0].size)[::-1])
        checksum1 = checksum1 % (2 ** self.__data_block_size)
        if checksum1 != correct_checksum1:
            return False

        correct_checksum2 = correct_checksum[1].dot(2 ** np.arange(correct_checksum[1].size)[::-1])
        checksum2 = checksum2 % (2 ** self.__data_block_size)
        if checksum2 != correct_checksum2:
            return False

        return True
