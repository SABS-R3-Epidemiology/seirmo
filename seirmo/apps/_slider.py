#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash_daq as daq
import dash_html_components as html
import numpy as np


class _SliderComponent(object):
    """Slider Class:

    Controls the creation and grouping of slider for the app
    """

    def __init__(self): # noqa
        super(_SliderComponent, self).__init__()

        self._sliders = {}
        self._slider_groups = {}

    def __call__(self):
        """
        Return a html Div for grouped sliders
        """

        slider_group_component = []

        for group_id, slider_id in self._slider_groups.items():

            slider_object = []
            for slider_members in slider_id:
                slider_object += [self._sliders[slider_members]]

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
            mark_num = 11

        slider_id = str(slider_id)

        new_slider = html.Div([
            html.Label(label),
            daq.Slider(
                id=slider_id,
                min=min_value,
                max=max_value,
                value=initial_value,
                step=step_size,
                handleLabel={"showCurrentValue": True,
                             "label": slider_id,
                             "style": {"size": 0.5}},
                marks={i: '{:.1f}'.format(i) for i in np.linspace( # noqa
                    start=min_value,
                    stop=max_value,
                    num=mark_num)
                }
            )
        ], style={'marginBottom': '2em'})

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
        if not any(item in slider_ids for item in self._sliders.keys()):
            raise AssertionError(
                'at least one of the slider_ids not in list of added slider ids' # noqa
            )

        if group_id in self._slider_groups.keys():
            raise ValueError(
                'Group id is already used.'
            )
        
        for slider_id in slider_ids:
            for group in self._slider_groups.values():
                if slider_id in group:
                    raise ValueError(
                        'At least one of the provided slider IDs belongs to a slider group already.') # noqa

        self._slider_groups[group_id] = slider_ids

    def get_slider_ids(self):
        """
        Return list of all slider ids
        """

        return list(self._sliders.keys())

    def get_group_ids(self):
        """
        Return list of all group ids
        """

        return list(self._slider_groups.keys())

    def sliders_in_group(self, group_id):
        """
        Return slider ids in the group
        """

        return self._slider_groups[group_id]
