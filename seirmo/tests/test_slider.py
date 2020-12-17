#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest

import seirmo as se
from seirmo import apps

class TestSliderComponent(unittest.TestCase):
    """
    Test the '_SliderComponent' class.
    """
    def test__init__(self):
        apps._SliderComponent()

    def test__call__(self):
        slider = apps._SliderComponent()

        slider.add_slider('slider1', 0, 1)
        slider.add_slider('slider2', 0, 2)
        slider.add_slider('slider3', 0, 1)

        # Check slider group dictionary
        slider.group_sliders(['slider1', 'slider2'], 'group1')
        slider.group_sliders(['slider3'], 'group2')

        # Check that 2 slider group Div is created
        self.assertEqual(len(slider().children), 2)

        # Check that there are 3 parts (structure) in each slider group # noqa
        self.assertEqual(len(slider().children[0].children), 3)
        self.assertEqual(len(slider().children[1].children), 3)

        # Check that labels and slider is added for each slider group # noqa
        self.assertEqual(len(slider().children[0].children[2].children), 4)
        self.assertEqual(len(slider().children[1].children[2].children), 2)

    def test_add_slider(self):

        slider = apps._SliderComponent()

        slider_output = slider.add_slider('slider1', 0, 1)
        self.assertEqual(len(slider_output), 2)

    def test_group_sliders(self):

        slider = apps._SliderComponent()
        slider.add_slider('slider1', 0, 1)
        slider.add_slider('slider2', 0, 2)
        slider.add_slider('slider3', 0, 1)
        slider.add_slider('slider4', 0, 1)

        slider.group_sliders(['slider1', 'slider2'], 'group1')
        slider.group_sliders(['slider3'], 'group2')

        # Check group slider input
        with self.assertRaises(AssertionError):
            slider.group_sliders('1', 'group1')

        # Check error raised for used group id
        with self.assertRaises(ValueError):
            slider.group_sliders(['slider4'], 'group1')

        # Check new sliders to group are not in existing group
        with self.assertRaises(ValueError):
            slider.group_sliders(['slider3'], 'group3')

        # Check slider group dictionary
        self.assertEqual(slider.sliders_in_group('group1'), ['slider1', 'slider2']) # noqa
        self.assertEqual(slider.sliders_in_group('group2'), ['slider3'])

        

    def test_get_slider_ids(self):

        slider = apps._SliderComponent()
        slider.add_slider('slider1', 0, 1)
        slider.add_slider('slider2', 0, 2)

        self.assertEqual(slider.get_slider_ids(), ['slider1', 'slider2'])

    def test_get_group_ids(self):

        slider = apps._SliderComponent()
        slider.add_slider('slider1', 0, 1)
        slider.add_slider('slider2', 0, 2)
        slider.add_slider('slider3', 0, 1)

        slider.group_sliders(['slider1', 'slider2'], 'group1')
        slider.group_sliders(['slider3'], 'group2')

        self.assertEqual(slider.get_group_ids(), ['group1', 'group2'])

    def test_sliders_in_group(self):

        slider = apps._SliderComponent()
        slider.add_slider('slider1', 0, 1)
        slider.add_slider('slider2', 0, 2)

        slider.group_sliders(['slider1', 'slider2'], 'group1')

        self.assertEqual(slider.sliders_in_group('group1'), ['slider1', 'slider2']) # noqa  


if __name__ == '__main__':
    unittest.main()
