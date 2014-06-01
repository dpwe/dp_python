dp_python
=========

Optimized Dynamic Programming (Dynamic Time Warp) as a Python external.

Based on the Matlab DP external: http://labrosa.ee.columbia.edu/matlab/dtw/

Implments the classic dynamic programming best-path calculation.  Because the inner loop is implemented as a C routine, it is more than 1000x faster than the equivalent pure Python.

You need to execute `make -f Makefile.dpcore_py` to create the compiled object to load into Python.  The enclosed Makefile works for my Homebrew install of Python on my Macbook; other machines/installs will require edited Makefiles.

See `dp.py` for the source of an ipython notebook demonstrating the usage.  The output is here: http://nbviewer.ipython.org/github/dpwe/dp_python/blob/master/dp.ipynb

Functions in `dpcore.py`
------------------------

`dp(local_costs, penalty=0.0, gutter=0.0)`

Use dynamic programming to find a min-cost path through a matrix 
of local costs.

:params:
  local_costs : np.array of float
    matrix of local costs at each cell
  penalty : float
    additional cost incurred by (0,1) and (1,0) steps [default: 0.0]
  gutter : float
    proportion of edge length away from [-1,-1] that best path will 
    be accepted at. [default: 0.0 i.e. must reach top-right]

:returns:
  p, q : np.array of int
    row and column indices of best path
  total_costs : np.array of float
    matrix of minimum costs to each point
  phi : np.array of int
    traceback matrix indicating preceding best-path step for each cell:
      0  diagonal predecessor
      1  previous column, same row
      2  previous row, same column

:note:
  port of Matlab routine dp.m, 
  http://labrosa.ee.columbia.edu/matlab/dtw/



`dpcore(M, pen, use_extension=USE_EXTENSION)`

Core dynamic programming calculation of best path.

M[r,c] is the array of local costs.  
Create D[r,c] as the array of costs-of-best-paths to r,c, 
and phi[r,c] as the indicator of the point preceding [r,c] to 
allow traceback; 0 = (r-1,c-1), 1 = (r,c-1), 2 = (r-1, c)

:params:
    M : np.array of float
      Array of local costs
    pen : float
      Penalty to apply for non-diagonal steps

:returns:
    D : np.array of float
      Array of best costs to each point, starting from (0,0)
    phi : np.array of int
      Traceback indices indicating the last step taken by 
      the lowest-cost path reaching this point.  Values:
	0 : previous point was r-1, c-1
	1 : previous point was r, c-1
	2 : previous point was r-1, c
