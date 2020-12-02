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

    def __init__(self, slider_ids, mins, max, initial_values=None, step_sizes=None): # noqa
        super(_SliderComponent, self).__init__()

        # make sure size of all list are the same
        # make sure element of slider_ids are strings
        # 

        self.slider_ids = list(slider_ids)
        self.mins = list(mins)
        self.max = list(max)

        if initial_values is None:
            initial_values = mins
        if step_sizes is None:
            step_sizes = [(a - b)/10 for a, b in zip(max, mins)]

        self.initial_values = list(initial_values)
        self.step_sizes = list(step_sizes)

        self.slider_info = {'Slider_id': self.slider_ids,
                            'Min': self.mins,
                            'Max': self.max,
                            'Initial_value': self.initial_values,
                            'Step_size': self.step_sizes}
        self.slider_df = pd.DataFrame(
                            self.slider_info, 
                            columns=['Min', 'Max', 'Initial_value', 'Step_size'],
                            index=self.slider_ids)

    def add_slider(self, id):

        if not isinstance(id, str):
            raise TypeError(
                'Input id has to be string')

        if id not in self.slider_ids:
            raise NameError('Input id not in the list')

        label = html.H6(id)
        slider = dcc.Slider(
                    id=id,
                    min=self.slider_df.loc[id]['Min'],
                    max=self.slider_df.loc[id]['Max'],
                    value=self.slider_df.loc[id]['Initial_value'],
                    step=self.slider_df.loc[id]['Step_size'])

        return [label, slider]

    def group_sliders(self):

        slider_group = []
        for id in self.slider_ids:
            slider_group.append(self.add_slider(id)[0])
            slider_group.append(self.add_slider(id)[1])

        return html.Div(slider_group)

    def slider_ids(self):

        return self.slider_ids