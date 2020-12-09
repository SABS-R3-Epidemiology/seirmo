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

    Controls the slider for the app

    Parameters
    ----------
    model: seirmo.ForwardModel class
    """

    def __init__(self): # noqa
        super(_SliderComponent, self).__init__()

        self._slider_ids = []
        self._sliders = []

    def add_slider(self, slider_id, min, max, initial_value=None, step_size=None, label=None, mark_num=None):

        if initial_value is None:
            initial_value = min
        if step_size is None:
            step_size = (max - min)/100
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

    def group_sliders(self,slider_id, group_id):

        if slider_id not in self._slider_ids:
            raise AssertionError(
                'slider_id not in list of added slider ids'
        )

        return html.Div(children=slider_id,id=group_id)

    def slider_ids(self):

        return self._slider_ids