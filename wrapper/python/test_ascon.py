#!/usr/bin/python3

from curses.ascii import DLE
import ascon
import numpy as np
from random import randint, randbytes

# = (1 << 64) - 1
H = 0xFFFF_FFFF_FFFF_FFFF


def test_hash_kat():
    """
    This test case asserts Ascon Hash digests computed by my implementation
    against Known Answer Tests generated by
    https://github.com/meichlseder/pyascon/blob/236aadd9e09f40bc57064eba7cbade6f46a4c532/genkat.py
    """

    count = 0  # -many KATs to be run

    with open("LWC_HASH_KAT_256.txt", "r") as fd:
        while True:
            cnt = fd.readline()
            if not cnt:
                # no more KATs remaining
                break

            msg = fd.readline()
            md = fd.readline()

            # extract out required fields
            cnt = int([i.strip() for i in cnt.split("=")][-1])
            msg = [i.strip() for i in msg.split("=")][-1]
            md = [i.strip() for i in md.split("=")][-1]

            # convert input message to numpy ndarray of uint8_t
            msg = np.asarray(
                [
                    int(f"0x{msg[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(msg) >> 1)
                ],
                dtype=np.uint8,
            )

            # convert output digest to numpy ndarray of uint8_t
            md = np.asarray(
                [
                    int(f"0x{md[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(md) >> 1)
                ],
                dtype=np.uint8,
            )

            # compute Ascon Hash using my implementation
            digest = ascon.hash(msg)
            # check 32 -bytes element-wise
            check = (md == digest).all()

            assert check, f"[Ascon Hash KAT {cnt}] expected {md}, found {digest} !"

            # don't need this line, so discard
            fd.readline()
            # to keep track of how many KATs executed !
            count = cnt

    print(f"[test] passed {count} -many Ascon Hash KAT(s)")


def test_hashA_kat():
    """
    This test case asserts Ascon HashA digests computed by my implementation
    against Known Answer Tests generated by
    https://github.com/meichlseder/pyascon/blob/236aadd9e09f40bc57064eba7cbade6f46a4c532/genkat.py
    """

    count = 0  # -many KATs to be run

    with open("LWC_HASH_KAT_256.txt", "r") as fd:
        while True:
            cnt = fd.readline()
            if not cnt:
                # no more KATs remaining
                break

            msg = fd.readline()
            md = fd.readline()

            # extract out required fields
            cnt = int([i.strip() for i in cnt.split("=")][-1])
            msg = [i.strip() for i in msg.split("=")][-1]
            md = [i.strip() for i in md.split("=")][-1]

            # convert input message to numpy ndarray of uint8_t
            msg = np.asarray(
                [
                    int(f"0x{msg[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(msg) >> 1)
                ],
                dtype=np.uint8,
            )

            # convert output digest to numpy ndarray of uint8_t
            md = np.asarray(
                [
                    int(f"0x{md[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(md) >> 1)
                ],
                dtype=np.uint8,
            )

            # compute Ascon HashA using my implementation
            digest = ascon.hash_a(msg)
            # check 32 -bytes element-wise
            check = (md == digest).all()

            assert check, f"[Ascon Hash KAT {cnt}] expected {md}, found {digest} !"

            # don't need this line, so discard
            fd.readline()
            # to keep track of how many KATs executed !
            count = cnt

    print(f"[test] passed {count} -many Ascon HashA KAT(s)")


def test_ascon_128_kat():
    """
    This test case asserts Ascon-128 encrypt/ decrypt implementation
    using Known Answer Tests as input; generated by
    https://github.com/meichlseder/pyascon/blob/236aadd9e09f40bc57064eba7cbade6f46a4c532/genkat.py
    """

    count = 0  # -many KATs to be run

    with open("LWC_AEAD_KAT_128_128.txt", "r") as fd:
        while True:
            cnt = fd.readline()
            if not cnt:
                # no more KATs remaining
                break

            key = fd.readline()
            nonce = fd.readline()
            pt = fd.readline()
            ad = fd.readline()
            ct = fd.readline()

            # extract out required fields
            cnt = int([i.strip() for i in cnt.split("=")][-1])
            key = [i.strip() for i in key.split("=")][-1]
            nonce = [i.strip() for i in nonce.split("=")][-1]
            pt = [i.strip() for i in pt.split("=")][-1]
            ad = [i.strip() for i in ad.split("=")][-1]

            # 128 -bit secret key
            key = bytes.fromhex(key)
            # 128 -bit nonce
            nonce = bytes.fromhex(nonce)
            # plain text
            pt = np.asarray(
                [
                    int(f"0x{pt[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(pt) >> 1)
                ],
                dtype=np.uint8,
            )
            # associated data
            ad = np.asarray(
                [
                    int(f"0x{ad[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(ad) >> 1)
                ],
                dtype=np.uint8,
            )

            cipher, tag = ascon.encrypt_128(key, nonce, ad, pt)
            flag, text = ascon.decrypt_128(key, nonce, ad, cipher, tag)

            check = (pt == text).all()
            assert (
                check and flag
            ), f"[Ascon-128 KAT {cnt}] expected {pt}, found {text} !"

            # don't need this line, so discard
            fd.readline()
            # to keep track of how many KATs executed !
            count = cnt

    print(f"[test] passed {count} -many Ascon-128 KAT(s)")


def test_ascon_128a_kat():
    """
    This test case asserts Ascon-128a encrypt/ decrypt implementation
    using Known Answer Tests as input; generated by
    https://github.com/meichlseder/pyascon/blob/236aadd9e09f40bc57064eba7cbade6f46a4c532/genkat.py
    """

    count = 0  # -many KATs to be run

    with open("LWC_AEAD_KAT_128_128.txt", "r") as fd:
        while True:
            cnt = fd.readline()
            if not cnt:
                # no more KATs remaining
                break

            key = fd.readline()
            nonce = fd.readline()
            pt = fd.readline()
            ad = fd.readline()
            ct = fd.readline()

            # extract out required fields
            cnt = int([i.strip() for i in cnt.split("=")][-1])
            key = [i.strip() for i in key.split("=")][-1]
            nonce = [i.strip() for i in nonce.split("=")][-1]
            pt = [i.strip() for i in pt.split("=")][-1]
            ad = [i.strip() for i in ad.split("=")][-1]

            # 128 -bit secret key
            key = bytes.fromhex(key)
            # 128 -bit nonce
            nonce = bytes.fromhex(nonce)
            # plain text
            pt = np.asarray(
                [
                    int(f"0x{pt[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(pt) >> 1)
                ],
                dtype=np.uint8,
            )
            # associated data
            ad = np.asarray(
                [
                    int(f"0x{ad[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(ad) >> 1)
                ],
                dtype=np.uint8,
            )

            cipher, tag = ascon.encrypt_128a(key, nonce, ad, pt)
            flag, text = ascon.decrypt_128a(key, nonce, ad, cipher, tag)

            check = (pt == text).all()
            assert (
                check and flag
            ), f"[Ascon-128a KAT {cnt}] expected {pt}, found {text} !"

            # don't need this line, so discard
            fd.readline()
            # to keep track of how many KATs executed !
            count = cnt

    print(f"[test] passed {count} -many Ascon-128a KAT(s)")


def test_ascon_80pq_kat():
    """
    This test case asserts Ascon-80pq encrypt/ decrypt implementation
    using Known Answer Tests as input; generated by
    https://github.com/meichlseder/pyascon/blob/236aadd9e09f40bc57064eba7cbade6f46a4c532/genkat.py
    """

    count = 0  # -many KATs to be run

    with open("LWC_AEAD_KAT_160_128.txt", "r") as fd:
        while True:
            cnt = fd.readline()
            if not cnt:
                # no more KATs remaining
                break

            key = fd.readline()
            nonce = fd.readline()
            pt = fd.readline()
            ad = fd.readline()
            ct = fd.readline()

            # extract out required fields
            cnt = int([i.strip() for i in cnt.split("=")][-1])
            key = [i.strip() for i in key.split("=")][-1]
            nonce = [i.strip() for i in nonce.split("=")][-1]
            pt = [i.strip() for i in pt.split("=")][-1]
            ad = [i.strip() for i in ad.split("=")][-1]

            # 160 -bit secret key
            key = int(f"0x{key}", base=16).to_bytes(20, "big")
            # 128 -bit nonce
            nonce = int(f"0x{nonce}", base=16).to_bytes(16, "big")
            # plain text
            pt = np.asarray(
                [
                    int(f"0x{pt[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(pt) >> 1)
                ],
                dtype=np.uint8,
            )
            # associated data
            ad = np.asarray(
                [
                    int(f"0x{ad[(i << 1): ((i+1) << 1)]}", base=16)
                    for i in range(len(ad) >> 1)
                ],
                dtype=np.uint8,
            )

            cipher, tag = ascon.encrypt_80pq(key, nonce, ad, pt)
            flag, text = ascon.decrypt_80pq(key, nonce, ad, cipher, tag)

            check = (pt == text).all()
            assert (
                check and flag
            ), f"[Ascon-80pq KAT {cnt}] expected {pt}, found {text} !"

            # don't need this line, so discard
            fd.readline()
            # to keep track of how many KATs executed !
            count = cnt

    print(f"[test] passed {count} -many Ascon-80pq KAT(s)")


def flip_bit(inp: bytes) -> bytes:
    """
    Randomly selects a byte offset of a given byte array ( inp ), whose single random bit
    will be flipped. Input is **not** mutated & single bit flipped byte array is returned back.

    Taken from https://github.com/itzmeanjan/elephant/blob/2a21c7e/wrapper/python/test_elephant.py#L217-L237
    """
    arr = bytearray(inp)
    ilen = len(arr)

    idx = randint(0, ilen - 1)
    bidx = randint(0, 7)

    mask0 = (0xFF << (bidx + 1)) & 0xFF
    mask1 = (0xFF >> (8 - bidx)) & 0xFF
    mask2 = 1 << bidx

    msb = arr[idx] & mask0
    lsb = arr[idx] & mask1
    bit = (arr[idx] & mask2) >> bidx

    arr[idx] = msb | ((1 - bit) << bidx) | lsb
    return bytes(arr)


def test_ascon_128_kat_auth_fail():
    """
    Test that Ascon128 authentication fails when random bit of associated data
    and/ or encrypted text are flipped. Also it's ensured that in case of authentication
    failure unverified plain text is never released, instead memory allocation for
    decrypted plain text is zeroed.
    """
    DLEN = 32
    CTLEN = 32

    key = randbytes(16)
    nonce = randbytes(16)
    data = randbytes(DLEN)
    txt = randbytes(CTLEN)

    data_ = np.frombuffer(data, dtype=np.uint8)
    txt_ = np.frombuffer(txt, dtype=np.uint8)
    zeros = np.zeros(CTLEN, dtype=np.uint8)

    enc, tag = ascon.encrypt_128(key, nonce, data_, txt_)

    # case 0
    fdata = flip_bit(data)
    fdata_ = np.frombuffer(fdata, dtype=np.uint8)

    flg, dec = ascon.decrypt_128(key, nonce, fdata_, enc, tag)

    assert not flg, "Ascon128 authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 1
    fenc = flip_bit(enc.tobytes())
    fenc_ = np.frombuffer(fenc, dtype=np.uint8)

    flg, dec = ascon.decrypt_128(key, nonce, data_, fenc_, tag)

    assert not flg, "Ascon128 authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 2
    flg, dec = ascon.decrypt_128(key, nonce, fdata_, fenc_, tag)

    assert not flg, "Ascon128 authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"


def test_ascon_128a_kat_auth_fail():
    """
    Test that Ascon128a authentication fails when random bit of associated data
    and/ or encrypted text are flipped. Also it's ensured that in case of authentication
    failure unverified plain text is never released, instead memory allocation for
    decrypted plain text is zeroed.
    """
    DLEN = 32
    CTLEN = 32

    key = randbytes(16)
    nonce = randbytes(16)
    data = randbytes(DLEN)
    txt = randbytes(CTLEN)

    data_ = np.frombuffer(data, dtype=np.uint8)
    txt_ = np.frombuffer(txt, dtype=np.uint8)
    zeros = np.zeros(CTLEN, dtype=np.uint8)

    enc, tag = ascon.encrypt_128a(key, nonce, data_, txt_)

    # case 0
    fdata = flip_bit(data)
    fdata_ = np.frombuffer(fdata, dtype=np.uint8)

    flg, dec = ascon.decrypt_128a(key, nonce, fdata_, enc, tag)

    assert not flg, "Ascon128a aauthentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 1
    fenc = flip_bit(enc.tobytes())
    fenc_ = np.frombuffer(fenc, dtype=np.uint8)

    flg, dec = ascon.decrypt_128a(key, nonce, data_, fenc_, tag)

    assert not flg, "Ascon128a authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 2
    flg, dec = ascon.decrypt_128a(key, nonce, fdata_, fenc_, tag)

    assert not flg, "Ascon128a authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"


def test_ascon_80pq_kat_auth_fail():
    """
    Test that Ascon80pq authentication fails when random bit of associated data
    and/ or encrypted text are flipped. Also it's ensured that in case of authentication
    failure unverified plain text is never released, instead memory allocation for
    decrypted plain text is zeroed.
    """
    DLEN = 32
    CTLEN = 32

    key = randbytes(20)
    nonce = randbytes(16)
    data = randbytes(DLEN)
    txt = randbytes(CTLEN)

    data_ = np.frombuffer(data, dtype=np.uint8)
    txt_ = np.frombuffer(txt, dtype=np.uint8)
    zeros = np.zeros(CTLEN, dtype=np.uint8)

    enc, tag = ascon.encrypt_80pq(key, nonce, data_, txt_)

    # case 0
    fdata = flip_bit(data)
    fdata_ = np.frombuffer(fdata, dtype=np.uint8)

    flg, dec = ascon.decrypt_80pq(key, nonce, fdata_, enc, tag)

    assert not flg, "Ascon80pq authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 1
    fenc = flip_bit(enc.tobytes())
    fenc_ = np.frombuffer(fenc, dtype=np.uint8)

    flg, dec = ascon.decrypt_80pq(key, nonce, data_, fenc_, tag)

    assert not flg, "Ascon80pq authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"

    # case 2
    flg, dec = ascon.decrypt_80pq(key, nonce, fdata_, fenc_, tag)

    assert not flg, "Ascon80pq authentication must fail !"
    assert np.all(zeros == dec), "Unverified plain text must not be released !"


if __name__ == "__main__":
    print(f"Use `pytest` for running test cases/ benchmarks !")
