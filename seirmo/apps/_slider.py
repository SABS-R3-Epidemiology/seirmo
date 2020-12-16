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

        self._sliders = {}
        self._group_ids = {}
    
    def __call__(self):

        slider_group_component = []
        for group_id in list(self._group_ids.keys()):

            slider_object = []
            for slider_members in self._group_ids[group_id]:
                slider_object += self._sliders[slider_members]

            slider_group_component.append(html.Div([
                html.Label(group_id),
                html.Br(),
                html.Div(
                    children=slider_object,
                    id=group_id,
                    style={'marginBottom': '1em'})
            ]))

        return html.Div(slider_group_component)

    def add_slider(self, slider_id, min_value, max_value, initial_value=None, step_size=None, label=None, mark_num=None): # noqa
        """
        Creates new slider with label.

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
            initial_value = min_value
        if step_size is None:
            step_size = (max_value - min_value) / 100
        if label is None:
            label = slider_id
        if mark_num is None:
            mark_num = 10

        slider_id = str(slider_id)

        new_slider = [
            html.Label(label),
            dcc.Slider(
                id=slider_id,
                min=min_value,
                max=max_value,
                value=initial_value,
                step=step_size,
                marks={str(i): str(i) for i in np.arange(
                    start=min_value,
                    stop=max_value,
                    step=mark_num)
                }
            )
        ]

        self._sliders[slider_id] = new_slider

        return new_slider

    def group_sliders(self, slider_ids, group_id):
        """
        Group sliders by the slider_id input and assign a group id to the slider group # noqa
        Parameters
        ----------
        slider_id
            Unique id of slider to be grouped
        group_id
            Unique id of group of sliders
        """

        slider_ids = list(slider_ids)
        if not any(item in slider_ids for item in list(self._sliders.keys())):
            raise AssertionError(
                'at least one of the slider_ids not in list of added slider ids' # noqa
            )

        if group_id in list(self._group_ids.keys()):
            raise ValueError(
                'Group id is already used.'
            )

        self._group_ids[group_id] = slider_ids

    def get_slider_ids(self):
        """
        Return list of all slider ids
        """

        return list(self._sliders.keys())

    def get_group_ids(self):
        """
        Return list of all group ids
        """

        return list(self._group_ids.keys())

    def sliders_in_group(self, group_id):
        """
        Return slider ids in the group
        """

        return self._group_ids[group_id]
