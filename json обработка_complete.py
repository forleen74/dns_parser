import os
import json
import pandas as pd
from bs4 import BeautifulSoup

def process_cell_data(cell):
    cell_text = cell.get_text(separator="<br/>")
    split_data = [x.strip() for x in cell_text.split("<br/>")]

    if len(split_data) == 2:
        return split_data[0], split_data[1]
    elif len(split_data) == 1:
        return split_data[0], ""
    else:
        return "", ""

dataframes = []

json_files = [f for f in os.listdir('json-s') if f.endswith('.json')]

for json_file in json_files:
    with open(os.path.join('json-s', json_file)) as f:
        data = json.load(f)

    json_str = str(data)  # Преобразуем JSON в строку
    soup = BeautifulSoup(json_str, 'html.parser')

    tables = soup.find_all('table')
    table_names = ['DNS Servers', 'MX Records', 'Host Records']

    for table in tables:
        table_name = table.find_previous('p').text.strip()

        if any(name in table_name for name in table_names):
            rows = table.find_all('tr')

            data = []
            for row in rows:
                cells = row.find_all('td')
                processed_data = []

                for i, cell in enumerate(cells):
                    if i == 2:
                        company, country = process_cell_data(cell)
                        processed_data.extend([company, country])
                    else:
                        processed_data.append(cell.get_text().strip())

                data.append(processed_data)

            df = pd.DataFrame(data)

            if 'DNS Servers' in table_name:
                df['DNS_MX_HOST'] = 'DNS Servers'
            elif 'MX Records' in table_name:
                df['DNS_MX_HOST'] = 'MX Records'
            elif 'Host Records' in table_name:
                df['DNS_MX_HOST'] = 'HOST Records'

            df['site_adress'] = os.path.splitext(json_file)[0]  # сайт-источник, (позже название компании)

            dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# запись в csv и xlsx
combined_df.to_csv('result_.csv', index=False)
combined_df.to_excel('result_.xlsx', index=False)
