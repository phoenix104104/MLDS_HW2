#include <stdlib.h>

typedef struct Entry {
  double value;
  int    prev;
  int    prev_rank;
} Entry;

void swap_entry(Entry*, Entry*);
void heap_init(int n);
void heap_clear();
void heap_insert(Entry);
size_t heap_size();
void heap_pop();
Entry heap_head();

