#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define MAX_FNAME 40

int getint_finish = 0;
int getint_noeol(FILE* fin) 
{
	int rv = -1;
	char ch;
	while (1) {
		ch = fgetc(fin);
		if (ch == EOF) assert(0);
		if (ch == '\n') {
			getint_finish = 1;
			return -1;
		}
		if (ch >= '0' && ch <= '9') break;
	}
	rv = ch - '0';
	while (1) {
		ch = fgetc(fin);
		if (ch == EOF) assert(0);
		if (ch == '\n') {
			getint_finish = 1;
			return rv;
		}
		if (ch < '0' || ch > '9')
			return rv;
		rv = rv * 10 + (ch - '0');
	}
}

int main(int argc, char** argv)
{
	if (argc != 2) {
		printf("Usage: %s NUM_OF_TXT\n", argv[0]);
		return 1;
	}
	FILE* fout = fopen("txt.graph", "w");
	int n = atoi(argv[1]);
	char fname[MAX_FNAME];
	for (int i = 1; i <= n; i++) {
		sprintf(fname, "%d.txt", i);
		printf("reading %s\n", fname);
		FILE* fin = fopen(fname, "r");
		assert(fin != NULL);
		int id;
		fscanf(fin, "%d", &id);
		if (id != i) {
			printf("%s: first line is %d, expected %d\n", fname, id, i);
			return 1;
		}
		fprintf(fout, "%d: ", id);
		while (fgetc(fin) != '\n') ; // skip first line
		while (fgetc(fin) != '\n') ; // skip second line
		getint_finish = 0;
		while (!getint_finish) {
			fprintf(fout, "%d ", getint_noeol(fin));
		}
		fprintf(fout, "\n");
		fclose(fin);
	}
	fclose(fout);
	return 0;
}
