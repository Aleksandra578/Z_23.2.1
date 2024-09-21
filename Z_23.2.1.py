import requests
from bs4 import BeautifulSoup
import pandas as pd


def collect_user_rates(user_login):
   page_num = 1
   data = []

   while True:
       url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
       html_content = requests.get(url).text
       soup = BeautifulSoup(html_content, 'lxml')
       entries = soup.find_all('div', class_='item')
       if len(entries) == 0:  # Признак остановки
           break
       for entry in entries:
           #название фильма
           nameRus = entry.find('div', class_='nameRus')
           film_name = nameRus.find('a').text
           #тк дата релиза указана в названии, то я взяла дату просмотра фильма
           release_date = entry.find('div', class_='date').text
           #рейтинг пользователя
           vote = entry.find('div', class_='vote').text
           data.append({'film_name': film_name, 'release_date': release_date, 'rating': vote})
       print(data[:5])

       page_num += 1  # Переходим на следующую страницу
   return data

user_rates = collect_user_rates(user_login='134059543')
df = pd.DataFrame(user_rates)
df.to_excel('user_rates.xlsx')
print(df)