import numpy as np

import simulation
# ==================== Simulation Parameters ====================

#   Długość zawartości do przesłania

dataLength = 100

#   Długość pakietu
packetLength = 20

#   Prawdopodobieństwo błędu 0<ϵ<1
errorProbability = 0.1

'''
    Rodzaj kanału:
        > (1) - Binary Symmetric Channel
        > (2) - Binary Erasure Channel
'''
channelType = 2

'''
    Typ kodowania:
        > (1) - Parity Check
        > (2) - Cyclic Redundancy Check
        > (3) - Longitudinal Redundancy Check
        > (4) - Fletcher's Checksum
'''
codeType = 1

# ===============================================================


if __name__ == '__main__':
    simulation.simulation(dataLength, packetLength, codeType, errorProbability, channelType)
    pass
