# NooLite MTRF MQTT

Ретранслятор сообщений с последовательного порта MTRF в MQTT сообщения

## Установка

Для установки проекта нужен Python 3.5+ и pip

### Из репозитория

В системе должны быть установлены:

- pip для третий версии python

- git

```bash
$ pip3 install git+https://bitbucket.org/AlekseevAV/noolite-mtrf-to-mqtt
```

К примеру установка проекта на ArchLinux будет выглядеть следующим образом:
```bash
# Устанавливаем необходимые пакеты
$ pacman -S python python-pip git
# Устанавливаем noolite_api
$ pip3 install git+https://bitbucket.org/AlekseevAV/noolite-mtrf-to-mqtt
```

### Из исходников

```bash
# Клонируем репозиторий
$ git clone https://bitbucket.org/AlekseevAV/noolite-mtrf-to-mqtt

# Заходим в созданную папку репозитория
$ cd noolite-mtrf-to-mqtt

# Устанавливаем сервер
$ python setup.py install
```

## Запуск

```
$ noolite_mtrf_mqtt
```

## Работа

MQTT топики для работы:
- noolite/mtrf/send - топик для отправки сообщений на адаптер
- noolite/mtrf/receive - топик, куда публикуются все принятые сообщения с адаптера
