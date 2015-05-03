/***********************************************************************/
/*                                                                     */
/*   svm_struct_api.c                                                  */
/*                                                                     */
/*   Definition of API for attaching implementing SVM learning of      */
/*   structures (e.g. parsing, multi-label classification, HMM)        */ 
/*                                                                     */
/*   Author: Thorsten Joachims                                         */
/*   Date: 03.07.04                                                    */
/*                                                                     */
/*   Copyright (c) 2004  Thorsten Joachims - All rights reserved       */
/*                                                                     */
/*   This software is available for non-commercial use only. It must   */
/*   not be modified and distributed without prior permission of the   */
/*   author. The author is not responsible for implications from the   */
/*   use of this software.                                             */
/*                                                                     */
/***********************************************************************/

#include <stdio.h>
#include <string.h>
#include "svm_struct/svm_struct_common.h"
#include "svm_struct_api.h"

// memory block used in Viterbi ( classify_example(), find_most_violated )
static double* viterbi_val_block = NULL;
static int* viterbi_prev_block = NULL;
static int viterbi_block_size = 0;

int strsplit(char** array, char* str, const char* del) {
  int len = 0;
  char *s = strtok(str, del);
  while( s != NULL ) {
    array[len] = s;
    s = strtok(NULL, del);
    len++;
  }
  return len;
}

void check_y(LABEL y, int label_num) {
  int i;
  for(i = 0; i < y.frame_num; i++) {
    if(y.y[i]<0 || y.y[i] >= label_num) {
      printf("ERROR! y[%d] out of range\n", i);
      exit(-1);
    }
  }
}

void extract_filename(char* filename, char* input_string) {

  char** filename_buffer = (char**)malloc(sizeof(char*)*3);
  strsplit(filename_buffer, input_string, "_");
  memset(filename, 0, strlen(filename));
  strcpy(filename, filename_buffer[0]);
  strcat(filename, "_");
  strcat(filename, filename_buffer[1]);

}

void        svm_struct_learn_api_init(int argc, char* argv[])
{
  /* Called in learning part before anything else is done to allow
     any initializations that might be necessary. */
}

void        svm_struct_learn_api_exit()
{
  /* Called in learning part at the very end to allow any clean-up
     that might be necessary. */
}

void        svm_struct_classify_api_init(int argc, char* argv[])
{
  /* Called in prediction part before anything else is done to allow
     any initializations that might be necessary. */
}

void        svm_struct_classify_api_exit()
{
  /* Called in prediction part at the very end to allow any clean-up
     that might be necessary. */
}

SAMPLE      read_struct_examples(char *input_filename, STRUCT_LEARN_PARM *sparm)
{
  /* Reads struct examples and returns them in sample. The number of
     examples must be written into sample.n */
  SAMPLE   sample;  /* sample */
  EXAMPLE  *examples;
  long     n;       /* number of examples */

  printf("\n");

  int max_feature_dim = 2000;
  int max_example_num = 5000;

  FILE* file;

  int buffer_len = 1000;
  char* buffer = (char*)malloc(sizeof(char)*buffer_len);

  char** line = (char**)malloc(sizeof(char*)*(max_feature_dim+2));
  char** filename_list = (char**)malloc(sizeof(char*)*max_example_num);
  int*   frame_num_list = (int*)malloc(sizeof(int)*max_example_num);
  char*  filename = (char*)malloc(sizeof(char)*50);
  char*  filename_current = (char*)malloc(sizeof(char)*50);
  int n_element   = 0;  // number of element in one line
  int n_frame     = 0;  // number of frame in one example
  int feature_dim = 0;  // input feature dimension
  int i, j, k;


  // first parse (get n, frame_num, feature_dim)
  printf("First parsing...\n");
  file = fopen(input_filename, "r");
  n = 0;
  while( getline(&buffer, &buffer_len, file) != -1 ) {
    n_element = strsplit(line, buffer, " ");
    feature_dim = n_element - 2;
  
    extract_filename(filename, line[0]);
    if( strcmp(filename, filename_current) != 0 ) {
      memset(filename_current, 0, strlen(filename_current));
      strcpy(filename_current, filename);

      filename_list[n] = (char*)malloc(sizeof(char)*strlen(filename));
      strcpy(filename_list[n], filename);
      if( n > 0 ) {
        frame_num_list[n-1] = n_frame;
      }
      n += 1;
      n_frame = 0;
    }
    n_frame++;
  }  
  frame_num_list[n-1] = n_frame;      

  printf("input feature dimension = %d\n", feature_dim);
  printf("number of example = %d\n", n);
  examples=(EXAMPLE *)my_malloc(sizeof(EXAMPLE)*n);
  sparm->feature_dim = feature_dim;
  sparm->label_num = 48; 
//  for(i=0 ; i<n ; i++) {
//    printf("%s\tn_frame = %d\n", filename_list[i], frame_num_list[i]);
// }
  
  // second parse (allocate pattern and label)
  printf("Second parsing...\n");
  fseek(file, 0, SEEK_SET); // reset file pointer to the beginning of file
  memset(filename_current, 0, strlen(filename_current));
  i = -1; // counter of example
  while( getline(&buffer, &buffer_len, file) != -1 ) {
    n_element = strsplit(line, buffer, " ");
    extract_filename(filename, line[0]);

    if( strcmp(filename, filename_current) != 0 ) {
      i += 1;
      memset(filename_current, 0, strlen(filename_current));
      strcpy(filename_current, filename);
      
      examples[i].x.x = (double**)my_malloc(sizeof(double*)*frame_num_list[i]);
      for(j=0 ; j<frame_num_list[i] ; j++) {
        examples[i].x.x[j] = (double*)my_malloc(sizeof(double)*feature_dim);
      }

      examples[i].y.y = (int*)my_malloc(sizeof(int)*frame_num_list[i]);
      examples[i].x.filename = (char*)my_malloc(sizeof(char)*strlen(filename_list[i]));
      strcpy(examples[i].x.filename, filename_list[i]);
      examples[i].y.filename = examples[i].x.filename;

      examples[i].x.frame_num = frame_num_list[i];
      examples[i].y.frame_num = frame_num_list[i];

      j = 0; // counter of frame
    }
    
    examples[i].y.y[j] = atoi(line[1]);
    for(k=2 ; k<n_element; k++) {
        examples[i].x.x[j][k-2] = atof(line[k]);
    }
    j++;    
  }  

  fclose(file);
  
  int max_num_frame = 0;
  for(i=0 ; i<n ; i++) {
    if(frame_num_list[i] > max_num_frame) {
      max_num_frame = frame_num_list[i];
    }
  }
  printf("max_num_frame = %d\n", max_num_frame);
  // debug
  /*
  printf("debug...\n"); 
  for(i=0 ; i<3 ; i++) {
    
    printf("x.filename = %s, x.frame_num = %d\n", examples[i].x.filename, examples[i].x.frame_num);
    
    for(j=examples[i].x.frame_num-1 ; j<examples[i].x.frame_num ; j++) {
      for(k=0 ; k<feature_dim ; k++) {
        printf("x[%d][%d] = %.8f\n", j, k, examples[i].x.x[j][k]);
      }
    }
    

    printf("y.filename = %s, y.frame_num = %d\n", examples[i].y.filename, examples[i].y.frame_num);
    for(j=0 ; j<examples[i].y.frame_num ; j++) {

      printf("%d ", examples[i].y.y[j]);
    }
    printf("\n");
    
    
    check_y(examples[i].y, sparm->label_num);
  }
  */
  
  
  // release memory
  free(buffer);
  free(line);
  for(i=0 ; i<max_example_num ; i++) {
    free(filename_list[i]);
  }
  free(filename_list);
  free(frame_num_list);
  free(filename);
  free(filename_current);
  sample.n=n;
  sample.examples=examples;
  return(sample);
}

void        init_struct_model(SAMPLE sample, STRUCTMODEL *sm, 
			      STRUCT_LEARN_PARM *sparm, LEARN_PARM *lparm, 
			      KERNEL_PARM *kparm)
{
  /* Initialize structmodel sm. The weight vector w does not need to be
     initialized, but you need to provide the maximum size of the
     feature space in sizePsi. This is the maximum number of different
     weights that can be learned. Later, the weight vector w will
     contain the learned weights for the model. */

  sm->sizePsi = (sparm->feature_dim) * (sparm->label_num) + (sparm->label_num) * (sparm->label_num); /* replace by appropriate number of features */
}

CONSTSET    init_struct_constraints(SAMPLE sample, STRUCTMODEL *sm, 
				    STRUCT_LEARN_PARM *sparm)
{
  /* Initializes the optimization problem. Typically, you do not need
     to change this function, since you want to start with an empty
     set of constraints. However, if for example you have constraints
     that certain weights need to be positive, you might put that in
     here. The constraints are represented as lhs[i]*w >= rhs[i]. lhs
     is an array of feature vectors, rhs is an array of doubles. m is
     the number of constraints. The function returns the initial
     set of constraints. */
  CONSTSET c;
  long     sizePsi=sm->sizePsi;
  long     i;
  WORD     words[2];

  if(1) { /* normal case: start with empty set of constraints */
    c.lhs=NULL;
    c.rhs=NULL;
    c.m=0;
  }
  else { /* add constraints so that all learned weights are
            positive. WARNING: Currently, they are positive only up to
            precision epsilon set by -e. */
    c.lhs=my_malloc(sizeof(DOC *)*sizePsi);
    c.rhs=my_malloc(sizeof(double)*sizePsi);
    for(i=0; i<sizePsi; i++) {
      words[0].wnum=i+1;
      words[0].weight=1.0;
      words[1].wnum=0;
      /* the following slackid is a hack. we will run into problems,
         if we have move than 1000000 slack sets (ie examples) */
      c.lhs[i]=create_example(i,0,1000000+i,1,create_svector(words,"",1.0));
      c.rhs[i]=0.0;
    }
  }
  return(c);
}

LABEL       classify_struct_example(PATTERN x, STRUCTMODEL *sm, 
				    STRUCT_LEARN_PARM *sparm)
{
  /* Finds the label yhat for pattern x that scores the highest
     according to the linear evaluation function in sm, especially the
     weights sm.w. The returned label is taken as the prediction of sm
     for the pattern x. The weights correspond to the features defined
     by psi() and range from index 1 to index sm->sizePsi. If the
     function cannot find a label, it shall return an empty label as
     recognized by the function empty_label(y). */
  LABEL ybar;

  /* insert your code for computing the predicted label y here */
  // TODO
  ybar.y = my_malloc(sizeof(int) * x.frame_num);
  ybar.filename = x.filename;
  ybar.frame_num = x.frame_num;

  if(viterbi_val_block == NULL) {
    viterbi_block_size = 1000 * sparm->label_num;
    viterbi_val_block = my_malloc(sizeof(double) * viterbi_block_size);
    viterbi_prev_block = my_malloc(sizeof(int) * viterbi_block_size);
  }

  if(viterbi_block_size < (x.frame_num * sparm->label_num)) {
    free(viterbi_val_block);
    free(viterbi_prev_block);
    while(viterbi_block_size < (x.frame_num * sparm->label_num)) {
      viterbi_block_size = viterbi_block_size * 2;
    }
    viterbi_val_block = my_malloc(sizeof(double) * viterbi_block_size);
    viterbi_prev_block = my_malloc(sizeof(int) * viterbi_block_size); 
  }

  int w_offset = 1;
  int w_trans_offset = w_offset + sparm->feature_dim * sparm->label_num;

  // first frame
  int i = 0,j = 0,m = 0;

  for(i = 0; i < sparm->label_num; i++) {
    viterbi_val_block[i] = 0;
    viterbi_prev_block[i] = -1;  // no prev for first frame
    int offset = i * sparm->feature_dim + w_offset;
    for(j = 0; j < sparm->feature_dim; j++) {
      viterbi_val_block[i] += sm->w[offset+j] * x.x[0][j];
    }
  }

  // forward
  for(m = 1; m < x.frame_num; m++) {
    int viterbi_prev_offset = (m - 1) * sparm->label_num;
    int viterbi_offset = m * sparm->label_num;
    for(j = 0; j < sparm->label_num; j++) {
      // transition from 0 to j
      double max = viterbi_val_block[viterbi_prev_offset] + sm->w[w_trans_offset+j];
      int maxIdx = 0;
      for(i = 1; i < sparm->label_num; i++) {
        // transition from i to j
        double temp = viterbi_val_block[viterbi_prev_offset+i]
                        + sm->w[w_trans_offset + i * sparm->label_num + j];
        if(temp > max) {
          max = temp;
          maxIdx = i;
        }
      }
      // max found, add feature weights
      int offset = j * sparm->feature_dim + w_offset;
      for(i = 0; i < sparm->feature_dim; i++) {
        max += sm->w[offset+i] * x.x[m][i];
      }
      viterbi_val_block[viterbi_offset+j] = max;
      viterbi_prev_block[viterbi_offset+j] = maxIdx;
    }
  }

  // backtrace
  int viterbi_offset = (x.frame_num - 1) * sparm->label_num;
  int maxIdx = 0;
  double max = viterbi_val_block[viterbi_offset];
  for(i = 1; i < sparm->label_num; i++) {
    if( viterbi_val_block[viterbi_offset + i] > max ) {
      max = viterbi_val_block[viterbi_offset + i];
      maxIdx = i;
    }
  }

  for(i = x.frame_num-1; i >= 0; i--) {
    ybar.y[i] = maxIdx;
    maxIdx = viterbi_prev_block[i * sparm->label_num + maxIdx];
  }
  //check_y(ybar, sparm->label_num);
  return(ybar);
}

LABEL       find_most_violated_constraint_slackrescaling(PATTERN x, LABEL y, 
						     STRUCTMODEL *sm, 
						     STRUCT_LEARN_PARM *sparm)
{
  /* Finds the label ybar for pattern x that that is responsible for
     the most violated constraint for the slack rescaling
     formulation. For linear slack variables, this is that label ybar
     that maximizes

            argmax_{ybar} loss(y,ybar)*(1-psi(x,y)+psi(x,ybar)) 

     Note that ybar may be equal to y (i.e. the max is 0), which is
     different from the algorithms described in
     [Tschantaridis/05]. Note that this argmax has to take into
     account the scoring function in sm, especially the weights sm.w,
     as well as the loss function, and whether linear or quadratic
     slacks are used. The weights in sm.w correspond to the features
     defined by psi() and range from index 1 to index
     sm->sizePsi. Most simple is the case of the zero/one loss
     function. For the zero/one loss, this function should return the
     highest scoring label ybar (which may be equal to the correct
     label y), or the second highest scoring label ybar, if
     Psi(x,ybar)>Psi(x,y)-1. If the function cannot find a label, it
     shall return an empty label as recognized by the function
     empty_label(y). */
  LABEL ybar;

  /* insert your code for computing the label ybar here */
  // TODO...?
  // 
  return(ybar);
}

LABEL       find_most_violated_constraint_marginrescaling(PATTERN x, LABEL y, 
						     STRUCTMODEL *sm, 
						     STRUCT_LEARN_PARM *sparm)
{
  /* Finds the label ybar for pattern x that that is responsible for
     the most violated constraint for the margin rescaling
     formulation. For linear slack variables, this is that label ybar
     that maximizes

            argmax_{ybar} loss(y,ybar)+psi(x,ybar)

     Note that ybar may be equal to y (i.e. the max is 0), which is
     different from the algorithms described in
     [Tschantaridis/05]. Note that this argmax has to take into
     account the scoring function in sm, especially the weights sm.w,
     as well as the loss function, and whether linear or quadratic
     slacks are used. The weights in sm.w correspond to the features
     defined by psi() and range from index 1 to index
     sm->sizePsi. Most simple is the case of the zero/one loss
     function. For the zero/one loss, this function should return the
     highest scoring label ybar (which may be equal to the correct
     label y), or the second highest scoring label ybar, if
     Psi(x,ybar)>Psi(x,y)-1. If the function cannot find a label, it
     shall return an empty label as recognized by the function
     empty_label(y). */
  LABEL ybar;

  /* insert your code for computing the predicted label y here */
  // TODO
  ybar.y = my_malloc(sizeof(int) * x.frame_num);
  ybar.filename = x.filename;
  ybar.frame_num = x.frame_num;

  if(viterbi_val_block == NULL) {
    viterbi_block_size = 1000 * sparm->label_num;
    viterbi_val_block = my_malloc(sizeof(double) * viterbi_block_size);
    viterbi_prev_block = my_malloc(sizeof(int) * viterbi_block_size);
  }

  if(viterbi_block_size < (x.frame_num * sparm->label_num)) {
    free(viterbi_val_block);
    free(viterbi_prev_block);
    while(viterbi_block_size < (x.frame_num * sparm->label_num)) {
      viterbi_block_size = viterbi_block_size * 2;
    }
    viterbi_val_block = my_malloc(sizeof(double) * viterbi_block_size);
    viterbi_prev_block = my_malloc(sizeof(int) * viterbi_block_size); 
  }

  int w_offset = 1;
  int w_trans_offset = w_offset + sparm->feature_dim * sparm->label_num;

  // first frame
  int i = 0,j = 0,m = 0;

  for(i = 0; i < sparm->label_num; i++) {
    viterbi_val_block[i] = 0;
    viterbi_prev_block[i] = -1;  // no prev for first frame
    int offset = i * sparm->feature_dim + w_offset;
    for(j = 0; j < sparm->feature_dim; j++) {
      viterbi_val_block[i] += sm->w[offset+j] * x.x[0][j];
    }
    if(i != y.y[0]) {
      viterbi_val_block[i] += 1;
    }
  }

  // forward
  for(m = 1; m < x.frame_num; m++) {
    int viterbi_prev_offset = (m - 1) * sparm->label_num;
    int viterbi_offset = m * sparm->label_num;
    for(j = 0; j < sparm->label_num; j++) {
      // transition from 0 to j
      double max = viterbi_val_block[viterbi_prev_offset] + sm->w[w_trans_offset+j];
      int maxIdx = 0;
      for(i = 1; i < sparm->label_num; i++) {
        // transition from i to j
        double temp = viterbi_val_block[viterbi_prev_offset+i]
                        + sm->w[w_trans_offset + i * sparm->label_num + j];
        if(temp > max) {
          max = temp;
          maxIdx = i;
        }
      }
      // max found, add feature weights
      int offset = j * sparm->feature_dim + w_offset;
      for(i = 0; i < sparm->feature_dim; i++) {
        max += sm->w[offset+i] * x.x[m][i];
      }
      if(j != y.y[m]){
        max += 1;
      }
      viterbi_val_block[viterbi_offset+j] = max;
      viterbi_prev_block[viterbi_offset+j] = maxIdx;
    }
  }

  // backtrace
  int viterbi_offset = (x.frame_num - 1) * sparm->label_num;
  int maxIdx = 0;
  double max = viterbi_val_block[viterbi_offset];
  for(i = 1; i < sparm->label_num; i++) {
    if( viterbi_val_block[viterbi_offset + i] > max ) {
      max = viterbi_val_block[viterbi_offset + i];
      maxIdx = i;
    }
  }

  for(i = x.frame_num-1; i >= 0; i--) {
    ybar.y[i] = maxIdx;
    maxIdx = viterbi_prev_block[i * sparm->label_num + maxIdx];
  }


  return(ybar);
}

int         empty_label(LABEL y)
{
  /* Returns true, if y is an empty label. An empty label might be
     returned by find_most_violated_constraint_???(x, y, sm) if there
     is no incorrect label that can be found for x, or if it is unable
     to label x at all */
  return(0);
}

SVECTOR     *psi(PATTERN x, LABEL y, STRUCTMODEL *sm,
		 STRUCT_LEARN_PARM *sparm)
{
  /* Returns a feature vector describing the match between pattern x
     and label y. The feature vector is returned as a list of
     SVECTOR's. Each SVECTOR is in a sparse representation of pairs
     <featurenumber:featurevalue>, where the last pair has
     featurenumber 0 as a terminator. Featurenumbers start with 1 and
     end with sizePsi. Featuresnumbers that are not specified default
     to value 0. As mentioned before, psi() actually returns a list of
     SVECTOR's. Each SVECTOR has a field 'factor' and 'next'. 'next'
     specifies the next element in the list, terminated by a NULL
     pointer. The list can be though of as a linear combination of
     vectors, where each vector is weighted by its 'factor'. This
     linear combination of feature vectors is multiplied with the
     learned (kernelized) weight vector to score label y for pattern
     x. Without kernels, there will be one weight in sm.w for each
     feature. Note that psi has to match
     find_most_violated_constraint_???(x, y, sm) and vice versa. In
     particular, find_most_violated_constraint_???(x, y, sm) finds
     that ybar!=y that maximizes psi(x,ybar,sm)*sm.w (where * is the
     inner vector product) and the appropriate function of the
     loss + margin/slack rescaling method. See that paper for details. */
  SVECTOR *fvec=NULL;

  /* insert code for computing the feature vector for x and y here */
  // TODO
  if(x.frame_num != y.frame_num) {
    printf("ERROR: unequal frame_num in psi()\n");
    exit(-1);
  }
  WORD* words = (WORD*) my_malloc(sizeof(WORD) * (sm->sizePsi + 1));
  int i = 0, j = 0;
  for(i = 0; i < sm->sizePsi; i++) {
    words[i].wnum = i+1;
    words[i].weight = 0;
  }
  words[sm->sizePsi].wnum = 0;
  words[sm->sizePsi].weight = 0;

  for(i = 0; i < x.frame_num; i++) {
    int frame_label = y.y[i];
    int offset = frame_label * sparm->feature_dim;
    for(j = 0; j < sparm->feature_dim; j++) {
      words[offset+j].weight += x.x[i][j];
    }
  }

  int offset = sparm->label_num * sparm->feature_dim;
  for(i = 1; i < x.frame_num; i++) {
    int prev_label = y.y[i-1];
    int this_label = y.y[i];
    words[offset + prev_label * sparm->label_num + this_label].weight += 1;
  }

  // we already alloc words, use shallow copy
  fvec = create_svector_shallow(words, NULL, 1.0);

  return(fvec);
}

double      loss(LABEL y, LABEL ybar, STRUCT_LEARN_PARM *sparm)
{
  /* loss for correct label y and predicted label ybar. The loss for
     y==ybar has to be zero. sparm->loss_function is set with the -l option. */
  
  //if(sparm->loss_function == 0) { /* type 0 loss: 0/1 loss */
  //                                /* return 0, if y==ybar. return 1 else */
  //}
  //else {
    /* Put your code for different loss functions here. But then
       find_most_violated_constraint_???(x, y, sm) has to return the
       highest scoring label with the largest loss. */
  //}
  // TODO
  if(y.frame_num != ybar.frame_num) {
    printf("ERROR: unequal label length in loss()\n");
    exit(-1);
  }
  int i = 0;
  double cost = 0;
  for(i = 0; i < y.frame_num; i++) {
    if(y.y[i] != ybar.y[i]) {
      cost += 1;
    }
  }
  return cost;
}

int         finalize_iteration(double ceps, int cached_constraint,
			       SAMPLE sample, STRUCTMODEL *sm,
			       CONSTSET cset, double *alpha, 
			       STRUCT_LEARN_PARM *sparm)
{
  /* This function is called just before the end of each cutting plane iteration. ceps is the amount by which the most violated constraint found in the current iteration was violated. cached_constraint is true if the added constraint was constructed from the cache. If the return value is FALSE, then the algorithm is allowed to terminate. If it is TRUE, the algorithm will keep iterating even if the desired precision sparm->epsilon is already reached. */
  return(0);
}

void        print_struct_learning_stats(SAMPLE sample, STRUCTMODEL *sm,
					CONSTSET cset, double *alpha, 
					STRUCT_LEARN_PARM *sparm)
{
  /* This function is called after training and allows final touches to
     the model sm. But primarly it allows computing and printing any
     kind of statistic (e.g. training error) you might want. */
}

void        print_struct_testing_stats(SAMPLE sample, STRUCTMODEL *sm,
				       STRUCT_LEARN_PARM *sparm, 
				       STRUCT_TEST_STATS *teststats)
{
  /* This function is called after making all test predictions in
     svm_struct_classify and allows computing and printing any kind of
     evaluation (e.g. precision/recall) you might want. You can use
     the function eval_prediction to accumulate the necessary
     statistics for each prediction. */
}

void        eval_prediction(long exnum, EXAMPLE ex, LABEL ypred, 
			    STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm, 
			    STRUCT_TEST_STATS *teststats)
{
  /* This function allows you to accumlate statistic for how well the
     predicition matches the labeled example. It is called from
     svm_struct_classify. See also the function
     print_struct_testing_stats. */
  if(exnum == 0) { /* this is the first time the function is
		      called. So initialize the teststats */
  }
}

void        write_struct_model(char *file, STRUCTMODEL *sm, 
			       STRUCT_LEARN_PARM *sparm)
{
  /* Writes structural model sm to file file. */
  // TODO
  FILE* fp;
  fp = fopen(file, "w");
  int i = 0;
  fprintf(fp, "%d\n", sm->sizePsi);
  for(i = 0; i < sm->sizePsi+1; i++) {
    fprintf(fp, "%f ", sm->w[i]);
  }
  fclose(fp);
}

STRUCTMODEL read_struct_model(char *file, STRUCT_LEARN_PARM *sparm)
{
  /* Reads structural model sm from file file. This function is used
     only in the prediction module, not in the learning module. */
  // TODO
  FILE* fp;
  STRUCTMODEL sm;

  fp = fopen(file, "r");

  fscanf(fp, "%d", &sm.sizePsi);

  sm.w = my_malloc(sizeof(double)*(sm.sizePsi+1));

  int i = 0;
  for(i = 0;i < sm.sizePsi+1; i++) {
    fscanf(fp, "%f", &sm.w[i]);
  }
  fclose(fp);
  
  return(sm);
}

void        write_label(FILE *fp, LABEL y)
{
  /* Writes label y to file handle fp. */
  int i;
  fprintf(fp, "%s", y.filename);
  for(i=0 ; i<y.frame_num ; i++) {
    fprintf(fp, " %d", y.y[i]);
  }
  fprintf(fp, "\n");
} 

void        free_pattern(PATTERN pattern) {
  /* Frees the memory of x. */
  int i;
  if( pattern.frame_num > 0 ) {
    for(i=0 ; i<pattern.frame_num ; i++) {
      free(pattern.x[i]);
    }
    free(pattern.x);
  }
  if( pattern.filename ) {
    free(pattern.filename);
  }
}

void        free_label(LABEL label) {
  /* Frees the memory of y. */
  if( label.frame_num > 0 ) {
    free(label.y);
  }
}

void        free_struct_model(STRUCTMODEL sm) 
{
  /* Frees the memory of model. */
  /* if(sm.w) free(sm.w); */ /* this is free'd in free_model */
  if(sm.svm_model) free_model(sm.svm_model,1);
  /* add free calls for user defined data here */
}

void        free_struct_sample(SAMPLE s)
{
  /* Frees the memory of sample s. */
  int i;
  for(i=0;i<s.n;i++) { 
    free_pattern(s.examples[i].x);
    free_label(s.examples[i].y);
  }
  free(s.examples);
}

void        print_struct_help()
{
  /* Prints a help text that is appended to the common help text of
     svm_struct_learn. */
  printf("         --* string  -> custom parameters that can be adapted for struct\n");
  printf("                        learning. The * can be replaced by any character\n");
  printf("                        and there can be multiple options starting with --.\n");
}

void         parse_struct_parameters(STRUCT_LEARN_PARM *sparm)
{
  /* Parses the command line parameters that start with -- */
  int i;

  for(i=0;(i<sparm->custom_argc) && ((sparm->custom_argv[i])[0] == '-');i++) {
    switch ((sparm->custom_argv[i])[2]) 
      { 
      case 'a': i++; /* strcpy(learn_parm->alphafile,argv[i]); */ break;
      case 'e': i++; /* sparm->epsilon=atof(sparm->custom_argv[i]); */ break;
      case 'k': i++; /* sparm->newconstretrain=atol(sparm->custom_argv[i]); */ break;
      default: printf("\nUnrecognized option %s!\n\n",sparm->custom_argv[i]);
	       exit(0);
      }
  }
}

void        print_struct_help_classify()
{
  /* Prints a help text that is appended to the common help text of
     svm_struct_classify. */
  printf("         --* string -> custom parameters that can be adapted for struct\n");
  printf("                       learning. The * can be replaced by any character\n");
  printf("                       and there can be multiple options starting with --.\n");
}

void         parse_struct_parameters_classify(STRUCT_LEARN_PARM *sparm)
{
  /* Parses the command line parameters that start with -- for the
     classification module */
  int i;

  for(i=0;(i<sparm->custom_argc) && ((sparm->custom_argv[i])[0] == '-');i++) {
    switch ((sparm->custom_argv[i])[2]) 
      { 
      /* case 'x': i++; strcpy(xvalue,sparm->custom_argv[i]); break; */
      default: printf("\nUnrecognized option %s!\n\n",sparm->custom_argv[i]);
	       exit(0);
      }
  }
}

