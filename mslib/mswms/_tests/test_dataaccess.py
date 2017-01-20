# -*- coding: iso-8859-1 -*-
"""
    MSS - some common code for testing

    @copyright: 2017 Reimar Bauer,

    @license: License: Apache-2.0, see LICENSE.txt for details.
"""
import os
import pytest
from datetime import datetime
from mslib.mswms import dataaccess
from mslib.mswms.dataaccess import ECMWFDataAccess
from conftest import BASE_DIR, DATA_DIR, VALID_TIME_CACHE

# ToDo
dataaccess.valid_time_cache = VALID_TIME_CACHE


if not os.path.exists(BASE_DIR):
    pytest.skip("Demo Data not existing")


class Test_NWPDataAccess(object):
    def setup(self):
        self.ECMWFDataAccess = ECMWFDataAccess(DATA_DIR, "EUR_LL015")

    def test_get_filename(self):
        filename = self.ECMWFDataAccess.get_filename("air_pressure", "ml",
                                                     datetime(2012, 10, 17, 12, 0),
                                                     datetime(2012, 10, 17, 11, 0))
        assert filename == "20121017_12_ecmwf_forecast.P_derived.EUR_LL015.036.ml.nc"

        filename = self.ECMWFDataAccess.get_filename("air_pressure", "ml",
                                                     datetime(2012, 10, 17, 12, 0),
                                                     datetime(2012, 10, 17, 11, 0),
                                                     fullpath=True)
        assert filename == os.path.join(DATA_DIR, filename)

    def test_get_datapath(self):
        assert self.ECMWFDataAccess.get_datapath() == DATA_DIR

    def test_get_all_datafiles(self):
        all_files = self.ECMWFDataAccess.get_all_datafiles()
        assert all_files == os.listdir(DATA_DIR)

    def test_get_init_times(self):
        all_init_times = self.ECMWFDataAccess.get_init_times()
        assert all_init_times == [datetime(2012, 10, 17, 12, 0)]

    def test_md5_filename(self):
        filename = self.ECMWFDataAccess.get_filename("air_pressure", "ml",
                                                     datetime(2012, 10, 17, 12, 0),
                                                     datetime(2012, 10, 17, 11, 0),
                                                     fullpath=True)
        md5_filename = self.ECMWFDataAccess.md5_filename(filename)
        assert md5_filename.endswith("vt_cache_pickle")

    def test_check_valid_cache(self):
        filename = self.ECMWFDataAccess.get_filename("air_pressure", "ml",
                                                     datetime(2012, 10, 17, 12, 0),
                                                     datetime(2012, 10, 17, 11, 0),
                                                     fullpath=True)
        valid_cache = self.ECMWFDataAccess.check_valid_cache(filename)
        if not os.path.exists(filename):
            assert valid_cache is not None
        else:
            if valid_cache is not None:
                # follow up test can remove a cache file
                assert valid_cache == datetime(2012, 10, 17, 12, 0)

    def test_save_valid_cache(self):
        filename = self.ECMWFDataAccess.get_filename("air_pressure", "ml",
                                                     datetime(2012, 10, 17, 12, 0),
                                                     datetime(2012, 10, 17, 11, 0),
                                                     fullpath=True)
        valid_times = datetime(2012, 10, 17, 12, 0)
        self.ECMWFDataAccess.save_valid_cache(filename, valid_times)
        assert os.path.exists(VALID_TIME_CACHE)
        assert len(os.listdir(VALID_TIME_CACHE)) > 0

    def test_serviceCache(self):
        # set lowest possible number to delete all files
        dataaccess.valid_time_cache_max_age_seconds = 0
        self.ECMWFDataAccess.serviceCache()
        assert len(os.listdir(VALID_TIME_CACHE)) == 0

    def test_mfDatasetArgs(self):
        mfDatasetArgs = self.ECMWFDataAccess.mfDatasetArgs()
        assert mfDatasetArgs == {'skipDimCheck': ['lon']}

    def test_build_filetree(self):
        tree = self.ECMWFDataAccess.build_filetree()
        assert tree == {datetime(2012, 10, 17, 12, 0): {
            36: {u'CC': u'20121017_12_ecmwf_forecast.CC.EUR_LL015.036.ml.nc',
                 u'PRESSURE_LEVELS': u'20121017_12_ecmwf_forecast.PRESSURE_LEVELS.EUR_LL015.036.pl.nc',
                 u'P_derived': u'20121017_12_ecmwf_forecast.P_derived.EUR_LL015.036.ml.nc',
                 u'Q': u'20121017_12_ecmwf_forecast.Q.EUR_LL015.036.ml.nc',
                 u'SFC': u'20121017_12_ecmwf_forecast.SFC.EUR_LL015.036.sfc.nc',
                 u'T': u'20121017_12_ecmwf_forecast.T.EUR_LL015.036.ml.nc',
                 u'U': u'20121017_12_ecmwf_forecast.U.EUR_LL015.036.ml.nc',
                 u'V': u'20121017_12_ecmwf_forecast.V.EUR_LL015.036.ml.nc',
                 u'W': u'20121017_12_ecmwf_forecast.W.EUR_LL015.036.ml.nc'
                 }
        }}
