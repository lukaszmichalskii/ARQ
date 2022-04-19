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


def encode(packet: np.ndarray, codeType) -> Union[ndarray, list]:
    if codeType == 1:
        return parity_check_encode(packet)
    if codeType == 2:
        crc = CyclicRedundancyCheck()
        return crc.encode(packet)
    if codeType == 3:
        lrc = LongitudinalRedundancyCheck()
        return lrc.encode(packet)
    if codeType == 4:
        fletcher = FletcherChecksum()
        return fletcher.encode(packet)
    print("Wrong code number, returned without encoding")
    return packet


def channel_transmission(packet: np.ndarray, errorProbability, channelType) -> np.ndarray:
    if channelType == 1:
        bsc = komm.BinarySymmetricChannel(errorProbability)
        return bsc(packet)
    if channelType == 2:
        bec = komm.BinaryErasureChannel(errorProbability)
        return bec(packet)
    print("Wrong channel type number, returning same values")
    return packet


def code_check(packet: np.ndarray, codeType) -> bool:
    if codeType == 1:
        return parity_check_decode(packet)
    if codeType == 2:
        crc = CyclicRedundancyCheck()
        return crc.check(packet)
    if codeType == 3:
        lrc = LongitudinalRedundancyCheck()
        return lrc.check(packet)
    if codeType == 4:
        fletcher = FletcherChecksum()
        return fletcher.check(packet)

'''def code_check(packet: list, codeType) -> bool:
    if codeType == 3:
        lrc = errorDetectingCodes.LongitudinalRedundancyCheck()
        return lrc.check(packet)
    if codeType == 4:
        fletcher = errorDetectingCodes.FletcherChecksum()
        return fletcher.check(packet)'''


def simulation(data_length, packet_length, error_detecting_method, error_probablity, channel_type):
    data = np.random.randint(0, 2, data_length)
    packets = split_into_packets(data, packet_length)

    # Simulation outputs
    packets_successfully_sent = 0
    repeated_packets = 0
    undetected_errors = 0

    for ndarray in packets:
        counter = 0
        while (True):
            packet_encoded = encode(ndarray, error_detecting_method)
            packet_sent = channel_transmission(packet_encoded, error_probablity, channel_type)
            if code_check(packet_sent, error_detecting_method):
                comparison = packet_sent == packet_encoded
                statement = comparison.all()
                if statement:
                    if counter == 0:
                        packets_successfully_sent += 1
                    break
                else:
                    if counter == 0:
                        undetected_errors += 1
                    break
            else:
                if counter == 0:
                    counter+=1
                    repeated_packets += 1

    return {"PacketSuccessfullySent": packets_successfully_sent,
            "RepeatedPackets": repeated_packets,
            "UndetectedErrors": undetected_errors }


if __name__ == '__main__':
    results = simulation(Config.DATA_LENGTH,
                         Config.PACKET_LENGTH,
                         Config.ERROR_DETECTING_METHOD.get("ParityCheck"),
                         Config.ERROR_PROBABILITY,
                         Config.CHANNEL_TYPE.get("BinaryErasureChannel"))

    print("Packet successfully sent: {}\nRepeated packets: {}\nUndetected errors: {}".format(results.get("PacketSuccessfullySent"),
                                                                                             results.get("RepeatedPackets"),
                                                                                             results.get("UndetectedErrors")))
