#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class _SliderComponent(object):
    """Slider Class:

    Controls the slider for the app

    Parameters
    ----------
    model: seirmo.ForwardModel class
    """

    def __init__(self): # noqa
        super(_SliderComponent, self).__init__()

    def add_slider(self, slider_id, min, max, initial_value=None, step_size=None):

        if initial_values is None:
            initial_value = min
        if step_sizes is None:
            step_sizes = (max - min)/100

        if not isinstance(slider_id, str):
            raise TypeError(
                'Slider id has to be string')

        label = html.H6(id)
        slider = dcc.Slider(
                    id=slider_id,
                    min=min,
                    max=max,
                    value=initial_value,
                    step=step_size)

        return [label, slider]

    def group_sliders(self,slider_id, group_id):

        slider_group = []
        for id in self.slider_ids:
            slider_group.append(self.add_slider(id)[0])
            slider_group.append(self.add_slider(id)[1])

        return html.Div(slider_group)

    def slider_ids(self):

        return self.slider_ids