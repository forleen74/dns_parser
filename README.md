#### Это парсер на Selenium для сбора информации с сайта dnsdumpster.com
Парсер содержит два скрипта:
* сам парсер (parser_nofttp) - заходит на сайт, вбивает адрес в виде example.com и забирает весь html полученной страницы в папку json-s. При этом файл будет называться example.com.json
* скрипт для обработки (json_обработка_complete) - обрабатывает все собранные страницы и собирает нужную информацию в таблицу result_
(файл result урезан в целях конфиденциальности)

#### В парсере реализованы:
* задержка перед сбором информации следующего сайта
* подмена прокси для обхода ограничения сайта на число запросов в сутки  

#### Парсер позволяет собрать данные о сетевой инфраструктуре сайта, информацию о котором может предоставить dnspumpster
