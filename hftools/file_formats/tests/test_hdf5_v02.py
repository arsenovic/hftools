
#-----------------------------------------------------------------------------
# Copyright (c) 2014, HFTools Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
import h5py
import numpy as np

import hftools
import hftools.file_formats.hdf5.v_02 as v_02
import hftools.file_formats.hdf5 as hdf5
from hftools import path
from hftools.testing import TestCase
import hftools.file_formats.tests.base_test as base_test
from hftools.dataset import DataBlock, hfarray, DimSweep, DimRep
from hftools.file_formats.common import Comments

from hftools.file_formats.hdf5.v_01 import save_hdf5 as save_hdf5_v01
from hftools.file_formats.hdf5.v_02 import append_hdf5
from hftools.file_formats.hdf5.helper import hdf5context
testpath = path(__file__).dirname()


readfun = hftools.file_formats.hdf5.v_02.read_hdf5
savefun = hftools.file_formats.hdf5.v_02.save_hdf5


class Test_hdf5_data_1(base_test.Test_1):
    readfun = [readfun]
    basepath = testpath
    dirname = "hdf5/v02"
    extension = ".hdf5"
    readpars = dict(verbose=False)


class Test_hdf5_data_1b(base_test.Test_1):
    readfun = [readfun]
    basepath = testpath
    dirname = "hdf5/v02"
    extension = ".hdf5"
    filename = "test1b"
    readpars = dict(verbose=False)


class Test_hdf5_main_data_1(Test_hdf5_data_1):
    readfun = [hdf5.read_hdf5]


class Test_hdf5_main_data_1b(Test_hdf5_data_1b):
    readfun = [hdf5.read_hdf5]


class Test_hdf5_specific(TestCase):
    def test_both(self):
        d1 = readfun(testpath / "testdata/hdf5/v02/test1.hdf5")
        with h5py.File(testpath / "testdata/hdf5/v02/test1.hdf5", "r") as fil:
            d2 = readfun(fil)
        self.assertAllclose(d1.S, d2.S)

    def test_none(self):
        db = DataBlock()
        db.x = hfarray(1)
        fname = testpath / "testdata/hdf5/v02/slask.hdf5"
        savefun(db, fname)
        db = readfun(fname)
        self.assertIsNone(db.blockname)
        fname.unlink()


class Test_read_hdf5_handle(TestCase):
    def test1(self):
        self.assertRaises(IOError, v_02.read_hdf5_handle, "unknown.hdf5")

# There is no point to make tests based on Test_2 and Test_3 as they are
# dB/arg, mag/arg


class Test_hdf5_data_save_exceptions(TestCase):
    savefun = [savefun]

    @classmethod
    def setUpClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        if not p.exists():  # pragma: no cover
            p.makedirs()

    @classmethod
    def tearDownClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        for f in p.glob("*"):  # pragma: no cover
            f.unlink()
        p.removedirs()

    def test_1(self):
        d = DataBlock()
        d["b/a"] = hfarray([2], dims=(DimSweep("a", 1),))
        fname = testpath / "testdata/hdf5/v02/savetest/slask.hdf5"
        self.assertRaises(Exception, self.savefun[0], d, fname)
        fname.unlink()


class Test_hdf5_data_save(TestCase):
    savefun = [savefun]

    @classmethod
    def setUpClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        if not p.exists():  # pragma: no cover
            p.makedirs()

    @classmethod
    def tearDownClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        for f in p.glob("*"):  # pragma: no cover
            f.unlink()
        p.removedirs()

    def test_1(self):
        d = DataBlock()
        d.b = hfarray([2], dims=(DimSweep("a", 1),))
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"
        self.savefun[0](d, fname)
        fname.unlink()

    def test_2(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10"])
#        import pdb;pdb.set_trace()
        d.b = hfarray([2], dims=(DimSweep("a", 1),))
        fname = testpath / "testdata/hdf5/v02/savetest/res_2.hdf5"
        self.savefun[0](d, fname)
        fname.unlink()

    def test_3(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dims = (DimSweep("f", 3, outputformat="%.1f"),
                DimSweep("i", 2, outputformat="%.0f"),
                DimSweep("j", 2, outputformat="%.0f"), )
        d.c = hfarray([[[1, 2], [3, 4]],
                       [[10, 20], [30, 40]],
                       [[10, 20], [30, 40]]],
                      dims=dims,
                      outputformat="%.2f")
        fname = testpath / "testdata/hdf5/v02/savetest/res_3.hdf5"
        self.savefun[0](d, fname)
        fname.unlink()

    def test_4(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        fname = testpath / "testdata/hdf5/v02/savetest/res_4.hdf5"
        self.savefun[0](d, fname)
        fname.unlink()

    def test_5(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        d.date = hfarray("2012-08-13 08:03:01", dtype="datetime64[us]")
        fname = testpath / "testdata/hdf5/v02/savetest/res_5.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        fname.unlink()
        self.assertEqual(d2.date, d.date)

    def test_6(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        d.date = hfarray(["2012-08-13 08:03:01"] * 3, dims=(dim, ),
                         dtype="datetime64[us]")
        fname = testpath / "testdata/hdf5/v02/savetest/res_6.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        fname.unlink()
        self.assertEqual(str(d2.date), str(d.date))

    def test_7(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        d.date = hfarray(["2012-08-13 08:03:01"],
                         dims=(DimSweep("dateidx", 1),),
                         dtype="datetime64[us]")
        fname = testpath / "testdata/hdf5/v02/savetest/res_7.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        fname.unlink()
        self.assertEqual(d2.date, d.date)

    def test_8(self):
        d = DataBlock()
        d.b = hfarray([2], dims=(DimSweep("a", 1),))
        fname = testpath / "testdata/hdf5/v02/savetest/res_8.hdf5"
        with h5py.File(fname, mode="w") as fil:
            self.savefun[0](d, fil)
        fname.unlink()

    def test_9(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10"])
#        import pdb;pdb.set_trace()
        d.b = hfarray([2], dims=(DimSweep("a", 1), ), unit="V")
        fname = testpath / "testdata/hdf5/v02/savetest/res_9.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        self.assertEqual(d2.b.unit, "V")
        fname.unlink()

    def test_10(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10"])
#        import pdb;pdb.set_trace()
        d.b = hfarray([2], dims=(DimSweep("a", 1), ), unit="V")
        d.b.outputformat = ""
        fname = testpath / "testdata/hdf5/v02/savetest/res_10.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        self.assertEqual(d2.b.outputformat, "%d")

        fname.unlink()

    def test_11(self):
        ia = DimSweep("a", 1)
        d = DataBlock()
        d.comments = Comments(["Hej=10"])
#        import pdb;pdb.set_trace()
        d.b = hfarray([u"kalle"], dims=(ia, ), unit="V")
        d.c = hfarray(u"kalle")
        fname = testpath / "testdata/hdf5/v02/savetest/res_11.hdf5"
        self.savefun[0](d, fname)
        d2 = readfun(fname)
        self.assertEqual(d2.b[0], u"kalle")
        self.assertEqual(d2.c, u"kalle")
        fname.unlink()


class Test_hdf5_main_data_save(Test_hdf5_data_save):
    savefun = [lambda d, x: hdf5.save_hdf5(d, x, version="0.2")]


class Test_hdf5_data_expandable(TestCase):
    @classmethod
    def setUpClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        if not p.exists():  # pragma: no cover
            p.makedirs()

    @classmethod
    def tearDownClass(cls):
        p = path(testpath / "testdata/hdf5/v02/savetest")
        p.removedirs()

    def test_1(self):
        i1 = DimSweep("a", 1, unit="s", outputformat="")
        i2 = DimSweep("INDEX", 2)
        d1 = DataBlock()
        d1.b = hfarray([2], dims=(i1,), outputformat="")
        d2 = DataBlock()
        d2.b = hfarray([3], dims=(i1,))
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"
        with hdf5context(fname, mode="w") as fil:
            savefun(d1, fil, expandable=True)
            append_hdf5(d2, fil)
        d = readfun(fname)
        self.assertAllclose(hfarray([[2, 3]], dims=(i1, i2)), d.b)
        self.assertEqual(d.ivardata["a"].unit, "s")
        self.assertEqual(d.ivardata["a"].outputformat, "%d")
        self.assertEqual(d.b.outputformat, "%d")
        fname.unlink()

    def test_2(self):
        i1 = DimSweep("a", 1, unit="s", outputformat="")
        i2 = DimSweep("INDEX", 2, unit="s")
        iexpand = DimRep("INDEX", 1, unit="s", outputformat="")
        d1 = DataBlock()
        d1.b = hfarray([2], dims=(i1,), outputformat="")
        d1.c = hfarray(3)
        d2 = DataBlock()
        d2.b = hfarray([3], dims=(i1,))
        d2.c = hfarray(2)
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"
        with hdf5context(fname, mode="w") as fil:
            savefun(d1, fil, expandable=True, expanddim=iexpand)
            append_hdf5(d2, fil, expanddim=iexpand)
        d = readfun(fname)
        self.assertAllclose(hfarray([[2, 3]], dims=(i1, i2)), d.b)
        self.assertAllclose(hfarray([3, 2], dims=(i2,)), d.c)
        self.assertEqual(d.ivardata["a"].unit, "s")
        self.assertEqual(d.ivardata["INDEX"].unit, "s")
        self.assertEqual(d.ivardata["a"].outputformat, "%d")
        self.assertEqual(d.ivardata["INDEX"].outputformat, "%d")
        self.assertEqual(d.b.outputformat, "%d")
        fname.unlink()

    def test_cant_append(self):
        i1 = DimSweep("a", 1, unit="s", outputformat="")
        i2 = DimSweep("INDEX", 2, unit="s")
        iexpand = DimRep("INDEX", 1, unit="s", outputformat="")
        d1 = DataBlock()
        d1.b = hfarray([2], dims=(i1,), outputformat="")
        d1.c = hfarray(3)
        d2 = DataBlock()
        d2.b = hfarray([3], dims=(i1,))
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"
        with hdf5context(fname, mode="w") as fil:
            savefun(d1, fil, expandable=True, expanddim=iexpand)
            self.assertRaises(ValueError, append_hdf5, d2, fil)
        fname.unlink()




    def test_wrong_version_1(self):
        ia = DimSweep("a", 1, unit="")
        d1 = DataBlock()
        d1.b = hfarray([2], dims=(ia,))
        d2 = DataBlock()
        d2.b = hfarray([3], dims=(ia,))
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"

        with hdf5context(fname, mode="w") as fil:
            save_hdf5_v01(d1, fil)
            self.assertRaises(Exception, append_hdf5, d2, fil)
#            append_hdf5(d2, fil)
        fname.unlink()

    def test_wrong_version_2(self):
        ia = DimSweep("a", 1, unit="")
        d1 = DataBlock()
        d1.b = hfarray([2], dims=(ia,))
        d2 = DataBlock()
        d2.b = hfarray([3], dims=(ia,))
        fname = testpath / "testdata/hdf5/v02/savetest/res_1.hdf5"

        with hdf5context(fname, mode="w") as fil:
            save_hdf5_v01(d1, fil)
            self.assertRaises(Exception, append_hdf5, d2, fil)
#            append_hdf5(d2, fil)
        fname.unlink()


if __name__ == '__main__':
    d = DataBlock()
    d.comments = Comments(["Hej=10", "Svejs=11"])
    dims = (DimSweep("f", 3, outputformat="%.1f"),
            DimSweep("i", 2, outputformat="%.0f"),
            DimSweep("j", 2, outputformat="%.0f"),)
    d.c = hfarray([[[1, 2], [3, 4]],
                   [[10, 20], [30, 40]],
                   [[10, 20], [30, 40]]], dims=dims, outputformat="%.2f")
    fname = testpath / "testdata/sp-data/savetest/res_3.txt"
    hftools.file_formats.spdata.save_spdata(d, fname)
    fname2 = testpath / "testdata/sp-data/a.txt"
    d2 = hftools.file_formats.read_spdata(fname2, verbose=False)
