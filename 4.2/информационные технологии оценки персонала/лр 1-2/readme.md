# Занятия 1–2 (лабораторное)

## 1. Зарубежный и отечественный рынок информационных систем для управления и оценки персонала

**Зарубежный рынок.** Доминируют облачные HCM-платформы (Workday, SAP SuccessFactors, Oracle HCM Cloud, UKG и др.) с подпиской на пользователя в месяц, глубокой аналитикой и модулями компенсаций, обучения и талант-менеджмента. Для крупных организаций сохраняются коробочные / on-premise внедрения (SAP ERP HCM, Oracle PeopleSoft, часть решений Infor, Sage) из соображений регуляторики и интеграции с учётными системами. Для оценки персонала типичны модули performance / 360°, LMS и ATS (Greenhouse, BambooHR, Cornerstone и т.д.), часто в связке с BI.

**Отечественный рынок (без учёта 1С в задании).** Представлены облачные сервисы рекрутинга и HRM (Хантфлоу, Skillaz, Битрикс24, продукты экосистемы Контур/СБИС, Мегаплан и др.), а также коробочные поставки западных и открытых платформ через интеграторов (в т.ч. Odoo, Moodle, ONLYOFFICE Workspace) и отечественные «коробки» (Битрикс24, отраслевые ERP с кадровым контуром). Требования 152-ФЗ и локализация интерфейса часто становятся решающими при выборе.

## 2. ИТ-обеспечение ассесмент-центров

Ассесмент-центр опирается на **расписание и сценарии** упражнений, **сбор наблюдений** (чек-листы, шкалы компетенций), **видео- и телекоммуникации** для удалённых участников, **хранение материалов кейсов** и **отчёты** для заказчика. ИТ-уровень включает: специализированные AC-платформы или модули HCM/TM; конференц-связь (Zoom, MS Teams, TrueConf и т.д.); СЭД и порталы обучения; иногда симуляторы и игровые механики. Важны разграничение доступа к персональным данным и протоколирование решений.

## 3. Выполнение заданий лабораторной работы

Проанализированы зарубежный и отечественный рынки информационных систем для управления и оценки персонала; результаты сведены в таблицы ниже.

В каждой группе — **пять** продуктов в сегменте **десктопные (локальная / коробочная установка или толстый клиент)** и **пять** — в сегменте **онлайн (SaaS)**. По заданию **1С не включалась**. Отечественные продукты отобраны среди вендоров и сервисов, ориентированных на РФ.

Ниже после таблиц — **скриншоты интерфейсов в том же порядке (№ 1–20)**.

### Столбцы (по методичке)

| Столбец | Содержание |
|--------|------------|
| Лицензия; регистрация | Проприетарная / открытая; нужна ли регистрация для доступа к продукту. |
| Бесплатно / платно | Демо, freemium или только коммерческая лицензия. |
| Управление и оценка | Кадровый учёт, подбор, обучение; оценка, KPI, 360°, AC. |
| Инструкция | Документация, база знаний, обучающие видео. |
| IT-компания | Уместность для IT: гибкий график, проектные роли, удалёнка. |

---

## Таблица результатов анализа

### 1. Зарубежный рынок — десктопные (локальная установка / on-premise)

| № | Название | Ссылка | Лицензия; регистрация | Бесплатно / платно | Цена | Язык | Управление и оценка персонала | Инструкция | Впечатления; IT-компания |
|---|----------|--------|----------------------|-------------------|------|------|------------------------------|------------|--------------------------|
| 1 | SAP ERP / SAP HCM (on-premise, классический клиент) | [sap.com](https://www.sap.com/products/hcm.html) | Проприетарная; регистрация для портала поддержки | Платно; пробные сценарии через партнёров | По запросу (проект внедрения + лицензии) | EN, DE и др.; RU через партнёров | Управление: штат, кадровые данные, расчёт, интеграция с FI. Оценка: цели, обучение, отчётность; кастомизация под методики | Есть: SAP Help Portal, курсы, **видео** у партнёров | Мощная, но тяжёлая для малого IT-бизнеса; для крупной ИТ-компании с глобальной политикой HR — уместно |
| 2 | Oracle PeopleSoft HCM | [oracle.com](https://www.oracle.com/human-capital-management/peoplesoft/) | Проприетарная; регистрация на My Oracle Support | Платно | По запросу | EN (+ локализации) | Управление: кадровый учёт, самообслуживание сотрудников, компенсации. Оценка: цели, ревью, карьерные планы | Есть: Oracle Docs, **текст** и вебинары | Зрелое enterprise-решение; для IT-контрактора с legacy-стеком на PeopleSoft — логично |
| 3 | Microsoft Dynamics 365 Human Resources | [microsoft.com](https://www.microsoft.com/dynamics-365/products/human-resources) | Проприетарная; учётная запись Microsoft | Платно; trial | Подписка за пользователя/месяц; калькулятор на сайте | Многоязычный UI | Управление: кадры, отпуска, бенефиты, интеграция с Microsoft 365. Оценка: цели, обратная связь, модули через партнёров | Есть: Learn Microsoft, **видео**, **текст** | Хорошо ложится на IT-компанию в экосистеме Microsoft/Azure |
| 4 | SAP Business One (HR-контур и аддоны) | [sap.com](https://www.sap.com/products/business-one.html) | Проприетарная | Платно; демо через партнёров | Лицензия + внедрение; по запросу | Локализации, RU у партнёров | Управление: МСП: сотрудники, простые кадровые процессы, отчётность. Оценка — в основном через партнёрские расширения | Есть: SAP Help, **текст** | Для небольшой IT-фирмы может быть проще S/4, но функционал HR урезан по сравнению с HCM |
| 5 | DynaFile (клиент документооборота HR) | [dynafile.com](https://www.dynafile.com/) | Проприетарная; регистрация для облачного сервиса | Платно; демо по запросу | Подписка; публичный прайс уточнять | EN | Управление: хранение кадровых документов, согласия, аудит. Оценка: косвенно — портфолио достижений, материалы ревью | Есть: база знаний, **текст** | Полезно как слой compliance; в IT-компании — для кадрового архива и ISO |

### 2. Зарубежный рынок — онлайн (SaaS)

| № | Название | Ссылка | Лицензия; регистрация | Бесплатно / платно | Цена | Язык | Управление и оценка персонала | Инструкция | Впечатления; IT-компания |
|---|----------|--------|----------------------|-------------------|------|------|------------------------------|------------|--------------------------|
| 6 | Workday HCM | [workday.com](https://www.workday.com/) | Проприетарная; регистрация | Платно; демо по заявке | Подписка; сумма по запросу | EN и др. | Управление: единый HCM, компенсации, тайм-менеджмент. Оценка: цели, ревью, развитие | Есть: Workday Help, **видео**, академия | Стандарт де-факто для крупных tech-работодателей; для SMB — избыточно и дорого |
| 7 | BambooHR | [bamboohr.com](https://www.bamboohr.com/) | Проприетарная; регистрация | Платно; trial | Тарифы по числу сотрудников | EN (частично другие) | Управление: мастер-данные, онбординг, отпуска. Оценка: опросы, производительность в расширениях | Есть: справка, **текст**, вебинары | Удобный «лёгкий» HRIS для растущей IT-компании |
| 8 | SAP SuccessFactors | [sap.com](https://www.sap.com/products/human-resources-hcm.html) | Проприетарная; регистрация SAP | Платно; trial по согласованию | Подписка | Многоязычный | Управление: core HR в облаке. Оценка: цели, 360°, обучение, преемственность | Есть: SAP Help, **видео** | Сильны талант и обучение; подходит IT-холдингу с глобальной политикой |
| 9 | Ethnio (исследования кандидатов / UX-рекрутинг) | [ethnio.com](https://ethn.io/) | Проприетарная; регистрация | Платно; trial | По подписке | EN | Управление: не полный HRIS; фокус на отборе и исследованиях UX. Оценка: поведенческие данные, скрининг | Есть: документация, **текст** | Для IT-продукта — инструмент исследовательского рекрутинга, не замена HRIS |
| 10 | Betterworks (OKR и performance) | [betterworks.com](https://www.betterworks.com/) | Проприетарная; регистрация | Платно; демо | По запросу | EN | Управление: цели и чек-ины. Оценка: OKR, лёгкие ревью | Есть: Help Center, **текст**, **видео** | Хорошо для IT с культурой OKR и матричной структурой |

### 3. Отечественный рынок (без 1С) — десктопные

| № | Название | Ссылка | Лицензия; регистрация | Бесплатно / платно | Цена | Язык | Управление и оценка персонала | Инструкция | Впечатления; IT-компания |
|---|----------|--------|----------------------|-------------------|------|------|------------------------------|------------|--------------------------|
| 11 | Битрикс24 (коробочная версия) | [bitrix24.ru](https://www.bitrix24.ru/) | Проприетарная; регистрация | Платно; ограниченный облачный free отдельно | Лицензия на коробку по прайсу | RU, EN | Управление: структура, задачи, документы, согласования. Оценка: чек-листы, опросы, KPI в задачах | Есть: Helpdesk Битрикс24, **видео**, **текст** | Частый выбор SMB и IT-интеграторов в РФ; гибкая доработка |
| 12 | Moodle (on-prem: LMS для оценки обучения) | [moodle.org](https://www.moodle.org/) | GPL-совместимая открытая; регистрация не обязательна | Бесплатно ПО; платно хостинг/поддержка | 0 за ПО; внедрение — по договору | Многоязычный, RU | Управление: курсы, компетенции. Оценка: тесты, задания, ведомости | Огромная база: **текст**, **видео**, сообщество | Уместно для IT-академии и внутреннего L&D |
| 13 | ONLYOFFICE Workspace (коробка, документооборот) | [onlyoffice.com](https://www.onlyoffice.com/ru/workspace.aspx) | Проприетарная / AGPL для Community; регистрация | Community бесплатно; Enterprise платно | От бесплатного CE до Enterprise | RU, EN | Управление: совместная работа, приказы, регламенты. Оценка: косвенно через HR-документооборот | Есть: Help Center, **текст** | Подходит IT-компании, если акцент на документах и совместной работе |
| 14 | Odoo (частная установка, модуль Employees / HR) | [odoo.com](https://www.odoo.com/app/employees) | LGPL / проприетарные модули; регистрация для Enterprise | Community бесплатно; Enterprise платно | Подписка Odoo.sh / лицензия | RU, EN | Управление: сотрудники, отпуска, рекрутинг (модули). Оценка: аппрейзалы через сторонние модули | Есть: Odoo Docs, **текст**, **видео** | Гибко для IT-стартапа; нужны компетенции внедрения |
| 15 | Mahara (on-prem: электронное портфолио, оценка компетенций) | [mahara.org](https://mahara.org/) | GPL; регистрация не обязательна | Бесплатно ПО | 0; хостинг своими силами | RU в языковых пакетах | Управление: ограниченно. Оценка: портфолио, рефлексия, витрина навыков | Есть: **текст**, вики | Полезно в вузовской/корпоративной академии IT-направления |

### 4. Отечественный рынок (без 1С) — онлайн

| № | Название | Ссылка | Лицензия; регистрация | Бесплатно / платно | Цена | Язык | Управление и оценка персонала | Инструкция | Впечатления; IT-компания |
|---|----------|--------|----------------------|-------------------|------|------|------------------------------|------------|--------------------------|
| 16 | Хантфлоу | [huntflow.ru](https://huntflow.ru/) | Проприетарная; регистрация | Платно; trial | Тарифы на сайте | RU, EN | Управление: воронка подбора, командная работа рекрутёров. Оценка: скоринг кандидатов, отчёты | Есть: база знаний, **текст**, **видео** | Сильный стандарт для IT-рекрутинга в РФ |
| 17 | Skillaz | [skillaz.ru](https://skillaz.ru/) | Проприетарная; регистрация | Платно; демо | По запросу | RU | Управление: подбор, аналитика воронки. Оценка: тесты и методики оценки кандидатов | Есть: поддержка, **текст** | Подходит mid-size+ IT-нанимателям |
| 18 | E-Staff (E-Staff Recruitment) | [e-staff.ru](https://e-staff.ru/) | Проприетарная; регистрация | Платно; демо | По запросу | RU | Управление: ATS, кадровый резерв. Оценка: методики в подборе | Есть: документация, **текст** | Распространено в enterprise; для продуктовой IT — по масштабу |
| 19 | СБИС (экосистема СКБ Контур: кадры и учёт) | [saby.ru](https://saby.ru/) | Проприетарная; регистрация Контур | Платно; пробный период | Тарифы на сайте | RU | Управление: кадровый учёт, ЭДО, отчётность. Оценка: вспомогательно отчётами | Есть: Контур.Помощь, **текст**, **видео** | Уместно для IT-компании, ориентированной на РФ и отчётность |
| 20 | Мегаплан (CRM/задачи; HR-процессы SMB) | [megaplan.ru](https://www.megaplan.ru/) | Проприетарная; регистрация | Платно; trial | Тарифы на сайте | RU | Управление: задачи, клиенты, внутренние процессы. Оценка: KPI в задачах, отчёты | Есть: справка, **текст**, **видео** | Для небольшой IT-фирмы как «лёгкая» альтернатива тяжёлому HCM |

---

## Скриншоты интерфейсов (порядок 1–20)

| № | Продукт (таблица) | Изображение | Источник |
|---|-------------------|-------------|----------|
| 1 | SAP (десктоп) | ![SAP Account overview](https://upload.wikimedia.org/wikipedia/commons/c/c7/Account_overview.JPG) | [Account overview.JPG](https://commons.wikimedia.org/wiki/File:Account_overview.JPG) |
| 2 | PeopleSoft (десктоп) | ![PeopleSoft logo](https://upload.wikimedia.org/wikipedia/commons/3/36/PeopleSoft_logo.svg) | [PeopleSoft logo.svg](https://commons.wikimedia.org/wiki/File:PeopleSoft_logo.svg) |
| 3 | Dynamics 365 HR (десктоп) | ![Dynamics 365 Business Central](https://upload.wikimedia.org/wikipedia/commons/d/d0/Rozw%C3%B3j_produktu_Microsoft_Dynamics_365_Business_Central.png) | [Rozwój produktu Microsoft Dynamics 365 Business Central.png](https://commons.wikimedia.org/wiki/File:Rozw%C3%B3j_produktu_Microsoft_Dynamics_365_Business_Central.png) |
| 4 | SAP Business One (десктоп) | ![SAP Business One client](https://upload.wikimedia.org/wikipedia/commons/b/b2/SAP_Business_One_Klient.png) | [SAP Business One Klient.png](https://commons.wikimedia.org/wiki/File:SAP_Business_One_Klient.png) |
| 5 | DynaFile (десктоп) | ![DynaFile HR example](https://upload.wikimedia.org/wikipedia/commons/d/dd/DynaFile_Index_Browser_-_Human_Resources_Example.jpg) | [DynaFile Index Browser - Human Resources Example.jpg](https://commons.wikimedia.org/wiki/File:DynaFile_Index_Browser_-_Human_Resources_Example.jpg) |
| 6 | Workday (онлайн) | ![Workday logo](https://upload.wikimedia.org/wikipedia/commons/3/3b/Workday_Logo.png) | [Workday Logo.png](https://commons.wikimedia.org/wiki/File:Workday_Logo.png) |
| 7 | BambooHR (онлайн) | ![BambooHR logo](https://upload.wikimedia.org/wikipedia/commons/d/d7/BambooHR_logo.svg) | [BambooHR logo.svg](https://commons.wikimedia.org/wiki/File:BambooHR_logo.svg) |
| 8 | SAP SuccessFactors (онлайн) | ![SAP web dashboard](https://upload.wikimedia.org/wikipedia/commons/4/4b/Webapplicationdashboartd.png) | [Webapplicationdashboartd.png](https://commons.wikimedia.org/wiki/File:Webapplicationdashboartd.png) |
| 9 | Ethnio (онлайн) | ![Ethnio recruit](https://upload.wikimedia.org/wikipedia/commons/e/eb/Ethnio_recruit_ad.png) | [Ethnio recruit ad.png](https://commons.wikimedia.org/wiki/File:Ethnio_recruit_ad.png) |
| 10 | Betterworks (онлайн) | ![Betterworks OKR](https://upload.wikimedia.org/wikipedia/commons/3/36/Betterworks_overview_guide_OKR_update_screen.png) | [Betterworks overview guide OKR update screen.png](https://commons.wikimedia.org/wiki/File:Betterworks_overview_guide_OKR_update_screen.png) |
| 11 | Битрикс24 коробка (десктоп) | ![Битрикс24](https://upload.wikimedia.org/wikipedia/commons/2/25/Bitrix24_logo.png) | [Bitrix24 logo.png](https://commons.wikimedia.org/wiki/File:Bitrix24_logo.png) |
| 12 | Moodle (десктоп) | ![Moodle 2.0](https://upload.wikimedia.org/wikipedia/commons/3/36/Moodle_2.0_on_Firefox_4.0.png) | [Moodle 2.0 on Firefox 4.0.png](https://commons.wikimedia.org/wiki/File:Moodle_2.0_on_Firefox_4.0.png) |
| 13 | ONLYOFFICE (десктоп) | ![ONLYOFFICE](https://upload.wikimedia.org/wikipedia/commons/c/c3/ONLYOFFICE_logo_%28centered%29.svg) | [ONLYOFFICE logo (centered).svg](https://commons.wikimedia.org/wiki/File:ONLYOFFICE_logo_(centered).svg) |
| 14 | Odoo (десктоп) | ![Odoo 14](https://upload.wikimedia.org/wikipedia/commons/f/f7/Odoo_14.png) | [Odoo 14.png](https://commons.wikimedia.org/wiki/File:Odoo_14.png) |
| 15 | Mahara (десктоп) | ![Mahara dashboard](https://upload.wikimedia.org/wikipedia/commons/d/d2/Mahara_software_dashboard.png) | [Mahara software dashboard.png](https://commons.wikimedia.org/wiki/File:Mahara_software_dashboard.png) |
| 16 | Хантфлоу (онлайн) | ![Хантфлоу](https://huntflow.ru/static/promo-static/landing-2021/src/images/pages/index/og/ru/og.png) | [huntflow.ru](https://huntflow.ru/) |
| 17 | Skillaz (онлайн) | ![Skillaz](https://static.tildacdn.com/tild6630-3364-4562-a264-626461353838/Frame_2085652471.png) | [skillaz.ru](https://skillaz.ru/) |
| 18 | E-Staff (онлайн) | ![E-Staff](https://static.tildacdn.com/tild6335-3636-4437-a139-653461646335/Slide_16_9_-_3.png) | [e-staff.ru](https://e-staff.ru/) |
| 19 | СБИС (онлайн) | ![СБИС](https://saby.ru/resources/SitesCommonExt/SEO/resources/images/preview.png) | [saby.ru](https://saby.ru/) |
| 20 | Мегаплан (онлайн) | ![Мегаплан](https://megaplan.ru/share.png) | [megaplan.ru](https://megaplan.ru/) |
