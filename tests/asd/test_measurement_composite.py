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
        assert 0 == MeasurementComposite.FIRST_SET_INDEX

    def test_second_set_index(self):
        assert 10 == MeasurementComposite.SECOND_SET_INDEX

    def test_sequence_length(self):
        assert 10 == MeasurementComposite.SET_COUNT

    # __init__
    def test_input_dir(self, subject, test_data_path):
        assert test_data_path == subject.input_dir

    def test_file_prefix(self, subject, file_prefix):
        assert file_prefix == subject._file_prefix

    def test_set_1_index_default(self, subject):
        assert 0 == subject._set_1_index

    def test_set_1_index_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_index=2
        )
        assert 2 == subject._set_1_index

    def test_set_2_index_default(self, subject):
        assert 10 == subject._set_2_index

    def test_set_2_index_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_2_index=2
        )
        assert 2 == subject._set_2_index

    def test_set_1_count_default(self, subject):
        assert 10 == subject._set_1_count

    def test_set_1_count_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_count=2
        )
        assert 2 == subject._set_1_count

    def test_set_2_count_default(self, subject):
        assert 10 == subject._set_2_count

    def test_set_2_count_2(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_2_count=2
        )
        assert 2 == subject._set_2_count

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
        assert MeasurementFile.BAND_COUNT == subject.set_1.size

    def test_set_2(self, subject):
        assert isinstance(subject.set_2, np.ndarray)
        assert MeasurementFile.BAND_COUNT == subject.set_2.size

    # Methods
    def test_calculate_sets_results(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._adjust_detector_split(subject.set_1 / subject.set_2),
            subject.result
        )
        assert pytest.approx(1.2915, abs=0.0001) == subject.result[0]

    def test_calculate_sets_first(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._average_set(subject._set_1_index, subject._set_1_count),
            subject.set_1
        )
        assert pytest.approx(692.0561, abs=0.0001) == subject.set_1[0]

    def test_calculate_sets_second(self, subject):
        subject.calculate()
        assert np.array_equal(
            subject._average_set(subject._set_2_index, subject._set_2_count),
            subject.set_2
        )
        print(subject.set_2)
        assert pytest.approx(525.8092, abs=0.0001) == subject.set_2[0]

    def test_save(self, subject):
        subject.calculate()
        outfile = Path(subject.save(self.TEST_RESULT_FILE))
        assert outfile.exists()
        assert pytest.approx(
            np.loadtxt(outfile.as_posix())[0], abs=.0001
        ) == subject.result[0]

        outfile.unlink()

    def test_save_no_results(self, subject):
        assert '' == MeasurementComposite('','').save(self.TEST_RESULT_FILE)
        assert not subject.input_dir.joinpath(
            f"{subject._file_prefix}_{self.TEST_RESULT_FILE}.txt"
        ).exists()

    # ## Private Methods
    def test_average_set_with_defaults(self, subject):
        average = subject._average_set(
            subject._set_1_index, subject._set_1_count
        )
        assert pytest.approx(692.0561, abs=0.0001) == average[0]

    def test_average_set_with_custom_counts(self, test_data_path, file_prefix):
        subject = MeasurementComposite(
            test_data_path, file_prefix, set_1_count=1
        )
        average = subject._average_set(
            subject._set_1_index, subject._set_1_count
        )
        assert pytest.approx(688.9380, abs=0.0001) == average[0]

    def test_average_set_raise_error(self, subject):
        with pytest.raises(FileNotFoundError):
            subject._average_set(99, 0)

    def test_adjust_detector_split(self):
        measurements = np.ones(700, dtype=np.float32)
        measurements[651] = 2.0

        measurements = MeasurementComposite._adjust_detector_split(measurements)

        assert 50 == measurements[651:].sum()
        assert 0.5 * 650 == measurements[0:650].sum()
