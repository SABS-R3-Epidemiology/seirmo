#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas

class _SliderComponent(object):
    """Slider Class:

    Controls the slider for the app

    Parameters
    ----------
    model: seirmo.ForwardModel class
    """

    def __init__(self, slider_ids, mins, max, initial_values, step_sizes): # noqa
        super(_SliderComponent, self).__init__()

        self.slider_ids = list(slider_ids)
        self.mins = list(mins)
        self.max = list(max)
        self.initial_values = list(initial_values)
        self.step_sizes = list(step_sizes)

        self.slider_info = {'Slider_id': self.slider_ids,
                            'Min': self.mins,
                            'Max': self.max,
                            'Initial_value': self.initial_values,
                            'Step_size': self.step_sizes}
        self.slider_df = pd.DataFrame(
                            slider_info, 
                            columns=['Min', 'Max', 'Initial_value', 'Step_size'],
                            index=self.slider_ids)

    def add_slider(self, id):

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
            slider_group.append(add_slider(id))
        
        return html.Div(slider_group)

    def slider_ids(self):

        return self.slider_ids