McEliece cryptosystem implementation

Usage:
0. pip install numpy and galois
1. generate.py - generate and save public and private keys
2. send pubkey.py and encode.py to your friend
3. your friend runs encode.py, write secret string and send message.py to you
4. decode.py - get secret string

Hacker can get your private key if he will know a half of it (and pubkey.py, decode.py and Reed-Solomon algo).
Check break.py to understand how hacker can do this.

todo: check randomization during encode (add vector z, check https://en.wikipedia.org/wiki/McEliece_cryptosystem)