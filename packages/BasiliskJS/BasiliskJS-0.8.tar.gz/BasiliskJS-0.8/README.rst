
BasiliskJS - Scriptable Headless WebKit
=========================

`BasiliskJS <https://pypi.python.org/pypi/BasiliskJS>`_ Представляет собой WebKit для python, основан на `PhantomJS <http://phantomjs.org>`_ .

Возможность
============

- **Быстрое тестирование**. Возможность быстрого тестирования без браузера!
- **Автоматизация dom**. Простой интерфейс.
- **Работа с js**. Есть возможность выполнять JavaScript, парсинг динамических страниц.
- **Захват экрана**. Возможность сделать снимок страницы любого размера.


Пример работы
-------------
Простой get запрос на https://github.com/lich666dead/BasiliskJS.

.. code-block:: python

    >>> from basilisk import PhantomJS
    >>> PhantomJS().get("https://github.com/lich666dead/BasiliskJS")
    {'status': 'success', 'urls': ['https://github.com/lich666dead/BasiliskJS']}

Простой post запрос на https://github.com/lich666dead/BasiliskJS.

.. code-block:: python

    >>> from basilisk import PhantomJS
    >>> PhantomJS().post("https://github.com/lich666dead/BasiliskJS", {'post_data': 'post_data'})
    {'status': 'success', 'urls': ['https://github.com/lich666dead/BasiliskJS']}

Запрос с выполнением js.

.. code-block:: python

    from basilisk import PhantomJS

    js = '''
    var temp = {};
    for (var i = 0; i != document.getElementsByClassName('nav-item-name').length; i++) {
        temp[i] = document.getElementsByClassName('nav-item-name')[i].innerText;
     }
     return temp;
     '''
     bs = PhantomJS()

     bs.evaluate(js)

     print(bs.get("http://phantomjs.org/documentation/"))

     result = {
     'status': 'success',
     'js': {
          '0': 'Download', '1': 'Build',
          '2': 'Releases', '3': 'Release Names',
          '4': 'REPL', '5': 'Quick Start',
          '6': 'Headless Testing', '7': 'Screen Capture',
          '8': 'Network Monitoring', '9': 'Page Automation',
          '10': 'Inter Process Communication', '11': 'Command Line Interface',
          '12': 'Troubleshooting', '13': 'FAQ',
          '14': 'Examples', '15': 'Best Practices',
          '16': 'Tips and Tricks', '17': 'Supported Web Standards',
          '18': 'Buzz', '19': "Who's using PhantomJS?",
          '20': 'Related Projects', '21': 'Contributing',
          '22': 'Source Code', '23': 'Test Suite',
          '24': 'Release Preparation', '25': 'Crash Reporting',
          '26': 'Bug Reporting'
          },
     'urls': ['http://phantomjs.org/documentation/']
     }


Метод include_js позволяет ипортировать любую js библиотеку.

.. code-block:: python


    from basilisk import PhantomJS

    js = '''
    var $loginForm = $('form#login');
    $loginForm.find('input[name="username"]').value('phantomjs');
    $loginForm.find('input[name="password"]').value('c45p3r');'''

    bs = PhantomJS()

    bs.include_js("https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js")

    bs.evaluate(js)

    bs.get("http://phantomjs.org/documentation/")


Показать html контент:

.. code-block:: python


    >>> from basilisk import PhantomJS
    >>> PhantomJS(content=True).get('http://phantomjs.org/')


Событие закрытие браузер зависит от параметра (conversion). Это количество переходов по ссылки.
Теперь можно переходить по ссылкам, этим параметром нужно пользоваться осторожно,
иначе можно вызвать зацикливание.
Пример работы с параметром:

.. code-block:: python


    from basilisk import PhantomJS

    js = '''
    document.getElementById('projectUrl1').value = 'phantomjs.org';
    document.getElementById('button1').click();'''

    bs = PhantomJS(conversion=2)

    bs.evaluate(js)

    print(bs.get("https://altrumseo.ru/"))

    result = {'status': 'success', 'js': None, 'urls': ['https://altrumseo.ru/', 'https://altrumseo.ru/analitics/']}

Как видно у нас в масиве 2 url, закрытие браузер работает на
событие, зависищие от параметра (conversion).
Например если параметра conversion=3, то выполнение просто не зациклится!

Параметры инициализатора:
-------------    
- **url**. - url для get запроса.
- **content**. - Паказать content, по умолчанию( False ).
- **image_size**. - Размер изоброжения по умолчанию( {'width': 1920, 'height': 1080} ).
- **add_cookie**. - Дает возможность изменить cookie.
- **screenshot**. - Сделать скриншот, по умолчанию( False ).
- **image_name**. - Путь, название выходного изображения.
- **get_cookies**. - Получить cookies, по умолчанию( False ).
- **user_agent**. - Изменить user-agent.
- **load_images**. - Загрузка изображений на странице, по умолчанию( False ).
- **command**. - Параметр отвечает за путь к браузеру phantomjs.
- **conversion**. - Количество переходов на странице.


Развитие
-------------   
На данный момент я на стадии Pre-Alpha. Вы можете увидеть сообщения об ошибках и т.д.
    