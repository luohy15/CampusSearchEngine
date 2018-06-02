#include "hash.h"

#include <stdlib.h>
#include <assert.h>

hash_link hlpool[MAX_HLPOOL];
unsigned hlpoolsz = 0;

hash_link* slot[N_HASH_SLOTS];
hash_link* rslot[N_HASH_SLOTS]; // reverse hash

void hash_init(void)
{
  for (unsigned i = 0; i < N_HASH_SLOTS; i++)
    slot[i] = NULL;
  hlpoolsz = 0;
}

hash_link* hash_get(unsigned k)
{
  unsigned s = k % N_HASH_SLOTS; // hash function
  hash_link* hl = slot[s];
  for (; hl; hl = hl->next)
    if (hl->k == k)
      return hl;
  return NULL;
}

/* must guarantee the non-existence */
hash_link* hash_add(unsigned k, unsigned v)
{
  unsigned s = k % N_HASH_SLOTS; // hash function
  hash_link* hl = hlpool + hlpoolsz++;
  hl->k = k;
  hl->v = v;
  hl->next = slot[s];
  slot[s] = hl;
  // reverse hash
  s = v % N_HASH_SLOTS; // hash function
  hash_link* hl1 = hlpool + hlpoolsz++;
  hl1->k = v;
  hl1->v = k;
  hl1->next = rslot[s];
  rslot[s] = hl1;
  assert(hlpoolsz < MAX_HLPOOL);
  return hl;
}

hash_link* hash_getr(unsigned v)
{
  unsigned s = v % N_HASH_SLOTS; // hash function
  hash_link* hl = rslot[s];
  for (; hl; hl = hl->next)
    if (hl->k == v)
      return hl;
  return NULL;
}

