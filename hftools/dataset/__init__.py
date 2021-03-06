# -*- coding: ISO-8859-1 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, HFTools Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from hftools.dataset.dim import DimSweep, DimRep,\
    DimMatrix_i, DimMatrix_j, _DimMatrix, DerivAxis, IndepAxis, DiagAxis, \
    ComplexDerivAxis, ComplexIndepAxis, ComplexDiagAxis, dims_has_complex,\
    DimPartial, DimBase, CPLX

from hftools.dataset.arrayobj import make_matrix, hfarray, ismatrix,\
    make_same_dims, make_same_dims_list, change_shape, remove_tail,\
    remove_rep, isfullcomplex, make_fullcomplex_array, DimsList, make_vector,\
    ValueArray    #Deprecated


from hftools.dataset.dataset import DataDict, DataBlock, \
    change_dim, DataBlockError, yield_dim_consistent_datablocks,\
    convert_matrices_to_elements

from hftools.dataset.comments import Comments
