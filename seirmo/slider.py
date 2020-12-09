#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash_core_components as dcc
import dash_html_components as html
import numpy as np


class _SliderComponent(object):
    """Slider Class:

    Controls the creation and grouping of slider for the app
    """

    def __init__(self): # noqa
        super(_SliderComponent, self).__init__()

        self._slider_ids = []
        self._sliders = []

    def add_slider(self, slider_id, min, max, initial_value=None, step_size=None, label=None, mark_num=None): # noqa
        """
        Creates new slider with label

        Parameters
        ----------
        slider_id
            Unique id to identify the slider.
        min
            Minimum value of the slider.
        max
            Maximum value of the slider.
        initial_value (optional)
            Starting value of the slider when the app is executed.
            Default value is minimum value of slider.
        step_size (optional)
            Step size of possible values on the slider
            Default value is 1/100th of range of slider
        label (optional)
            Label for the slider, to be shown to user
            Default is slider id
        mark_num (optional)
            Indicators of value on slider
            Default is 1/10th of range of slider
        """

        if initial_value is None:
            initial_value = min
        if step_size is None:
            step_size = (max - min) / 100
        if label is None:
            label = slider_id
        if mark_num is None:
            mark_num = 10

        if not isinstance(slider_id, str):
            raise TypeError(
                'Slider id has to be string')

        new_slider = [
            html.Label(label),
            dcc.Slider(
                id=slider_id,
                min=min,
                max=max,
                value=initial_value,
                step=step_size,
                marks={str(i): str(i) for i in np.arange(
                    start=min,
                    stop=max,
                    step=mark_num)
                }
            )
        ]

        self._slider_ids.append(slider_id)
        self._sliders += new_slider

        return new_slider

    def group_sliders(self, slider_id, group_id):
        """
        Group the sliders with respect to their unique group id

        Parameters
        ----------
        slider_id
            Unique id of slider to be grouped
        group_id
            Unique id of group of sliders
        """

        if slider_id not in self._slider_ids:
            raise AssertionError(
                'slider_id not in list of added slider ids'
            )

        return html.Div(children=slider_id, id=group_id)

    def slider_ids(self):
        """
        Return list of all slider ids
        """

        return self._slider_ids
