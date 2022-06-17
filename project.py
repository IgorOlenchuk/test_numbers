import gspread
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials



# настраиваем доступ к Google Sheets и Googli Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# Подключаем ключи доступа
creds = ServiceAccountCredentials.from_json_keyfile_name("testpython-353519-60e571fd76e4.json", scope)
client = gspread.authorize(creds)
# Указываем имя выгружаемой таблицы и её страницу
sheet = client.open("test").sheet1
# В data записываем все записи из таблицы и листа
data = sheet.get_all_records()
df = pd.DataFrame.from_dict(data)
print(df)

currency_rub = list(df['стоимость,$'])
#курс доллара к рублю из ЦБ РФ на актуальную дату
currency = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
rateUSD = currency['Valute']['USD']['Value']
conversions = []
for index in range(len(currency_rub)):
    conversions.append(currency_rub[index] * rateUSD)
#добавляем колону "стоимость, руб." к таблице
df['стоимость в руб.'] = conversions

print(df)
print('Итого в долларах США:', sum(df['стоимость,$']))
print('Итого в рублях по курсу ЦБ на актуальную дату:', sum(df['стоимость в руб.']))

