Transmit beamforming requires the knowledge of the channel state to compute a steering matrix that is applied to the transmitted signal to optimize reception at one or more receivers. 

Following is the MathWorks' description of what Tx Beamforming is 

"Transmit beamforming focuses energy towards a receiver to improve the SNR of a link. In this scheme the transmitter is called a beamformer and the receiver is called a beamformee. A steering matrix is used by the beamformer to direct the energy to the beamformee. The steering matrix is calculated using channel state information obtained through channel measurements. In IEEE 802.11ac (WiFi) these measurements are obtained by sounding the channel between beamformer and beamformee. To sound the channel the beamformer sends an NDP (Null Data Packet) to the beamformee. The beamformee uses the channel information provided by sounding to calculate a feedback matrix. This matrix is fedback to the beamformer in a compressed format. The beamformer can then use the feedback matrix to create a steering matrix and beamform transmissions to the beamformee."

This repository provides a simple Pyhton implementation of a Tx beamforming scheme where the channel information is utilized on the transmitting side in a MIMO setting. 

## Channel and Noise Model

1. It will be assumed that the channel is a flat fading Rayleigh multipath channel (single tap) which means that the 
convolution operation reduces to a simple multiplication.

2. Note that we will have 1 receive antenna and 2 transmit antennas (1x2 MIMO) for the sake our simulation in case Tx 
beamforming is applied and we will assume that the channels between each tx-rx pair (h1 and h2) are independent of each other 
and known at each Tx antenna. 

3. The channel seen by each Rx antenna is randomly varying in time. 

4. Noise on each Rx antenna has Gaussian PDF with zero-mean and N0/2 variance.  

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq6.PNG) ![, ](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq7.PNG) ![, ](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq8.PNG)  

## Receiver

On the receiving antenna, the signal "y" can be written as

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq1.PNG)

where 

y is the received symbol,
h1, h2 are the channels on the transmit antennas,
x is the transmitted symbol and
n is the noise on the receive antenna.

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/txbf_beam_steering.png)

## Tx Beamforming 

The idea behind the Tx beamforming is that we multiply the symbol "x" at each Tx antenna with the inverse of the phase of the 
corresponding channel to make sure the signals are constructively added at the receiving antenna. In that case, the received 
signal becomes,

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq2.PNG)

where 

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq3.PNG)

Hence, the signal at the receiver becomes

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq4.PNG)

for equalization, we need to divide the received symbol "y" with the new channel, 

![](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/eq5.PNG)

## Conclusion

1x2 MIMO (2 tx by 1 rx) simulation result shows that repeating the same information on two antennas did not provide diversity gain.
That is simply because adding two channels result in again a Rayleigh channel. Hence the results is same as the 1 by 1 SISO BER 
performance. 

On the other hand, utilizing the channel information at the transmitter to align phases at the receiver provided diversity gain. 
Its performance is close to Maximum Ratio Combining receiver (1 tx by 2 rx antennas) where the signals at two receiving antennas are combined to get the 
maximum SNR.

![BER for BPSK in Rayleigh channel](https://github.com/tayyarg/dspbox/blob/master/tx_beamforming/images/txbf_ber.png)
