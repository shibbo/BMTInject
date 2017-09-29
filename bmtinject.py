import struct, sys

def injectBMT(in_bmd, in_bmt, out_bmd):
    with open(in_bmd, "rb") as f:
        bmdData = f.read()
    with open(in_bmt, "rb") as f:
        bmtData = f.read()

    # file verification
    # if it doesnt exist it would have thrown a trackback by now
    bmd_magic, = struct.unpack_from('>I', bmdData, 0)
    bmt_magic, = struct.unpack_from('>I', bmtData, 0)

    if bmd_magic != 0x4A334432:
        print("Not a valid BMD file.")
        return
    else:
        print("File is a valid BMD.")

    if bmt_magic != 0x4A334432:
        print("Not a valid BMT file.")
        return
    else:
        print("File is a valid BMT file.")

    print("Attempting to get BMD data...")
    print("Trying to find TEX1 section...")
    # we start at INF1
    offset = 0x20
    while(True):
        tempStr, = struct.unpack_from('4s', bmdData, offset)
        if tempStr != b'TEX1':
            tempInt, = struct.unpack_from('>I', bmdData, offset+4)
            offset+=tempInt
        elif tempStr == b'TEX1':
            print("Found TEX1!")
            bmdFullData = bytearray(bmdData[:offset])
            break
        else:
            print("Error! Found string " + str(tempStr))
            break

    print("Attempting to get BMT data...")
    bmtPos = 0x20
    bmtTEX1 = bytearray(bmtData[bmtPos:])
    print("Success!")

    print("Now writing to file...")
    with open(out_bmd, "wb") as f:
        f.write(bmdFullData)
        f.write(bmtTEX1)

    print("Done!")

if len(sys.argv) < 4:
    print("BMT Inject v0.1 by shibboleet")
    print("Syntax: bmtinject.py in.bmd in.bmt out.bmd")
else:
    injectBMT(sys.argv[1], sys.argv[2], sys.argv[3])
