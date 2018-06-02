#include "fastio.h"

#include <stdio.h>
#include <string.h>

/*
 * MODULE FASTIO
 *
 *  fast decimal unsigned input and output.
 */

/*****************************************************************************/
/* read */
#define MAX_BUFR_SIZE 2000000
/* 2MB write buffer */

static char bufr[MAX_BUFR_SIZE];
static char *readptr = bufr + MAX_BUFR_SIZE;
int fastio_err_eof = 0;
static char* at_eof_end = bufr + MAX_BUFR_SIZE + 10;
static FILE* fastio_fin = NULL;

void set_fastio_fin(FILE* fin) {
  fastio_fin = fin;
}

void fastio_reinit_in() {
  readptr = bufr + MAX_BUFR_SIZE;
  fastio_err_eof = 0;
  at_eof_end = bufr + MAX_BUFR_SIZE + 10;
  fastio_fin = NULL;
}

unsigned readint(void) {
  // skip remaining garbage
  while (readptr < at_eof_end && (*readptr < '0' || *readptr > '9'))
    readptr++;
  if (readptr >= at_eof_end && at_eof_end <= bufr + MAX_BUFR_SIZE) {
    // already eof, and reach eof
    fastio_err_eof = 1;
    return ~0u; // error hack
  }

  if (readptr > bufr + MAX_BUFR_SIZE)
    readptr = bufr + MAX_BUFR_SIZE;

  // if remaining buffer in bufr is too small,
  // start a new read (and copy old data to the beginning of bufr)
  size_t cpsz = bufr + MAX_BUFR_SIZE - readptr;
  size_t rdsz = MAX_BUFR_SIZE - cpsz;
  if (at_eof_end > bufr + MAX_BUFR_SIZE && cpsz < 20) {
    // copy only happens when eof is not reached
    memcpy(bufr, readptr, cpsz);
    readptr = bufr;
    size_t n_read = fread(bufr + cpsz, sizeof(char), rdsz, fastio_fin);
    if (n_read < rdsz) {
      at_eof_end = bufr + cpsz + n_read;
    }
  }

  unsigned r = 0;
  r = *(readptr++) - '0';
  while (*readptr >= '0' && *readptr <= '9')
      r = r * 10 + *(readptr++) - '0';
  return r;
}

char peekchar() {
  return *readptr;
}

/****************************************************************************/
/* write */
#define MAX_BUFW_SIZE 2000000
/* 2MB write buffer */

static char bufw[MAX_BUFW_SIZE];
static char* writeptr = bufw;
static FILE* fastio_fout = NULL;

void set_fastio_fout(FILE* fout) {
  fastio_fout = fout;
}

static inline void writeint_unsafe(unsigned v) {
    static char digits[12];
    int len;
    for (len = 0; v; v /= 10)
        digits[len++] = v % 10 + '0';
    if (!len)
        digits[len++] = '0';
    while (len--)
        *(writeptr++) = digits[len];
}

void writeint(unsigned v) {
  size_t wrsz = writeptr - bufw;
  if (MAX_BUFW_SIZE - wrsz < 20) {
    fwrite(bufw, sizeof(char), writeptr - bufw, fastio_fout);
    writeptr = bufw;
  }
  writeint_unsafe(v);
}

void writechar(char v) {
  size_t wrsz = writeptr - bufw;
  if (MAX_BUFW_SIZE - wrsz < 20) {
    fwrite(bufw, sizeof(char), writeptr - bufw, fastio_fout);
    writeptr = bufw;
  }
  *(writeptr++) = v;
}

void fastio_flush() {
  size_t wrsz = writeptr - bufw;
  if (wrsz != 0) {
    fwrite(bufw, sizeof(char), writeptr - bufw, fastio_fout);
  }
}
