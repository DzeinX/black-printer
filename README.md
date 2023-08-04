## [1.1.2] - 2023-05-06
### Особенности запуска:
- <h3> Первый запуск:</h3>
- - Создать <i>venv</i>;
- - Установить зависимости из <i>requirements.txt</i>;
- - Изменить в файле <i>migrations/versions/50609ad96891_удаление_колонки_dn_в_user.py</i> 14 строку с <i>(down_revision = None)</i> на <i>(down_revision = 'f6f0c3fafff6')</i>;
- - Запустить миграции командой <i>flask db upgrade f6f0c3fafff6@head</i> в терминале;
- - Всё сохранить и можно запускать;
 

- <h3>Запуск с готовой БД:</h3>
- - Создать <i>venv</i>;
- - Установить зависимости из <i>requirements.txt</i>;
- - Проверить, что в файле <i>migrations/versions/50609ad96891_удаление_колонки_dn_в_user.py</i> в 14 строке стоит <i>(down_revision = None)</i>;
- - Запустить миграции командой <i>flask db upgrade 50609ad96891@head</i> в терминале;
- - Всё сохранить и можно запускать;
