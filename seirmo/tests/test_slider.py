#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import seirmo as se

class TestSliderComponent(unittest.TestCase):
    """
    Test the '_SliderComponent' class.
    """
    def test__init__(self):
        slider = se._SliderComponent(['1','2'],[0,0],[1,2])
        
        # Check defaul initial value
        self.assertEqual(slider.initial_values,[0,0])
        
        # Check default step size
        self.assertEqual(slider.step_sizes,[0.1,0.2])

        # Check initialisation of data frame
        self.assertEqual(slider.slider_df.shape,(2,4))

    def test_add_slider(self):

        slider = se._SliderComponent('1',[0],[1])

        # Check input type
        with self.assertRaises(TypeError):
            slider.add_slider(1)

        with self.assertRaises(NameError):
            slider.add_slider('3')

        # Check function

    # def test_group_sliders(self):

        # Check slider

    def test_slider_ids(self):
        
        slider = se._SliderComponent('1',[0],[1])

        self.assertEqual(slider.slider_ids,['1'])


if __name__ == '__main__':
    unittest.main()
