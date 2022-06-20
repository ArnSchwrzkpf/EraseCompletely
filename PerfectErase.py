# PerfectErase PY
import os
import sys
import random
def overWriteSpecific(filePath, data):
    contentLength = os.path.getsize(filePath)
    with open(filePath, "r+b") as f:
        for i in range(contentLength):
            f.write(data)
        f.flush()
def overWriteRandom(filePath):
    contentLength = os.path.getsize(filePath)
    with open(filePath, "r+b") as f:
        for i in range(contentLength):
            data = random.randrange(256).to_bytes(1, 'little')
            f.write(data)
        f.flush()
if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        overWriteSpecific(args[1], b'\x00')
        overWriteSpecific(args[1], b'\xff')
        overWriteRandom(args[1])
