#pragma once
#include "permutation.hpp"
#include "utils.hpp"

// Ascon-Xof
namespace ascon_xof {

// Bit width of rate portion of Ascon permutation state
constexpr size_t RATE = 64;

// How many rounds of Ascon permutation is applied for p^a
constexpr size_t ROUNDS_A = 12;

// How many rounds of Ascon permutation is applied for p^b
constexpr size_t ROUNDS_B = 12;

// Ascon-Xof ( extendable output function ), supporting incremental hashing.
//
// See section 2.5 of Ascon specification
// https://ascon.iaik.tugraz.at/files/asconv12-nist.pdf
struct ascon_xof
{
private:
  uint64_t state[5]{ 0xb57e273b814cd416,
                     0x2b51042562ae2420,
                     0x66a3a7768ddf2218,
                     0x5aad0a7a8153650c,
                     0x4f3e0e32539493b6 };
  size_t offset = 0;
  size_t readable = 0;
  alignas(4) bool absorbed = false;

public:
  // Initialization values taken from section 2.5.1 of Ascon spec.
  constexpr ascon_xof() = default;

  // Given N -bytes input message, this routine consumes those into
  // Ascon permutation state.
  //
  // Note, this routine can be called arbitrary number of times, each time with
  // arbitrary bytes of input message, until Ascon permutation state is
  // finalized ( by calling routine with similar name ).
  inline void absorb(const uint8_t* const msg, const size_t mlen)
  {
    constexpr size_t rbytes = RATE / 8;

    if (!absorbed) {
      uint8_t blk_bytes[rbytes];

      const size_t blk_cnt = (offset + mlen) / rbytes;
      size_t moff = 0;

      for (size_t i = 0; i < blk_cnt; i++) {
        std::memset(blk_bytes, 0, offset);
        std::memcpy(blk_bytes + offset, msg + moff, rbytes - offset);

        const auto word = ascon_utils::from_be_bytes<uint64_t>(blk_bytes);
        state[0] ^= word;

        moff += (rbytes - offset);
        offset += (rbytes - offset);

        ascon_permutation::permute<ROUNDS_B>(state);
        offset %= rbytes;
      }

      const size_t rm_bytes = mlen - moff;

      std::memset(blk_bytes, 0, rbytes);
      std::memcpy(blk_bytes + offset, msg + moff, rm_bytes);

      const auto word = ascon_utils::from_be_bytes<uint64_t>(blk_bytes);
      state[0] ^= word;

      offset += rm_bytes;

      if (offset == rbytes) {
        ascon_permutation::permute<ROUNDS_B>(state);
        offset %= rbytes;
      }
    }
  }

  // After consuming N -many bytes ( by invoking absorb routine arbitrary many
  // times, each time with arbitrary input bytes ), this routine is invoked when
  // no more input bytes remaining to be consumed by Ascon permutation state.
  //
  // Note, once this routine is called, calling absorb() or finalize() again, on
  // same Ascon-XOF object, doesn't do anything. After finalization, one would
  // like to read arbitrary many bytes of digest by squeezing sponge, which is
  // done by calling `read()` function as many times required.
  inline void finalize()
  {
    constexpr size_t rbytes = RATE / 8;

    if (!absorbed) {
      const size_t pad_bytes = rbytes - offset;
      const size_t pad_bits = pad_bytes * 8;
      const uint64_t pad_mask = 1ul << (pad_bits - 1);

      state[0] ^= pad_mask;
      absorbed = true;
      offset = 0;

      ascon_permutation::permute<ROUNDS_A>(state);
      readable = RATE / 8;
    }
  }

  // Given that N -bytes input message is already absorbed into Ascon
  // permutation state using, this routine is used for squeezing M -bytes out of
  // consumable part of state ( i.e. rate portion of state ).
  //
  // This routine can be used for squeezing arbitrary number of bytes from Ascon
  // permutation state.
  //
  // Make sure you absorb message bytes first, then only call this function,
  // otherwise it can't squeeze out anything.
  inline void read(uint8_t* const out, const size_t olen)
  {
    if (!absorbed) {
      return;
    }

    constexpr size_t rbytes = RATE / 8;

    size_t ooff = 0;
    while (ooff < olen) {
      const size_t elen = std::min(readable, olen - ooff);
      const size_t soff = rbytes - readable;

      uint64_t word = state[0];

      if constexpr (std::endian::native == std::endian::little) {
        word = ascon_utils::bswap(word);
      }

      std::memcpy(out + ooff, reinterpret_cast<uint8_t*>(&word) + soff, elen);

      readable -= elen;
      ooff += elen;

      if (readable == 0) {
        ascon_permutation::permute<ROUNDS_B>(state);
        readable = RATE / 8;
      }
    }
  }
};

}
