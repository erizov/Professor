#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate English words to Russian in school.ru.md and univer.ru.md files.
Preserves code blocks, file paths, and technical terms.
"""

import re
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]

# Phrase translations (checked before word translations)
# Order matters - longer phrases first
PHRASE_TRANSLATIONS = {
    'machine learning / ai': 'машинное обучение / AI',
    'machine learning/ai': 'машинное обучение/AI',
    'machine learning': 'машинное обучение',
    'data engineering / data governance': 'инженерия данных / управление данными',
    'data engineering/data governance': 'инженерия данных/управление данными',
    'data engineering': 'инженерия данных',
    'data governance': 'управление данными',
    'computer science': 'информатика',
    'monitoring & security': 'мониторинг и безопасность',
    'monitoring and security': 'мониторинг и безопасность',
    'applying in': 'применение в',
    'application in': 'применение в',
    'in machine learning': 'в машинном обучении',
    'in data engineering': 'в инженерии данных',
    'in computer science': 'в информатике',
}

# Common English to Russian translations
TRANSLATIONS = {
    # Common words
    'algorithm': 'алгоритм',
    'data': 'данные',
    'datum': 'данное',
    'processing': 'обработка',
    'engineering': 'инженерия',
    'governance': 'управление',
    'learning': 'обучение',
    'machine': 'машина',
    'advanced': 'продвинутый',
    'basic': 'базовый',
    'intermediate': 'средний',
    'simple': 'простой',
    'complex': 'сложный',
    'blockchain': 'блокчейн',
    'lecture': 'лекция',
    'downsampling': 'понижающая дискретизация',
    'system': 'система',
    'application': 'приложение',
    'implementation': 'реализация',
    'example': 'пример',
    'task': 'задача',
    'level': 'уровень',
    'basic': 'базовый',
    'advanced': 'продвинутый',
    'intermediate': 'средний',
    'simple': 'простой',
    'complex': 'сложный',
    'method': 'метод',
    'function': 'функция',
    'class': 'класс',
    'object': 'объект',
    'variable': 'переменная',
    'array': 'массив',
    'list': 'список',
    'tree': 'дерево',
    'graph': 'граф',
    'node': 'узел',
    'edge': 'ребро',
    'search': 'поиск',
    'sort': 'сортировка',
    'sorting': 'сортировка',
    'structure': 'структура',
    'database': 'база данных',
    'query': 'запрос',
    'table': 'таблица',
    'field': 'поле',
    'record': 'запись',
    'index': 'индекс',
    'key': 'ключ',
    'value': 'значение',
    'result': 'результат',
    'input': 'вход',
    'output': 'выход',
    'error': 'ошибка',
    'exception': 'исключение',
    'test': 'тест',
    'testing': 'тестирование',
    'performance': 'производительность',
    'optimization': 'оптимизация',
    'complexity': 'сложность',
    'time': 'время',
    'space': 'пространство',
    'memory': 'память',
    'storage': 'хранилище',
    'file': 'файл',
    'folder': 'папка',
    'directory': 'директория',
    'path': 'путь',
    'name': 'имя',
    'type': 'тип',
    'size': 'размер',
    'number': 'число',
    'string': 'строка',
    'character': 'символ',
    'boolean': 'логический',
    'integer': 'целое число',
    'float': 'вещественное число',
    'double': 'двойная точность',
    'operation': 'операция',
    'operator': 'оператор',
    'expression': 'выражение',
    'statement': 'оператор',
    'condition': 'условие',
    'loop': 'цикл',
    'iteration': 'итерация',
    'recursion': 'рекурсия',
    'recursive': 'рекурсивный',
    'iteration': 'итерация',
    'iterative': 'итеративный',
    'step': 'шаг',
    'process': 'процесс',
    'procedure': 'процедура',
    'execution': 'выполнение',
    'runtime': 'время выполнения',
    'compile': 'компиляция',
    'compilation': 'компиляция',
    'source': 'исходный',
    'code': 'код',
    'program': 'программа',
    'programming': 'программирование',
    'language': 'язык',
    'syntax': 'синтаксис',
    'semantic': 'семантический',
    'compiler': 'компилятор',
    'interpreter': 'интерпретатор',
    'debug': 'отладка',
    'debugging': 'отладка',
    'bug': 'ошибка',
    'feature': 'функциональность',
    'requirement': 'требование',
    'specification': 'спецификация',
    'documentation': 'документация',
    'comment': 'комментарий',
    'description': 'описание',
    'definition': 'определение',
    'explanation': 'объяснение',
    'instruction': 'инструкция',
    'guide': 'руководство',
    'tutorial': 'учебник',
    'manual': 'руководство',
    'reference': 'справочник',
    'example': 'пример',
    'sample': 'образец',
    'case': 'случай',
    'scenario': 'сценарий',
    'use case': 'вариант использования',
    'pattern': 'шаблон',
    'design': 'дизайн',
    'architecture': 'архитектура',
    'framework': 'фреймворк',
    'library': 'библиотека',
    'module': 'модуль',
    'package': 'пакет',
    'component': 'компонент',
    'interface': 'интерфейс',
    'api': 'API',
    'service': 'сервис',
    'server': 'сервер',
    'client': 'клиент',
    'request': 'запрос',
    'response': 'ответ',
    'protocol': 'протокол',
    'network': 'сеть',
    'connection': 'соединение',
    'session': 'сессия',
    'user': 'пользователь',
    'account': 'аккаунт',
    'login': 'вход',
    'logout': 'выход',
    'password': 'пароль',
    'security': 'безопасность',
    'authentication': 'аутентификация',
    'authorization': 'авторизация',
    'encryption': 'шифрование',
    'decryption': 'расшифровка',
    'hash': 'хеш',
    'hash function': 'хеш-функция',
    'cryptography': 'криптография',
    'cryptographic': 'криптографический',
    'key': 'ключ',
    'public key': 'открытый ключ',
    'private key': 'закрытый ключ',
    'signature': 'подпись',
    'certificate': 'сертификат',
    'ssl': 'SSL',
    'tls': 'TLS',
    'https': 'HTTPS',
    'http': 'HTTP',
    'url': 'URL',
    'uri': 'URI',
    'domain': 'домен',
    'ip address': 'IP-адрес',
    'port': 'порт',
    'socket': 'сокет',
    'tcp': 'TCP',
    'udp': 'UDP',
    'dns': 'DNS',
    'email': 'электронная почта',
    'message': 'сообщение',
    'notification': 'уведомление',
    'alert': 'предупреждение',
    'warning': 'предупреждение',
    'error': 'ошибка',
    'exception': 'исключение',
    'failure': 'сбой',
    'success': 'успех',
    'status': 'статус',
    'state': 'состояние',
    'event': 'событие',
    'action': 'действие',
    'activity': 'активность',
    'operation': 'операция',
    'transaction': 'транзакция',
    'commit': 'фиксация',
    'rollback': 'откат',
    'abort': 'прервать',
    'cancel': 'отменить',
    'confirm': 'подтвердить',
    'approve': 'одобрить',
    'reject': 'отклонить',
    'accept': 'принять',
    'decline': 'отклонить',
    'submit': 'отправить',
    'send': 'отправить',
    'receive': 'получить',
    'download': 'загрузить',
    'upload': 'загрузить',
    'save': 'сохранить',
    'load': 'загрузить',
    'open': 'открыть',
    'close': 'закрыть',
    'read': 'читать',
    'write': 'писать',
    'create': 'создать',
    'delete': 'удалить',
    'remove': 'удалить',
    'update': 'обновить',
    'modify': 'изменить',
    'change': 'изменить',
    'edit': 'редактировать',
    'add': 'добавить',
    'insert': 'вставить',
    'append': 'добавить',
    'prepend': 'добавить в начало',
    'replace': 'заменить',
    'merge': 'объединить',
    'split': 'разделить',
    'join': 'объединить',
    'combine': 'объединить',
    'separate': 'разделить',
    'divide': 'разделить',
    'multiply': 'умножить',
    'add': 'добавить',
    'subtract': 'вычесть',
    'increment': 'увеличить',
    'decrement': 'уменьшить',
    'increase': 'увеличить',
    'decrease': 'уменьшить',
    'expand': 'расширить',
    'collapse': 'свернуть',
    'show': 'показать',
    'hide': 'скрыть',
    'display': 'отобразить',
    'render': 'отобразить',
    'print': 'печатать',
    'output': 'вывод',
    'input': 'ввод',
    'enter': 'ввести',
    'exit': 'выход',
    'quit': 'выйти',
    'stop': 'остановить',
    'start': 'начать',
    'begin': 'начать',
    'end': 'конец',
    'finish': 'закончить',
    'complete': 'завершить',
    'pause': 'пауза',
    'resume': 'возобновить',
    'continue': 'продолжить',
    'break': 'прервать',
    'return': 'вернуть',
    'yield': 'вернуть',
    'throw': 'бросить',
    'catch': 'поймать',
    'handle': 'обработать',
    'process': 'обработать',
    'execute': 'выполнить',
    'run': 'запустить',
    'launch': 'запустить',
    'invoke': 'вызвать',
    'call': 'вызвать',
    'invoke': 'вызвать',
    'trigger': 'запустить',
    'activate': 'активировать',
    'deactivate': 'деактивировать',
    'enable': 'включить',
    'disable': 'выключить',
    'turn on': 'включить',
    'turn off': 'выключить',
    'switch': 'переключить',
    'toggle': 'переключить',
    'select': 'выбрать',
    'choose': 'выбрать',
    'pick': 'выбрать',
    'option': 'опция',
    'choice': 'выбор',
    'menu': 'меню',
    'item': 'элемент',
    'entry': 'запись',
    'button': 'кнопка',
    'link': 'ссылка',
    'image': 'изображение',
    'picture': 'картинка',
    'photo': 'фото',
    'video': 'видео',
    'audio': 'аудио',
    'sound': 'звук',
    'music': 'музыка',
    'text': 'текст',
    'font': 'шрифт',
    'style': 'стиль',
    'format': 'формат',
    'color': 'цвет',
    'background': 'фон',
    'foreground': 'передний план',
    'border': 'граница',
    'margin': 'отступ',
    'padding': 'отступ',
    'width': 'ширина',
    'height': 'высота',
    'size': 'размер',
    'position': 'позиция',
    'location': 'местоположение',
    'coordinate': 'координата',
    'x': 'x',
    'y': 'y',
    'z': 'z',
    'axis': 'ось',
    'point': 'точка',
    'line': 'линия',
    'curve': 'кривая',
    'surface': 'поверхность',
    'plane': 'плоскость',
    'angle': 'угол',
    'degree': 'градус',
    'radian': 'радиан',
    'distance': 'расстояние',
    'length': 'длина',
    'area': 'площадь',
    'volume': 'объем',
    'speed': 'скорость',
    'velocity': 'скорость',
    'acceleration': 'ускорение',
    'force': 'сила',
    'energy': 'энергия',
    'power': 'мощность',
    'pressure': 'давление',
    'temperature': 'температура',
    'heat': 'тепло',
    'cold': 'холод',
    'light': 'свет',
    'dark': 'темнота',
    'bright': 'яркий',
    'dim': 'тусклый',
    'color': 'цвет',
    'red': 'красный',
    'green': 'зеленый',
    'blue': 'синий',
    'yellow': 'желтый',
    'orange': 'оранжевый',
    'purple': 'фиолетовый',
    'pink': 'розовый',
    'brown': 'коричневый',
    'black': 'черный',
    'white': 'белый',
    'gray': 'серый',
    'grey': 'серый',
    'silver': 'серебряный',
    'gold': 'золотой',
    'transparent': 'прозрачный',
    'opaque': 'непрозрачный',
    'visible': 'видимый',
    'invisible': 'невидимый',
    'hidden': 'скрытый',
    'shown': 'показанный',
    'displayed': 'отображаемый',
    'rendered': 'отображаемый',
    'drawn': 'нарисованный',
    'painted': 'нарисованный',
    'printed': 'напечатанный',
    'scanned': 'отсканированный',
    'copied': 'скопированный',
    'pasted': 'вставленный',
    'cut': 'вырезанный',
    'selected': 'выбранный',
    'highlighted': 'выделенный',
    'focused': 'в фокусе',
    'blurred': 'размытый',
    'sharp': 'резкий',
    'smooth': 'гладкий',
    'rough': 'шероховатый',
    'soft': 'мягкий',
    'hard': 'жесткий',
    'flexible': 'гибкий',
    'rigid': 'жесткий',
    'elastic': 'эластичный',
    'plastic': 'пластичный',
    'solid': 'твердый',
    'liquid': 'жидкий',
    'gas': 'газ',
    'plasma': 'плазма',
    'matter': 'материя',
    'substance': 'вещество',
    'material': 'материал',
    'element': 'элемент',
    'compound': 'соединение',
    'mixture': 'смесь',
    'solution': 'раствор',
    'suspension': 'суспензия',
    'colloid': 'коллоид',
    'emulsion': 'эмульсия',
    'foam': 'пена',
    'gel': 'гель',
    'paste': 'паста',
    'powder': 'порошок',
    'crystal': 'кристалл',
    'mineral': 'минерал',
    'rock': 'камень',
    'stone': 'камень',
    'metal': 'металл',
    'alloy': 'сплав',
    'steel': 'сталь',
    'iron': 'железо',
    'copper': 'медь',
    'bronze': 'бронза',
    'brass': 'латунь',
    'aluminum': 'алюминий',
    'aluminium': 'алюминий',
    'gold': 'золото',
    'silver': 'серебро',
    'platinum': 'платина',
    'titanium': 'титан',
    'tungsten': 'вольфрам',
    'uranium': 'уран',
    'plutonium': 'плутоний',
    'hydrogen': 'водород',
    'helium': 'гелий',
    'lithium': 'литий',
    'beryllium': 'бериллий',
    'boron': 'бор',
    'carbon': 'углерод',
    'nitrogen': 'азот',
    'oxygen': 'кислород',
    'fluorine': 'фтор',
    'neon': 'неон',
    'sodium': 'натрий',
    'magnesium': 'магний',
    'aluminum': 'алюминий',
    'silicon': 'кремний',
    'phosphorus': 'фосфор',
    'sulfur': 'сера',
    'chlorine': 'хлор',
    'argon': 'аргон',
    'potassium': 'калий',
    'calcium': 'кальций',
    'scandium': 'скандий',
    'titanium': 'титан',
    'vanadium': 'ванадий',
    'chromium': 'хром',
    'manganese': 'марганец',
    'iron': 'железо',
    'cobalt': 'кобальт',
    'nickel': 'никель',
    'copper': 'медь',
    'zinc': 'цинк',
    'gallium': 'галлий',
    'germanium': 'германий',
    'arsenic': 'мышьяк',
    'selenium': 'селен',
    'bromine': 'бром',
    'krypton': 'криптон',
    'rubidium': 'рубидий',
    'strontium': 'стронций',
    'yttrium': 'иттрий',
    'zirconium': 'цирконий',
    'niobium': 'ниобий',
    'molybdenum': 'молибден',
    'technetium': 'технеций',
    'ruthenium': 'рутений',
    'rhodium': 'родий',
    'palladium': 'палладий',
    'silver': 'серебро',
    'cadmium': 'кадмий',
    'indium': 'индий',
    'tin': 'олово',
    'antimony': 'сурьма',
    'tellurium': 'теллур',
    'iodine': 'йод',
    'xenon': 'ксенон',
    'cesium': 'цезий',
    'barium': 'барий',
    'lanthanum': 'лантан',
    'cerium': 'церий',
    'praseodymium': 'празеодим',
    'neodymium': 'неодим',
    'promethium': 'прометий',
    'samarium': 'самарий',
    'europium': 'европий',
    'gadolinium': 'гадолиний',
    'terbium': 'тербий',
    'dysprosium': 'диспрозий',
    'holmium': 'гольмий',
    'erbium': 'эрбий',
    'thulium': 'тулий',
    'ytterbium': 'иттербий',
    'lutetium': 'лютеций',
    'hafnium': 'гафний',
    'tantalum': 'тантал',
    'tungsten': 'вольфрам',
    'rhenium': 'рений',
    'osmium': 'осмий',
    'iridium': 'иридий',
    'platinum': 'платина',
    'gold': 'золото',
    'mercury': 'ртуть',
    'thallium': 'таллий',
    'lead': 'свинец',
    'bismuth': 'висмут',
    'polonium': 'полоний',
    'astatine': 'астат',
    'radon': 'радон',
    'francium': 'франций',
    'radium': 'радий',
    'actinium': 'актиний',
    'thorium': 'торий',
    'protactinium': 'протактиний',
    'uranium': 'уран',
    'neptunium': 'нептуний',
    'plutonium': 'плутоний',
    'americium': 'америций',
    'curium': 'кюрий',
    'berkelium': 'берклий',
    'californium': 'калифорний',
    'einsteinium': 'эйнштейний',
    'fermium': 'фермий',
    'mendelevium': 'менделевий',
    'nobelium': 'нобелий',
    'lawrencium': 'лоуренсий',
    'rutherfordium': 'резерфордий',
    'dubnium': 'дубний',
    'seaborgium': 'сиборгий',
    'bohrium': 'борий',
    'hassium': 'хассий',
    'meitnerium': 'майтнерий',
    'darmstadtium': 'дармштадтий',
    'roentgenium': 'рентгений',
    'copernicium': 'коперниций',
    'nihonium': 'нихоний',
    'flerovium': 'флеровий',
    'moscovium': 'московий',
    'livermorium': 'ливерморий',
    'tennessine': 'теннессин',
    'oganesson': 'оганесон',
}

# Technical terms that should NOT be translated (commonly used in Russian as-is)
PRESERVE_TERMS = {
    'API', 'URL', 'URI', 'HTTP', 'HTTPS', 'SSL', 'TLS', 'TCP', 'UDP', 'DNS',
    'HTML', 'CSS', 'JavaScript', 'JSON', 'XML', 'YAML', 'CSV', 'TSV',
    'SQL', 'NoSQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
    'REST', 'SOAP', 'GraphQL', 'gRPC',
    'OAuth', 'JWT', 'JWT', 'RSA', 'AES', 'SHA', 'MD5',
    'CPU', 'GPU', 'RAM', 'ROM', 'SSD', 'HDD',
    'IDE', 'SDK', 'CLI', 'GUI', 'UI', 'UX',
    'AWS', 'Azure', 'GCP', 'S3', 'EC2', 'Lambda',
    'Docker', 'Kubernetes', 'K8s',
    'Git', 'GitHub', 'GitLab', 'Bitbucket',
    'Linux', 'Windows', 'macOS', 'Unix',
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
    'React', 'Vue', 'Angular', 'Node.js',
    'NumPy', 'Pandas', 'TensorFlow', 'PyTorch', 'Scikit-learn',
    'Apache', 'Spark', 'Kafka', 'Hadoop', 'Hive', 'Pig',
    'Prometheus', 'Grafana', 'Elasticsearch', 'Kibana',
    'Nginx', 'Apache', 'IIS',
    'MySQL', 'PostgreSQL', 'Oracle', 'SQLite',
    'MongoDB', 'Cassandra', 'CouchDB', 'Neo4j',
    'Redis', 'Memcached',
    'RabbitMQ', 'ActiveMQ', 'Kafka',
    'Jenkins', 'Travis', 'CircleCI', 'GitLab CI', 'GitHub Actions',
    'Ansible', 'Terraform', 'Chef', 'Puppet',
    'Vagrant', 'VirtualBox', 'VMware',
    'Jira', 'Confluence', 'Slack', 'Teams',
    'SaaS', 'PaaS', 'IaaS', 'FaaS',
    'CI/CD', 'DevOps', 'Agile', 'Scrum', 'Kanban',
    'MVP', 'API', 'SDK', 'IDE',
    'REST', 'SOAP', 'GraphQL',
    'OAuth', 'JWT', 'RSA', 'AES',
    'CPU', 'GPU', 'RAM', 'SSD',
    'HTML', 'CSS', 'JS', 'JSON',
    'XML', 'YAML', 'CSV',
    'SQL', 'NoSQL',
    'HTTP', 'HTTPS', 'FTP', 'SFTP',
    'TCP', 'UDP', 'IP', 'DNS',
    'SSL', 'TLS',
    'AWS', 'S3', 'EC2', 'Lambda',
    'Docker', 'K8s', 'Kubernetes',
    'Git', 'GitHub',
    'Linux', 'Windows', 'macOS',
    'Python', 'Java', 'JS', 'C++', 'C#',
    'React', 'Vue', 'Angular',
    'NumPy', 'Pandas', 'TF', 'PyTorch',
    'Apache', 'Spark', 'Kafka',
    'Prometheus', 'Grafana',
    'Nginx', 'MySQL', 'PostgreSQL',
    'MongoDB', 'Redis',
    'Jenkins', 'Ansible',
    'Jira', 'Slack',
    'SaaS', 'PaaS', 'IaaS',
    'CI/CD', 'DevOps',
    'MVP', 'API', 'SDK',
    'REST', 'OAuth', 'JWT',
    'CPU', 'GPU', 'RAM',
    'HTML', 'CSS', 'JSON',
    'SQL', 'HTTP', 'HTTPS',
    'TCP', 'IP', 'DNS',
    'AWS', 'Docker',
    'Git', 'Linux',
    'Python', 'Java',
    'React', 'NumPy',
    'Apache', 'Kafka',
    'MySQL', 'MongoDB',
    'Jenkins', 'Jira',
    'DevOps', 'API',
}


def should_preserve_word(word: str) -> bool:
    """Check if a word should be preserved (not translated)."""
    # Preserve if it's a technical term
    if word.upper() in PRESERVE_TERMS:
        return True
    
    # Preserve if it contains numbers or special characters (likely code/identifier)
    if re.search(r'[0-9_\-\.]', word):
        return True
    
    # Preserve if it's all uppercase (likely constant/identifier)
    if word.isupper() and len(word) > 1:
        return True
    
    # Preserve if it's a file extension
    if word.startswith('.') and len(word) > 1:
        return True
    
    return False


def translate_text(text: str) -> str:
    """Translate English words to Russian in text, preserving code blocks and technical terms."""
    # Split into lines to process separately
    lines = text.split('\n')
    translated_lines = []
    
    in_code_block = False
    code_block_language = ''
    
    for line in lines:
        # Check if we're entering/exiting a code block
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                # Extract language if present
                code_block_language = line.strip()[3:].strip()
            translated_lines.append(line)
            continue
        
        # Don't translate code blocks
        if in_code_block:
            translated_lines.append(line)
            continue
        
        # Don't translate lines that are clearly code (start with certain patterns)
        if re.match(r'^\s*[#\$@<>\[\]{}()]', line):
            translated_lines.append(line)
            continue
        
        # Translate the line
        translated_line = translate_line(line)
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)


def translate_line(line: str) -> str:
    """Translate English words in a single line."""
    translated = line
    
    # First, translate phrases (case-insensitive, order by length descending)
    # Sort by length descending to match longer phrases first
    sorted_phrases = sorted(PHRASE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for phrase_en, phrase_ru in sorted_phrases:
        # Create case-insensitive regex with flexible whitespace
        # Split phrase into words, handling slashes
        if '/' in phrase_en:
            # Handle phrases with slashes: "machine learning / ai"
            parts = phrase_en.split('/')
            left_part = parts[0].strip()
            right_part = parts[1].strip() if len(parts) > 1 else ''
            
            # Build pattern for left part (with flexible spaces)
            left_words = left_part.split()
            left_pattern = r'\s+'.join([re.escape(w) for w in left_words])
            
            if right_part:
                # Build pattern for right part
                right_words = right_part.split()
                right_pattern = r'\s+'.join([re.escape(w) for w in right_words])
                # Full pattern: left \s* / \s* right
                pattern_str = left_pattern + r'\s*/\s*' + right_pattern
            else:
                pattern_str = left_pattern
        else:
            # Handle phrases without slashes
            words = phrase_en.split()
            pattern_str = r'\s+'.join([re.escape(w) for w in words])
        
        pattern = re.compile(pattern_str, re.IGNORECASE)
        
        def replace_phrase(match):
            matched = match.group(0)
            # Preserve original case pattern
            if matched.isupper():
                return phrase_ru.upper()
            elif matched[0].isupper() and len(matched) > 1 and matched[1].isupper():
                # Title case (first two letters uppercase)
                return phrase_ru.title()
            elif matched[0].isupper():
                return phrase_ru.capitalize()
            else:
                return phrase_ru
        
        # Try to replace, but only if we find a match
        new_translated = pattern.sub(replace_phrase, translated)
        if new_translated != translated:
            translated = new_translated
    
    # Then, translate individual words
    def replace_word(match):
        word = match.group(0)
        
        # Check if we should preserve this word
        if should_preserve_word(word):
            return word
        
        # Try to find translation (case-insensitive)
        word_lower = word.lower()
        if word_lower in TRANSLATIONS:
            translation = TRANSLATIONS[word_lower]
            # Preserve original case
            if word[0].isupper():
                translation = translation.capitalize()
            if word.isupper():
                translation = translation.upper()
            return translation
        else:
            # No translation found, keep original
            return word
    
    # Replace words using word boundaries, preserving all non-word characters and spaces
    translated = re.sub(r'\b\w+\b', replace_word, translated)
    return translated


def fix_file(file_path: Path) -> bool:
    """Translate English words to Russian in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Translate
        content = translate_text(content)
        
        # Only write if changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] Failed to translate {file_path}: {e}")
        return False


def main():
    """Main function to translate all MD files."""
    print("=" * 70)
    print("ПЕРЕВОД АНГЛИЙСКИХ СЛОВ НА РУССКИЙ В MD ФАЙЛАХ")
    print("=" * 70)
    print()
    
    # Find all school.ru.md and univer.ru.md files
    school_files = list(ROOT.rglob("school.ru.md"))
    univer_files = list(ROOT.rglob("univer.ru.md"))
    all_files = school_files + univer_files
    all_files.sort()
    
    print(f"Найдено файлов:")
    print(f"  school.ru.md: {len(school_files)}")
    print(f"  univer.ru.md: {len(univer_files)}")
    print(f"  Всего: {len(all_files)}")
    print()
    
    translated_count = 0
    error_count = 0
    
    for idx, file_path in enumerate(all_files, 1):
        relative_path = file_path.relative_to(ROOT)
        print(f"[{idx}/{len(all_files)}] {relative_path}")
        
        if fix_file(file_path):
            print(f"  [OK] Переведено")
            translated_count += 1
        else:
            print(f"  [OK] Без изменений")
        
        if idx % 100 == 0:
            print(f"\nПрогресс: {idx}/{len(all_files)} обработано\n")
    
    print()
    print("=" * 70)
    print(f"Итоги:")
    print(f"  Всего файлов: {len(all_files)}")
    print(f"  Переведено: {translated_count}")
    print(f"  Без изменений: {len(all_files) - translated_count}")
    print(f"  Ошибок: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

