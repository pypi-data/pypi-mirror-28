scikit-traveltime: traveltime calculation using the fast marching method for Python
===================================================================================


.. code:: 

   import numpy as np
   import traveltime as tt
   plt.ion() 
   
   #%% CREATE REFERENCE VELOCITY MODEL
   dx=0.1;
   x = np.arange(-1,6,dx)
   y = np.arange(-1,13,dx)
   V=0.1*np.ones((len(y),len(x)))
   
   #%% SET SOURCE AND RECEIVERS
   S=np.array([[0,2],[0,5],[0,4]])
   R=np.array([[5,12],[5,5],[5,1]])
   
   t = tt.eikonal_traveltime(x,y,[],V,S,R)
       

Documentation
--------------

PyPI
~~~~~~~~~~~
`<http://pypi.python.org/pypi/scikit-traveltime>`

Requirements
~~~~~~~~~~~
* Numpy >= 1.0.2
* scikit-fmm >= 1

Bugs, questions, patches, feature requests, discussion & cetera
~~~~~~~~~~~
* Open a GitHub pull request or a GitHub issue

Installing
~~~~~~~~~~~
* Via pip: `pip install scikit-traveltime`

Version History:
~~~~~~~~~~~
* 0.0.1: July 1st, 2017
* 0.0.4: January 3rd, 2017
  
Copyright 2018 Thomas Mejer Hansen

BSD-style license. See LICENSE.txt in the source directory.
