#ifndef HASH_H
#define HASH_H
/*
 * a stupid hashmap implementation
 */

#define N_HASH_SLOTS 3000017
#define MAX_HLPOOL 8000000

typedef struct hash_link {
  unsigned k;
  unsigned v;
  struct hash_link* next;
} hash_link;

void hash_init(void);
hash_link* hash_get(unsigned k);
hash_link* hash_add(unsigned k, unsigned v);
hash_link* hash_getr(unsigned v);

#endif // HASH_H
