McEliece cryptosystem implementation by vovuas2003
New repository after 28.11.2024: https://meowgit.nekoea.red/C01-119/McEliece_App

Required additional Python libraries: numpy, galois (numpy extension).

UPDATE: version 2 is available. Check cryptosystem_core_v2 and McEliece_console_v2.

All cryptosystem functions are implemented in cryptosystem_core.py, just import it into your project and enjoy!
For example, I coded a console menu (that works with text in txt files and also with any files in binary mode) and a GUI app (for text encryption).

It is possible to build portable exe with pyinstaller and run code on a computer that does not have Python installed.
But it is NOT compilation, so exe file will be quite large.

The pdf presentation in Russian contains a bit of theory about the Mceliece cryptosystem.
icon.ico is an optional file for pyinstaller
old_portable.py can support another order of galois field, but saves raw integers and does not specify utf-8 encoding for strings and txt files
