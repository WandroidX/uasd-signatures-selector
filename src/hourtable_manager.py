import re, functools
import logging
from typing import Match, Pattern


logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s', level=logging.DEBUG, filemode='a',
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

def calc_minimun_days(credits_list: list[int], time_available: str) -> list[list[int]] :
    times_of_same_credit: dict[int, int] = {}
    # sort credits_list: neccesary to ensure found the best combination
    credits_list.sort(reverse=True)
    logging.info(f'{ credits_list =}')

    max_credits_per_day: int = parse_course_credits_amount(time_available)
    # logging.info(f'{max_credits_per_day=}')
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

    # logging.info(f'{ times_of_same_credit= }')
    max_amount_of_credit_list: list[int] = [credit_number * credit_times for credit_number, credit_times in list( times_of_same_credit.items() )]
    # logging.info(f'{ max_amount_of_credit_list= }')
    total_credits: int = sum(max_amount_of_credit_list)
    original_max_credits_per_day: int = max_credits_per_day
    # this will get the minimun days of class that are neccesary
    minimun_days_float: float = total_credits /  original_max_credits_per_day
    logging.debug(f'before add 1 {minimun_days_float=}')
    if not minimun_days_float.is_integer():
        minimun_days_float +=  1
        logging.debug(f'after add 1 {minimun_days_float=}')
    minimun_days = int(minimun_days_float)
    logging.debug(f'{minimun_days=}')

    # logging.debug(f'\n{total_credits=}')
    # logging.debug(f'\n{max_credits_per_day=}')
    # logging.info(f'{ minimun_days =}')
    credits_left: dict[int, int] = times_of_same_credit
    daily_credits: list[list[int]] = []
    index: int = -1
    # here, will be built the credits combinations
    for credit_number in list(times_of_same_credit):
        max_credits_per_day = original_max_credits_per_day

        # logging.debug(f'{ credit_number= }')
        if credit_number not in credits_left:
            continue
        key_in_credits_left: bool = True
        while key_in_credits_left:
            if not credits_left:
                break
            # logging.debug('in while')
            # logging.debug('inside while: before conditions')
            # logging.debug(f'{ credit_number= }')
            # logging.debug(f'{ credit_times= }')
            credit_times: int = credits_left[credit_number]
            max_amount_of_credit: int = credit_times * credit_number
            # logging.debug(f'{ max_amount_of_credit= }')
            try:
                # logging.debug(f'{daily_credits[-1]=}')
                total_credits_of_last_day: int = sum(daily_credits[-1])
                # logging.debug(f'{total_credits_of_last_day=}')
                if total_credits_of_last_day < original_max_credits_per_day:
                    credits_left_to_fill_last_day: int = original_max_credits_per_day - total_credits_of_last_day
                    # logging.debug(f'{credits_left_to_fill_last_day=}')
                    # logging.debug(f'{credit_number % credits_left_to_fill_last_day= }')
                    if credits_left_to_fill_last_day % credit_number == 0:
                        # logging.debug(f'is multiplier of credits_left')
                        number_of_times: int = credits_left_to_fill_last_day // credit_number
                        # logging.debug(f'{number_of_times=}')
                        # logging.debug(f'this is {number_of_times=}')
                        # logging.debug(f'this is {credit_number=}')
                        if number_of_times > credits_left[credit_number]:
                            # logging.info(f'this is {credits_left[credit_number]=}')
                            # logging.info(f'this is {credit_number=}')
                            number_of_times = credits_left[credit_number]
                        # logging.debug('in number of times')

                        daily_credits[-1].extend([credit_number] * number_of_times)
                        credits_left[credit_number] -= number_of_times
                        if credits_left[credit_number] == 0:
                            credits_left.pop(credit_number)
                            key_in_credits_left: bool = False
            except IndexError:
                logging.debug('error because is the first element and daily_credits is empty')

            if max_amount_of_credit <= original_max_credits_per_day:
                # logging.debug(f'this is {credits_left=}')
                # logging.debug(f'this is {credit_number=}')
                # in case of come here but the credits_left dict is empty
                if not credits_left:
                    break

                key_in_credits_left: bool = False
                daily_credits.append([credit_number] * credit_times)
                credits_left.pop(credit_number)
                # logging.debug('is equal to max_credits_per_day')
            elif max_amount_of_credit > max_credits_per_day:
                number_of_times = max_credits_per_day // credit_number
                # logging.debug(f'this is {number_of_times=}')
                # logging.debug(f'this is {credit_number=}')
                if number_of_times:
                    if number_of_times > credits_left[credit_number]:
                        # logging.info(f'this is {credits_left[credit_number]=}')
                        # logging.info(f'this is {credit_number=}')
                        number_of_times = credits_left[credit_number]
                    # logging.debug('in number of times')
                    daily_credits.append([credit_number] * number_of_times)
                    credits_left[credit_number] -= number_of_times
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False
                else:
                    # logging.debug('not in number of times')
                    number_of_times = 1
                    # logging.info(f'this is {number_of_times=}')
                    # logging.info(f'this is {credit_number=}')
                    daily_credits.append([credit_number] * number_of_times)
                    credits_left[credit_number] -= number_of_times
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False
                # logging.debug('is greater to max_credits_per_day')



    
        index: int
        for index, day_of_credits in enumerate(list(daily_credits)):
            # logging.debug(f'trying to fill day_of_credits n={index}')
            total_credits_of_last_day: int = sum(day_of_credits)

            # this verify if there is a day_of_credits that needs fill
            if total_credits_of_last_day < original_max_credits_per_day:
                # logging.debug('in tried to fill')
                credits_left_to_fill_last_day: int = original_max_credits_per_day - total_credits_of_last_day
                # logging.debug(f'{ total_credits_of_last_day= }')
                # logging.debug(f'{ credits_left_to_fill_last_day= }')
                # try to find a credit number that can fill the hole of credits
                credit_number_filler: int | None = credits_left.get(credits_left_to_fill_last_day)
                # logging.info(f'{ credit_number_filler= }')

                if credit_number_filler:
                    # logging.warning(f'1: { credits_left =} before the error')
                    # logging.warning(f'1: before supposed issue: { credits_left =}')
                    # logging.warning(f'1: before supposed issue: { daily_credits =}')
                    credit_number: int = credits_left_to_fill_last_day
                    # logging.warning(f'before supposed issue: { credits_left =}')
                    daily_credits[index].append(credit_number)
                    credits_left[ credit_number ] -= 1
                    # logging.warning(f'1: after supposed issue: { credits_left =}')
                    # logging.warning(f'1: after supposed issue: { daily_credits =}')
                    # logging.warning(f'1: after supposed issue: { credit_number =}')
                    # logging.warning(f'after supposed issue: { credit_times =}')
                    # logging.warning(f'{ credit_times =} before the error')
                    # logging.warning(f'after supposed issue: { credits_left =}')
                    # logging.warning(f'{ credit_number =} before the error')
                    if credits_left[credit_number] == 0:
                        credits_left.pop(credit_number)
                        key_in_credits_left: bool = False
                else:
                    # logging.warning(f'2: before supposed issue: { credits_left =}')
                    # logging.warning(f'2: before supposed issue: { daily_credits =}')
                    # logging.warning(f'2: before supposed issue: { credit_number =}')
                    max_amount_of_credit_list: list[int] = [credit_number * credit_times for credit_number, credit_times in list( credits_left.items() )]
                    credit_number_list: list[int] = [credit_number for credit_number in list( credits_left )]
                    # logging.warning(f'{ max_amount_of_credit_list =}')
                    # logging.warning(f'{ credit_number_list =}')
                    # logging.warning(f'2: after supposed issue: { credits_left =}')
                    # logging.warning(f'2: after supposed issue: { daily_credits =}')
                    # logging.warning(f'2: after supposed issue: { credit_number =}')
                    # logging.info('this is in the begining')
                    # logging.debug(f'{ credit_number_list= }')
                    # logging.debug(f'{ max_amount_of_credit_list= }')
                    if not max_amount_of_credit_list and not credit_number_list:
                        continue
                    # logging.error(f'{ credits_left_to_fill_last_day =}')
                    # logging.error(f'{ max_amount_of_credit_list= }')

                    if credits_left_to_fill_last_day in max_amount_of_credit_list:
                        # logging.info('credits fits perfectly')
                        index_of_filler: int = max_amount_of_credit_list.index(credits_left_to_fill_last_day)
                        credit_number: int = credit_number_list[index_of_filler]
                        credit_times = credits_left[credit_number]
                        daily_credits[index].extend([credit_number] * credit_times)
                        credits_left.pop(credit_number)

                    else:
                        i: int
                        for i, max_amount_of_credit in enumerate( max_amount_of_credit_list ):
                            if max_amount_of_credit > credits_left_to_fill_last_day:
                                # logging.warning(f'3: before supposed issue: { credits_left =}')
                                # logging.warning(f'3: before supposed issue: { daily_credits =}')
                                # logging.warning(f'3: before supposed issue: { credit_number =}')
                                # logging.warning(f'3: before supposed issue: { max_amount_of_credit =}')
                                # logging.warning(f'3: before supposed issue: { i =}')
                                # logging.warning(f'3: before supposed issue: { credits_left_to_fill_last_day =}')
                                credit_number = credit_number_list[i]
                                # if credit_number is multiplier of credits_left_to_fill_last_day
                                # surely will be possible fill the hole of credits
                                if credits_left_to_fill_last_day % credit_number == 0:
                                    # logging.warning(f'4: before supposed issue: { credits_left =}')
                                    # logging.warning(f'4: before supposed issue: { daily_credits =}')
                                    # logging.warning(f'4: before supposed issue: { credit_number =}')
                                    credit_times = credits_left_to_fill_last_day // credit_number
                                    # logging.warning(f'4: before supposed issue: { credit_times =}')
                                    daily_credits[index].extend([credit_number] * credit_times)
                                    credits_left[credit_number] -= credit_times
                                    # logging.warning(f'4: after supposed issue: { credits_left =}')
                                    # logging.warning(f'4: after supposed issue: { daily_credits =}')
                                    # logging.warning(f'4: after supposed issue: { credit_number =}')
                                    if credits_left[credit_number] == 0:
                                        credits_left.pop(credit_number)
                                        key_in_credits_left: bool = False
                                    break
                        else:
                            ### vision: if comes here, means that there is no credit_number that 
                            ###can fill the credits left (if the max_amount of credits_number_list are
                            ### lesser than the required or greater but not multiplier or there are no
                            ### equals or there are no exact number filler)
                            ### will try fo find a combination of max_amounts that can fill it
                            ### by 
                            # this will find if there is a combination of max_amount_of_credit that
                            # can fill the hole
                            for i, max_amount in enumerate(list(  max_amount_of_credit_list ) ):
                                credit_amount_left_to_fill: int = credits_left_to_fill_last_day - max_amount
                                element_index: int = len(max_amount_of_credit_list) 
                                # logging.warning(f'5: before supposed issue: { credits_left =}')
                                # logging.warning(f'5: before supposed issue: { daily_credits =}')
                                # logging.warning(f'5: before supposed issue: { credit_number =}')
                                combinated_credit_amount: int = sum(max_amount_of_credit_list)
                                # if even with all the credits available cant fill the credit_day
                                if combinated_credit_amount <= credit_amount_left_to_fill:
                                    # logging.debug(combinated_credit_amount)
                                    for credit_number in  list(credit_number_list):
                                        credit_times: int = credits_left[credit_number]
                                        daily_credits[index].extend([credit_number] * credit_times)
                                        credits_left.pop(credit_number)
                                    break
                                # logging.warning(f'5: after supposed issue: { credits_left =}')
                                # logging.warning(f'5: after supposed issue: { daily_credits =}')
                                # logging.warning(f'5: after supposed issue: { credit_number =}')

                                while True:
                                    # to avoid an error of index
                                    if element_index == i:
                                        break
                                    element_index -= 1
                                    combinated_credit_amount: int = sum(max_amount_of_credit_list[i:element_index])


                                    amount_would_left: int = credit_amount_left_to_fill - combinated_credit_amount
                                    if combinated_credit_amount == credit_amount_left_to_fill:
                                        # logging.debug(combinated_credit_amount)


                                        for credit_number in  credit_number_list[i: element_index]:
                                            credit_times: int = credits_left[credit_number]
                                            daily_credits[index].extend([credit_number] * credit_times)
                                            # logging.warning(f'6: before supposed issue: { credits_left =}')
                                            # logging.warning(f'6: before supposed issue: { daily_credits =}')
                                            # logging.warning(f'6: before supposed issue: { credit_number =}')
                                            credits_left[credit_number] -= credit_times
                                            if credits_left[credit_number] == 0:
                                                credits_left.pop(credit_number)
                                                key_in_credits_left: bool = False

                                        break
                                    elif amount_would_left > 0:
                                        # logging.warning(f'7: before supposed issue: { credits_left =}')
                                        # logging.warning(f'7: before supposed issue: { daily_credits =}')
                                        # logging.warning(f'7: before supposed issue: { credit_number =}')
                                        # will try to find a multiplier of the amount lacking
                                        for credit_number in  list(credit_number_list[element_index: ] ):
                                            # logging.info(f'in start of for { credits_left= }')
                                            # logging.warning(f'8: before supposed issue: { credits_left =}')
                                            # logging.warning(f'8: before supposed issue: { daily_credits =}')
                                            # logging.warning(f'8: before supposed issue: { credit_number =}')
                                            if credit_number not in credits_left:
                                                # logging.info(f'not in dict { credits_left= }')
                                                # logging.info(f'not in dict { credit_number= }')
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
                                                # logging.warning(f'9: before supposed issue: { credits_left =}')
                                                # logging.warning(f'9: before supposed issue: { daily_credits =}')
                                                # logging.warning(f'9: before supposed issue: { credit_number =}')

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
                                                # logging.warning(f'10: before supposed issue: { amount_would_left  =}')
                                                # logging.warning(f'10: before supposed issue: { credits_left =}')
                                                # logging.warning(f'10: before supposed issue: { daily_credits =}')
                                                # logging.warning(f'10: before supposed issue: { credit_number =}')
                                                # logging.warning(f'10: before supposed issue: { credit_times =}')
                                                # logging.info(f'before issue { credits_left= }')
                                                # logging.info(f'before issue { credit_number= }')
                                                # logging.warning(f'after issue { credits_left= }')
                                                # logging.warning(f'11: before supposed issue: { credits_left =}')
                                                # logging.warning(f'11: before supposed issue: { daily_credits =}')
                                                # logging.warning(f'11: before supposed issue: { credit_number =}')
                                                # logging.warning(f'11: before supposed issue: { credit_times =}')
                                                break


    # here, will try to merge the day_of_credits (daily_credits list) that are lesser than 
    # the original_max_credits_per_day , will remove them from daily_credits
    logging.debug(f'before trying to fill 2nd time: {daily_credits=}')
    daily_credits_lesser_than_max_credits: list[list[int]] = list(filter(lambda day_of_credit: sum(day_of_credit) < original_max_credits_per_day, daily_credits))
    logging.debug(f'in trying to fill 2nd time: {daily_credits_lesser_than_max_credits=}')
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
        logging.debug(f'{day_of_credits=}')
        credits_left_to_fill_day: int = original_max_credits_per_day - max_amount_of_credit
        logging.debug(f'{i=}')
        logging.debug(f'{credits_left_to_fill_day=}')
        try:
            for i_future, future_day_of_credits in enumerate( list(daily_credits_lesser_than_max_credits[i+1 :]), i+1):
                for credit_number in list(future_day_of_credits):
                    logging.debug(f'{credit_number=}')
                    if credit_number <= credits_left_to_fill_day:
                        logging.debug(f'before pop {daily_credits_lesser_than_max_credits[i_future]=}')
                        logging.debug(f'before pop {daily_credits_lesser_than_max_credits}')
                        logging.debug(f'{i_future=}')
                        daily_credits_lesser_than_max_credits[i_future].remove(credit_number)
                        logging.debug(f'after pop {daily_credits_lesser_than_max_credits[i_future]=}')
                        day_of_credits.append(credit_number)
                        logging.debug(f'{day_of_credits=}')
                        credits_left_to_fill_day -= credit_number
        except IndexError:
            logging.debug('there was an index error')
            pass
        daily_credits.append(day_of_credits)
    if len(daily_credits) != minimun_days:
        logging.error(f'lenghth of daily_credits ({len(daily_credits)}) is not equal to minimun_days ({minimun_days}) ')
    logging.info(f'result of function: {daily_credits}')
    logging.info('\n')
    return daily_credits





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

    

    courses_dicts_list: dict = {}

    if prefered_interval_of_course:
        prefered_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(prefered_interval_of_course)
    else:
        prefered_interval_dict: dict[str, str ] = {}

    if black_interval_of_course:
        black_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(black_interval_of_course)
    else:
        black_interval_dict: dict[str, str ] = {}

    

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
    # its general punctuation
    for courses_names in courses_dicts_list:
        original_courses_list: list[dict] | None = courses_dicts_list.get( courses_names )
        if original_courses_list:
            course: dict
            ordered_courses: list[dict] = sorted(original_courses_list,
                key = lambda course: course[GENERAL_PUNCTUATION_KEY])
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


    list_possible_courses_full_timetable: list[list] = []
    # here will be the first course of all timetables
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






    





