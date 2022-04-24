from typing import Union

import komm
from numpy import ndarray

from arq.arq_service.error_detecting_codes.error_detecting_codes import *
from config import Config


def split_into_packets(data: np.array, packet_length) -> np.ndarray:
    if data.size % packet_length != 0:
        missing_elements_to_valid_block_size = packet_length - data.size % packet_length
        for element in range(0, missing_elements_to_valid_block_size):
            data = np.insert(data, 0, 0)
    packets = np.array_split(data, data.size / packet_length)
    return packets


def encode(packet: np.ndarray, code_type) -> Union[ndarray, list]:
    if code_type == 1:
        return parity_check_encode(packet)
    if code_type == 2:
        crc = CyclicRedundancyCheck()
        return crc.encode(packet)
    if code_type == 3:
        lrc = LongitudinalRedundancyCheck()
        return lrc.encode(packet)
    if code_type == 4:
        fletcher = FletcherChecksum()
        return fletcher.encode(packet)
    print("Wrong code number, returned without encoding")
    return packet


def channel_transmission(packet: Union[np.ndarray, list], error_probability, code_type, channel_type) -> Union[np.ndarray, list]:
    if code_type == 1 or code_type == 2:
        if channel_type == 1:
            bsc = komm.BinarySymmetricChannel(error_probability)
            return bsc(packet)
        if channel_type == 2:
            bec = komm.BinaryErasureChannel(error_probability)
            array = bec(packet)
            array = array[array != 2]
            return array
        print("Wrong channel type number, returning same values")
        return packet

    if code_type == 3 or code_type == 4:
        bsc = komm.BinarySymmetricChannel(error_probability)
        if channel_type == 1:
            arrays = []
            for array in packet:
                arrays.append(bsc(array))
            return arrays
        if channel_type == 2:
            bec = komm.BinaryErasureChannel(error_probability)
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


def code_check(packet: Union[np.ndarray, list], code_type) -> bool:
    if code_type == 1:
        return parity_check_decode(packet)
    if code_type == 2:
        crc = CyclicRedundancyCheck()
        return crc.check(packet)
    if code_type == 3:
        lrc = LongitudinalRedundancyCheck()
        return lrc.check(packet)
    if code_type == 4:
        fletcher = FletcherChecksum()
        return fletcher.check(packet)


def check_undetected_errors( original_packet: Union[np.ndarray], delivered_packet: Union[np.ndarray], code_type) -> bool:
    counter = 0
    if code_type == 1 or code_type == 2:
        return np.array_equal(original_packet, delivered_packet)
    if code_type == 3 or code_type == 4:
        for array in delivered_packet:
            if not np.array_equal(original_packet[counter-1], array):
                return False
            counter += 1


def simulation(data_length, packet_length, code_type, error_probability, channel_type):
    data = np.random.randint(0, 2, data_length)
    packets = split_into_packets(data, packet_length)

    # Simulation outputs
    packets_successfully_sent = 0
    repeated_packets = 0
    undetected_errors = 0

    for array in packets:
        counter = 0
        while (True):
            packet_encoded = encode(array, code_type)
            packet_sent = channel_transmission(packet_encoded, error_probability, code_type, channel_type)
            if code_check(packet_sent, code_type):
                if check_undetected_errors(packet_encoded, packet_sent, code_type):
                    if counter == 0:
                        packets_successfully_sent += 1
                    break
                else:
                    if counter == 0:
                        undetected_errors += 1
                    break
            else:
                if counter == 0:
                    counter += 1
                    repeated_packets += 1

    return {"PacketSuccessfullySent": packets_successfully_sent,
            "RepeatedPackets": repeated_packets,
            "UndetectedErrors": undetected_errors}


if __name__ == '__main__':
    results = simulation(Config.DATA_LENGTH,
                         Config.PACKET_LENGTH,
                         Config.ERROR_DETECTING_METHOD.get("ParityCheck"),
                         Config.ERROR_PROBABILITY,
                         Config.CHANNEL_TYPE.get("BinaryErasureChannel"))

    print("Packet successfully sent: {}\nRepeated packets: {}\nUndetected errors: {}".format(results.get("PacketSuccessfullySent"),
                                                                                             results.get("RepeatedPackets"),
                                                                                             results.get("UndetectedErrors")))