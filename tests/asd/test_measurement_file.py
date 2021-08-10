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
        assert 484 == MeasurementFile.HEADER_BYTES

    def test_band_count(self):
        assert 2151 == MeasurementFile.BAND_COUNT

    def test_min_wavelength(self):
        assert 350 == MeasurementFile.MIN_WAVELENGTH

    def test_max_wavelength(self):
        assert 2500 == MeasurementFile.MAX_WAVELENGTH

    def test_file_name(self, subject, data_file):
        assert data_file == subject.file.name

    def test_data(self, subject):
        assert pytest.approx(688.93, 0.01) == subject.data[0]

    def test_data_dtype(self, subject):
        assert np.float32 == subject.data.dtype

    def test_bands_from_data(self, subject):
        assert MeasurementFile.BAND_COUNT == subject.data.size

    def test_header(self, subject):
        assert b'ASDAtwater' == subject.header[0:10]
