#!/usr/bin/python3
from qiling import *
from qiling.const import QL_VERBOSE

from qiling.os.windows.api import *
from qiling.os.windows.const import *
from qiling.os.windows.fncc import *
from qiling.os.windows.structs import *

import base64

def customb64decode(chars, customcharset=""):
    if customcharset == "":
        return base64.b64decode(chars)
    else:
        b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        decodedset = str.maketrans(customcharset,b64charset)

        translatedstr = chars.translate(decodedset)
        return base64.b64decode(translatedstr)

# Override the generic ReadFile hook that comes with Qiling

# BOOL ReadFile(
#   HANDLE       hFile,
#   LPVOID       lpBuffer,
#   DWORD        nNumberOfBytesToRead,
#   LPDWORD      lpNumberOfBytesRead,
#   LPOVERLAPPED lpOverlapped
# );
@winsdkapi(cc=STDCALL, params={
    'hFile'                : HANDLE,
    'lpBuffer'             : LPVOID,
    'nNumberOfBytesToRead' : DWORD,
    'lpNumberOfBytesRead'  : LPDWORD,
    'lpOverlapped'         : LPOVERLAPPED
})
def my_ReadFile(ql: Qiling, address: int, params):
    hFile = params["hFile"]
    lpBuffer = params["lpBuffer"]
    nNumberOfBytesToRead = params["nNumberOfBytesToRead"]
    lpNumberOfBytesRead = params["lpNumberOfBytesRead"]

    encodedstr = ql.mem.read(0x40D160, 52) # reads encoded string
    customcharset = ql.mem.read(0x413000, 64) # reads custom b64 charset
    data = customb64decode(encodedstr.decode('ascii'), customcharset.decode('ascii'))
    print(f'Mocked input = {data}')

    ql.mem.write(lpBuffer, data + b"\x00")
    # for some reason, just using len(data) isn't long enough
    ql.mem.write(lpNumberOfBytesRead, ql.pack(len(data)+2))

    return 1

def my_sandbox(path, rootfs):
    ql = Qiling(path, rootfs, verbose=QL_VERBOSE.DEFAULT, profile='windows.ql')
    ql.set_api("ReadFile", my_ReadFile)
    ql.run(begin=0x401420, end=0x4014db)

if __name__ == '__main__':
    my_sandbox(["./challenge1.exe"], "/mnt/c/tools/qiling/examples/rootfs/x86_windows")