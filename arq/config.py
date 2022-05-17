class Config:
    DATA_LENGTH = 1000
    PACKET_LENGTH = 20
    ERROR_PROBABILITY = 0.05
    CHANNEL_TYPE = {"BinarySymmetricChannel": 1,
                    "BinaryErasureChannel": 2}
    ERROR_DETECTING_METHOD = {"ParityCheck": 1,
                              "CyclicRedundancyCheck": 2,
                              "LongitudinalRedundancyCheck": 3,
                              "FletchersChecksum": 4}
