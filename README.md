dp_python
=========

Optimized Dynamic Programming (DP) / Dynamic Time Warp (DTW) as a Python external.

Implments the classic dynamic programming best-path calculation.  Because the inner loop is implemented as a C routine, it is 500-1000x faster than the equivalent pure Python.

The external library needs to be compiled; this should be possible with `python setup.py build`.  This creates the `_dpcore_py.so` file that needs to go in the same directory as `dpcore.py`.  (If you're using HomeBrew on a Mac, you may be able to simply `make -f Makefile.dpcore_py` to create the compiled object.)  

See http://nbviewer.ipython.org/github/dpwe/dp_python/blob/master/dp.ipynb for an ipython notebook demonstrating the DTW alignment of two spoken utterances.

Based on the Matlab DP external: http://labrosa.ee.columbia.edu/matlab/dtw/

<HR>

Functions in `dpcore.py`
------------------------

#####`dp(local_costs, penalty=0.0, gutter=0.0)`

Use dynamic programming to find a min-cost path through a matrix 
of local costs.

**params**
<DL>
  <DT>local_costs : <I>np.array of float</I></DT>
    <DD>matrix of local costs at each cell</DD>
  <DT>penalty : <I>float</I></DT>
    <DD>additional cost incurred by (0,1) and (1,0) steps [default: 0.0]</DD>
  <DT>gutter : <I>float</I></DT>
    <DD>proportion of edge length away from [-1,-1] that best path will 
    be accepted at. [default: 0.0 i.e. must reach top-right]</DD>
</DL>

**returns**
<DL>
  <DT>p, q : <I>np.array of int</I></DT>
    <DD>row and column indices of best path</DD>
  <DT>total_costs : <I>np.array of float</I></DT>
    <DD>matrix of minimum costs to each point</DD>
  <DT>phi : <I>np.array of int</I></DT>
    <DD>traceback matrix indicating preceding best-path step for each cell:
       <UL>
         <LI>0  -- diagonal predecessor </LI>
         <LI>1  -- previous column, same row</LI>
         <LI>2  -- previous row, same column</LI>
       </UL></DD>
</DL>

**note**
  Port of Matlab routine `dp.m` (with some modifications).  See 
  http://labrosa.ee.columbia.edu/matlab/dtw/

<HR>

#####`dpcore(M, pen, use_extension=True)`

Core dynamic programming calculation of best path.

M[r,c] is the array of local costs.  
Create D[r,c] as the array of costs-of-best-paths to r,c, 
and phi[r,c] as the indicator of the point preceding [r,c] to 
allow traceback; 0 = (r-1,c-1), 1 = (r,c-1), 2 = (r-1, c)

**params**
<DL>
    <DT>M : <I>np.array of float</I></DT>
      <DD>Matrix of local costs</DD>
    <DT>pen : <I>float</I></DT>
      <DD>Penalty to apply for non-diagonal steps</DD>
    <DT>use_extension : <I>boolean</I></DT>
      <DD>If False, use the pure-python parallel implementation [default: True]</DD>
</DL>

**returns**
<DL>
    <DT>D : <I>np.array of float</I></DT>
      <DD>Array of best costs to each point, starting from (0,0)</DD>
    <DT>phi : <I>np.array of int</I></DT>
      <DD>Traceback indices indicating the last step taken by 
      the lowest-cost path reaching this point.  Values:
         <UL>
	   <LI>0  -- previous point was r-1, c-1</LI>
           <LI>1  -- previous point was r, c-1</LI>
           <LI>2  -- previous point was r-1, c</LI>
         </UL></DD>
</DL>
