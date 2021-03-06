#-----------------------------------------------------------------------------
# Copyright (c) 2014, HFTools Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
import hftools.file_formats
from hftools import path
from hftools.testing import TestCase
from hftools.file_formats.tests import base_test
from hftools.dataset import DataBlock, hfarray, DimSweep
from hftools.file_formats.common import Comments
from hftools.core.exceptions import HFToolsIOError

testpath = path(__file__).dirname()


class Test_hdf5_data_1(base_test.Test_1):
    readfun = [hftools.file_formats.read_spdata]
    basepath = testpath
    dirname = "sp-data"
    extension = ".txt"
    readpars = dict(verbose=False)


class Test_hdf5_data_1b(base_test.Test_1):
    readfun = [hftools.file_formats.read_spdata]
    basepath = testpath
    dirname = "sp-data"
    extension = ".txt"
    filename = "test1b"
    readpars = dict(verbose=False)


class Test_fullcoments(TestCase):
    def test_1(self):
        f1 = testpath / "testdata/sp-data/full_comments.txt"
        a = hftools.file_formats.read_spdata(f1)
        self.assertFalse("Fullcomments" in a.comments.fullcomments)

# There is no point to make tests based on Test_2 and Test_3 as they are
# dB/arg, mag/arg


class TestSPdata_Comment_1(base_test.Test_Comment_1):
    readfun = [hftools.file_formats.read_spdata]
    basepath = testpath
    dirname = "sp-data"
    extension = ".txt"


class TestSPdata_Comment_2(base_test.Test_Comment_2):
    readfun = [hftools.file_formats.read_spdata]
    basepath = testpath
    dirname = "sp-data"
    extension = ".txt"


class TestSPdata_multiple_columns(TestCase):
    def test_1(self):
        f1 = testpath / "testdata/sp-data/multiple_columns.txt"
        d = hftools.file_formats.read_spdata(f1, verbose=False)
        self.assertAllclose(d.a, [[0, 1], [3, 4], [6, 7]])
        self.assertAllclose(d.x, [2, 5, 8])


class TestSPdata_merge(TestCase):
    def test_1(self):
        f1 = testpath / "testdata/sp-data/a.txt"
        d_in = hftools.file_formats.read_spdata(f1, verbose=False)
        d = d_in.hyper(["I", "J"], "INDEX1")
        self.assertAllclose(d.Power, [[1.1, 1.2], [2.1, 2.2]])
        self.assertEqual(d.Power.unit, "dBm")
        self.assertAllclose(d.I, [1, 2])
        self.assertAllclose(d.J, [1, 2])
        self.assertAllclose(d.f, [1, 2, 3])
        self.assertAllclose(d.a, [[[0, 10], [0, 10]],
                                  [[3, 13], [3, 13]],
                                  [[6, 16], [6, 16]]])
        self.assertAllclose(d.b, [[[1, 11], [1, 11]],
                                  [[4, 14], [4, 14]],
                                  [[7, 17], [7, 17]]])
        self.assertAllclose(d.x, [[[2, 12], [2, 12]],
                                  [[5, 15], [5, 15]],
                                  [[8, 18], [8, 18]]])


class TestSPdata_read_single_column(TestCase):
    def test_1(self):
        f1 = testpath / "testdata/sp-data/single_freq.txt"
        d = hftools.file_formats.read_spdata(f1, verbose=False)
        self.assertAllclose(d.freq, [1e3, 1e5, 1e6])
        self.assertTrue("freq" in d.ivardata)
        self.assertTrue("freq" not in d.vardata)


class TestSPdata_errors_1(TestCase):
    def test_1(self):
        self.assertRaises(HFToolsIOError,
                          hftools.file_formats.read_spdata,
                          testpath / "testdata/sp-data/test_error_1.txt",
                          verbose=False)

    def test_2(self):
        self.assertRaises(HFToolsIOError,
                          hftools.file_formats.read_spdata,
                          testpath / "testdata/sp-data/test_error_2.txt",
                          verbose=False)

    def test_3(self):
        self.assertRaises(HFToolsIOError,
                          hftools.file_formats.read_spdata,
                          testpath / "testdata/sp-data/test_error_3.txt",
                          verbose=False)

    def test_4(self):
        self.assertRaises(HFToolsIOError,
                          hftools.file_formats.read_spdata,
                          testpath / "testdata/sp-data/test_error_4.txt",
                          verbose=False)


class TestSPdata_save(TestCase):
    def test_1(self):
        d = DataBlock()
        d.b = hfarray([2], dims=(DimSweep("a", 1),))
        f1 = testpath / "testdata/sp-data/savetest/res_1.txt"
        f2 = testpath / "testdata/sp-data/savetest/facit_1.txt"
        hftools.file_formats.spdata.save_spdata(d, f1)
        with open(f1) as resfil:
            with open(f2) as facitfil:
                for idx, (rad1, rad2) in enumerate(zip(resfil, facitfil)):
                    msg = "\nFailed on line %d\n  result: %r\n  facit: %r"
                    args = (idx + 1, rad1, rad2)
                    self.assertEqual(rad1, rad2, msg=msg % args)

    def test_2(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10"])
#        import pdb;pdb.set_trace()
        d.b = hfarray([2], dims=(DimSweep("a", 1),))
        f1 = testpath / "testdata/sp-data/savetest/res_2.txt"
        f2 = testpath / "testdata/sp-data/savetest/facit_2.txt"
        hftools.file_formats.spdata.save_spdata(d, f1)
        with open(f1) as resfil:
            with open(f2) as facitfil:
                for idx, (rad1, rad2) in enumerate(zip(resfil, facitfil)):
                    msg = "\nFailed on line %d\n  result: %r\n  facit: %r"
                    args = (idx + 1, rad1, rad2)
                    self.assertEqual(rad1, rad2, msg=msg % args)

    def test_3(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dims = (DimSweep("f", 3, outputformat="%.1f"),
                DimSweep("i", 2, outputformat="%.0f"),
                DimSweep("j", 2, outputformat="%.0f"),)
        d.c = hfarray([[[1, 2], [3, 4]],
                       [[10, 20], [30, 40]],
                       [[10, 20], [30, 40]]], dims=dims, outputformat="%.2f")
        f1 = testpath / "testdata/sp-data/savetest/res_3.txt"
        f2 = testpath / "testdata/sp-data/savetest/facit_3.txt"
        hftools.file_formats.spdata.save_spdata(d, f1)
        with open(f1) as resfil:
            with open(f2) as facitfil:
                for idx, (rad1, rad2) in enumerate(zip(resfil, facitfil)):
                    msg = "\nFailed on line %d\n  result: %r\n  facit: %r"
                    args = (idx + 1, rad1, rad2)
                    self.assertEqual(rad1, rad2, msg=msg % args)

    def test_4(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        fname = testpath / "testdata/sp-data/savetest/res_4.txt"
        facitfname = testpath / "testdata/sp-data/savetest/facit_4.txt"
        hftools.file_formats.spdata.save_spdata(d, fname)
        with open(fname) as resfil:
            with open(facitfname) as facitfil:
                for idx, (rad1, rad2) in enumerate(zip(resfil, facitfil)):
                    msg = "\nFailed on line %d\n  result: %r\n  facit: %r"
                    args = (idx + 1, rad1, rad2)
                    self.assertEqual(rad1, rad2, msg=msg % args)

    def test_5(self):
        d = DataBlock()
        d.comments = Comments(["Hej=10", "Svejs=11"])
        dim = DimSweep("f", 3, outputformat="%.1f")
        d.freq = dim
        fname = testpath / "testdata/sp-data/savetest/res_5.txt"
        facitfname = testpath / "testdata/sp-data/savetest/facit_5.txt"
        with open(fname, "w") as fil:
            hftools.file_formats.spdata.save_spdata(d, fil)
        with open(fname) as resfil:
            with open(facitfname) as facitfil:
                for idx, (rad1, rad2) in enumerate(zip(resfil, facitfil)):
                    msg = "\nFailed on line %d\n  result: %r\n  facit: %r"
                    args = (idx + 1, rad1, rad2)
                    self.assertEqual(rad1, rad2, msg=msg % args)


if __name__ == '__main__':
    d = DataBlock()
    d.comments = Comments(["Hej=10", "Svejs=11"])
    dims = (DimSweep("f", 3, outputformat="%.1f"),
            DimSweep("i", 2, outputformat="%.0f"),
            DimSweep("j", 2, outputformat="%.0f"), )
    d.c = hfarray([[[1, 2], [3, 4]],
                   [[10, 20], [30, 40]],
                   [[10, 20], [30, 40]]], dims=dims, outputformat="%.2f")
    f1 = testpath / "testdata/sp-data/savetest/res_3.txt"
    f2 = testpath / "testdata/sp-data/a.txt"
    hftools.file_formats.spdata.save_spdata(d, f1)
    d2 = hftools.file_formats.read_spdata(f2, verbose=False)
