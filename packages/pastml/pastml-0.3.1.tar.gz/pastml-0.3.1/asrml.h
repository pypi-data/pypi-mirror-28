#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <limits.h>

#ifndef ASRML_H
#define ASRML_H

#define ITMAX_O 1000
#define ITMAX 200
#define EPS 1.0e-10
#define TOL 2.0e-4
#define GOLD 1.618034
#define GLIMIT 100.0
#define TINY 1.0e-20
#define CGOLD 0.3819660
#define ZEPS 1.0e-10
#define STEP 1.0e-4
#define STEP2 1.0e-4
#define STEP3 1.0e-9
#define SCAL_MIN 1.0e-4
#define SIGMA 1.0e-3

#define MAXLNAME 255
#define MAXLLINE 10000
#define MAXNSP 50000
#define MAXPOLY 10000
#define MAXCHAR 50
#define MIN_BRLEN    1e-5
#define MAX_TREELENGTH    10000000 /* more or less 10MB for a tree file in NH format */
#define MAX_NODE_DEPTH    100000 /* max depth for nodes in the tree */
#define MAX_NAMELENGTH        255    /* max length of a taxon name */
#define MAX_COMMENTLENGTH    255    /* max length of a comment string in NHX format */
#define MAXNTREE 1
#define TRUE 1
#define FALSE 0
#define SIMREP 50
#define EPSILON 1e-10
#define LIM_P pow(2,-50)
#define POW -50
#define MAX_TAX 10000
#define LOG2 0.69314718055994528623
#define MIN(a, b) ((a)<(b)?(a):(b))

#ifndef _IO_H
#define _IO_H

#endif

typedef struct __Node {
    char *name;
    char *comment;        /* for further use: store any comment (e.g. from NHX format) */
    int id;            /* unique id attributed to the node */
    short int nneigh;    /* number of neighbours */
    struct __Node **neigh;    /* neighbour nodes */
    struct __Edge **br;    /* corresponding branches going from this node */
    double depth;        /* the depth of a node is its min distance to a leaf */

    double **pij;           /* probability of substitution */
    double *condlike;       /*conditional likelihoods at the node*/
    double *condlike_mar;
    double *marginal;
    int *tmp_best;
    double *mar_prob;
    double *up_like;
    double *sum_down;
    int up_factor;
    int down_factor;
    double **rootpij;
    int pupko_state;
    int *local_flag;
    int count;

} Node;


/* Every edge connects two nodes.
   By convention, all terminal branches will have the tip on their RIGHT end */


typedef struct __Edge {
    int id;
    Node *left, *right;        /* in rooted trees the right end will always be the descendant.
			      		 In any case, a leaf is always on the right side of its branch. */
    double brlen;
    double branch_support;
    int *subtype_counts[2];        /* first index is 0 for the left of the branch, 1 for its right side */

    short int had_zero_length;    /* set at the moment when we read the tree, even though
				      		   we then immediately set the branch length to MIN_BRLEN */
    short int has_branch_support;
    int topo_depth;            /* the topological depth is the number of taxa on the lightest side of the bipar */
} Edge;


typedef struct __Tree {
    Node **a_nodes;            /* array of node pointers */
    Edge **a_edges;            /* array of edge pointers */
    Node *node0;            /* the root or pseudo-root node */
    int nb_nodes;
    int nb_edges;
    int nb_taxa;
    char **taxa_names;        /* store only once the taxa names */
    int next_avail_node_id;
    int next_avail_edge_id;
    int next_avail_taxon_id;
    char **taxname_lookup_table;
    double avgbl;
    double min_bl;
} Tree;

#endif // ASRML_H
