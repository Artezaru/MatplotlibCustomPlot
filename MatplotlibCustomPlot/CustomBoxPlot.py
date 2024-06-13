from typing import Tuple, Union, Optional, Sequence
import matplotlib.pyplot
import matplotlib.figure
import numpy
import copy
import matplotlib.patches

class CustomBoxPlot:
    """
    CustomBoxPlot is a class to manage an ax on a given matplotlib.pyplot.figure object.
    This ax allows ploting BoxPlot with the following properties:

    - center of the box: average value of the data. 
    - dimension of the box: standard deviation values of the data.
    - dimension of the bar: minimum and maximum value of the data. 

    Parameters
    ----------
    figure : matplotlib.figure.Figure
        The figure on which the ax will be created.

    ax_location : Tuple[int]
        The location of the ax on the figure. See figure.add_subplot() method.
        The Tuple must contains 3 positive integers.

        Default : (1,1,1), means that the ax use the entire space of the figure.
    
    Raises
    ------
    TypeError : If a given argument is wrong type or the length of the Tuple is not 3. See figure.add_subplot() method.

    ValueError : If a given number is not positive integer or correct value.

    Examples
    --------
    Basic usage of `CustomBoxPlot`:

        .. code-block:: python
            
            import matplotlib.pyplot
            import numpy
            from MatplotlibCustomPlot import CustomBoxPlot

            numpy.random.seed(0)
            data1 = numpy.random.normal(0, 1, (2, 100))
            data2 = numpy.random.normal(1, 0.5, 100)

            fig = matplotlib.pyplot.figure()
            BoxPlot = CustomBoxPlot(fig, ax_location=(1,1,1))
            BoxPlot.add_boxplot(data1, (1,2), ('Data1.1','Data1.2'))
            BoxPlot.add_boxplot(data2, 3, 'Data2')

            fig.canvas.show()
    """
    def __init__(self,
                 figure: matplotlib.figure.Figure,
                 ax_location: Tuple[int] = (1,1,1)) -> None:
        self.ax = figure.add_subplot(*ax_location)
        self.current_positions = []
        self.current_ticklabels = []

    def add_boxplot(self, 
                    data: numpy.ndarray,
                    position: Union[int, Sequence[int]],
                    label: Optional[Union[int, Sequence[int]]] = None,
                    *,
                    box_color: Union[str, Sequence[str]] = "black",
                    average_color: Union[str, Sequence[str]] = "red",
                    linewidth: Union[int, Sequence[int]] = 2,
                    draw_whiskers: Union[bool, Sequence[bool]] = True,
                    draw_average: Union[bool, Sequence[bool]] = True,
                    print_average: Union[bool, Sequence[bool]] = False) -> None:
        """
        Adds a custom boxplot to the given position.

        Parameters
        ----------
        data : numpy.ndarray
            The data to create the bowplot. The array must be 1-dimensional or
            2-dimensional. If data is 2-dimensional, each line will be use to plot a
            boxplot.

        position : Union[int, Sequence[int]]
            The position(s) on the x-axis at which the box plot is ploted.

        label : Optional[Union[int, Sequence[int]]]
            The label(s) corresponding with the bowplot to put on the x-axis.

            Default : None, means that the label is position parameter.

        box_color : Union[str, Sequence[str]]
            The color(s) of the box.

            Default : 'black'

        average_color : Union[str, Sequence[str]]
            The color(s) of the average line.

            Default : 'red'  

        linewidth : Union[int, Sequence[int]]
            The width(s) of the boxplot lines.

            Default : 2  

        draw_whiskers : Union[bool, Sequence[bool]] 
            If the min-max bar(s) need to be ploted.

            Default : True

        draw_average : Union[bool, Sequence[bool]] 
            If the average bar(s) need to be ploted.

            Default : True

        print_average : Union[bool, Sequence[bool]] 
            If the average value should be printing.

            Default : False

        Raises
        ------
        TypeError : If a given argument is wrong type.

        ValueError : If a given argument as not correct value or size.
        """
        def convert2sequence(value, N, name, itype) -> Sequence:
            if isinstance(value,itype):
                return [value for index in range(N)]
            elif isinstance(value, Sequence):
                if not len(value) == N:
                    raise ValueError(f"Parameter {name} must be a {itype} or sequence of {itype} with length {N}, not length {len(value)}.")
                for index in range(len(value)):
                    if not isinstance(value[index], itype):
                        raise TypeError(f"Parameter {name} must be a {itype} or sequence of {itype} with length {N}.")
                return value
            else:
                raise TypeError(f"Parameter {name} must be a {itype} or sequence of {itype} with length {N}.")
            
        if label is None:
            label = copy.deepcopy(position)

        if not isinstance(data, numpy.ndarray):
            raise TypeError('Parameter data is not an array')

        if data.ndim >= 3:
            raise ValueError(f'Parameter data must be 1 or 2-dimentionnal array, not {data.ndim}-dimentionnal.')
        
        N = data.shape[0]
        position = convert2sequence(position, N, 'position', int)
        label = convert2sequence(label, N, 'label', str)
        box_color = convert2sequence(box_color, N, 'box_color', str)
        average_color = convert2sequence(average_color, N, 'average_color', str)
        linewidth = convert2sequence(linewidth, N, 'linewidth', int)
        draw_whiskers = convert2sequence(draw_whiskers, N, 'draw_whiskers', bool)
        draw_average = convert2sequence(draw_average, N, 'draw_average', bool)
        print_average = convert2sequence(print_average, N, 'print_average', bool)

        if data.ndim == 2:
            for index in range(N):
                self.add_boxplot(data[index,:], 
                                 position[index], 
                                 label=label[index],
                                 box_color=box_color[index],
                                 average_color=average_color[index],
                                 linewidth=linewidth[index],
                                 draw_whiskers=draw_whiskers[index],
                                 draw_average=draw_average[index],
                                 print_average=print_average[index])
            return
        
        # Computing stat values
        mean = numpy.nanmean(data)
        std = numpy.nanstd(data)
        min_val = numpy.nanmin(data)
        max_val = numpy.nanmax(data)

        # Position of elements on the graph
        center = mean
        box_start = mean - std
        box_end = mean + std
        whisker_min = min_val
        whisker_max = max_val

        # Box layout (contours only)
        rect = matplotlib.patches.Rectangle((position[0] - 0.1, box_start), 0.2, box_end - box_start, fill=False, edgecolor=box_color[0], linewidth=linewidth[0])
        self.ax.add_patch(rect)

        # Bars (whiskers)
        if draw_whiskers[0]:
            self.ax.plot([position[0], position[0]], [whisker_min, box_start], color=box_color[0], lw=linewidth[0])  # Bottom bar
            self.ax.plot([position[0], position[0]], [box_end, whisker_max], color=box_color[0], lw=linewidth[0])  # Top bar
            self.ax.plot([position[0] - 0.1, position[0] + 0.1], [whisker_min, whisker_min], color=box_color[0], lw=linewidth[0])  # Bottom cap
            self.ax.plot([position[0] - 0.1, position[0] + 0.1], [whisker_max, whisker_max], color=box_color[0], lw=linewidth[0])  # Top cap

        # Average plot
        if draw_average[0]:
            self.ax.plot([position[0] - 0.1, position[0] + 0.1], [center, center], color=average_color[0], lw=linewidth[0])  # Average bar

        # Add labels for the average
        if print_average[0]:
            self.ax.text(position[0] + 0.2, center, f'{mean:.2f}', verticalalignment='center', color=average_color[0], fontsize=10, fontweight='bold')

        # Update ticks and ticklabels
        if position[0] not in self.current_positions:
            self.current_positions.append(position[0])
            self.current_ticklabels.append(label[0])

            # Trier les positions et les ticklabels
            sorted_indices = numpy.argsort(self.current_positions)
            sorted_positions = numpy.array(self.current_positions)[sorted_indices]
            sorted_ticklabels = numpy.array(self.current_ticklabels)[sorted_indices]

            self.ax.set_xticks(sorted_positions)
            self.ax.set_xticklabels(sorted_ticklabels)

    def set_title(self, title: str, *args, **kwargs) -> None:
        """
        Sets the title of the ax.
        
        Parameters
        ----------
        title : str
            The title to set on the ax.
        """
        self.ax.set_title(title, *args, **kwargs)

    def set_xlabel(self, xlabel: str, *args, **kwargs) -> None:
        """
        Sets the xlabel of the ax.
        
        Parameters
        ----------
        xlabel : str
            The xlabel to set on the ax.
        """
        self.ax.set_xlabel(xlabel, *args, **kwargs)
        
    def set_ylabel(self, ylabel: str, *args, **kwargs) -> None:
        """
        Sets the ylabel of the ax.
        
        Parameters
        ----------
        ylabel : str
            The ylabel to set on the ax.
        """
        self.ax.set_ylabel(ylabel, *args, **kwargs)


def main():
    numpy.random.seed(0)
    data1 = numpy.random.normal(0, 1, (2, 100))
    data2 = numpy.random.normal(1, 0.5, 100)

    fig = matplotlib.pyplot.figure()
    BoxPlot = CustomBoxPlot(fig, ax_location=(1,1,1))
    BoxPlot.add_boxplot(data1, (1,2), ('Data1.1','Data1.2'))
    BoxPlot.add_boxplot(data2, 3, 'Data2')
    BoxPlot.set_ylabel("my data", color='red')

    fig.canvas.show()

if __name__ == "__main__":
    main()
