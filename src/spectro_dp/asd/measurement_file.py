from pathlib import PurePath

import numpy as np


class MeasurementFile:
    """
    Manage output file of one measurement with the ASD field spectrometer.

    Each band has a measurement recorded as a digital number (DN)
    """

    HEADER_BYTES = 484
    BAND_COUNT = 2151

    MIN_WAVELENGTH = 350  # in micro-meter
    MAX_WAVELENGTH = 2500  # in micro-meter
    BAND_RANGE = np.arange(MIN_WAVELENGTH, MAX_WAVELENGTH + 1)

    def __init__(self, filepath) -> None:
        self._filepath = PurePath(filepath)
        self._header = None
        self._data = None

    @property
    def file(self) -> PurePath:
        return self._filepath

    @property
    def header(self) -> bytes:
        if self._header is None:
            self._header = self._read_header()

        return self._header

    @property
    def data(self) -> np.array:
        if self._data is None:
            self._data = np.fromfile(
                self.file.as_posix(),
                offset=self.HEADER_BYTES,
                dtype=np.float32
            )

            # Check for expected number of bands
            assert self._data.size == self.BAND_COUNT

        return self._data

    def _read_header(self) -> bytes:
        with open(self.file, 'rb') as infile:
            header = infile.read(self.HEADER_BYTES)
        return header
