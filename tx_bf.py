import scipy.special
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Transmitter
N = np.power(10, 6)

# Let's generate random bits with equal probability
m = np.random.random((1, N)) > .5

# BPSK moduation
s = 2*m-1
nTx = 2

# define Eb/N0 values
EbN = np.linspace(0, 35, 36)

nE1 = []
nE2 = []

for ii in range(0, len(EbN)):

    # generate white gaussian noise with 0dB variance
    n = (1/np.sqrt(2))*np.random.randn(1, N) + 1j * np.random.randn(1, N)
    # generate rayleigh channel
    h = (1/np.sqrt(2))*np.random.randn(nTx, N) + 1j * np.random.randn(nTx, N)
    h_effective = np.multiply(h, np.exp(-1j*np.angle(h)))
    # compute kronecker tensor product
    sr = (1/np.sqrt(nTx))*np.kron(np.ones((nTx, 1)), s)

    # channel and noise noise addition
    y1 = np.sum(np.multiply(h, sr), 0) + np.power(10, -1 * (EbN[ii] / 20)) * n
    y2 = np.sum(np.multiply(h_effective, sr), 0) + np.power(10, -1 * (EbN[ii] / 20)) * n

    # Receiver

    # equalization
    y1eq = np.divide(y1, np.sum(h, 0))
    y2eq = np.divide(y2, np.sum(h_effective, 0))

    # hard decision decoding
    m1est = np.real(y1eq) > 0
    m2est = np.real(y2eq) > 0

    # counting the errors
    nE1.append(np.sum(m ^ m1est))
    nE2.append(np.sum(m ^ m2est))

realBer1 = np.divide(nE1, N)  # real ber (no beamforming)
realBer2 = np.divide(nE2, N)  # real ber (with beamforming)

theoryBerAWGN = []
for eb in EbN:
    # theoretical AWGN ber
    theoryBerAWGN.append(0.5*scipy.special.erfc(np.sqrt(np.power(10, eb/10))))

EbNLin = np.power(10, np.divide(EbN, 10))
theoryBer = []
theoryBer_mrc = []

for eb in EbNLin:
    theoryBer.append(0.5*(1-np.sqrt(np.divide(eb, (eb+1)))))
    p = 1/2 - 1/2 * np.power((1 + 1/eb), -1/2)
    theoryBer_mrc.append(np.power(p, 2)*(1+2*(1-p)))

plt.semilogy(EbN, theoryBer, 'k--', label="1x1 SISO Expected")
plt.semilogy(EbN, realBer1, 'b-', label="1x2 MIMO No beamforming")
plt.semilogy(EbN, theoryBer_mrc, 'r', label="2x1 MIMO MRC expected")
plt.semilogy(EbN, realBer2, 'g+', label="1x2 MIMO w/ Tx Beamforming")

plt.xlabel('Eb/N0, dB')
plt.ylabel('Bit Error Rate')
plt.title('BER for BPSK modulation in Rayleigh channel')
plt.grid(True)
legend = plt.legend(loc='upper right', shadow=True)
plt.show()
