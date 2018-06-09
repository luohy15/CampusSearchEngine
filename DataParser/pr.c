#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "fastio.h"
#include "hash.h"

/*
 * Pagerank implementation
 *
 * initialize p: p[u] = 1/N
 *
 * for k=0 to n_iter-1
 *  S = 0
 *  initialize p': p'[u] = alpha/N
 *  for u=1 to N
 *    if (od(u) == 0)
 *      S += p[u]
 *    else
 *      for v in u->v:
 *        p'[v] += (1-alpha)*p[u]/od(u)
 *  for v=1 to N
 *    p'[v] += (1-alpha)*S/N
 *  p = p'
 *
 */

#define MAX_EDGE 35000000
#define MAX_NODE 4000000

unsigned n_nodes = 0;

#define MAX_FINAME 256
const char* finame;
const char* default_finame = "../html.graph";

typedef struct {
  unsigned t;
  unsigned next;
} edge;
edge edgepl[MAX_EDGE];
unsigned edgeplsz = 1;
unsigned eout[MAX_NODE];
unsigned od[MAX_NODE];
unsigned id[MAX_NODE];

typedef float real_t; // don't use double ... too slow
real_t p[MAX_NODE];
real_t p1[MAX_NODE];
float alpha = 0.15;
unsigned TN = 30;

typedef struct {
  unsigned u;
  unsigned id;
  unsigned od;
  float v;
} prres_ent;
prres_ent prres[MAX_NODE];

void scannodes(void)
{
  while (1) {
    unsigned nodeno = readint();
    if (fastio_err_eof) break;
    if (hash_get(nodeno) == NULL)
      hash_add(nodeno, n_nodes++);
  }
  printf("discret ok. n_nodes: %d\n", n_nodes);
}

void readdata(void)
{
  FILE* fin = fopen(finame, "r");
	assert(fin != NULL);
  // discretise nodes
  set_fastio_fin(fin);
  fseek(fin, 0, SEEK_SET);
  scannodes();
  // make graph
  fseek(fin, 0, SEEK_SET);
  fastio_reinit_in();
  set_fastio_fin(fin);
  unsigned u = 0;
  while (1) {
    unsigned v = readint();
    if (fastio_err_eof) break;
    v = hash_get(v)->v;
    if (peekchar() == ':') {
      // a new starting node
      u = v;
      continue;
    } else {
      // new edge u->v
      unsigned already_exist = 0;
      for (unsigned e = eout[u]; e; e = edgepl[e].next)
        // this is bad efficiency
        if (edgepl[e].t == v) {
          already_exist = 1;
          break;
        }
      if (!already_exist) {
        edgepl[edgeplsz].t = v;
        edgepl[edgeplsz].next = eout[u];
        eout[u] = edgeplsz++;
        od[u]++;
        id[v]++;
      }
    }
  }
  printf("make graph ok, n_edges: %d\n", edgeplsz - 1);
#ifdef DUMP_GRAPH
  for (unsigned u = 0; u < n_nodes; u++) {
    printf("%d:", hash_getr(u)->v);
    for (unsigned e = eout[u]; e; e = edgepl[e].next)
      printf("%d,", hash_getr(edgepl[e].t)->v);
    printf("\n");
  }
#endif
  fclose(fin);
}

#define STDOUTBUF_SZ 16000000
char stdoutbuf[STDOUTBUF_SZ]; // 16 MB of buffer

void run_pagerank(unsigned n_iter)
{
  unsigned N = n_nodes; // shorthand

  for (unsigned u = 0; u < N; u++)
    p[u] = ((float) 1) / N;

  while (n_iter--) {
    printf("iter beg.\n");
    float S = 0;
    for (unsigned u = 0; u < N; u++)
      p1[u] = alpha / N;
    for (unsigned u = 0; u < N; u++)
      if (od[u] == 0) {
        S += p[u];
      } else {
        for (unsigned e = eout[u]; e; e = edgepl[e].next) {
          unsigned v = edgepl[e].t;
          p1[v] += (1-alpha)*p[u]/od[u];
        }
      }
    for (unsigned u = 0; u < N; u++)
      p[u] = p1[u] + (1-alpha)*S/N;
  }

}

int cmp_prres_ent(const void* a, const void* b)
{
  float va = ((prres_ent*) a)->v;
  float vb = ((prres_ent*) b)->v;
  if (va < vb)
    return 1; // reverse comparison
  return -1;
  // a little fp error is acceptable
}

#define MAX_FNAME 20

void better_output(void)
{
  printf("generate last info\n");
  unsigned N = n_nodes; // shorthand
  for (unsigned u = 0; u < N; u++) {
    prres[u].u = u;
    prres[u].v = p[u];
    prres[u].id = id[u];
    prres[u].od = od[u];
  }

  qsort(prres, N, sizeof(prres_ent), cmp_prres_ent);

	char fname[MAX_FNAME];
  for (unsigned i = 0; i < N; i++) {
		sprintf(fname, "%d.txt", hash_getr(prres[i].u)->v);
		FILE* fout = fopen(fname, "a");
		fprintf(fout, "%.8f\n", prres[i].v);
		fclose(fout);
  }
}

int main(int argc, char** argv)
{
	if (argc > 2) {
		printf("Usage: %s INPUT_GRAPH_FILE\n", argv[0]);
		return 1;
	}
	if (argc == 2) {
		finame = argv[1];
	} else {
		finame = default_finame;
	}
  readdata();
  run_pagerank(TN);
  better_output();
  return 0;
}
