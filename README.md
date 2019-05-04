## Spike - json formatter with logging in python

[![Build Status](https://travis-ci.org/FabienArcellier/spike_json_formatter_for_logging_python.svg?branch=master)](https://travis-ci.org/FabienArcellier/spike_json_formatter_for_logging_python)

Python fournit dans la librairie standard une API au travers du package
`logging`.

Pour pouvoir traiter ces messages de logs sur une plateforme de log management
comme `elastic`, `splunk` ou ..., les messages de logs doivent pouvoir
être parsé nativement.

Le format `json lines` consiste à écrire chaque record de log sous
la forme d'un enregistrement json. C'est un format interopérable qui supporte
bien les opérations courantes sur un journal d'activité comme :

* la rotation de log
* l'archivage
* les données imbriquées
* la lecture par un agent comme `filebeat`, ...
* le transport natif comme sur `docker`
* ...

D'autres alternatives sont utilisables comme Avro mais elles
sont plus difficiles à interopérer.

### Références

* https://docs.python.org/3/howto/logging.html
* [json lines](http://jsonlines.org/)


## 1. sélectionner un formatter en json

* [structlog](https://www.structlog.org/en/stable/getting-started.html)

    librairie de logs structurée. Structlog propose des fonctionnalités avancés pour
    mieux travailler l'enregistrement tel que le Data binding, les pipelines, ...

    cette librairie peut s'appuyer sur logging pour le rendu mais a vocation
    à la remplacer.

    * [Structlog - standard Library Logging](https://www.structlog.org/en/stable/standard-library.html)

* [python-json-logger](https://github.com/madzak/python-json-logger/tree/12ab1c30c24846cadfba214fa9cd2c00d899ab2a)

    formatter json pour étendre le package `logging`.

* implémenter son propre formatter avec json.dumps

    pratique simple qui peut mener à réimplémenter certaines
    logiques proposées par `python-json-logger` comme :

    * string pour sélectionner les champs à publier
    * configuration de l'encoder json

    à faire si il y'a une exigence de stabilité dans les temps

Pour ce spike, nous utiliserons `python-json-logger` car nous
souhaitons étendre la librairie standard `logging` et toujours utiliser
cette API, pas la remplacer.

La librairie logging évolue régulièrement et plusieurs des spécificités
offertes par structlog sont déjà inclus :

* le data binding avec les [LoggerAdapter](https://docs.python.org/3/library/logging.html#loggeradapter-objects)
* les processing pipeline avec les [Filters](https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information)

### utiliser python-json-logger

* 1 . enregistrer la librairie dans les dépendances

```python
# setup.py

setup(
    install_requires = [
        'click',
        'decorator',
        'python-json-logger'
    ]
)
```

* 2 . mettre à jour les dépendances

```bash
make freeze_requirements
```

## 2. utiliser le formatter json

plus d'information dans [`mycommand_tests/spikes/using_json_formatter_with_logging.py`](mycommand_tests/spikes/using_json_formatter_with_logging.py)

_output :_

```
{"message": "hello world"}
```

par défaut, le formatter inclut juste le champs message. Il manque plusieurs informations
comme le timestamp du message, la ligne ou il a été émis, le module, le fichier, ...

## 3. récupérer des meta-données standard sur le message de log

plus d'information dans [`mycommand_tests/spikes/using_json_formatter_with_logging_with_more_details.py`](mycommand_tests/spikes/using_json_formatter_with_logging_with_more_details.py)

```python
formatter = jsonlogger.JsonFormatter('(asctime) (levelname) (message)')
```

* [logging - level record attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)

## 4. formater un timestamp au format ISO8601

Ce pattern peut être utilisé pour :

* ajouter un champs à partir des champs existants
* renommer un champs

plus d'information dans [`mycommand_tests/spikes/using_json_formatter_with_logging_with_timestamp_iso8601.py`](mycommand_tests/spikes/using_json_formatter_with_logging_with_timestamp_iso8601.py)

* 1 . étendre le formatter

```python
class Iso8601JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(Iso8601JsonFormatter, self).add_fields(log_record, record, message_dict)
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['timestamp'] = now
```

* 2 . configurer pour utiliser le champs timestamp

```
formatter = Iso8601JsonFormatter('(timestamp) (levelname) (message)')
```

```text
{"timestamp": "2019-05-04T13:30:11.248545Z", "levelname": "INFO", "message": "hello world"}
```

## 5. implémenter un module pour le cli ``cli_logger``

plus d'information dans [`mycommand/cli_logger.py`](mycommand/cli_logger.py)

### ajouter des attributs au message de log

```python
logger = get_logger('mycommand')
logger.info("arguments", extra={'arguments': {'name': name}})
```

```text
{"timestamp": "2019-05-04T13:50:41.414548Z", "name": "mycommand", "level": "INFO", "filename": "cli.py", "lineno": 19, "message": "arguments", "arguments": {"name": "fabien"}}
```

### ignorer les logs dans les tests automatiques

Pour ne pas afficher les logs sur la sortie standard dans les tests
automatiques, nous pouvons utiliser `logging.disable()`

```python
class CliTest(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.FATAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)
```

### capturer la sortie standard pour tester le logger

plus de détails dans [mycommand_tests/acceptances/test_cli_logger.py](mycommand_tests/acceptances/test_cli_logger.py)

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/spike_json_formatter_for_logging_python.git
```

## Usage

You can run the application with the following command

```bash
python -m mycommand.cli command1 --name fabien

# inside a virtualenv or after installation with pip
mycommand command1 --name fabien
```

## Developper guideline

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
make install_requirements_dev
```

### Update release dependencies

Use make to instanciate a python virtual environment in ./venv and freeze
dependencies version on requirement.txt.

```bash
make update_requirements
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
make venv
source venv/bin/activate
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2018 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
