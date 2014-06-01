/*
 * dpcore_py.c - calculate dynamic programming inner loop
 *   Python extension version
 * 2014-05-30 Dan Ellis dpwe@ee.columbia.edu
 */

/* see http://wiki.scipy.org/Cookbook/C_Extensions/NumPy_arrays */
#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <numpy/npy_math.h>

static void calc_dpcore(
			double *pM,  /* input scores */
			int rows,      /* size of arrays */
			int cols, 
			double pen,     /* nondiagonal penalty score */
			double *pD,  /* output best-cost matrix */
			int   *pP   /* output traceback matrix */
			)
{
    /* Data is passed in as pointers to contiguous, row-first memory 
       blocks for each array, that we interpret appropriately here */
    int i, j, k, tb;
    double d1, d2, d3, v;
    double *costs;
    int *steps;
    int ncosts;
    
    /* setup cost matrix */
    int ii;

    ncosts = 3;
    costs = (double *)malloc(ncosts*sizeof(double));
    steps = (int *)malloc(ncosts*2*sizeof(int));
    steps[0] = 1;	steps[1] = 1;	costs[0] = 0.0;
    steps[2] = 0;	steps[3] = 1;	costs[1] = pen;
    steps[4] = 1;	steps[5] = 0;	costs[2] = pen;

    /* do dp */
    v = pM[0];	
    tb = 0;	/* value to use for 0,0 */
    for (j = 0; j < cols; ++j) {
	for (i = 0; i < rows; ++i) {
	    d1 = pM[i*cols + j];
	    for (k = 0; k < ncosts; ++k) {
		if ( i >= steps[2*k] && j >= steps[2*k+1] ) {
		    d2 = d1 + costs[k] + pD[(i-steps[2*k])*cols + (j-steps[2*k+1])];
		    if (d2 < v) {
			v = d2;
			tb = k;
		    }
		}
	    }

	    pD[i*cols + j] = v;
	    pP[i*cols + j] = tb;
	    v = NPY_INFINITY;
	}
    }
    free((void *)costs);
    free((void *)steps);
}

//////////////////////////// python extension wrapper /////////////////////

/* ==== Check that PyArrayObject is a double (Float) type and a matrix ==========
    return 1 if an error and raise exception */ 
int  not_doublematrix(PyArrayObject *mat)  {
    if (mat->descr->type_num != NPY_DOUBLE || mat->nd != 2)  {
        PyErr_SetString(PyExc_ValueError,
			"In not_doublematrix: array must be of type Float and 2 dimensional (n x m).");
        return 1;  }
    return 0;
}

static PyObject *
dpcore_py_dpcore(PyObject *self, PyObject *args)
{
    PyArrayObject *Sin, *Dout, *Pout;
    double pen;
    double *Sptr, *Dptr;
    int *Pptr;
    int nrows, ncols;
    npy_intp dims[2];
    
    /* parse input args */
    if (!PyArg_ParseTuple(args, "O!d", 
			  &PyArray_Type, &Sin, &pen))
	return NULL;
    if (Sin == NULL)  return NULL;

    /* Check that object input is 'double' type and a matrix
       Not needed if python wrapper function checks before call to this routine */
    if (not_doublematrix(Sin)) return NULL;

    /* Get the dimension of the input */
    nrows = Sin->dimensions[0];
    ncols = Sin->dimensions[1];

    /* Set up output matrices */
    dims[0] = nrows;
    dims[1] = ncols;
    Dout = (PyArrayObject *)PyArray_SimpleNew(2, dims, NPY_DOUBLE);
    Pout = (PyArrayObject *)PyArray_SimpleNew(2, dims, NPY_INT);

    /* Change contiguous arrays into C *arrays */
    Sptr = (double *)Sin->data;
    Dptr = (double *)Dout->data;
    Pptr = (int *)Pout->data;

    /* run calculation */
    calc_dpcore(Sptr, nrows, ncols, pen, Dptr, Pptr);

    /* return the result */
    PyObject *tupleresult = PyTuple_New(2);
    PyTuple_SetItem(tupleresult, 0, PyArray_Return(Dout));
    PyTuple_SetItem(tupleresult, 1, PyArray_Return(Pout));
    return tupleresult;
}

/* standard hooks to Python, per http://docs.python.org/2/extending/extending.html */
	
static PyMethodDef DpcoreMethods[] = {
    {"dpcore",  dpcore_py_dpcore, METH_VARARGS},
    {NULL, NULL}        /* Sentinel */
};


/* ==== Initialize the C_test functions ====================== */
// Module name must be _dpcoremodule in compile and linked 
void init_dpcore_py()  {
    (void) Py_InitModule("_dpcore_py", DpcoreMethods);
    import_array();  // Must be present for NumPy.  Called first after above line.
}



