import re
import logging
from typing import Match, Pattern


logging.basicConfig(format='[%(asctime)s] - %(levelname)s - filename: %(filename)s - lineno: %(lineno)s - function name: %(funcName)s -  %(message)s', level=logging.DEBUG, filemode='a',
                    filename='./hourtable.log')


def convert_hour_to_seconds(hour: str) -> str:
    '''Receive an hour in HH format 
    and transforms it in seconds.
    The seconds count from 00 to 23'''
    hours: int = int(hour)

    MINUTES_IN_HOUR: int = 60
    SECONDS_IN_MINUTE: int = 60
    SECONDS_IN_HOUR: int = MINUTES_IN_HOUR * SECONDS_IN_MINUTE
    return str(hours * SECONDS_IN_HOUR)

def parse_timetable_from_timetables(timetables: str) -> list[str]:
    '''Receive a string with several timetables and return
    a list with all of them in the string'''
    return timetables.split(',')

def merge_several_timetables_in_str(timetable_str: str) -> str:
    # are divided by groups because is needed for comparison
    re_timetable: Pattern = re.compile(r'(\d{2}) a (\d{2})')
    timetables: list[tuple[ str, str ]] = re_timetable.findall(timetable_str)
    START_TIME_INDEX: int = 0
    END_TIME_INDEX: int = 1
    # this number is the index of the last element in the tuples of the list inmediately before

    # this is called fr
    merged_start_time: str = ''
    merged_end_time: str  = ''
    for timetable in timetables:
        start_time_timetable: str = timetable[START_TIME_INDEX]
        end_time_timetable: str = timetable[END_TIME_INDEX]
        if not merged_start_time:
            merged_start_time = start_time_timetable
        else:
            # this means that the {timetable} is before the merged timetable (merged_start_time and
            # merged_end_time)
            current_timetable_before_the_merged: bool = end_time_timetable == merged_start_time > start_time_timetable
            if current_timetable_before_the_merged:
                merged_start_time = start_time_timetable

        if not merged_end_time == 0:
            merged_end_time = end_time_timetable
        else:
            # this mean that the {timetable} is afther the merged timetable (merged_start_time and
            # merged_end_time)
            if merged_end_time == start_time_timetable:
                merged_end_time = end_time_timetable

    return f'{merged_start_time} a {merged_end_time}'

def get_start_and_end_time_from_timetable(timetable: str) -> dict[str, str] :
    '''Receive a timetable (only one) and get the start and the final hour of it'''
    re_timetable: Pattern = re.compile(r'(\d{2}) a (\d{2})')
    start_hour: str
    end_hour: str
    hours_found: Match | None = re_timetable.search(timetable) 

    
    if hours_found:
        start_hour, end_hour = (
                hours_found.groups()
        )

        time_dict: dict[str, str] = {
            'start_time': start_hour,
            'end_time': end_hour,
            'str_timetable': timetable

        }
        return time_dict
    else:
        raise Exception(f'the argument is not a timetable: {timetable}')

def parse_days(days: str) -> list[str]:
    '''Receive a string with several days and return a list with 
    all of them'''
    re_days: Pattern = re.compile(r'(\w{2})')

    days_found = re_days.findall(days)
    return days_found

def parse_course_credits_amount(timetable_str: str = '', timetables: list[str] = [], DEFAULT_VALUE: int = 0) -> int:
    """Return the amount of credit based on the given timetables in the parameter"""
    credits_amount: int = DEFAULT_VALUE
    if timetables:
        timetable: str
        for timetable in timetables:
            timetable_dict: dict[str, str] = get_start_and_end_time_from_timetable(timetable)
            start_time_str: str | None = timetable_dict.get('start_time')
            end_time_str: str | None = timetable_dict.get('end_time')
            if start_time_str and end_time_str:
                # the difference between the end_time and the start time is added to credit_amount
                hours_differences: int = int(end_time_str) - int(start_time_str)
                credits_amount += hours_differences
    elif timetable_str:
        timetable_dict: dict[str, str] = get_start_and_end_time_from_timetable(timetable_str)
        start_time_str: str | None = timetable_dict.get('start_time')
        end_time_str: str | None = timetable_dict.get('end_time')
        if start_time_str and end_time_str:
            # the difference between the end_time and the start time is added to credit_amount
            hours_differences: int = int(end_time_str) - int(start_time_str)
            credits_amount += hours_differences
    return credits_amount


def timetable_to_timetable_dict(days: str, timetable: str) -> dict:
    '''Receive a string with days and a string with timetables.
    Return a dict with the start and end time and the same but
    converted to seconds (useful for time comparisons)'''
    timetables_list: list[str] = parse_timetable_from_timetables(timetable)
    for index, timetable in enumerate( timetables_list ):
        if len( timetable ) > 7:
            timetables_list[index] = merge_several_timetables_in_str(timetable)


    days_list: list[str] = parse_days(days)

    # in case of that there be more timetables than days, the timetables will be merged

    assert len(days_list) >= len(timetables_list), f'CANT BE MORE TIMETABLES THAN DAYS: {days_list=}, {timetables_list=}'

    COURSE_TIMETABLES_KEY: str = 'course_timetables'
    COURSE_START_TIME_KEY: str = 'start_time'
    COURSE_END_TIME_KEY: str = 'end_time'
    STR_TIMETABLE_KEY: str = 'str_timetable'

    timetable_dict: dict = {}
    if COURSE_TIMETABLES_KEY not in  timetable_dict:
        timetable_dict.update({
            COURSE_TIMETABLES_KEY: {}
        })
    for i, day in enumerate( days_list ):
        current_day_timetable: str
        try:
            current_day_timetable = timetables_list[i]
        except IndexError:
            current_day_timetable = timetables_list[-1]

        start_end_dict: dict = get_start_and_end_time_from_timetable(current_day_timetable)
        start_time: str | None = start_end_dict.get(COURSE_START_TIME_KEY)
        end_time: str | None = start_end_dict.get(COURSE_END_TIME_KEY)
        str_timetable: str | None = start_end_dict.get(STR_TIMETABLE_KEY)
        new_start_end_dict: dict = {}

        if start_time and end_time and str_timetable:

            new_start_end_dict.update({
                STR_TIMETABLE_KEY: str_timetable,
                COURSE_START_TIME_KEY: start_time,
                COURSE_END_TIME_KEY: end_time

                
            })

        timetable_dict[COURSE_TIMETABLES_KEY].update(
            {
                day: new_start_end_dict
            }
        )

    return timetable_dict


    
def compare_timetable_interference(first_timetable: str | dict, second_timetable: str | dict) -> bool:
    '''Return if second timetable interfere with first_timetable'''
    
    if isinstance(first_timetable, str) and isinstance(second_timetable, str):
        first_timetable_dict: dict = get_start_and_end_time_from_timetable(first_timetable)
        second_timetable_dict: dict = get_start_and_end_time_from_timetable(second_timetable)
    elif isinstance(first_timetable, dict) and isinstance(second_timetable, dict):
        first_timetable_dict: dict = first_timetable
        second_timetable_dict: dict = second_timetable
    else:
        raise Exception('arguments must be both dicts or str')

    COURSE_START_TIME_KEY: str = 'start_time'
    COURSE_END_TIME_KEY: str = 'end_time'

    first_timetable_start_secs: str = convert_hour_to_seconds(first_timetable_dict[COURSE_START_TIME_KEY])
    first_timetable_end_secs: str = convert_hour_to_seconds(first_timetable_dict[COURSE_END_TIME_KEY])
    second_timetable_start_secs: str = convert_hour_to_seconds(second_timetable_dict[COURSE_START_TIME_KEY])
    second_timetable_end_secs: str = convert_hour_to_seconds(second_timetable_dict[COURSE_END_TIME_KEY])

    start_time_between_course: bool = first_timetable_start_secs > second_timetable_start_secs and\
        first_timetable_start_secs < second_timetable_end_secs

    end_time_between_course: bool = first_timetable_end_secs > second_timetable_start_secs and\
        first_timetable_end_secs < second_timetable_end_secs

    start_time_between_course2: bool = second_timetable_start_secs > first_timetable_start_secs and\
        second_timetable_start_secs < first_timetable_end_secs

    end_time_between_course2: bool = second_timetable_end_secs > first_timetable_start_secs and\
        second_timetable_end_secs < first_timetable_end_secs

    start_time_is_interfering: bool = second_timetable_start_secs == first_timetable_start_secs or\
        start_time_between_course or start_time_between_course2

    end_time_is_interfering: bool =  second_timetable_end_secs ==  first_timetable_end_secs or \
        end_time_between_course or end_time_between_course2

    if start_time_is_interfering or end_time_is_interfering:
        return True
    return False

def calc_minimun_days(credits_list: list[int], time_available: str | list[str]) -> list[list[int]] :
    times_of_same_credit: dict[int, int] = {}
    # sort credits_list: neccesary to ensure found the best combination
    credits_list.sort(reverse=True)

    # if time_available is a list, will find the max_credits_per_day calculating and adding all the 
    # str in that list
    if isinstance(time_available, list):
        max_credits_per_day = 0
        for time_str in time_available:
            max_credits_per_day: int =+ parse_course_credits_amount(time_str)
    else:
        max_credits_per_day: int = parse_course_credits_amount(time_available)
    # adds the differents credits of the courses (just once) e.g. [1, 2, 4] if there are courses
    # with 1, 2 and 4 credits
    for credit in credits_list:
        # if a credit is greater than the max_credits_per_day, it will be excluded
        if credit <=  max_credits_per_day:
            # if the credit key is not in the times_of_same_credit dict, adds it with 1 as value
            # if is in the dict, adds 1 to the current value
            if credit not in times_of_same_credit:
                times_of_same_credit.update({
                    credit: 1
                })
            else:
                times_of_same_credit[credit] += 1

    max_amount_of_credit_list: list[int] = [credit_number * credit_times for credit_number, credit_times in list( times_of_same_credit.items() )]
    total_credits: int = sum(max_amount_of_credit_list)
    original_max_credits_per_day: int = max_credits_per_day
    # this will get the minimun days of class that are neccesary
    minimun_days_float: float = total_credits /  original_max_credits_per_day
    if not minimun_days_float.is_integer():
        minimun_days_float +=  1
    minimun_days = int(minimun_days_float)

    credits_left: dict[int, int] = times_of_same_credit
    daily_credits: list[list[int]] = []
    index: int = -1
    # here, will be built the credits combinations
    for credit_number in list(times_of_same_credit):
        max_credits_per_day = original_max_credits_per_day

        if credit_number not in credits_left:
            continue
        key_in_credits_left: bool = True
        while key_in_credits_left:
            if not credits_left:
                break
            credit_times: int = credits_left[credit_number]
            max_amount_of_credit: int = credit_times * credit_number
            if daily_credits:
                total_credits_of_last_day: int = sum(daily_credits[-1])
                if total_credits_of_last_day < original_max_credits_per_day:
                    credits_left_to_fill_last_day: int = original_max_credits_per_day - total_credits_of_last_day
                    if credits_left_to_fill_last_day % credit_number == 0:
                        number_of_times: int = credits_left_to_fill_last_day // credit_number
                        if number_of_times > credits_left[credit_number]:
                            number_of_times = credits_left[credit_number]

                        daily_credits[-1].extend([credit_number] * number_of_times)
                        credits_left[credit_number] -= number_of_times
                        if credits_left[credit_number] == 0:
                            credits_left.pop(credit_number)
                            key_in_credits_left: bool = False
                            break
            credit_times: int = credits_left[credit_number]
            max_amount_of_credit: int = credit_times * credit_number
            if max_amount_of_credit <= original_max_credits_per_day:
                # in case of come here but the credits_left dict is empty
                if not credits_left:
                    break

                key_in_credits_left: bool = False
                daily_credits.append([credit_number] * credit_times)
                credits_left.pop(credit_number)
            elif max_amount_of_credit > max_credits_per_day:
                number_of_times = max_credits_per_day // credit_number
                if number_of_times:
                    if number_of_times > credits_left[credit_number]:
                        number_of_times = credits_left[credit_number]
                    daily_credits.append([credit_number] * number_of_times)
                    credits_left[credit_number] -= number_of_times
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False
                else:
                    number_of_times = 1
                    daily_credits.append([credit_number] * number_of_times)
                    credits_left[credit_number] -= number_of_times
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False



    
        index: int
        for index, day_of_credits in enumerate(list(daily_credits)):
            total_credits_of_last_day: int = sum(day_of_credits)
            # this verify if there is a day_of_credits that needs fill
            if total_credits_of_last_day < original_max_credits_per_day:
                credits_left_to_fill_last_day: int = original_max_credits_per_day - total_credits_of_last_day
                # try to find a credit number that can fill the hole of credits
                credit_number_filler: int | None = credits_left.get(credits_left_to_fill_last_day)

                if credit_number_filler:
                    credit_number: int = credits_left_to_fill_last_day
                    daily_credits[index].append(credit_number)
                    credits_left[ credit_number ] -= 1
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False
                else:
                    max_amount_of_credit_list: list[int] = [credit_number * credit_times for credit_number, credit_times in list( credits_left.items() )]
                    credit_number_list: list[int] = [credit_number for credit_number in list( credits_left )]
                    if not max_amount_of_credit_list and not credit_number_list:
                        continue

                    if credits_left_to_fill_last_day in max_amount_of_credit_list:
                        index_of_filler: int = max_amount_of_credit_list.index(credits_left_to_fill_last_day)
                        credit_number: int = credit_number_list[index_of_filler]
                        credit_times = credits_left[credit_number]
                        daily_credits[index].extend([credit_number] * credit_times)
                        credits_left.pop(credit_number)

                    else:
                        i: int
                        for i, max_amount_of_credit in enumerate( max_amount_of_credit_list ):
                            if max_amount_of_credit > credits_left_to_fill_last_day:
                                credit_number = credit_number_list[i]
                                # if credit_number is multiplier of credits_left_to_fill_last_day
                                # surely will be possible fill the hole of credits
                                if credits_left_to_fill_last_day % credit_number == 0:
                                    credit_times = credits_left_to_fill_last_day // credit_number
                                    daily_credits[index].extend([credit_number] * credit_times)
                                    credits_left[credit_number] -= credit_times
                                    if credits_left[credit_number] == 0:
                                        credits_left.pop(credit_number)
                                        key_in_credits_left: bool = False
                                    break
                        else:
                            # this will find if there is a combination of max_amount_of_credit that
                            # can fill the hole of credits
                            for i, max_amount in enumerate(list(  max_amount_of_credit_list ) ):
                                credit_amount_left_to_fill: int = credits_left_to_fill_last_day - max_amount
                                element_index: int = len(max_amount_of_credit_list) 
                                combinated_credit_amount: int = sum(max_amount_of_credit_list)
                                # if even with all the credits available cant fill the credit_day
                                if combinated_credit_amount <= credit_amount_left_to_fill:
                                    for credit_number in  list(credit_number_list):
                                        credit_times: int = credits_left[credit_number]
                                        daily_credits[index].extend([credit_number] * credit_times)
                                        credits_left.pop(credit_number)
                                    break

                                while True:
                                    # to avoid an error of index
                                    if element_index == i:
                                        break
                                    element_index -= 1
                                    combinated_credit_amount: int = sum(max_amount_of_credit_list[i:element_index])
                                    amount_would_left: int = credit_amount_left_to_fill - combinated_credit_amount
                                    if combinated_credit_amount == credit_amount_left_to_fill:


                                        for credit_number in  credit_number_list[i: element_index]:
                                            credit_times: int = credits_left[credit_number]
                                            daily_credits[index].extend([credit_number] * credit_times)
                                            credits_left[credit_number] -= credit_times
                                            if credits_left[credit_number] == 0:
                                                credits_left.pop(credit_number)
                                                key_in_credits_left: bool = False

                                        break
                                    elif amount_would_left > 0:
                                        # will try to find a multiplier of the amount lacking
                                        for credit_number in  list(credit_number_list[element_index: ] ):
                                            if credit_number not in credits_left:
                                                continue
                                            if amount_would_left  % credit_number == 0:
                                                # try to add the current credit_number
                                                # if it can fill the hole, else will try with
                                                # all the other combinations
                                                credit_times = amount_would_left  // credit_number
                                                if credit_times > credits_left[credit_number] :
                                                    credit_times: int = credits_left[credit_number]
                                                max_amount_of_credit: int = credit_number * credit_times
                                                if max_amount_of_credit == amount_would_left:
                                                    daily_credits[index].extend([credit_number] * credit_times)
                                                    credits_left[credit_number] -= credit_times
                                                    if credits_left[credit_number] == 0:
                                                        credits_left.pop(credit_number)
                                                    break
                                                else:
                                                    amount_would_left2 = amount_would_left - max_amount_of_credit 

                                                for credit_number2 in  credit_number_list[i: element_index] :
                                                    if amount_would_left2  % credit_number2 == 0:
                                                        # try to add the current credit_number
                                                        # if it can fill the hole, else will try with
                                                        # all the other combinations
                                                        credit_times2 = amount_would_left2  // credit_number2
                                                        if credit_times2 > credits_left[credit_number2] :
                                                            credit_times2: int = credits_left[credit_number2]
                                                        max_amount_of_credit2: int = credit_number2 * credit_times2
                                                        if max_amount_of_credit2 == amount_would_left2:
                                                            daily_credits[index].extend([credit_number2] * credit_times2)
                                                            daily_credits[index].extend([credit_number] * credit_times)
                                                            credits_left[credit_number] -= credit_times
                                                            credits_left[credit_number2] -= credit_times2
                                                            if credits_left[credit_number] == 0:
                                                                credits_left.pop(credit_number)
                                                            if credits_left[credit_number2] == 0:
                                                                credits_left.pop(credit_number2)

                                                            break

                                                    credit_times: int = credits_left[credit_number2]
                                                    daily_credits[index].extend([credit_number2] * credit_times)
                                                    credits_left[credit_number2] -= credit_times
                                                    if credits_left[credit_number2] == 0:
                                                        credits_left.pop(credit_number2)
                                                        key_in_credits_left: bool = False

                                                # try to add the last credit_number found
                                                break


    # here, will try to merge the day_of_credits (daily_credits list) that are lesser than 
    # the original_max_credits_per_day , will remove them from daily_credits
    daily_credits_lesser_than_max_credits: list[list[int]] = list(filter(lambda day_of_credit: sum(day_of_credit) < original_max_credits_per_day, daily_credits))
    for day_of_credit in daily_credits_lesser_than_max_credits:
        daily_credits.remove(day_of_credit)

    for i in range(0, len(daily_credits_lesser_than_max_credits)):
        # this ensure that day_of_credits was not removed by the code
        # below and that it is not empty
        try:
            day_of_credits = daily_credits_lesser_than_max_credits[i]
            if not day_of_credits :
                continue
        except IndexError:
            break

        max_amount_of_credit: int = sum(day_of_credits)
        credits_left_to_fill_day: int = original_max_credits_per_day - max_amount_of_credit
        if i+1 < len(daily_credits_lesser_than_max_credits):
            for i_future, future_day_of_credits in enumerate( list(daily_credits_lesser_than_max_credits[i+1 :]), i+1):
                for credit_number in list(future_day_of_credits):
                    if credit_number <= credits_left_to_fill_day:
                        daily_credits_lesser_than_max_credits[i_future].remove(credit_number)
                        day_of_credits.append(credit_number)
                        credits_left_to_fill_day -= credit_number
        daily_credits.append(day_of_credits)
    if len(daily_credits) != minimun_days:
        logging.warning(f'lenghth of daily_credits ({len(daily_credits)}) is not equal to minimun_days ({minimun_days}) ')
    logging.info(f'credits_list was: {credits_list=}')
    logging.info(f'result of function: {daily_credits}\n')
    return daily_credits

def get_dicts_with_conditions( search_target: list[dict], day: str = '', credit_number_list:list[int] = [], start_time: str = '', end_time: str = '',  excluded_courses: list[str] = []) -> list[dict]:
    '''return the dicts that accomplish conditions in parameters'''
    for element in list(search_target):
        course_name: str | None = element.get('course_name')
        timetable: str | None =  element.get('timetable')
        credits_amount_value: int | None = element.get('credits_amount')
        days: str | None = element.get('days')
        # after verify if there are the proper keys in the ($element) will remove it from the 
        # from search_target if dont accomplish certain conditions
        #### FIX HERE
        #### FIX HERE
        if days: 
            days_list: list[str] = parse_days(days)

            if day and day not in days_list:
                search_target.remove(element)
                continue
        if course_name and  course_name in excluded_courses:
            search_target.remove(element)
            continue

        if timetable:
            if start_time or end_time:
                timetable_list: list[str] = parse_timetable_from_timetables(timetable)
                parsed_timetables: list[dict] = [get_start_and_end_time_from_timetable(parsed) for parsed in timetable_list]
                broken_condition: bool = False
                for parsed in parsed_timetables:
                    start_time_value: str | None = parsed.get('start_time')
                    end_time_value: str | None = parsed.get('end_time')

                    if start_time_value and start_time != start_time_value:
                        broken_condition: bool = True
                        break
                    if end_time_value and end_time != end_time_value:
                        broken_condition: bool = True
                        break
                if broken_condition:
                    search_target.remove(element)
                    continue
        if credits_amount_value and credits_amount_value not in credit_number_list:
            search_target.remove(element)
            continue
    ordered_search_target: list[dict] = sorted(search_target, key=lambda element: element['credits_amount'])
    return ordered_search_target

#### FIX HERE
#### FIX HERE
def can_be_more_courses_before(start_time: str, day: str, candidates_for_fill: list[dict], credits_day: list[int], min_credit: int) -> dict:
    TIMETABLES_KEY: str = 'course_timetables'
    if len(credits_day) == 1:
        return {}
    for candidate in candidates_for_fill:
        timetable: dict | None =  candidate.get('course_timetables')
        if timetable:
            days: list[str] = list(timetable.keys())
            parsed_timetables: list[dict] = list(timetable.values())
            for parsed in parsed_timetables:
                start_time_value: str | None = parsed.get('start_time')
                end_time_value: str | None = parsed.get('end_time')

                if start_time_value and start_time != start_time_value:
                    break



def make_courses_timetables(courses_timetables: list[dict[str, str]],
    prefered_days: list[str] = [],
    black_list_days: list[str] = [],
    prefered_courses: list[str] = [],
    black_list_courses: list[str] = [],
    prefered_teachers: list[str] = [],
    black_list_teachers: list[str] = [],
    prefered_interval_of_course: str = '',
    black_interval_of_course: str = ''
) -> list[list]:
    '''receive a list with several dicts of courses and create 
    timetable combining them'''

    TIMETABLES_KEY: str = 'course_timetables'
    TEACHER_KEY: str = 'teacher'
    NAME_KEY: str = 'course_name'
    STR_TIMETABLE_KEY: str = 'str_timetable'
    GENERAL_PUNCTUATION_KEY: str = 'general_punctuation'
    DAYS_PUNCTUATION_KEY: str = 'days_punctuation'
    COURSE_PUNCTUATION_KEY: str = 'course_punctuation'
    TIMETABLE_PUNCTUATION_KEY: str = 'timetable_punctuation'
    TEACHER_PUNCTUATION_KEY: str = 'teacher_punctuation'
    COMMON_DAY_PUNCTUATION_KEY: str = 'common_day_punctuation'
    CREDITS_AMOUNT_KEY: str = 'credits_amount'
    LESS_DAY_OF_CLASS_KEY: str = 'less_day_of_class_key'
    START_TIME_KEY: str = 'start_time'
    END_TIME_KEY: str = 'end_time'

    

    courses_dicts_list: dict = {}

    possible_start_number: str | None = '07'
    possible_end_number: str | None = '22'
    available_interval: str = f'{possible_start_number} a {possible_end_number}'
    available_interval_list: list[str] = []

    if prefered_interval_of_course:
        prefered_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(prefered_interval_of_course)
        possible_start_number: str | None = prefered_interval_dict.get(START_TIME_KEY)
        possible_end_number: str | None = prefered_interval_dict.get(END_TIME_KEY)
    else:
        prefered_interval_dict: dict[str, str ] = {}
    if black_interval_of_course:
        black_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(black_interval_of_course)
        alter_possible_start_number: str | None = black_interval_dict.get(START_TIME_KEY)
        alter_possible_end_number: str | None = black_interval_dict.get(END_TIME_KEY)
        available_interval_list = [f'{possible_start_number} a {alter_possible_start_number}', f'{alter_possible_end_number} a {possible_end_number}']
    else:
        black_interval_dict: dict[str, str ] = {}


    if possible_start_number and possible_end_number:
        start_number: str = possible_start_number
        end_number: str = possible_end_number

    

    # this groups courses with the same name in [courses_dicts_list]
    for course in courses_timetables:
        current_course_name: str | None = course.get(NAME_KEY)
        course_timetable: dict | None = course.get(TIMETABLES_KEY)
        if current_course_name:
            # if there is no a key in courses_dicts_list with the name of 
            # current_course_name, if creates it with empty list
            # as its value
            if current_course_name not in courses_dicts_list:
                courses_dicts_list.update({
                    current_course_name: []
                })

            # these conditionals filters the course and exclude it if includes
            # something that is in any black_list_* parameter
            if black_list_courses:
                if current_course_name in black_list_courses:
                    continue
            if black_list_days:

                # that is a dict with the days when the course is given
                # as its keys
                in_forbidden_day: bool = False
                if course_timetable:
                    for day in course_timetable:
                        if day in black_list_days:
                            in_forbidden_day = True
                            break
                    if in_forbidden_day:
                        continue

            if black_list_teachers:
                current_course_teacher: str | None = course.get(TEACHER_KEY)
                # if the teacher of the current course is in black list of teachers
                if current_course_teacher in black_list_teachers:
                    continue

            if black_interval_dict:
                if course_timetable:
                    in_forbidden_time: bool = False
                    for day in course_timetable.values():
                        forbidden_str_timetable: str | None = black_interval_dict.get(STR_TIMETABLE_KEY)
                        day_str_timetable: str | None = day.get(STR_TIMETABLE_KEY)

                        if forbidden_str_timetable and day_str_timetable:
                            in_forbidden_time = compare_timetable_interference(forbidden_str_timetable, day_str_timetable)
                            if in_forbidden_time:
                                break

                    if in_forbidden_time:
                        continue
            
            # adds to the apropriate courses if acomplish the conditions
            courses_dicts_list[current_course_name].append(course)

    # this will tell what are the most common days between signatures
    days_counter_dict: dict = {'LU': 0, 'MA': 0, 'MI': 0, 'JU': 0, 'VI': 0, 'SA': 0, 'DO': 0 }
    courses_dict_list: list[dict]
    for courses_dict_list in courses_dicts_list.values():
        course: dict
        for course in courses_dict_list:
            course_timetables: dict | None = course.get(TIMETABLES_KEY)
            if course_timetables:
                current_course_days: list[str] = list(course_timetables.keys())
                for day in current_course_days:
                    days_counter_dict[day] += 1

    days_counter_items: list[tuple[ str, int ]] = list(days_counter_dict.items())
    days_counter_dict = dict(sorted(days_counter_items, key= lambda tu: tu[1], reverse=True))
    days_counter_order_list: list = list(days_counter_dict.keys())

    #here will be saved the credit_list to make the combinations
    credits_list: list[int] = []

    # this punctuate the courses depending how many prefered conditions 
    # have. the conditions to punctuate are the prefered_* arguments
    # in the function
    courses_dict_list: list[dict]
    for courses_dict_list in courses_dicts_list.values():

        for index, course in enumerate( courses_dict_list ):
            course_timetable: dict | None = course.get(TIMETABLES_KEY)
            DEFAULT_PUNCTUATION: int | float = 0
            general_punctuation: int | float = DEFAULT_PUNCTUATION


            # this first add the extra punctuation if the days of the course are the most
            # common day
            if course_timetable:
                course_days: list = list(course_timetable.keys())
                max_extra_punctuation_per_common_day: float = 10 / len(course_days)
                extra_days_punctuation_val: int | float = DEFAULT_PUNCTUATION

                if index == 0:
                    # this will extract the amount of credits of the signatures
                    timetables_str_list: list[str] = []
                    for day_dict in course_timetable.values():
                        day_str_timetable: str  | None = day_dict.get(STR_TIMETABLE_KEY)
                        if day_str_timetable:
                            # append the timetable of the current day to the 
                            timetables_str_list.append(day_str_timetable)

                    # calc the credits and add it to the course as a key
                    credits_amount: int = parse_course_credits_amount(timetables=timetables_str_list)
                    credits_list.append(credits_amount)

                # adds a punctuation depending how many days must go to class
                # (the minus you must go the more is the punctuation)
                days_amount: int = len(course_days)
                less_days_of_class: float | int = 10 / days_amount
                general_punctuation += less_days_of_class
                course.update({
                    CREDITS_AMOUNT_KEY: credits_amount,
                    LESS_DAY_OF_CLASS_KEY: less_days_of_class

                })


                # this will add the 
                for day in course_days:
                    current_day_index: int = days_counter_order_list.index(day)
                    # this is the punctuation that will be added 
                    # depending how common is the day
                    extra_punctuation_per_common_day = (
                        max_extra_punctuation_per_common_day /
                        (current_day_index + 1)
                    )

                    extra_days_punctuation_val += extra_punctuation_per_common_day
                    general_punctuation += extra_punctuation_per_common_day

                course.update({
                    COMMON_DAY_PUNCTUATION_KEY: extra_days_punctuation_val
                })


            if prefered_courses:
                course_punctuation_val: int = DEFAULT_PUNCTUATION
                course_name: str | None = course.get(NAME_KEY)
                if course_name:
                    if course_name in prefered_teachers:
                        course_punctuation_val += 10
                        general_punctuation += 10
                course.update({
                    COURSE_PUNCTUATION_KEY: course_punctuation_val
                })
            if prefered_teachers:
                teacher_punctuation_val: int | float = DEFAULT_PUNCTUATION
                teacher_name: str | None = course.get(TEACHER_KEY)
                if teacher_name:
                    if teacher_name in prefered_teachers:
                        teacher_punctuation_val += 10
                        general_punctuation += 10
                course.update({
                    TEACHER_PUNCTUATION_KEY: teacher_punctuation_val
                })
                pass
            if prefered_interval_dict:
                timetable_punctuation_val: int | float = DEFAULT_PUNCTUATION
                prefered_time_str_timetable: str | None = prefered_interval_dict.get(STR_TIMETABLE_KEY) 

                if course_timetable and prefered_time_str_timetable:
                    # this is the punctuation that the course will receive per
                    # time of class that is in the prefered_interval
                    punctuation_per_day_in_good_interval: float = 10 / len(course_timetable.keys())
                    for day in course_timetable:
                        course_str_timetable: str | None = course.get(STR_TIMETABLE_KEY)
                        if course_str_timetable:
                            is_interfering_good: bool = compare_timetable_interference(
                                prefered_interval_dict,
                                course_str_timetable
                            )
                            # if is in the prefered_interval, the timetable punctuation increases
                            if is_interfering_good:
                                timetable_punctuation_val += punctuation_per_day_in_good_interval
                                general_punctuation += punctuation_per_day_in_good_interval


                course.update({
                    TIMETABLE_PUNCTUATION_KEY: timetable_punctuation_val
                })
            if prefered_days:
                days_punctuation_val: int | float = DEFAULT_PUNCTUATION
                if course_timetable:
                    course_days: list = list(course_timetable.keys())
                    punctuation_per_day_prefered_days: float = 10 / len(course_days)

                    # increase the days_punctuation_val if the day is in prefered days
                    for day in course_days:
                        if day in prefered_days:
                            days_punctuation_val += punctuation_per_day_prefered_days
                            general_punctuation += punctuation_per_day_prefered_days

                course.update({
                    DAYS_PUNCTUATION_KEY: days_punctuation_val
                })


            course.update({GENERAL_PUNCTUATION_KEY: general_punctuation})




    # here the dicts of each course will be ordered depending 
    # its LESS_DAY_OF_CLASS_KEY 
    for courses_names in courses_dicts_list:
        original_courses_list: list[dict] | None = courses_dicts_list.get( courses_names )
        if original_courses_list:
            course: dict
            ordered_courses: list[dict] = sorted(original_courses_list,
                key = lambda course: course[LESS_DAY_OF_CLASS_KEY])
            courses_dicts_list.update({
                courses_names: ordered_courses
            })


    # here, the courses dict list will be ordered in descendent accordingly to
    # its general_punctuation combinated
    courses_dicts_list_in_list: list[list[str | list[dict] | float]] = []
    courses_list: list[dict]
    signature_name: str
    for signature_name, courses_list in courses_dicts_list.items():
        signature_general_punctuation: int | float | None = 0
        for course in courses_list:
            course_general_punctuation: int | float | None = course.get(GENERAL_PUNCTUATION_KEY)
            if course_general_punctuation:
                signature_general_punctuation += course_general_punctuation

        list_to_append: list[str | list[dict] | float] = []
        list_to_append.append(signature_name)
        list_to_append.append(courses_list)
        list_to_append.append(signature_general_punctuation)
        courses_dicts_list_in_list.append(list_to_append)

    # here, order the signatures by the accumulate of general puctuation in descendent order
    # put here reverse=True to invert the order
    ordered_courses_dicts_list_in_list: list[list[str | list[dict] | float]] = sorted(courses_dicts_list_in_list, key=lambda course: course[2])
    # then, 
    ordered_courses_without_general_punct: list[list[str | list[dict] | float]]  = list(map(lambda course: course[:2], ordered_courses_dicts_list_in_list))

    # here, the signatures are ordered by the general puctuation
    courses_dicts_list = dict(ordered_courses_without_general_punct)


    if available_interval_list:
        credits_combinations: list[list[int]] = calc_minimun_days(credits_list=credits_list, time_available=available_interval_list)
    else:
        credits_combinations: list[list[int]] = calc_minimun_days(credits_list=credits_list, time_available=available_interval)

    alter_courses_timetable: list[dict] = []
    baned_courses_names: list[str] = []

    for credit_day in list( credits_combinations ): 
        all_courses_available: list[dict] = [course for course_list in list(courses_dicts_list.values()) for course in course_list ]
        for i in range(len(credit_day)):
            if i == 0:
                # in the first number of credit_day, will try to add a course with start_time
                # equal to the minimun start_time possible. in case of unsuccessssful result,
                # will add the first with the credit_number
                courses_candidates: list[dict] = get_dicts_with_conditions(all_courses_available, credit_number_list=[i], start_time= start_number)
                if not courses_candidates:
                    courses_candidates: list[dict] = get_dicts_with_conditions(all_courses_available, credit_number_list=[i])
                    for candidate in courses_candidates:
                        # before add the first course, verify if there is another signature that can be before it
                        candidate_to_timetable: dict = candidate
                        break
                    else:
                        candidate_to_timetable: dict = courses_candidates[0]
                    candidate_end_time: str | None = candidate_to_timetable.get(END_TIME_KEY)

                    if candidate_end_time and candidate_end_time != end_number

                    min
                else:
                    candidate_to_timetable: dict = courses[0]
                alter_courses_timetable.append(courses_candidates[0])
            else:
                courses_candidates: list[dict] = get_dicts_with_conditions(all_courses_available, credit_number_list= credit_day[i:], excluded_courses=baned_courses_names)

        pass

    list_possible_courses_full_timetable: list[list] = []
    course_number: int = 0
    for i in range(3):
        possible_courses_full_timetable: list[dict] = []
        course_dict_list: list[dict]
        for course_dict_list in courses_dicts_list.values():
            if possible_courses_full_timetable:

                course: dict
                for course in course_dict_list:

                    course_timetable: dict | None = course.get(TIMETABLES_KEY)

                    possible_course: dict
                    for possible_course in possible_courses_full_timetable:
                        
                        possible_course_timetable: dict | None = possible_course.get(TIMETABLES_KEY)

                        # this is a list with the days in common in the timetable
                        # of courses added to possible_courses_full_timetable and
                        # course
                        if course_timetable and possible_course_timetable:
                            days_in_common = [day for day in course_timetable if day in possible_course_timetable]

                            for day in days_in_common:
                                possible_course_str_timetable: str | None = possible_course_timetable[day].get(STR_TIMETABLE_KEY)
                                course_str_timetable: str | None = course_timetable[day].get(STR_TIMETABLE_KEY)
                                if possible_course_str_timetable and course_str_timetable:
                                    there_is_interference: bool = compare_timetable_interference(course_str_timetable, possible_course_str_timetable)

                                    if there_is_interference:
                                        break
                            else:
                                continue
                            break
                    else:
                        possible_courses_full_timetable.append(course)
                        break
            else:
                try:
                    possible_courses_full_timetable.append(course_dict_list[course_number])
                    course_number += 1
                except IndexError:
                    possible_courses_full_timetable.append(course_dict_list[-1])


        list_possible_courses_full_timetable.append(possible_courses_full_timetable)
    return list_possible_courses_full_timetable






    





