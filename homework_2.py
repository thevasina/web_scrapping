import json
from bs4 import BeautifulSoup as bs
import requests
from time import sleep


class HHscraper:
    def __init__(self, start_url, headers, params):
        self.start_url = start_url
        self.start_headers = headers
        self.start_params = params
        self.info_vacancy = []

    def get_html_string(self, url, headers='', params=''):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return bs(html_string, "html.parser")

    def run(self, page_count):
        next_button = ''
        while next_button is not None:
            if page_count == 0:
                print(f'Найдено {len(self.info_vacancy)} вакансий')
                return

            if next_button == '':
                html_string = self.get_html_string(self.start_url + '/search/vacancy', self.start_headers,
                                                   self.start_params)
            else:
                html_string = self.get_html_string(next_button, self.start_headers)
            page_count -= 1

            soup = HHscraper.get_dom(html_string)
            vacancy_list = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})
            self.get_info_from_element(vacancy_list)
            try:
                next_button = self.start_url + soup.find('a', attrs={'data-qa': 'pager-next'}).attrs["href"]
            except Exception as e:
                next_button = None
        print(f'Найдено {len(self.info_vacancy)} вакансий')

    def get_info_from_element(self, vacancy_list):

        for vacancy in vacancy_list:
            data = {}
            name = vacancy.find('a', {'class': 'bloko-link'}).getText()
            link = vacancy.find('a', {'class': 'bloko-link'}).attrs["href"]
            data['имя вакансии'] = name
            data['ссылка на вакансию'] = link
            data['источник'] = self.start_url
            self.get_salary(data, vacancy)
            self.info_vacancy.append(data)

    def get_salary(self, data, vacancy):
        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            salary = salary.replace('\u202f', '').split()
            if '–' in salary:
                data['мин зарплата'] = float(salary[0])
                data['макс зарплата'] = float(salary[2])
                data['валюта'] = salary[-1]
            elif 'от' in salary:
                data['мин зарплата'] = float(salary[1])
                data['валюта'] = salary[-1]
            elif 'до' in salary:
                data['макс зарплата'] = float(salary[1])
                data['валюта'] = salary[-1]

        except Exception as e:
            data['зарплата'] = None

    def save_info_vacancy(self):
        with open("vacancy.json", 'w', encoding="utf-8") as file:
            json.dump(self.info_vacancy, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_find = input('Введите вакансию: ')
    page_count = int(input('Введите сколько страниц надо обработать: '))

    main_link = "https://hh.ru"
    params_main = {"area": "1",
                      "fromSearchLine": "true",
                      "st": "searchVacancy",
                      "text": user_find,
                      "page": "0"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.77 Safari/537.36"}

    scraper = HHscraper(main_link, headers, params_main)
    scraper.run(page_count)
    scraper.save_info_vacancy()
