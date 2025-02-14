from copy import deepcopy
import unittest

from ..ssc import *


def testing_chart():
    return """
#NOTEDATA:;
#CHARTNAME:Brackets;
#STEPSTYPE:dance-single;
#DESCRIPTION:Brackets;
#CHARTSTYLE:;
#DIFFICULTY:Edit;
#METER:12;
#RADARVALUES:0.793,1.205,0.500,0.298,0.961;
#CREDIT:shala*;
#NOTES:

0000
0000
0000
0000
;
    """


def testing_charts():
    variants = tuple(SSCChart(testing_chart()) for _ in range(10))
    variants[1].chartname = 'My Cool Chart'
    variants[2].stepstype = 'dance-double'
    variants[3].description = 'Footswitches'
    variants[4].chartstyle = 'Pad'
    variants[5].difficulty = 'Challenge'
    variants[6].meter = '13'
    variants[7].radarvalues = '1.000,1.000,1.000,1.000,1.000'
    variants[8].credit = 'Unknown'
    variants[9].notes = '1000\n0100\n0010\n0001'
    return variants


def testing_simfile():
    return (
        '#VERSION:0.83;\n'
        '#TITLE:My Cool Song;\n'
        '#ARTIST:My Cool Alias;\n'
    ) + str(SSCCharts(testing_charts()))
    


class TestSSCChart(unittest.TestCase):
    
    def test_init_and_properties(self):
        unit = SSCChart(testing_chart())

        self.assertEqual('dance-single', unit.stepstype)
        self.assertEqual('Brackets', unit.description)
        self.assertEqual('Edit', unit.difficulty)
        self.assertEqual('12', unit.meter)
        self.assertEqual('0.793,1.205,0.500,0.298,0.961', unit.radarvalues)
        self.assertEqual('\n\n0000\n0000\n0000\n0000\n', unit.notes)
    
    def test_serialize(self):
        unit = SSCChart(testing_chart())
        expected = (
            '#NOTEDATA:;\n'
            '#CHARTNAME:Brackets;\n'
            '#STEPSTYPE:dance-single;\n'
            '#DESCRIPTION:Brackets;\n'
            '#CHARTSTYLE:;\n'
            '#DIFFICULTY:Edit;\n'
            '#METER:12;\n'
            '#RADARVALUES:0.793,1.205,0.500,0.298,0.961;\n'
            '#CREDIT:shala*;\n'
            '#NOTES:\n'
            '\n'
            '0000\n'
            '0000\n'
            '0000\n'
            '0000\n'
            ';\n'
            '\n'
        )


        self.assertEqual(expected, str(unit))

    def test_eq(self):
        variants = testing_charts()
        base = variants[0]
        copy = deepcopy(base)

        # Identity check
        self.assertEqual(base, base)

        # Equality check
        self.assertEqual(base, copy)

        # Inequality checks
        self.assertNotEqual(base, variants[1])
        self.assertNotEqual(base, variants[2])
        self.assertNotEqual(base, variants[3])
        self.assertNotEqual(base, variants[4])
        self.assertNotEqual(base, variants[5])
        self.assertNotEqual(base, variants[6])

    def test_repr(self):
        unit = SSCChart(testing_chart())

        self.assertEqual('<SSCChart: dance-single Edit 12>', repr(unit))


class TestSSCCharts(unittest.TestCase):
    
    def test_init_and_list_methods(self):
        unit = SSCCharts(testing_charts())
        
        self.assertEqual(10, len(unit))
        for chart in unit:
            self.assertIsInstance(chart, SSCChart)
    
    def test_serialize(self):
        unit = SSCCharts(testing_charts())

        value = str(unit)
    
    def test_repr(self):
        chart = SSCChart(testing_chart())
        repr_chart = repr(chart)
        unit = SSCCharts([chart])

        self.assertEqual(f'SSCCharts([{repr_chart}])', repr(unit))

        unit.append(chart)

        self.assertEqual(f'SSCCharts([{repr_chart}, {repr_chart}])', repr(unit))


class TestSSCSimfile(unittest.TestCase):
    
    def test_init_and_properties(self):
        unit = SSCSimfile(string=testing_simfile())
        
        self.assertEqual('My Cool Song', unit['TITLE'])
        self.assertEqual('My Cool Song', unit.title)
        self.assertEqual('My Cool Alias', unit['ARTIST'])
        self.assertEqual('My Cool Alias', unit.artist)
        self.assertNotIn('SUBTITLE', unit)
        self.assertEqual(10, len(unit.charts))

    def test_repr(self):
        unit = SSCSimfile(string=testing_simfile())

        self.assertEqual('<SSCSimfile: My Cool Song>', repr(unit))

        unit['SUBTITLE'] = '(edited)'

        self.assertEqual('<SSCSimfile: My Cool Song (edited)>', repr(unit))

    def test_eq(self):
        variants = tuple(SSCSimfile(string=testing_simfile()) for _ in range(3))
        variants[1]['TITLE'] = 'Cool Song 2'
        variants[2].charts[0].description = 'Footswitches'
        base = variants[0]
        copy = deepcopy(base)

        # Identity check
        self.assertEqual(base, base)

        # Equality check
        self.assertEqual(base, copy)

        # Inequality checks
        self.assertNotEqual(base, variants[1])
        self.assertNotEqual(base, variants[2])


if __name__ == '__main__':
    unittest.main()