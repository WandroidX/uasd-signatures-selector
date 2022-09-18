import unittest, sys
sys.path.append('src')
from src import hourtable_manager as timetable_manager
from src import file_management as filema


class TestTimetable(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_convert_hour(self):
        '''Convertion test'''
        hours: str = '15'
        hours_converted: str = timetable_manager.convert_hour_to_seconds(hours)
        self.assertEqual(hours_converted, str(15 * 3600 ))

    def test_parsing_timetables(self):
        '''Parsing test'''
        timetable: str = '15 a 20 16 a 20'
        timetables_parsed: list[str] = timetable_manager.parse_timetable_from_timetables(timetable)
        expected_value: list[str] = ['15 a 20', '16 a 20']
        self.assertEqual(timetables_parsed, expected_value )

    def test_parsing_days(self):
        days: str = 'MAJU'
        days_parsed: list[str] = timetable_manager.parse_days(days)
        expected_value: list[str ] =  ['MA', 'JU'] 
        self.assertEqual(days_parsed, expected_value)

    def test_parsing_days2(self):
        days: str = 'MA   JU'
        days_parsed: list[str] = timetable_manager.parse_days(days)
        expected_value: list[str ] =  ['MA', 'JU'] 
        self.assertEqual(days_parsed, expected_value)

    def test_start_end(self):
        timetable: str = '15 a 20'
        timetable_dict: dict = timetable_manager.get_start_and_end_time_from_timetable(timetable)

        self.assertEqual(timetable_dict, {'start_time': '15', 'end_time': '20', 'str_timetable': timetable})

    def test_timetable_to_dict(self):
        timetable: str = '15 a 20'
        day: str = 'MA'
        timetable_dict: dict = timetable_manager.timetable_to_timetable_dict(day, timetable)
        expected_value: dict = {'course_timetables': {'MA': {'start_time_in_secs': '54000', 'end_time_in_secs': '72000', 'str_timetable': '15 a 20'}}}
        self.assertEqual(timetable_dict, expected_value) 

class TestFileManager(unittest.TestCase):
    def test_interference(self):
        interference: bool = timetable_manager.compare_timetable_interference( '20 a 22', '18 a 24')
        self.assertTrue(interference)
    def test_get_signatures(self):
        USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
        signatures: list = filema.get_signatures_from_file('San Juan', r'c:\users\crist\downloads\personal_uasd_signatures.xlsx', USEFUL_SIGNATURES_NAMES, [1, 2, 4, 6, 10, 11], ['way_of_learning', 'NRC', 'course_name', 'teacher', 'timetable', 'days'])

        signature_dict: dict
        for signature_dict in signatures:
            signature_dict.update(
                timetable_manager.timetable_to_timetable_dict(
                    signature_dict['days'], signature_dict['timetable'])
            )



        selection: list[list[dict]] = timetable_manager.make_courses_timetables(signatures, black_interval_of_course='17 a 24', black_list_days= ['DO'], prefered_days=['VI'])

        signature_dict: dict
        file_content: str = ''
        

        for timetable in selection:
            print(timetable)
            for signature_dict in timetable:
                file_content += ';'.join(list(signature_dict.keys())) + '\n'
                break

            for signature_dict in timetable:
                file_content += ';'.join(list(map(lambda value: str(value), list( signature_dict.values() )))) + '\n'

            file_content += '\n'
        with open(file=r'c:\users\crist\desktop\final_selection.csv', mode='w', encoding='utf-8') as file:
            file.write(file_content)

        # print(signatures)
        self.assertEqual(1, 1)

    







if __name__ == "__main__":
    unittest.main()

