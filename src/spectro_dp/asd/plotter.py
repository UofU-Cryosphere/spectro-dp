import matplotlib.pyplot as plt
import numpy as np

from .measurement_file import MeasurementFile


class Plotter:
    """
    Base class to plot results of measurement composites
    """

    X_LABEL = r"Wavelength $\mu m$"
    AX1_TITLE = "Measurements"
    AX2_TITLE = "Ratio Set 1/Set 2"

    @staticmethod
    def show(measurement_composite, **kwargs) -> None:
        fig, (ax1, ax2) = plt.subplots(
            2, 1, sharex=True, dpi=300
        )

        label_set_1 = kwargs.get('set_1_label', 'Set 1')
        label_set_2 = kwargs.get('set_2_label', 'Set 2')

        x_ticks = np.arange(
            MeasurementFile.MIN_WAVELENGTH,
            MeasurementFile.MAX_WAVELENGTH + 1
        )

        ax1.set_title(Plotter.AX1_TITLE)
        ax1.plot(
            x_ticks, measurement_composite.set_1,
            label=label_set_1, c='goldenrod'
        )
        ax1.plot(
            x_ticks, measurement_composite.set_2,
            label=label_set_2, c='skyblue'
        )
        ax1.set_ylim(bottom=0)
        ax1.legend()

        composite_title = kwargs.get('composite_title', Plotter.AX2_TITLE)
        ax2.plot(x_ticks, measurement_composite.result, c='slateblue')
        ax2.set_title(composite_title)

        ax2.set_xlim(x_ticks.min() - 1, x_ticks.max() + 1)
        ax2.set_ylim(0, 1)
        ax2.set_xlabel(Plotter.X_LABEL)

        plt.show()
