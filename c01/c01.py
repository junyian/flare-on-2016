#!/usr/bin/python3
import base64

# custom base64 shamelessly copied from
# https://github.com/kingaling/custombase64/blob/master/custombase64.py
# and adapted to Python3

b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
cucharset  = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"

decodedset = str.maketrans(cucharset,b64charset)

str = "x2dtJEOmyjacxDemx2eczT5cVS9fVUGvWTuZWjuexjRqy24rV29q"

translatedstr = str.translate(decodedset)
decodedstr = base64.b64decode(translatedstr)
print(decodedstr)
