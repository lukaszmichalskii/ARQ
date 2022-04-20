from typing import Union

import komm
from numpy import ndarray

from arq.arq_service.error_detecting_codes.error_detecting_codes import *
from config import Config


def split_into_packets(data: np.array, packetLength) -> np.ndarray:
    if data.size % packetLength != 0:
        missing_elements_to_valid_block_size = packetLength - data.size % packetLength
        for element in range(0, missing_elements_to_valid_block_size):
            data = np.insert(data, 0, 0)
    packets = np.array_split(data, data.size / packetLength)
    return packets


def encode(packet: np.ndarray, codeType) -> Union[np.ndarray, list]:
    if codeType == 1:
        return errorDetectingCodes.parity_check_encode(packet)
    if codeType == 2:
        crc = errorDetectingCodes.CyclicRedundancyCheck()
        return crc.encode(packet)
    if codeType == 3:
        lrc = errorDetectingCodes.LongitudinalRedundancyCheck()
        return lrc.encode(packet)
    if codeType == 4:
        fletcher = errorDetectingCodes.FletcherChecksum()
        return fletcher.encode(packet)
    print("Wrong code number, returned without encoding")
    return packet


def channel_transmission(packet: Union[np.ndarray, list], errorProbability, codeType, channelType) -> Union[np.ndarray, list]:
    if codeType == 1 or codeType == 2:
        if channelType == 1:
            bsc = komm.BinarySymmetricChannel(errorProbability)
            return bsc(packet)
        if channelType == 2:
            bec = komm.BinaryErasureChannel(errorProbability)
            array = bec(packet)
            array = array[array != 2]
            return array
        print("Wrong channel type number, returning same values")
        return packet

    if codeType == 3 or codeType == 4:
        bsc = komm.BinarySymmetricChannel(errorProbability)
        if channelType == 1:
            arrays = []
            for array in packet:
                arrays.append(bsc(array))
            return arrays
        if channelType == 2:
            bec = komm.BinaryErasureChannel(errorProbability)
            arrays = []
            for array in packet:
                array = bec(array)
                array = array[array != 2]
                arrays.append(array)
            return arrays
        print("Wrong channel type number, returning same values")
        return packet
    print("Wrong code number, returning same values")
    return packet


def code_check(packet: Union[np.ndarray, list], codeType) -> bool:
    if codeType == 1:
        return errorDetectingCodes.parity_check_decode(packet)
    if codeType == 2:
        crc = errorDetectingCodes.CyclicRedundancyCheck()
        return crc.check(packet)
    if codeType == 3:
        lrc = errorDetectingCodes.LongitudinalRedundancyCheck()
        return lrc.check(packet)
    if codeType == 4:
        fletcher = errorDetectingCodes.FletcherChecksum()
        return fletcher.check(packet)


def simulation(dataLength, packetLength, codeType, errorProbablity, channelType):
    data = np.random.randint(0, 2, dataLength)
    packets = split_into_packets(data, packetLength)

    # Simulation outputs
    packetsSuccessfullysent = 0
    repeatedPackets = 0
    undetectedErrors = 0

    for ndarray in packets:
        counter = 0
        while (True):
            packetEncoded = encode(ndarray, codeType)
            packetSent = channel_transmission(packetEncoded, errorProbablity, codeType, channelType)
            if code_check(packetSent, codeType):
                if np.array_equal(packetSent, packetEncoded):
                    if counter == 0:
                        packetsSuccessfullysent += 1
                    break
                else:
                    if counter == 0:
                        undetectedErrors += 1
                    break
            else:
                if counter == 0:
                    counter+=1
                    repeatedPackets += 1
    print("Packets successfully sent: ", packetsSuccessfullysent)
    print("Repeated packets: ", repeatedPackets)
    print("Undetected errors: ", undetectedErrors)