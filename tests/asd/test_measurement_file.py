import numpy as np
import pytest

from spectro_dp.asd import MeasurementFile


@pytest.fixture(scope='module')
def data_file():
    return '210317_a.000'


@pytest.fixture(scope='module')
def subject(test_data_path, data_file):
    return MeasurementFile(test_data_path.joinpath(data_file))


class TestMeasurement(object):
    def test_header_constant(self):
        assert MeasurementFile.HEADER_BYTES == 484

    def test_band_count(self):
        assert MeasurementFile.BAND_COUNT == 2151

    def test_min_wavelength(self):
        assert MeasurementFile.MIN_WAVELENGTH == 350

    def test_max_wavelength(self):
        assert MeasurementFile.MAX_WAVELENGTH == 2500

    def test_band_range(self):
        assert MeasurementFile.BAND_COUNT == MeasurementFile.BAND_RANGE.size

    def test_band_range_min(self):
        assert MeasurementFile.MIN_WAVELENGTH == \
               MeasurementFile.BAND_RANGE[0]

    def test_band_range_max(self):
        assert MeasurementFile.MAX_WAVELENGTH == \
               MeasurementFile.BAND_RANGE[-1]

    def test_file_name(self, subject, data_file):
        assert subject.file.name == data_file

    def test_data(self, subject):
        assert subject.data[0] == pytest.approx(688.93, 0.01)

    def test_data_dtype(self, subject):
        assert subject.data.dtype == np.float32

    def test_bands_from_data(self, subject):
        assert subject.data.size == MeasurementFile.BAND_COUNT

    def test_header(self, subject):
        assert subject.header[0:10] == b'ASDAtwater'
