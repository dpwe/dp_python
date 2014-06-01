#
# dpcore.py
#
# Dynamic Programming routine in Python
# with optional C extension.
#
# 2014-05-30 Dan Ellis dpwe@ee.columbia.edu

import numpy as np

USE_EXTENSION = True

if USE_EXTENSION:
  import _dpcore_py

def dpcore(M, pen, use_extension=USE_EXTENSION):
    """Core dynamic programming calculation of best path.
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
    """
    if use_extension:
        D, phi = _dpcore_py.dpcore(M, pen)
    else:
        # Pure python equivalent
        D = np.zeros(M.shape, dtype=np.float)
        phi = np.zeros(M.shape, dtype=np.int)
        # bottom edge can only come from preceding column
        D[0,1:] = M[0,0]+np.cumsum(M[0,1:]+pen)
        phi[0,1:] = 1
        # left edge can only come from preceding row
        D[1:,0] = M[0,0]+np.cumsum(M[1:,0]+pen)
        phi[1:,0] = 2
        # initialize bottom left
        D[0,0] = M[0,0]
        phi[0,0] = 0
        # Calculate the rest recursively
        for c in range(1, np.shape(M)[1]):
            for r in range(1, np.shape(M)[0]):
                best_preceding_costs = [D[r-1,c-1], pen+D[r,c-1], pen+D[r-1, c]]
                tb = np.argmin(best_preceding_costs)
                D[r,c] = best_preceding_costs[tb] + M[r,c]
                phi[r,c] = tb

    return D, phi

def dp(local_costs, penalty=0.0, gutter=0.0):
    """
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
    """
    rows, cols = np.shape(local_costs)
    total_costs = np.zeros( (rows+1, cols+1), np.float)
    total_costs[0,:] = np.inf
    total_costs[:,0] = np.inf
    total_costs[0,0] = 0
    # add gutters at start too
    colgutter = int(np.maximum(1, np.round(gutter*cols)))
    total_costs[0, :colgutter] = -penalty * np.arange(colgutter)
    rowgutter = int(np.maximum(1, np.round(gutter*rows)))
    total_costs[:rowgutter, 0] = -penalty * np.arange(rowgutter)
    # copy in local costs
    total_costs[1:(rows+1), 1:(cols+1)] = local_costs

    # Core routine to calculate matrix of min costs
    total_costs, phi = dpcore(total_costs, penalty)

    # Strip off the edges of the matrices used to create gutters
    total_costs = total_costs[1:, 1:]
    phi = phi[1:,1:]
    
    if gutter == 0:
        # Traceback from top left
        i = rows-1
        j = cols-1
    else:
        # Traceback from lowest cost "to edge" (gutters)
        best_top_pt = (cols - colgutter 
                       + np.argmin(total_costs[-1, -colgutter:]))
        best_right_pt = (rows - rowgutter
                         + np.argmin(total_costs[-rowgutter:, -1]))
        if total_costs[-1, best_top_pt] < total_costs[best_right_pt, -1]:
            i = rows - 1
            j = best_top_pt
        else:
            i = best_right_pt
            j = cols - 1

    # Do traceback from best end point to find best path
    # Start from lowest-total-cost point
    p = [i]
    q = [j]
    # Work backwards until we get to starting point (0, 0)
    while i >= 0 and j >= 0:
        tb = phi[i,j];
        if (tb == 0):
            i = i-1
            j = j-1
        elif (tb == 1):
            j = j-1
        elif (tb == 2):
            i = i-1
        p.insert(0, i)
        q.insert(0, j)

    return p[1:], q[1:], total_costs, phi


