McEliece cryptosystem implementation

Update: portable version is available! All functions in one file. New features and some improvements!

Usage:
0. pip install numpy and galois
1. generate.py - generate and save public and private keys
2. send pubkey.py and encode.py to your friend
3. your friend runs encode.py, write secret string and send message.py to you
4. decode.py - get secret string

Hacker can get your private key if he will know a half of it (and pubkey.py, decode.py and Reed-Solomon algo).
Check break.py to understand how hacker can do this.

todo:
0. build portable exe with pyinstaller
1. left part of G is E, because we use Reed-Solomon algo; so left part of S @ G is S and cutting right colomns works; my_fix(G) returns E and in break_S we needn't get inv(G), just S = my_fix(G_ @ inv(P)); try break_S with another (not Reed-Solomon) code (matrix G will be different; will my_fix(G) and my_fix(G_) return nonsingular matrices?; of course, rank(G) = rank(G_) = k and we can iterate through all possible combinations of column deletions and find one that does not lead to nonsingular matrices); another way to get S is calculating it row by row (solving k systems, each has n equations with k variables, k < n, but we need to do it in Galois Field)
2. DONE! check randomization during encode (add vector z, check https://en.wikipedia.org/wiki/McEliece_cryptosystem)
3. DONE! make presentation that explains McEliece cryptosystem
