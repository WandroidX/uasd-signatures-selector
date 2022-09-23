import unittest, sys, random
import config
sys.path.append('src')
from src import hourtable_manager as timetable_manager
from src import file_management as filema


# class TestParseTimetable(unittest.TestCase):
    # def setUp(self):
        # self.maxDiff = None

    # def test_convert_hour(self):
        # '''Convertion test'''
        # hours: str = '15'
        # hours_converted: str = timetable_manager.convert_hour_to_seconds(hours)
        # self.assertEqual(hours_converted, str(15 * 3600 ))

    # def test_parsing_timetables(self):
        # '''Parsing test'''
        # timetable: str = '15 a 20,16 a 20'
        # timetables_parsed: list[str] = timetable_manager.parse_timetable_from_timetables(timetable)
        # expected_value: list[str] = ['15 a 20', '16 a 20']
        # self.assertEqual(timetables_parsed, expected_value )

    # def test_parsing_timetables2(self):
        # timetable: str = '15 a 20,16 a 20 20 a 24'
        # timetables_parsed: list[str] = timetable_manager.parse_timetable_from_timetables(timetable)
        # expected_value: list[str] = ['15 a 20', '16 a 20 20 a 24']
        # self.assertEqual(timetables_parsed, expected_value )


# class TestParseDays(unittest.TestCase):
    # def test_parsing_days(self):
        # days: str = 'MAJU'
        # days_parsed: list[str] = timetable_manager.parse_days(days)
        # expected_value: list[str ] =  ['MA', 'JU'] 
        # self.assertEqual(days_parsed, expected_value)

    # def test_parsing_days2(self):
        # days: str = 'MA   JU'
        # days_parsed: list[str] = timetable_manager.parse_days(days)
        # expected_value: list[str ] =  ['MA', 'JU'] 
        # self.assertEqual(days_parsed, expected_value)

# class TestTimetableDict(unittest.TestCase):
    # def test_start_end(self):
        # timetable: str = '15 a 20'
        # timetable_dict: dict = timetable_manager.get_start_and_end_time_from_timetable(timetable)

        # self.assertEqual(timetable_dict, {'start_time': '15', 'end_time': '20', 'str_timetable': timetable})

    # def test_timetable_to_dict(self):
        # timetable: str = '15 a 20'
        # day: str = 'MA'
        # timetable_dict: dict = timetable_manager.timetable_to_timetable_dict(day, timetable)
        # expected_value: dict = {'course_timetables': {'MA': {'start_time': '15', 'end_time': '20', 'str_timetable': '15 a 20'}}}
        # self.assertEqual(timetable_dict, expected_value) 

    # def test_timetable_to_dict_with_merge(self):
        # timetable: str = '15 a 20 20 a 25'
        # day: str = 'MA'
        # timetable_dict: dict = timetable_manager.timetable_to_timetable_dict(day, timetable)
        # expected_value: dict = {'course_timetables': {'MA': {'start_time': '15', 'end_time': '25', 'str_timetable': '15 a 25'}}}
        # self.assertEqual(timetable_dict, expected_value) 

    # def test_parse_credits(self) -> None:
        # timetable_list: list[str] = ['15 a 20', '20 a 25']
        # credits_amount: int = timetable_manager.parse_course_credits_amount(timetables=timetable_list)
        # self.assertEqual(credits_amount, 10)
        # pass


# class TestMergeTimetables(unittest.TestCase):
    # def test_merge_timetables(self) -> None:
        # timetable: str = '15 a 20,16 a 20 20 a 24'
        # timetables_parsed: list[str] = timetable_manager.parse_timetable_from_timetables(timetable)
        # merged_timetable: str = timetable_manager.merge_several_timetables_in_str(timetables_parsed[1])
        # self.assertEqual(merged_timetable, '16 a 24')

    # pass

# class TestFileManager(unittest.TestCase):
    # def test_interference(self):
        # interference: bool = timetable_manager.compare_timetable_interference( '20 a 22', '18 a 24')
        # self.assertTrue(interference)
    # def test_get_signatures_from_virtual(self):
        # USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
        # signatures: list = filema.get_signatures_from_file('San Juan', config.VIRTUAL_COURSES_XL_FILE_PATH, USEFUL_SIGNATURES_NAMES, config.USEFUL_COLUMNS_INDEX ,config.USEFUL_COLUMNS_HEADERS)

        # signature_dict: dict
        # for signature_dict in signatures:
            # signature_dict.update(
                # timetable_manager.timetable_to_timetable_dict(
                    # signature_dict['days'], signature_dict['timetable'])
            # )



        # selection: list[list[dict]] = timetable_manager.make_courses_timetables(signatures, black_interval_of_course='17 a 24', black_list_days= ['DO'], prefered_days=['VI'])

        # signature_dict: dict
        # file_content: str = ''
        

        # for timetable in selection:
            # for signature_dict in timetable:
                # file_content += ';'.join(list(signature_dict.keys())) + '\n'
                # break

            # for signature_dict in timetable:
                # file_content += ';'.join(list(map(lambda value: str(value), list( signature_dict.values() )))) + '\n'

            # file_content += '\n'
        # with open(file=config.OUTPUT_FILE_PATH, mode='w', encoding='utf-8') as file:
            # file.write(file_content)

        # # print(signatures)
        # self.assertEqual(1, 1)

    

    # def test_get_signatures_from_presential(self):
        # USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
        # signatures: list = filema.get_signatures_from_file('San Juan', config.PRESENCIAL_COURSES_XL_FILE_PATH, USEFUL_SIGNATURES_NAMES, config.USEFUL_COLUMNS_INDEX ,config.USEFUL_COLUMNS_HEADERS)

        # signature_dict: dict
        # for signature_dict in signatures:
            # signature_dict.update(
                # timetable_manager.timetable_to_timetable_dict(
                    # signature_dict['days'], signature_dict['timetable'])
            # )



        # selection: list[list[dict]] = timetable_manager.make_courses_timetables(signatures, black_interval_of_course='17 a 24', black_list_days= ['DO'], prefered_days=['VI'])

        # signature_dict: dict
        # file_content: str = ''
        

        # for timetable in selection:
            # for signature_dict in timetable:
                # file_content += ';'.join(list(signature_dict.keys())) + '\n'
                # break

            # for signature_dict in timetable:
                # file_content += ';'.join(list(map(lambda value: str(value), list( signature_dict.values() )))) + '\n'

            # file_content += '\n'
        # with open(file='/home/wanderson/Desktop/presential_output_file.csv', mode='w', encoding='utf-8') as file:
            # file.write(file_content)

        # # print(signatures)
        # self.assertEqual(1, 1)

    

class TestCalcCredits(unittest.TestCase):
    # def test_calc_credits1# (self):
        # list_of_credits: list[int] = [1, 2, 3, 4, 1, 2, 3]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    # def test_calc_credits2(self):
        # list_of_credits: list[int] = [1, 2, 3, 4, 1, 2, 3, 5]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)
    # def test_calc_credits3(self):
        # list_of_credits: list[int] = [1, 2, 3, 4, 1, 2, 3, 5, 5]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    # def test_calc_credits4(self):
        # list_of_credits: list[int] = [1, 2, 3, 4, 1, 2, 3, 5, 5, 3]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    # def test_calc_credits5(self):
        # list_of_credits: list[int] = [1, 2, 3, 4, 1, 2, 3, 5, 5, 3, 2, 1]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    # def test_calc_credits6(self):
        # list_of_credits_in_list: list[list[int]] = [[5, 3], [5, 1], [5, 1, 1, 1], [5, 1, 1, 1], [5, 1, 1, 1], [4, 4], [2]]
        # list_of_credits: list[int] = [number for credit_list in list_of_credits_in_list for number in credit_list]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    def test_calc_credits7(self):
        list_of_credits: list[int] = [random.randint(1, 5) for i in range(0, 10)]
        time_available: str = '07 a 15'
        credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        print(credits_ordered)
        self.assertEqual(1, 1)

    # def test_calc_credits8(self):
        # list_of_credits: list[int] = [random.randint(1, 5) for i in range(0, 10)]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)


    # def test_calc_credits9(self):
        # list_of_credits: list[int] = [random.randint(1, 5) for i in range(0, 10)]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

    # def test_calc_credits10(self):
        # list_of_credits: list[int] = [random.randint(1, 5) for i in range(0, 10)]
        # time_available: str = '07 a 15'
        # credits_ordered = timetable_manager.calc_minimun_days(list_of_credits, time_available)
        # print(credits_ordered)
        # self.assertEqual(1, 1)

if __name__ == "__main__":
    log_file = './hourtable.log'
    with open(log_file, "a") as f:
       runner = unittest.TextTestRunner(f)
       unittest.main(testRunner=runner)

