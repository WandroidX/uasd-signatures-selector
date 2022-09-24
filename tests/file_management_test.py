# important for avoid import error
import sys, os
sys.path.append(os.getcwd())
from src import file_management as filema
from src import hourtable_manager as timetable_manager
import config
import unittest

class TestFileManager(unittest.TestCase):
    def test_interference(self):
        interference: bool = timetable_manager.compare_timetable_interference( '20 a 22', '18 a 24')
        self.assertTrue(interference)
    def test_get_signatures_from_virtual(self):
        USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
        signatures: list = filema.get_signatures_from_file('San Juan', config.VIRTUAL_COURSES_XL_FILE_PATH, USEFUL_SIGNATURES_NAMES, config.USEFUL_COLUMNS_INDEX ,config.USEFUL_COLUMNS_HEADERS)

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
            for signature_dict in timetable:
                file_content += ';'.join(list(signature_dict.keys())) + '\n'
                break

            for signature_dict in timetable:
                file_content += ';'.join(list(map(lambda value: str(value), list( signature_dict.values() )))) + '\n'

            file_content += '\n'
        with open(file=config.OUTPUT_FILE_PATH, mode='w', encoding='utf-8') as file:
            file.write(file_content)

        # print(signatures)
        self.assertEqual(1, 1)

    

    def test_get_signatures_from_presential(self):
        USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
        signatures: list = filema.get_signatures_from_file('San Juan', config.PRESENCIAL_COURSES_XL_FILE_PATH, USEFUL_SIGNATURES_NAMES, config.USEFUL_COLUMNS_INDEX ,config.USEFUL_COLUMNS_HEADERS)

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
            for signature_dict in timetable:
                file_content += ';'.join(list(signature_dict.keys())) + '\n'
                break

            for signature_dict in timetable:
                file_content += ';'.join(list(map(lambda value: str(value), list( signature_dict.values() )))) + '\n'

            file_content += '\n'
        with open(file='/home/wanderson/Desktop/presential_output_file.csv', mode='w', encoding='utf-8') as file:
            file.write(file_content)

        # print(signatures)
        self.assertEqual(1, 1)

    
if __name__ == '__main__':

    log_file: str = './filema_unittest.log'
    with open(log_file, mode='w') as log:
        runner = unittest.TextTestRunner(log)
        unittest.main(testRunner=runner)
