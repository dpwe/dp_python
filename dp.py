# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%matplotlib inline

# <codecell>

cd /Users/dpwe/projects/millionsong/python/midi-dataset

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import dpcore

# <codecell>

reload(dpcore)

# <codecell>

M = np.random.rand(50,50)
plt.imshow(M, interpolation='none', cmap='binary')

# <codecell>

%timeit DC, phiC = dpcore.dpcore(M, 0.2, True)
%timeit DP, phiP = dpcore.dpcore(M, 0.2, False)

# <codecell>

DC, phiC = dpcore.dpcore(M, 0.2, True)
DP, phiP = dpcore.dpcore(M, 0.2, False)

# <codecell>

plt.imshow(DC,interpolation='none')

# <codecell>

plt.imshow(DC-DP, interpolation='none')
print np.max(np.abs(DC-DP))

# <codecell>

plt.imshow(phiC-phiP, interpolation='none')

# <codecell>

MM = np.random.rand(5, 5)
pen = 0.2
gut = 0.3
p,q,C,phi = dpcore.dp(MM, pen, gut)
print p, q
print MM
print C
print "best cost =", C[p[-1],q[-1]], "=", np.sum(MM[p, q])+pen*(np.sum(phi[p, q]>0))
plt.imshow(MM, interpolation='none', cmap='binary')
plt.hold(True)
plt.plot(q,p,'-r')
plt.hold(False)
plt.show()

# <codecell>

M2 = np.copy(M)
M2[20:30,20:30] += np.random.rand(10,10)
M2[10:40,10:40] += np.random.rand(30,30)
plt.imshow(M2, interpolation='none', cmap='binary')
p,q,C,phi = dpcore.dp(M2,0.1,0.1)
plt.hold(True)
plt.plot(q,p,'-r')
plt.hold(False)
plt.show()

# <codecell>

import librosa

# <codecell>

# Mirror matlab example from http://www.ee.columbia.edu/ln/rosa/matlab/dtw/
d1, sr = librosa.load('/Users/dpwe/projects/dtw/sm1_cln.wav', sr=16000)
d2, sr = librosa.load('/Users/dpwe/projects/dtw/sm2_cln.wav', sr=16000)
D1 = librosa.stft(d1, n_fft=512, hop_length=128)
D2 = librosa.stft(d2, n_fft=512, hop_length=128)
librosa.display.specshow(20*np.log10(np.abs(D1)), sr=sr, hop_length=128)

# <codecell>

# Cosine similarity matrix (slow one-liner)
SM = np.array([[np.sum(a*b)/np.sqrt(np.sum(a**2)*np.sum(b**2)) for b in np.abs(D2.T)] for a in np.abs(D1.T)])

# <codecell>

plt.imshow(SM)

# <codecell>

p, q, C, phi = dpcore.dp(1-SM)

# <codecell>

plt.imshow(SM, interpolation='none', cmap='binary')
plt.hold(True)
plt.plot(q,p,'-r')
plt.hold(False)
plt.show()

# <codecell>

C[-1,-1]

# <codecell>


