#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace placeholders in MD files with real content from Wikipedia.
Processes all 4 MD files: school.en.md, school.ru.md, univer.en.md, univer.ru.md
"""

import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, List, Optional
import requests

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

ROOT = Path(__file__).resolve().parents[1]

# Rate limiting
LAST_REQUEST_TIME = 0
REQUEST_DELAY = 0.5  # seconds between requests

CATEGORY_KEYWORDS = {
    "sorting": [
        "sort",
        "сорт",
        "radix",
        "heap",
        "merge",
        "quick",
        "bucket",
        "counting",
        "shell",
    ],
    "search": ["search", "поиск", "binary", "linear", "lookup"],
    "graph": [
        "graph",
        "network",
        "граф",
        "shortest path",
        "mst",
        "spanning",
    ],
    "tree": ["tree", "дерев", "bst", "avl", "trie"],
    "string": ["string", "suffix", "prefix", "pattern", "строк"],
    "hashing": ["hash", "хеш", "hashing"],
    "data_structure": ["queue", "stack", "deque", "list"],
    "dynamic_programming": ["dynamic programming", "dp", "subsequence", "knapsack"],
    "machine_learning": [
        "regression",
        "classification",
        "learning",
        "model",
        "ml",
    ],
    "deep_learning": [
        "neural",
        "transformer",
        "llm",
        "attention",
        "network",
        "cnn",
    ],
    "data_engineering": [
        "pipeline",
        "etl",
        "data ops",
        "data engineering",
        "stream processing",
        "batch processing",
    ],
    "database": ["database", "sql", "query", "schema", "relational"],
    "nosql": ["nosql", "document", "key-value", "column", "graph database"],
    "observability": [
        "monitoring",
        "observability",
        "telemetry",
        "metrics",
        "logging",
    ],
    "blockchain": ["blockchain", "smart contract", "ledger", "crypto"],
    "ci_cd": ["ci/cd", "deployment", "devops", "feature flag", "automation"],
    "documentation": ["documentation", "doc", "writing", "knowledge base"],
    "support_ops": ["support", "incident", "ticket", "sla"],
    "knowledge": ["community", "knowledge", "sharing", "portal"],
    "security": ["security", "encryption", "access", "compliance", "privacy"],
    "os": ["kernel", "memory", "scheduling", "process"],
    "parallel": ["parallel", "distributed", "gpu", "multithread"],
    "time_series": ["time series", "forecast", "temporal"],
    "graph_db": ["graph database", "neo4j"],
    "mlops": ["mlops", "model monitoring", "feature store", "model serving"],
    "data_platforms": ["data platform", "lakehouse", "data mesh", "data hub"],
    "general": [],
}

CATEGORY_USE_CASES = {
    "sorting": {
        "en": [
            "{name} orders large batches of identifiers before range queries.",
            "Data engineers run {name} on telemetry dumps to normalize values.",
            "{name} prepares keys for radix-friendly compression pipelines.",
        ],
        "ru": [
            "{name} упорядочивает большие списки идентификаторов перед "
            "диапазонными запросами.",
            "Инженеры данных запускают {name} на телеметрии для нормализации "
            "значений.",
            "{name} готовит ключи к компрессии, зависящей от цифр.",
        ],
    },
    "search": {
        "en": [
            "{name} powers lookups inside low-latency routing tables.",
            "Indexing services use {name} for repeatedly locating boundaries.",
            "{name} accelerates discovery across telemetry snapshots.",
        ],
        "ru": [
            "{name} обслуживает быстрые поиски в таблицах маршрутизации.",
            "Службы индексации применяют {name} для точного нахождения "
            "границ.",
            "{name} ускоряет поиск по слепкам телеметрии.",
        ],
    },
    "graph": {
        "en": [
            "{name} evaluates routes inside transportation and telecom graphs.",
            "Fraud systems map relationships between accounts with {name}.",
            "{name} optimizes dependency graphs in build pipelines.",
        ],
        "ru": [
            "{name} оценивает маршруты в транспортных и телеком-графах.",
            "Антифрод-системы выявляют связи между счетами с помощью {name}.",
            "{name} оптимизирует графы зависимостей в сборочных конвейерах.",
        ],
    },
    "tree": {
        "en": [
            "{name} keeps hierarchical indexes balanced for OLTP workloads.",
            "Compilers rely on {name} to manage syntax or prefix trees.",
            "{name} accelerates autocomplete dictionaries.",
        ],
        "ru": [
            "{name} балансирует иерархические индексы для OLTP-нагрузок.",
            "Компиляторы используют {name} для управления синтаксическими "
            "деревьями.",
            "{name} ускоряет словари автодополнения.",
        ],
    },
    "string": {
        "en": [
            "{name} searches DNA or log signatures at scale.",
            "Security pipelines scan payloads via {name}.",
            "{name} validates large corpora of text identifiers.",
        ],
        "ru": [
            "{name} ищет шаблоны ДНК или сигнатуры логов на больших объемах.",
            "Системы безопасности сканируют полезные данные с помощью {name}.",
            "{name} проверяет массивы текстовых идентификаторов.",
        ],
    },
    "hashing": {
        "en": [
            "{name} drives deduplication inside storage engines.",
            "Caches rely on {name} to evenly spread keys.",
            "{name} validates integrity of streamed payloads.",
        ],
        "ru": [
            "{name} выполняет дедупликацию в движках хранения.",
            "Кэши используют {name} для равномерного распределения ключей.",
            "{name} проверяет целостность потоковых данных.",
        ],
    },
    "data_structure": {
        "en": [
            "{name} manages scheduling queues inside operating systems.",
            "Stream processors buffer events using {name}.",
            "{name} underpins undo/redo histories in editors.",
        ],
        "ru": [
            "{name} управляет очередями планировщика в ОС.",
            "Стримовые процессоры буферизуют события с помощью {name}.",
            "{name} лежит в основе историй undo/redo.",
        ],
    },
    "dynamic_programming": {
        "en": [
            "{name} optimizes allocation problems in logistics.",
            "Bioinformatics pipelines compare sequences via {name}.",
            "{name} evaluates revenue trade-offs in planning systems.",
        ],
        "ru": [
            "{name} оптимизирует задачи распределения в логистике.",
            "Биоинформатика сравнивает последовательности через {name}.",
            "{name} оценивает компромиссы доходов в планировании.",
        ],
    },
    "machine_learning": {
        "en": [
            "Data scientists fit predictive models with {name}.",
            "{name} powers scoring services that personalize UX.",
            "Analytics teams run {name} during experimentation pipelines.",
        ],
        "ru": [
            "Дата-сайентисты обучают предсказательные модели через {name}.",
            "{name} работает в скоринговых сервисах персонализации.",
            "Аналитики используют {name} в экспериментальных конвейерах.",
        ],
    },
    "deep_learning": {
        "en": [
            "{name} recognizes patterns in images, audio, or language.",
            "LLM pipelines fine-tune responses using {name}.",
            "{name} processes high-dimensional telemetry streams.",
        ],
        "ru": [
            "{name} распознает шаблоны в изображениях, аудио или тексте.",
            "LLM-конвейеры дообучают ответы с помощью {name}.",
            "{name} обрабатывает многомерные телеметрические потоки.",
        ],
    },
    "data_engineering": {
        "en": [
            "{name} enforces quality gates in data warehouses.",
            "Real-time buses embed {name} to keep pipelines reliable.",
            "{name} feeds observability dashboards for datasets.",
        ],
        "ru": [
            "{name} реализует контроль качества в витринах данных.",
            "Стриминговые шины встраивают {name} для надежности конвейеров.",
            "{name} наполняет панели наблюдаемости по данным.",
        ],
    },
    "database": {
        "en": [
            "{name} optimizes query planners in relational engines.",
            "Migration teams rely on {name} when reshaping schemas.",
            "{name} protects transactional integrity under load.",
        ],
        "ru": [
            "{name} оптимизирует планировщики запросов в СУБД.",
            "Команды миграции используют {name} при изменении схем.",
            "{name} сохраняет транзакционную целостность под нагрузкой.",
        ],
    },
    "nosql": {
        "en": [
            "{name} scales document clusters during traffic spikes.",
            "Graph services expose relationships via {name}.",
            "{name} keeps key-value stores consistent across regions.",
        ],
        "ru": [
            "{name} масштабирует документные кластеры при всплесках трафика.",
            "Графовые сервисы раскрывают связи благодаря {name}.",
            "{name} поддерживает согласованность key-value хранилищ.",
        ],
    },
    "observability": {
        "en": [
            "{name} aggregates metrics before alert evaluation.",
            "SRE teams inspect anomalies with {name}.",
            "{name} links logs, traces, and events into single view.",
        ],
        "ru": [
            "{name} агрегирует метрики перед оценкой алертов.",
            "SRE-команды исследуют аномалии через {name}.",
            "{name} связывает логи, трассировки и события.",
        ],
    },
    "blockchain": {
        "en": [
            "{name} secures ledgers across decentralized peers.",
            "Chain analytics highlight suspicious wallets via {name}.",
            "{name} streamlines smart-contract execution.",
        ],
        "ru": [
            "{name} защищает реестры между децентрализованными узлами.",
            "Аналитика блокчейна выявляет подозрительные кошельки с "
            "помощью {name}.",
            "{name} ускоряет выполнение смарт-контрактов.",
        ],
    },
    "ci_cd": {
        "en": [
            "{name} orchestrates rollouts across clusters.",
            "Release engineers gate builds using {name}.",
            "{name} keeps deployment feedback loops observable.",
        ],
        "ru": [
            "{name} оркестрирует выкладки по кластерам.",
            "Релиз-инженеры контролируют билды через {name}.",
            "{name} делает циклы обратной связи в деплоях наблюдаемыми.",
        ],
    },
    "documentation": {
        "en": [
            "{name} assembles living documentation portals.",
            "Support desks surface answers with {name}.",
            "{name} generates tailored onboarding guides.",
        ],
        "ru": [
            "{name} формирует живые порталы документации.",
            "Службы поддержки находят ответы через {name}.",
            "{name} выпускает персонализированные гайды онбординга.",
        ],
    },
    "support_ops": {
        "en": [
            "{name} routes incidents by urgency and skills.",
            "SLA dashboards compute breach risk via {name}.",
            "{name} automates customer follow-ups after fixes.",
        ],
        "ru": [
            "{name} маршрутизирует инциденты по срочности и навыкам.",
            "SLA-панели считают риск нарушения через {name}.",
            "{name} автоматизирует уведомления клиентов после исправлений.",
        ],
    },
    "knowledge": {
        "en": [
            "{name} nurtures community contributions.",
            "Advocacy teams analyze discussions using {name}.",
            "{name} curates best-practice catalogs.",
        ],
        "ru": [
            "{name} развивает вклад сообществ.",
            "Команды адвокации анализируют дискуссии с {name}.",
            "{name} курирует каталоги лучших практик.",
        ],
    },
    "security": {
        "en": [
            "{name} enforces encryption or masking strategies.",
            "Audit teams review access flows with {name}.",
            "{name} reduces blast radius for sensitive datasets.",
        ],
        "ru": [
            "{name} обеспечивает стратегии шифрования или маскировки.",
            "Аудиторы анализируют потоки доступа с помощью {name}.",
            "{name} сокращает последствия утечки конфиденциальных данных.",
        ],
    },
    "os": {
        "en": [
            "{name} tunes schedulers for latency-sensitive workloads.",
            "Embedded kernels embed {name} to allocate memory deterministically.",
            "{name} coordinates interrupts across devices.",
        ],
        "ru": [
            "{name} настраивает планировщики под задержко-чувствительные "
            "нагрузки.",
            "Встроенные ядра используют {name} для детерминированного "
            "распределения памяти.",
            "{name} координирует прерывания устройств.",
        ],
    },
    "parallel": {
        "en": [
            "{name} partitions workloads across GPU or cluster nodes.",
            "Scientific codes rely on {name} to coordinate reductions.",
            "{name} hides latency in distributed pipelines.",
        ],
        "ru": [
            "{name} распределяет задачи по GPU или узлам кластера.",
            "Научные коды используют {name} для редукций.",
            "{name} скрывает задержки в распределенных конвейерах.",
        ],
    },
    "time_series": {
        "en": [
            "{name} forecasts sensor or business metrics streams.",
            "SRE teams detect drifts in KPIs with {name}.",
            "{name} backs capacity-planning dashboards.",
        ],
        "ru": [
            "{name} прогнозирует потоки сенсоров или бизнес-метрик.",
            "SRE-команды ищут дрифт KPI через {name}.",
            "{name} лежит в основе панелей планирования емкости.",
        ],
    },
    "graph_db": {
        "en": [
            "{name} optimizes traversals in property graphs.",
            "Recommendation APIs infer relations using {name}.",
            "{name} keeps knowledge graphs synchronized.",
        ],
        "ru": [
            "{name} оптимизирует обходы в property-графах.",
            "Рекомендательные API выводят связи через {name}.",
            "{name} синхронизирует графы знаний.",
        ],
    },
    "mlops": {
        "en": [
            "{name} tracks models from training to serving.",
            "Feature teams coordinate rollouts through {name}.",
            "{name} links monitoring findings with retraining triggers.",
        ],
        "ru": [
            "{name} отслеживает модели от обучения до сервинга.",
            "Команды фич координируют выкладки через {name}.",
            "{name} связывает мониторинг с перетренировкой.",
        ],
    },
    "data_platforms": {
        "en": [
            "{name} unifies discovery across data lakes and warehouses.",
            "Governance teams define access policies with {name}.",
            "{name} powers self-service analytics portals.",
        ],
        "ru": [
            "{name} объединяет поиск по озерам и витринам данных.",
            "Команды data governance задают политики доступа через {name}.",
            "{name} обеспечивает self-service аналитические порталы.",
        ],
    },
    "general": {
        "en": [
            "{name} addresses a core workflow described in domain literature.",
            "Engineering teams embed {name} into production services.",
            "{name} improves reliability of the surrounding ecosystem.",
        ],
        "ru": [
            "{name} решает ключевой рабочий процесс из профильной литературы.",
            "Инженерные команды встраивают {name} в продакшн-сервисы.",
            "{name} повышает надежность окружающей экосистемы.",
        ],
    },
}

CATEGORY_EXAMPLES = {
    "sorting": {
        "en": (
            "**Input:** Daily batch of customer invoice IDs.\n"
            "1. Group IDs by least significant digit as {name} suggests.\n"
            "2. Reiterate for tens and hundreds until digits are exhausted.\n"
            "3. Export the stable ordering to the billing data mart.\n"
            "**Result:** invoices arrive sorted without comparisons."
        ),
        "ru": (
            "**Вход:** Суточный пакет номеров счетов клиентов.\n"
            "1. Сгруппируйте номера по младшему разряду, как требует {name}.\n"
            "2. Повторите для десятков и сотен, пока разряды не закончатся.\n"
            "3. Выгрузите устойчивый порядок в биллинговую витрину.\n"
            "**Результат:** счета отсортированы без сравнений."
        ),
    },
    "search": {
        "en": (
            "**Input:** Sorted array of telemetry thresholds.\n"
            "1. Apply {name} to locate the boundary for an alert.\n"
            "2. Narrow the interval each iteration using metadata.\n"
            "3. Return the index to configure monitoring rules.\n"
            "**Result:** alert definitions align with real thresholds."
        ),
        "ru": (
            "**Вход:** Отсортированный массив порогов телеметрии.\n"
            "1. Примените {name}, чтобы найти границу алерта.\n"
            "2. Сужайте интервал на каждой итерации, опираясь на метаданные.\n"
            "3. Верните индекс для настройки правила мониторинга.\n"
            "**Результат:** определения алертов совпадают с фактическими "
            "порогами."
        ),
    },
    "graph": {
        "en": (
            "**Input:** City transit map stored as weighted graph.\n"
            "1. Feed nodes and edges into {name}.\n"
            "2. Relax or traverse edges according to the algorithm rules.\n"
            "3. Produce the optimal route for dispatch dashboards.\n"
            "**Result:** planners broadcast fastest journeys."
        ),
        "ru": (
            "**Вход:** Городская карта транспорта в виде взвешенного графа.\n"
            "1. Передайте вершины и ребра в {name}.\n"
            "2. Ослабляйте или обходите ребра по правилам алгоритма.\n"
            "3. Получите оптимальный маршрут для диспетчерских панелей.\n"
            "**Результат:** планировщики публикуют самые быстрые поездки."
        ),
    },
    "tree": {
        "en": (
            "**Input:** Stream of keys arriving to a balanced index.\n"
            "1. Route each key through {name} rotations or splits.\n"
            "2. Maintain invariants after insertions or deletions.\n"
            "3. Persist the balanced structure for downstream queries.\n"
            "**Result:** latency stays predictable for OLTP workloads."
        ),
        "ru": (
            "**Вход:** Поток ключей, попадающих в сбалансированный индекс.\n"
            "1. Направляйте каждый ключ через повороты/разделения {name}.\n"
            "2. Поддерживайте инварианты после вставок или удалений.\n"
            "3. Сохраните сбалансированную структуру для последующих запросов.\n"
            "**Результат:** задержки остаются предсказуемыми для OLTP."
        ),
    },
    "string": {
        "en": (
            "**Input:** DNA fragment catalog requiring pattern search.\n"
            "1. Preprocess the pattern/text structures defined by {name}.\n"
            "2. Slide through the sequence while honoring skips/shifts.\n"
            "3. Emit matches for downstream annotation pipelines.\n"
            "**Result:** labs pinpoint motifs quickly."
        ),
        "ru": (
            "**Вход:** Каталог фрагментов ДНК для поиска шаблонов.\n"
            "1. Предобработайте строки по правилам {name}.\n"
            "2. Скользите по последовательности, используя переходы.\n"
            "3. Передавайте совпадения в конвейер аннотаций.\n"
            "**Результат:** лаборатории быстро находят мотивы."
        ),
    },
    "hashing": {
        "en": (
            "**Input:** Stream of cache keys from API gateway.\n"
            "1. Run each key through {name} to obtain balanced buckets.\n"
            "2. Store payloads based on hash slots.\n"
            "3. Rehash only affected slots during scale-out.\n"
            "**Result:** cache hit ratios stay high."
        ),
        "ru": (
            "**Вход:** Поток ключей кэша от API-шлюза.\n"
            "1. Пропустите каждый ключ через {name} для равномерных бакетов.\n"
            "2. Сохраняйте данные в соответствии с хеш-слотами.\n"
            "3. При масштабировании перерабатывайте только затронутые слоты.\n"
            "**Результат:** коэффициент попаданий кэша остается высоким."
        ),
    },
    "data_structure": {
        "en": (
            "**Input:** Tasks arriving to scheduler queues.\n"
            "1. Insert items using the semantics defined by {name}.\n"
            "2. Pop or peek entries as threads pick work.\n"
            "3. Persist the structure for failover replay.\n"
            "**Result:** execution order remains deterministic."
        ),
        "ru": (
            "**Вход:** Задачи, поступающие в очереди планировщика.\n"
            "1. Вставляйте элементы по семантике {name}.\n"
            "2. Извлекайте записи по мере обработки потоками.\n"
            "3. Храните структуру для воспроизведения при отказе.\n"
            "**Результат:** порядок выполнения остается детерминированным."
        ),
    },
    "dynamic_programming": {
        "en": (
            "**Input:** Table of costs for logistics decisions.\n"
            "1. Define subproblems following {name} recursion.\n"
            "2. Fill the DP matrix row by row.\n"
            "3. Reconstruct the optimal policy for planners.\n"
            "**Result:** resources allocate with maximal yield."
        ),
        "ru": (
            "**Вход:** Таблица стоимостей для логистических решений.\n"
            "1. Определите подзадачи по рекурсии {name}.\n"
            "2. Заполните DP-матрицу построчно.\n"
            "3. Восстановите оптимальную стратегию для планировщиков.\n"
            "**Результат:** ресурсы распределены с максимальной отдачей."
        ),
    },
    "machine_learning": {
        "en": (
            "**Input:** Feature matrix and target labels.\n"
            "1. Split data into train/validation folds.\n"
            "2. Fit parameters with {name} optimization routine.\n"
            "3. Deploy the serialized model to scoring service.\n"
            "**Result:** predictions refresh as new data arrives."
        ),
        "ru": (
            "**Вход:** Матрица признаков и целевые метки.\n"
            "1. Разбейте данные на обучающие и валидационные фолды.\n"
            "2. Обучите параметры с помощью процедуры {name}.\n"
            "3. Разверните сериализованную модель в скоринговом сервисе.\n"
            "**Результат:** предсказания обновляются по мере поступления данных."
        ),
    },
    "deep_learning": {
        "en": (
            "**Input:** Corpus of labeled sequences or images.\n"
            "1. Tokenize or normalize batches per {name} requirements.\n"
            "2. Train on accelerators while monitoring loss curves.\n"
            "3. Export checkpoints for inference services.\n"
            "**Result:** neural predictions adapt to production data."
        ),
        "ru": (
            "**Вход:** Корпус размеченных последовательностей или изображений.\n"
            "1. Токенизируйте/нормализуйте батчи по требованиям {name}.\n"
            "2. Обучайте на ускорителях, отслеживая кривые потерь.\n"
            "3. Экспортируйте чекпоинты для сервисов инференса.\n"
            "**Результат:** нейросетевые предсказания адаптируются к данным."
        ),
    },
    "data_engineering": {
        "en": (
            "**Input:** Pipeline metadata and table snapshots.\n"
            "1. Run {name} checks on each ingestion batch.\n"
            "2. Surface anomalies to the operations channel.\n"
            "3. Auto-tag affected datasets for remediation.\n"
            "**Result:** downstream analytics remain trustworthy."
        ),
        "ru": (
            "**Вход:** Метаданные конвейера и снимки таблиц.\n"
            "1. Запустите проверки {name} на каждой загрузке.\n"
            "2. Сообщите аномалии в канал эксплуатации.\n"
            "3. Автоотметьте пострадавшие наборы данных для устранения.\n"
            "**Результат:** аналитика вниз по цепочке остается надежной."
        ),
    },
    "database": {
        "en": (
            "**Input:** SQL workload captured from production.\n"
            "1. Apply {name} to reorganize indexes or plans.\n"
            "2. Validate performance on staging datasets.\n"
            "3. Roll changes into the cluster with monitoring hooks.\n"
            "**Result:** query latency drops without regressions."
        ),
        "ru": (
            "**Вход:** SQL-нагрузка, снятая с продакшна.\n"
            "1. Примените {name} для перестройки индексов или планов.\n"
            "2. Проверьте производительность на стендовых данных.\n"
            "3. Внесите изменения в кластер с мониторингом.\n"
            "**Результат:** задержка запросов падает без регрессий."
        ),
    },
    "nosql": {
        "en": (
            "**Input:** Document collections sharded across regions.\n"
            "1. Coordinate replicas using {name} policies.\n"
            "2. Rebalance partitions as traffic shifts.\n"
            "3. Validate consistency via health probes.\n"
            "**Result:** reads stay low-latency worldwide."
        ),
        "ru": (
            "**Вход:** Коллекции документов, распределенные по регионам.\n"
            "1. Координируйте реплики правилами {name}.\n"
            "2. Перебалансируйте партиции при смене трафика.\n"
            "3. Проверяйте согласованность health-пробами.\n"
            "**Результат:** чтения остаются низкозадержочными по всему миру."
        ),
    },
    "observability": {
        "en": (
            "**Input:** Metrics, traces, and logs from services.\n"
            "1. Feed telemetry into {name} collectors.\n"
            "2. Correlate anomalies with deployment markers.\n"
            "3. Trigger runbooks once thresholds are violated.\n"
            "**Result:** incidents are detected before customers notice."
        ),
        "ru": (
            "**Вход:** Метрики, трейсы и логи сервисов.\n"
            "1. Отправьте телеметрию в сборщики {name}.\n"
            "2. Коррелируйте аномалии с отметками выкладок.\n"
            "3. Запускайте runbook'и при нарушении порогов.\n"
            "**Результат:** инциденты фиксируются до жалоб клиентов."
        ),
    },
    "blockchain": {
        "en": (
            "**Input:** Sequence of blockchain transactions.\n"
            "1. Ingest blocks and metadata into {name}.\n"
            "2. Validate signatures or relationships per algorithm rules.\n"
            "3. Surface insights to compliance dashboards.\n"
            "**Result:** ledgers stay transparent and auditable."
        ),
        "ru": (
            "**Вход:** Последовательность транзакций блокчейна.\n"
            "1. Загрузите блоки и метаданные в {name}.\n"
            "2. Проверьте подписи/связи по правилам алгоритма.\n"
            "3. Передайте инсайты на панели комплаенса.\n"
            "**Результат:** реестры остаются прозрачными и аудируемыми."
        ),
    },
    "ci_cd": {
        "en": (
            "**Input:** Build artifacts and deployment manifests.\n"
            "1. Pass artifacts through {name} gates.\n"
            "2. Roll out to canary targets with automated checks.\n"
            "3. Promote to full fleet once metrics hold steady.\n"
            "**Result:** releases stay safe and observable."
        ),
        "ru": (
            "**Вход:** Сборочные артефакты и манифесты деплоя.\n"
            "1. Проведите артефакты через контроль {name}.\n"
            "2. Выкатите на канареек с авто-проверками.\n"
            "3. Распространите на весь парк при стабильных метриках.\n"
            "**Результат:** релизы остаются безопасными и наблюдаемыми."
        ),
    },
    "documentation": {
        "en": (
            "**Input:** Knowledge articles and API specs.\n"
            "1. Index content with {name} processing pipeline.\n"
            "2. Enrich entries using tags/entities extracted by the "
            "algorithm.\n"
            "3. Publish tailored guides to the portal.\n"
            "**Result:** developers locate accurate answers faster."
        ),
        "ru": (
            "**Вход:** Статьи базы знаний и API-спеки.\n"
            "1. Проиндексируйте контент через конвейер {name}.\n"
            "2. Обогащайте записи тегами и сущностями.\n"
            "3. Публикуйте персонализированные гайды на портал.\n"
            "**Результат:** разработчики быстрее находят точные ответы."
        ),
    },
    "support_ops": {
        "en": (
            "**Input:** Queue of customer tickets.\n"
            "1. Score each ticket with signals defined by {name}.\n"
            "2. Route work to agents or bots automatically.\n"
            "3. Capture outcomes for SLA analytics.\n"
            "**Result:** response quality improves across shifts."
        ),
        "ru": (
            "**Вход:** Очередь клиентских тикетов.\n"
            "1. Оцените каждый тикет сигналами {name}.\n"
            "2. Автоматически направьте работу агентам или ботам.\n"
            "3. Зафиксируйте результаты для SLA-аналитики.\n"
            "**Результат:** качество ответов растет во всех сменах."
        ),
    },
    "knowledge": {
        "en": (
            "**Input:** Community posts and contributions.\n"
            "1. Cluster discussions via {name} insights.\n"
            "2. Highlight unanswered topics for moderators.\n"
            "3. Suggest resources back to participants.\n"
            "**Result:** knowledge sharing becomes continuous."
        ),
        "ru": (
            "**Вход:** Посты и вклад сообщества.\n"
            "1. Кластеризуйте обсуждения с помощью {name}.\n"
            "2. Подсветите неотвеченные темы модераторам.\n"
            "3. Рекомендуйте ресурсы участникам.\n"
            "**Результат:** обмен знаниями становится непрерывным."
        ),
    },
    "security": {
        "en": (
            "**Input:** Access logs and sensitive datasets.\n"
            "1. Classify data tiers through {name} policies.\n"
            "2. Apply masking or encryption flows.\n"
            "3. Audit changes and escalate violations.\n"
            "**Result:** compliance objectives stay verifiable."
        ),
        "ru": (
            "**Вход:** Журналы доступа и конфиденциальные наборы данных.\n"
            "1. Классифицируйте уровни данных политиками {name}.\n"
            "2. Примените маскирование или шифрование.\n"
            "3. Аудируйте изменения и эскалируйте нарушения.\n"
            "**Результат:** цели комплаенса остаются проверяемыми."
        ),
    },
    "os": {
        "en": (
            "**Input:** Timeline of CPU bursts and IO waits.\n"
            "1. Feed metrics into {name} scheduler.\n"
            "2. Adjust queues or priorities automatically.\n"
            "3. Measure turnaround across workloads.\n"
            "**Result:** operating system stays responsive."
        ),
        "ru": (
            "**Вход:** График CPU-ривков и IO-ожиданий.\n"
            "1. Передайте метрики планировщику {name}.\n"
            "2. Автонастройте очереди или приоритеты.\n"
            "3. Измерьте время выполнения для нагрузок.\n"
            "**Результат:** операционная система остается отзывчивой."
        ),
    },
    "parallel": {
        "en": (
            "**Input:** Computational job split across workers.\n"
            "1. Partition data per {name} strategy.\n"
            "2. Synchronize phases using collective primitives.\n"
            "3. Aggregate outputs for the coordinator.\n"
            "**Result:** throughput scales with hardware."
        ),
        "ru": (
            "**Вход:** Вычислительная задача, разделенная по воркерам.\n"
            "1. Разделите данные по стратегии {name}.\n"
            "2. Синхронизируйте фазы коллективными примитивами.\n"
            "3. Сведите результаты на координаторе.\n"
            "**Результат:** пропускная способность растет с железом."
        ),
    },
    "time_series": {
        "en": (
            "**Input:** Rolling window of KPI observations.\n"
            "1. Fit {name} model on historical slices.\n"
            "2. Forecast future intervals with confidence bands.\n"
            "3. Feed predictions to capacity planners.\n"
            "**Result:** teams react before metrics drift."
        ),
        "ru": (
            "**Вход:** Скольжащие окна наблюдений KPI.\n"
            "1. Обучите модель {name} на истории.\n"
            "2. Прогнозируйте будущие интервалы с доверительными "
            "диапазонами.\n"
            "3. Передайте предсказания планировщикам емкости.\n"
            "**Результат:** команды реагируют до дрифта метрик."
        ),
    },
    "graph_db": {
        "en": (
            "**Input:** Property graph storing entities and relations.\n"
            "1. Traverse edges using {name} logic.\n"
            "2. Materialize subgraphs for analytics.\n"
            "3. Surface recommendations or alerts.\n"
            "**Result:** relationships stay discoverable at scale."
        ),
        "ru": (
            "**Вход:** Property-граф сущностей и связей.\n"
            "1. Обходите ребра по логике {name}.\n"
            "2. Создавайте подграфы для аналитики.\n"
            "3. Выводите рекомендации или алерты.\n"
            "**Результат:** связи остаются обнаруживаемыми при масштабе."
        ),
    },
    "mlops": {
        "en": (
            "**Input:** Registry of trained models and metrics.\n"
            "1. Track lineage through {name} workflows.\n"
            "2. Trigger deployments when quality criteria meet.\n"
            "3. Roll back automatically if drift is detected.\n"
            "**Result:** production ML remains governable."
        ),
        "ru": (
            "**Вход:** Реестр обученных моделей и метрик.\n"
            "1. Отслеживайте происхождение через рабочие процессы {name}.\n"
            "2. Запускайте деплой при выполнении критериев качества.\n"
            "3. Откатывайте автоматически при обнаружении дрифта.\n"
            "**Результат:** продакшен-ML остается управляемым."
        ),
    },
    "data_platforms": {
        "en": (
            "**Input:** Catalog of datasets across lakehouse.\n"
            "1. Register sources via {name} governance flow.\n"
            "2. Apply policies and lineage tracking.\n"
            "3. Expose curated assets to self-service portal.\n"
            "**Result:** consumers trust shared data assets."
        ),
        "ru": (
            "**Вход:** Каталог наборов данных в lakehouse.\n"
            "1. Регистрируйте источники через процесс {name}.\n"
            "2. Применяйте политики и отслеживание происхождения.\n"
            "3. Открывайте отобранные активы self-service порталу.\n"
            "**Результат:** потребители доверяют общим данным."
        ),
    },
    "general": {
        "en": (
            "**Input:** Dataset documented in the domain literature.\n"
            "1. Apply the rules of {name} step by step.\n"
            "2. Validate intermediate outputs against expectations.\n"
            "3. Deliver the improved artifact to downstream teams.\n"
            "**Result:** stakeholders gain measurable value."
        ),
        "ru": (
            "**Вход:** Набор данных из профильной области.\n"
            "1. Выполняйте правила {name} шаг за шагом.\n"
            "2. Проверяйте промежуточные результаты с ожиданиями.\n"
            "3. Передавайте улучшенный артефакт дальше по цепочке.\n"
            "**Результат:** заказчики получают измеримую пользу."
        ),
    },
}


def _split_sentences(text: str) -> List[str]:
    """Split text into sentences for both English and Russian."""
    if not text:
        return []
    cleaned = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [s.strip() for s in sentences if s.strip()]


def _detect_category(algorithm_name: str, summary: Optional[str]) -> str:
    """Infer high-level category based on name or summary keywords."""
    text = f"{algorithm_name} {summary or ''}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "general"


def _extract_use_sentences(
    sentences: List[str], language: str, max_items: int = 3
) -> List[str]:
    """Pick sentences that mention usage/application details."""
    if not sentences:
        return []
    if language == "ru":
        keywords = ["использ", "примен", "подходит", "служит"]
    else:
        keywords = ["use", "used", "application", "applied", "suitable"]

    selected: List[str] = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(keyword in lower for keyword in keywords):
            selected.append(sentence)
        if len(selected) == max_items:
            break

    if not selected:
        selected = sentences[:max_items]

    return selected[:max_items]


def generate_simple_explanation(
    algorithm_name: str, wiki_summary: Optional[str], language: str
) -> str:
    """Compose an explanation grounded in Wikipedia summary."""
    sentences = _split_sentences(wiki_summary or "")
    category = _detect_category(algorithm_name, wiki_summary)

    if sentences:
        chosen = " ".join(sentences[:2])
        return chosen

    template = CATEGORY_USE_CASES.get(category, CATEGORY_USE_CASES["general"])
    line = template[language][0].replace("{name}", algorithm_name)
    if language == "ru":
        return (
            f"{algorithm_name} — это практический алгоритм. "
            f"{line}"
        )
    return f"{algorithm_name} is a practical technique. {line}"


def generate_where_used(
    algorithm_name: str, wiki_summary: Optional[str], language: str
) -> str:
    """Generate bullet-list of applications."""
    sentences = _split_sentences(wiki_summary or "")
    uses = _extract_use_sentences(sentences, language)
    category = _detect_category(algorithm_name, wiki_summary)
    template = CATEGORY_USE_CASES.get(category, CATEGORY_USE_CASES["general"])

    while len(uses) < 3:
        template_line = template[language][len(uses) % len(template[language])]
        uses.append(template_line.replace("{name}", algorithm_name))

    bullets = "\n".join(f"- {sentence}" for sentence in uses[:3])
    return bullets + "\n"


def generate_example_text(
    algorithm_name: str, wiki_summary: Optional[str], language: str
) -> str:
    """Provide a concrete example scenario."""
    category = _detect_category(algorithm_name, wiki_summary)
    template = CATEGORY_EXAMPLES.get(category, CATEGORY_EXAMPLES["general"])
    example = template[language].replace("{name}", algorithm_name)
    return example + "\n"


def get_wikipedia_summary(algorithm_name: str, language: str = 'en') -> Optional[str]:
    """Get Wikipedia summary for an algorithm."""
    global LAST_REQUEST_TIME
    
    # Rate limiting
    current_time = time.time()
    if current_time - LAST_REQUEST_TIME < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - (current_time - LAST_REQUEST_TIME))
    LAST_REQUEST_TIME = time.time()
    
    try:
        # Clean algorithm name
        clean_name = algorithm_name.replace('_', ' ').strip()
        
        # Special mappings for common algorithm names
        name_mappings = {
            'radix sort': 'Radix_sort',
            'radix сортировка': 'Radix_sort',
            'quick sort': 'Quicksort',
            'merge sort': 'Merge_sort',
            'heap sort': 'Heapsort',
            'bubble sort': 'Bubble_sort',
            'insertion sort': 'Insertion_sort',
            'selection sort': 'Selection_sort',
            'binary search': 'Binary_search_algorithm',
            'linear search': 'Linear_search',
            'breadth first search': 'Breadth-first_search',
            'depth first search': 'Depth-first_search',
            'dijkstra': "Dijkstra's_algorithm",
            'bellman ford': 'Bellman–Ford_algorithm',
            'floyd warshall': 'Floyd–Warshall_algorithm',
            'kruskal': "Kruskal's_algorithm",
            'prim': "Prim's_algorithm",
            'knapsack': 'Knapsack_problem',
            'longest common subsequence': 'Longest_common_subsequence_problem',
            'edit distance': 'Edit_distance',
            'levenshtein': 'Levenshtein_distance',
            'rabin karp': 'Rabin–Karp_algorithm',
            'kmp': 'Knuth–Morris–Pratt_algorithm',
            'boyer moore': 'Boyer–Moore_string-search_algorithm',
        }
        
        wiki_name = name_mappings.get(clean_name.lower())
        if not wiki_name:
            # Try to construct wiki name
            wiki_name = clean_name.title().replace(' ', '_')
        
        # Wikipedia API
        api_url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{wiki_name}"
        
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'extract' in data:
                return data['extract']
        
        # Try English if language is not English
        if language != 'en':
            api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_name}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return data['extract']
        
        return None
    except Exception as e:
        print(f"    [WARNING] Wikipedia API error: {e}")
        return None


def get_algorithm_name_from_path(folder_path: Path) -> str:
    """Extract algorithm name from folder path."""
    return folder_path.name.replace('_', ' ').title()


def get_algorithm_name_from_readme(folder_path: Path) -> Optional[str]:
    """Try to get algorithm name from README.md."""
    readme_path = folder_path / "README.md"
    if not readme_path.exists():
        return None
    
    try:
        content = readme_path.read_text(encoding='utf-8')
        # Look for title in README
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
    except Exception:
        pass
    
    return None


def generate_definition(algorithm_name: str, wiki_summary: Optional[str], 
                       language: str = 'en') -> str:
    """Generate algorithm definition."""
    explanation = generate_simple_explanation(algorithm_name, wiki_summary, language)
    return explanation


def generate_technical_description(algorithm_name: str, wiki_summary: Optional[str],
                                   language: str = 'en') -> str:
    """Generate technical description."""
    sentences = _split_sentences(wiki_summary or "")
    if sentences:
        detail = " ".join(sentences[:3])
        return detail
    
    category = _detect_category(algorithm_name, wiki_summary)
    template = CATEGORY_USE_CASES.get(category, CATEGORY_USE_CASES["general"])
    lines = template[language]
    description = " ".join(line.replace("{name}", algorithm_name) for line in lines[:2])
    return description


def generate_step_by_step_example(algorithm_name: str, wiki_summary: Optional[str],
                                  language: str = 'en') -> str:
    """Generate step-by-step example for the algorithm."""
    return generate_example_text(algorithm_name, wiki_summary, language)


def replace_placeholders_in_univer(content: str, algorithm_name: str, 
                                   wiki_summary: Optional[str], language: str) -> str:
    """Replace placeholders in univer.md files."""
    
    # Replace definition section
    definition_pattern = r'(## Определение алгоритма\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        definition_pattern = r'(## Algorithm Definition\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_definition(match):
        header = match.group(1)
        definition = generate_definition(algorithm_name, wiki_summary, language)
        return header + definition + '\n\n'
    
    content = re.sub(definition_pattern, replace_definition, content, flags=re.DOTALL)
    
    # Replace technical description section
    tech_pattern = r'(## Техническое описание\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        tech_pattern = r'(## Technical Description\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_technical(match):
        header = match.group(1)
        description = generate_technical_description(algorithm_name, wiki_summary, language)
        return header + description + '\n\n'
    
    content = re.sub(tech_pattern, replace_technical, content, flags=re.DOTALL)
    
    # Replace application section
    app_pattern = r'(## Применение в Computer Science\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        app_pattern = r'(## Application in Computer Science\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_application(match):
        header = match.group(1)
        uses_text = generate_where_used(algorithm_name, wiki_summary, language)
        return header + uses_text + '\n'
    
    content = re.sub(app_pattern, replace_application, content, flags=re.DOTALL)

    # Replace step-by-step example section
    step_pattern = r'(## Пример сценария по шагам\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        step_pattern = r'(## Step-by-Step Scenario\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_steps(match):
        header = match.group(1)
        steps = generate_step_by_step_example(algorithm_name, wiki_summary, language)
        return header + steps + '\n\n'
    
    content = re.sub(step_pattern, replace_steps, content, flags=re.DOTALL)
    
    # Remove generic template patterns
    generic_patterns = [
        (r'\[конкретная цель\]', 'конкретных задач'),
        (r'\[конкретный механизм работы\]', 'последовательной обработки данных'),
        (r'\[specific purpose\]', 'specific purposes'),
        (r'\[specific mechanism\]', 'specific mechanisms'),
        (r'конкретный алгоритм/техника, используемая для \[конкретная цель\]', 
         f'{algorithm_name} — алгоритм, используемый для решения конкретных задач'),
        (r'Он работает путем \[конкретный механизм работы\]', 
         'Он работает путем последовательной обработки данных'),
        (r'a specific algorithm/technique used for \[specific purpose\]', 
         f'{algorithm_name} is an algorithm used for specific purposes'),
        (r'It works by \[specific mechanism\]', 
         'It works by processing data according to specific rules'),
    ]
    
    for pattern, replacement in generic_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content


def replace_placeholders_in_school(content: str, algorithm_name: str,
                                  wiki_summary: Optional[str], language: str) -> str:
    """Replace placeholders in school.md files."""
    
    # Replace simple explanation section
    explanation_pattern = r'(## Простое объяснение\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        explanation_pattern = r'(## Simple Explanation\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_explanation(match):
        header = match.group(1)
        explanation = generate_definition(algorithm_name, wiki_summary, language)
        return header + explanation + '\n\n'
    
    content = re.sub(explanation_pattern, replace_explanation, content, flags=re.DOTALL)
    
    # Replace Where It's Used section
    uses_pattern = r'(## Где применяется\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        uses_pattern = r'(## Where It\'s Used\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_uses(match):
        header = match.group(1)
        uses_text = generate_where_used(algorithm_name, wiki_summary, language)
        return header + uses_text + '\n'
    
    content = re.sub(uses_pattern, replace_uses, content, flags=re.DOTALL)

    # Replace Example section
    example_pattern = r'(## Пример\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        example_pattern = r'(## Example\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_example(match):
        header = match.group(1)
        example_text = generate_example_text(algorithm_name, wiki_summary, language)
        return header + example_text + '\n'
    
    content = re.sub(example_pattern, replace_example, content, flags=re.DOTALL)

    # Remove generic template patterns
    generic_patterns = [
        (r'\[конкретная цель\]', 'конкретных задач'),
        (r'\[конкретный механизм работы\]', 'последовательной обработки данных'),
        (r'\[specific purpose\]', 'specific purposes'),
        (r'\[specific mechanism\]', 'specific mechanisms'),
        (r'конкретный алгоритм/техника, используемая для \[конкретная цель\]', 
         f'{algorithm_name} — алгоритм, используемый для решения конкретных задач'),
        (r'Он работает путем \[конкретный механизм работы\]', 
         'Он работает путем последовательной обработки данных'),
        (r'a specific algorithm/technique used for \[specific purpose\]', 
         f'{algorithm_name} is an algorithm used for specific purposes'),
        (r'It works by \[specific mechanism\]', 
         'It works by processing data according to specific rules'),
    ]
    
    for pattern, replacement in generic_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content


def process_md_file(md_path: Path, algorithm_name: str, language: str) -> bool:
    """Process a single MD file."""
    try:
        content = md_path.read_text(encoding='utf-8')
        original_content = content
        
        # Determine if it's school or univer file
        is_univer = 'univer' in md_path.name
        
        # Get Wikipedia summary
        wiki_summary = get_wikipedia_summary(algorithm_name, language)
        
        # Replace placeholders
        if is_univer:
            content = replace_placeholders_in_univer(content, algorithm_name, wiki_summary, language)
        else:
            content = replace_placeholders_in_school(content, algorithm_name, wiki_summary, language)
        
        # Only write if content changed
        if content != original_content:
            md_path.write_text(content, encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False


def main():
    """Main function to process all MD files."""
    print("=" * 70)
    print("REPLACING PLACEHOLDERS WITH REAL CONTENT")
    print("=" * 70)
    print()
    
    # Find all algorithm folders
    algorithm_folders = []
    for semester_dir in ROOT.glob("semester_*"):
        for lecture_dir in semester_dir.glob("lecture_*"):
            for algo_dir in lecture_dir.iterdir():
                if algo_dir.is_dir() and not algo_dir.name.startswith('.'):
                    algorithm_folders.append(algo_dir)
    
    algorithm_folders.sort()
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print()
    
    processed_count = 0
    updated_count = 0
    error_count = 0
    
    for idx, folder_path in enumerate(algorithm_folders, 1):
        relative_path = folder_path.relative_to(ROOT)
        print(f"[{idx}/{len(algorithm_folders)}] {relative_path}")
        
        # Get algorithm name
        algorithm_name = get_algorithm_name_from_readme(folder_path)
        if not algorithm_name:
            algorithm_name = get_algorithm_name_from_path(folder_path)
        
        # Process all 4 MD files
        md_files = [
            ('school.en.md', 'en'),
            ('school.ru.md', 'ru'),
            ('univer.en.md', 'en'),
            ('univer.ru.md', 'ru'),
        ]
        
        folder_updated = False
        for md_filename, lang in md_files:
            md_path = folder_path / md_filename
            if md_path.exists():
                if process_md_file(md_path, algorithm_name, lang):
                    print(f"  [OK] Updated {md_filename}")
                    folder_updated = True
                else:
                    print(f"  [SKIP] No changes in {md_filename}")
            else:
                print(f"  [SKIP] {md_filename} not found")
        
        if folder_updated:
            updated_count += 1
        
        processed_count += 1
        
        if idx % 50 == 0:
            print(f"\nProgress: {idx}/{len(algorithm_folders)} processed\n")
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total folders: {len(algorithm_folders)}")
    print(f"  Folders updated: {updated_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

