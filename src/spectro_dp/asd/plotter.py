import matplotlib.pyplot as plt

from .measurement_file import MeasurementFile


class Plotter:
    """
    Base class to plot results of measurement composites
    """

    AX1_TITLE = "Measurements"
    AX2_TITLE = "Ratio Set 1/Set 2"

    LINE_OPTS = dict(lw=1)

    @staticmethod
    def show_composite(measurement_composite, **kwargs) -> None:
        """
        Plot the results of a measurement composite, existing of two sets of
        measurements.

        :param measurement_composite: MeasurementComposite
        :param kwargs: Arguments to pass to the plot
            Options:
             * 'composite_title': Title for the plot
             * 'set_1_label': Legend label for set_1
             * 'set_2_label': Legend label for set_2
        """
        fig, (ax1, ax2) = plt.subplots(
            2, 1, sharex=True, dpi=300
        )

        label_set_1 = kwargs.get('set_1_label', 'Set 1')
        label_set_2 = kwargs.get('set_2_label', 'Set 2')

        x_ticks = MeasurementFile.BAND_RANGE

        ax1.set_title(Plotter.AX1_TITLE)
        ax1.plot(
            x_ticks, measurement_composite.set_1,
            label=label_set_1, c='goldenrod', **Plotter.LINE_OPTS
        )
        ax1.plot(
            x_ticks, measurement_composite.set_2,
            label=label_set_2, c='skyblue', **Plotter.LINE_OPTS
        )
        ax1.set_ylim(bottom=0)
        ax1.legend()

        ax2.plot(
            x_ticks, measurement_composite.result,
            c='slateblue', **Plotter.LINE_OPTS
        )

        ax2.set_title(
            kwargs.get('composite_title', Plotter.AX2_TITLE)
        )
        ax2.set_xlim(x_ticks.min() - 1, x_ticks.max() + 1)
        ax2.set_ylim(0, 1)
        ax2.set_xlabel(MeasurementFile.X_LABEL)

        plt.show()
