#include <assert.h>
#include "entry_heap.h"

static Entry* heapSpace    = 0;
static size_t heapSize     = 0;
static size_t heapCapacity = 0;

void swap_entry(Entry* a, Entry* b) {
  Entry temp = *a;
  *a = *b;
  *b = temp;
}

void heap_init(int n) {
  if(heapSpace == 0) {
    heapSpace = malloc(sizeof(Entry) * n);
    heapCapacity = n;
    heapSize = 0;
  }
  if(heapCapacity < n) {
    free(heapSpace);
    heapSpace = malloc(sizeof(Entry) * n);
    heapCapacity = n; 
    heapSize = 0;
  }
}

void heap_clear() {
  heapSize = 0;
}

void heap_insert(Entry entry) {
  assert(heapSize < heapCapacity);
  int idx = heapSize;
  heapSpace[heapSize] = entry;
  while(idx > 0) {
    int idx2 = (idx - 1) / 2;
    if(heapSpace[idx2].value < heapSpace[idx].value) {
      swap_entry(&heapSpace[idx2], &heapSpace[idx]);
      idx = idx2; 
    } else {
      break;
    }
  }
  heapSize++;
}

void heap_pop() {
  swap_entry(&heapSpace[0], &heapSpace[heapSize-1]);
  heapSize--;
  int idx = 0;
  int idx2 = 2*idx + 1;
  while(idx2 < heapSize) {
    int max_idx = idx2;
    double max_val = heapSpace[idx2].value;
    if((idx2 + 1) < heapSize) {
      if(heapSpace[idx2 + 1].value < max_val) {
        max_val = heapSpace[idx2 + 1].value;
        max_idx = idx2 + 1;
      }
    }
    if(max_val > heapSpace[idx].value) {
      swap_entry(&heapSpace[idx], &heapSpace[max_idx]);
      idx = max_idx;
      idx2 = 2*idx + 1;
    } else {
      break;
    }
  }
}

size_t heap_size() {
  return heapSize;
}

Entry heap_head() {
  if(heapSize > 0) {
    return heapSpace[0];
  } else {
    Entry e;
    e.value = e.prev = e.prev_rank = -1;
    return e;
  }
}
