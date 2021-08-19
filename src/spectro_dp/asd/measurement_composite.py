from pathlib import Path
from typing import Iterable

import numpy as np

from .measurement_file import MeasurementFile


class MeasurementComposite:
    """
    Calculate an observation by averaging two sets of spectra sets collected
    with the ASD field spectrometer.

    For albedo it is the up- versus the down-looking sequence.
    The radiance is taken from white-references versus measured values.

    This is typically computed from 20 total measurements total,
    ten up-looking and ten down-looking. This processor assume sequentially
    taken measurements and averages each sequence.
    """
    FIRST_SET_INDEX = 0
    SECOND_SET_INDEX = 10
    SET_COUNT = 10

    FILE_GLOB = '{file_prefix}*.{file_number:03d}'

    def __init__(self,
                 input_dir,
                 file_prefix,
                 set_1_index=FIRST_SET_INDEX,
                 set_2_index=SECOND_SET_INDEX,
                 **kwargs) -> None:
        """
        :param input_dir: Directory with all the measurements
        :param file_prefix: Naming prefix for the input files
        :param set_1_index: File number of the first set of measurements
                            (Default: 0)
        :param set_2_index: File number of the second set of measurements
                            (Default: 10)
        :param kwargs: Optional - Possible options
            set_1_count: Number of first set measurements (Default: 10)
            set_2_count: Number of second set measurements (Default: 10)
            debug: Print processing progress
        """
        self._input_dir = Path(input_dir)
        self._file_prefix = file_prefix
        self._set_1_index = set_1_index
        self._set_1_count = kwargs.get('set_1_count', self.SET_COUNT)
        self._set_2_index = set_2_index
        self._set_2_count = kwargs.get('set_2_count', self.SET_COUNT)

        self._debug = kwargs.get('debug', False)

        self._set_1 = np.zeros(MeasurementFile.BAND_COUNT, dtype=np.float32)
        self._set_2 = np.zeros(MeasurementFile.BAND_COUNT, dtype=np.float32)
        self._result = None

    @property
    def input_dir(self) -> Path:
        """
        Directory containing the up and down measurements

        :return: Path object with the directory
        """
        return self._input_dir

    @property
    def set_1(self) -> np.ndarray:
        """
        Values of averaged set_1 measurements per band

        :return: Array indexed by band
        """
        return self._set_1

    @property
    def set_2(self) -> np.ndarray:
        """
        Values of averaged set_2 measurements per band

        :return: Array indexed by band
        """
        return self._set_2

    @property
    def result(self) -> np.ndarray:
        """
        Result from the calculate() method.

        :return: Array indexed by band
        """
        return self._result

    def save(self, file_suffix) -> str:
        """
        Save the result as .txt file with the given suffix. The file will be
        stored in the initialized input directory along with the input files.
        Each entry will have four decimal point precision.

        This method requires the results to be calculated first.

        :param file_suffix: Name to use as a file name suffix
        :return Full path of saved file
        """
        if self.result is not None:
            outfile = self.input_dir.joinpath(
                f"{self._file_prefix}_{file_suffix}.txt"
            ).as_posix()
            np.savetxt(outfile, self.result, fmt='%.4f')
            return outfile
        else:
            print(
                "ERROR: No results calculated. Did you run calculate() first?"
            )
            return ''

    def calculate(self) -> np.array:
        """
        Calculate the ratio of set_1 versus set_2 measurement values.
        The ratio will be corrected by the detector split spike.

        result = set_1 / set_2

        :return: Array with ratios per band
        """
        self._print_progress("Processing set-1:\n  Averaging files:")
        self._set_1 = self._average_set(self._set_1_index, self._set_1_count)
        self._print_progress("Processing set-2:\n  Averaging files:")
        self._set_2 = self._average_set(self._set_2_index, self._set_2_count)

        self._print_progress("Calculating: set-1 / set-2")
        self._result = self._adjust_detector_split(self._set_1 / self._set_2)

    def _file_glob(self, file_index) -> Iterable[Path]:
        file_glob = self.FILE_GLOB.format(
            file_prefix=self._file_prefix,
            file_number=file_index
        )
        return self.input_dir.glob(file_glob)

    def _average_set(self, start_index, file_count) -> np.ndarray:
        """
        Average set of measurements read from a sequence of data files

        :param start_index: File index to start reading from
        :param file_count: Number of files to average from the start index
        :return: Array with averages for each band
        """
        measurements = np.zeros(MeasurementFile.BAND_COUNT, dtype=np.float32)
        read_count = 0

        for file_number in range(start_index, start_index + file_count):
            for file in self._file_glob(file_number):
                self._print_progress(f"  - {file.as_posix()}")
                measurements += MeasurementFile(file).data
                read_count += 1

        if measurements.sum() == 0:
            raise FileNotFoundError('No input files found to average.')
        elif read_count != file_count:
            print(
                f'Warning: Only read {read_count} input file(s), but '
                f'{file_count} file(s) were set to be read'
            )

        return measurements / read_count

    def _print_progress(self, message) -> None:
        """
        Helper to print progress when debugging is enabled

        :param message: message to print
        """
        if self._debug:
            print(message)

    @staticmethod
    def _adjust_detector_split(measurement, band=650) -> np.ndarray:
        """
        Fix the spike from the detector split. This uses given band number and
        the band following the given (band + 1) from the measurement parameter
        and adjusts the bands from 0 to the given band.
        Spikes are a known issue with the ASD spectrometer detectors.

        :param measurement: Array with uncorrected measurements
        :param band: Band number to use for spike adjustment. (Default: 650)
        :return: Spike adjust measurement for the first 650 bands
        """
        band_ratio = measurement[band + 1] / measurement[band]
        measurement[0:band] *= band_ratio
        return measurement
