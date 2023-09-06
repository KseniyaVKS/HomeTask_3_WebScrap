import requests
import bs4
import fake_headers
from pprint import pprint
import re
import time
from unicodedata import normalize
import json

vacancy_data = []

for page in range(10):
    url = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={page}'
    headers_gen = fake_headers.Headers(browser='opera', os='win')
    response = requests.get(url, headers=headers_gen.generate())
    main_html = response.text
    main_soup = bs4.BeautifulSoup(main_html, features='lxml')
    vacancy_list_tag = main_soup.find_all('div', class_="vacancy-serp-item__layout")

    for vacancy_tag in vacancy_list_tag:
        h3_tag = vacancy_tag.find('h3', class_='bloko-header-section-3')
        vacancy_name = h3_tag.text
        vacancy_link = h3_tag.find('a')['href']
        vacancy_salary_tag = vacancy_tag.find('span', class_='bloko-header-section-2')
        vacancy_salary = ''

        if vacancy_salary_tag == None:
            vacancy_salary = 'Зарплата не указана'
        else:
            vacancy_salary = vacancy_salary_tag.text

        time.sleep(0.5)
        response_vacancy_full = requests.get(vacancy_link, headers=headers_gen.generate())
        response_vacancy_full_html = response_vacancy_full.text
        vacancy_full_soup = bs4.BeautifulSoup(response_vacancy_full_html, features='lxml')
        vacancy_full_tag = vacancy_full_soup.find('div', class_='g-user-content')
        vacancy_full_text = vacancy_full_tag.text
        vacancy_company_tag = vacancy_tag.find('div', class_='vacancy-serp-item__meta-info-company')
        vacancy_company = vacancy_company_tag.text
        vacancy_city_tag = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
        vacancy_city = vacancy_city_tag.text.split(',')[0]
        vacancy_data.append({
            'vacancy_name': normalize('NFKD',vacancy_name),
            'vacancy_link': vacancy_link,
            'vacancy_salary': normalize('NFKD', vacancy_salary),
            'vacancy_company': normalize('NFKD',vacancy_company),
            'vacancy_city': vacancy_city
            })

with open('vacancy_info.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(vacancy_data, indent=2, ensure_ascii=False))