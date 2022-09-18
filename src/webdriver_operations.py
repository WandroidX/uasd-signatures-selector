import time
from selenium.webdriver.common.by import By

def get_signatures_table_info(driver) -> list[dict]:
    '''Get the info contained in the table of the uasd webpage with codes and names'''
    signatures_table_txt = driver.execute_script(
        'let tbodyElements = Array.from(document.getElementsByTagName("tbody")); return tbodyElements[4].innerText')
    signatures_info: list[list[str]] = [signature.split('\t') for signature in signatures_table_txt.split('\n')]
    signatures_list_dict: list[dict] =  []
    headers_name: list[str] = signatures_info[0]
    for element in signatures_info[1: ]:
        signature_dict: dict = {}
        for header_i, name in enumerate(headers_name):
            signature_dict.update({name: element[header_i]})
        signatures_list_dict.append(signature_dict)
    return signatures_list_dict

def open_uasd_in_selection_page(driver, username, password):
    '''Open the uasd autoservice and enters in selection page'''
    driver.get('https://ssb.uasd.edu.do/ssomanager/c/SSB')
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(username)
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)
    access_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[2]/form/div[3]/div/button')
    access_btn.click()
    time.sleep(5)
    alumn_btn = driver.find_element(By.XPATH, '/html/body/div[19]/div[3]/div[2]/div[1]/span[2]/span/span[3]/button/div/div/span')
    alumn_btn.click()
    time.sleep(5)
    inscription_btn = driver.find_element(By.CSS_SELECTOR, '#bmenu--P_RegMnu___UID0')
    inscription_btn.click()
    time.sleep(5)
    add_btn = driver.find_element(By.XPATH, '/html/body/div[19]/div[3]/div[2]/div[2]/div/div[4]/ul/li[2]/a/h3')
    add_btn.click()
    time.sleep(5)
    send_period_btn = driver.find_element(By.XPATH, '//*[@id="id____UID6"]/div/div/div')
    send_period_btn.click()

def search_signatures_by_nrc_in_uasd(driver, nrc_list):
    position_number = 0
    signatures_dicts_list = []
    for nrc in nrc_list:
        nrc_inputs = []

        for i in range(1, 11):
            nrc_input = driver.find_element(By.ID, f'crn_id{i}')
            nrc_inputs.append(nrc_input)

        if nrc:
            nrc_inputs[position_number].send_keys(nrc)
            position_number += 1
            if nrc == nrc_list[-1]:
                position_number = 0
                send_signatures_btn = driver.find_element(By.XPATH, '//*[@id="id____UID4"]/div/div/div')
                send_signatures_btn.click()
                time.sleep(3)
                signatures_dicts_list += get_signatures_table_info(driver)
                print('ya no hay más asignaturas')
            elif position_number == 10:
                position_number = 0
                send_signatures_btn = driver.find_element(By.XPATH, '//*[@id="id____UID4"]/div/div/div')
                send_signatures_btn.click()
                time.sleep(3)
                signatures_dicts_list += get_signatures_table_info(driver)


    return signatures_dicts_list
        
