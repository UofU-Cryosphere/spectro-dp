from pathlib import Path

import numpy as np
import pytest

from spectro_dp.asd import MeasurementComposite, MeasurementFile


@pytest.fixture(scope='module')
def file_prefix():
    return '210317_a'


@pytest.fixture(scope='module')
def subject(test_data_path, file_prefix):
    return MeasurementComposite(test_data_path, file_prefix)


class TestMeasurementComposite:
    TEST_RESULT_FILE = 'pytest'

    # Constants
    def test_first_set_index(self):
        assert MeasurementComposite.FIRST_SET_INDEX == 0

    def test_second_set_index(self):
        assert MeasurementComposite.SECOND_SET_INDEX == 10

    def test_sequence_length(self):
        assert MeasurementComposite.SET_COUNT == 10

    # __init__
    def test_input_dir(self, subject, test_data_path):
        assert subject.input_dir == test_data_path

    def test_file_prefix(self, subject, file_prefix):
        assert subject._file_prefix == file_prefix

    def test_set_1_index_default(self, subject):
        assert subject._set_1_index == 0

    def test_set_1_index_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_index=2
        )
        assert subject._set_1_index == 2

    def test_set_2_index_default(self, subject):
        assert subject._set_2_index == 10

    def test_set_2_index_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_2_index=2
        )
        assert subject._set_2_index == 2

    def test_set_1_count_default(self, subject):
        assert subject._set_1_count == 10

    def test_set_1_count_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_count=2
        )
        assert subject._set_1_count == 2

    def test_set_2_count_default(self, subject):
        assert subject._set_2_count == 10

    def test_set_2_count_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_2_count=2
        )
        assert subject._set_2_count == 2

    def test_debug_default_to_false(self, subject):
        assert not subject._debug

    def test_debug_enable(self):
        subject = MeasurementComposite('', '', debug=True)
        assert subject._debug

    # Properties
    def test_input_dir_property(self, subject):
        assert isinstance(subject.input_dir, Path)

    def test_results(self, subject):
        assert subject.result is None

    def test_set_1(self, subject):
        assert isinstance(subject.set_1, np.ndarray)
        assert subject.set_1.size == MeasurementFile.BAND_COUNT

    def test_set_2(self, subject):
        assert isinstance(subject.set_2, np.ndarray)
        assert subject.set_2.size == MeasurementFile.BAND_COUNT

    # Methods
    def test_calculate_sets_results(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._adjust_detector_split(subject.set_1 / subject.set_2),
            subject.result
        )
        assert  subject.result[0] == pytest.approx(1.2915, abs=0.0001)

    def test_calculate_sets_first(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._average_set(subject._set_1_index, subject._set_1_count),
            subject.set_1
        )
        assert  subject.set_1[0] == pytest.approx(692.0561, abs=0.0001)

    def test_calculate_sets_second(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._average_set(subject._set_2_index, subject._set_2_count),
            subject.set_2
        )
        print(subject.set_2)
        assert  subject.set_2[0] == pytest.approx(525.8092, abs=0.0001)

    def test_save(self, subject):
        subject.calculate()
        outfile = Path(subject.save(self.TEST_RESULT_FILE))
        assert outfile.exists()
        assert subject.result[0] == pytest.approx(
            np.loadtxt(outfile.as_posix())[0], abs=.0001
        )

        outfile.unlink()

    def test_save_no_results(self, subject):
        assert MeasurementComposite('', '').save(self.TEST_RESULT_FILE) == ''
        assert not subject.input_dir.joinpath(
            f"{subject._file_prefix}_{self.TEST_RESULT_FILE}.txt"
        ).exists()

    # ## Private Methods
    def test_average_set_with_defaults(self, subject):
        average = subject._average_set(
            subject._set_1_index, subject._set_1_count
        )
        assert average[0] == pytest.approx(692.0561, abs=0.0001)

    def test_average_set_with_custom_counts(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_count=1
        )
        average = subject._average_set(
            subject._set_1_index, subject._set_1_count
        )
        assert average[0] == pytest.approx(688.9380, abs=0.0001)

    def test_average_set_raise_error(self, subject):
        with pytest.raises(FileNotFoundError):
            subject._average_set(99, 0)

    def test_adjust_detector_split(self):
        measurements = np.ones(700, dtype=np.float32)
        measurements[651] = 2.0
        ratio = measurements[651] / measurements[650]

        measurements = MeasurementComposite._adjust_detector_split(
            measurements
        )

        assert measurements[651:].sum() == 50
        assert measurements[0:650].sum() == ratio * 650
