# Архитектура — ADR-001

Статус: выбранное направление; модули ниже создаются в JG-001 и следующих задачах.
Основание: один Android-телефон, один BLE-датчик, локальные данные, приоритет измерений.

## Стек

| Область | Решение |
|---|---|
| Приложение | Kotlin, Jetpack Compose, Material 3, ViewModel, Coroutines/Flow |
| Навигация | Navigation 3 при появлении нескольких экранов |
| Хранение | Room для сессий/индексов/результатов; отдельные append-only raw-файлы |
| Получение данных | Android BLE GATT за интерфейсом SensorTransport |
| Фоновая запись | Foreground service типа connectedDevice, запуск из видимого приложения |
| Анализ | Детерминированное Kotlin/JVM-ядро без Android |
| Исследования | Python, фиксируем зависимости при добавлении первого анализа |
| Сборка | Gradle Kotlin DSL, version catalog, wrapper с checksum, фиксированные версии |
| Проверки | JVM unit/replay; Android lint; Compose/instrumented; реальный телефон |

Версии Kotlin/AGP/Gradle/JDK/SDK и minSdk фиксирует агент JG-001 после проверки
официальной таблицы совместимости. Не выбирать несогласованный набор «самых последних»
версий. Никаких dynamic versions или preview-зависимостей без причины и ADR.

Направление согласуется с [рекомендациями Android](https://developer.android.com/topic/architecture/recommendations).
Возможности фонового BLE и ограничения запуска service проверять по
[официальной документации](https://developer.android.com/develop/connectivity/bluetooth/ble/background)
для фактического target SDK. WorkManager не является непрерывным BLE-регистратором.

## Границы

Планируемые модули:

- `:app`: UI, permissions, foreground service, сборка зависимостей.
- `:core:measurement`: модели SI, качество сигнала, обнаружение прыжков, оценка высоты.
- `:core:sensor`: BLE-адаптер и протокол WT9011DCL; декодер тестируется без радиоканала.
- `:core:storage`: Room, raw-файлы, восстановление незавершённой сессии, экспорт/удаление.

Measurement не импортирует Android, sensor, storage или UI. Sensor декодирует физические
измерения, но не решает, был ли прыжок. App координирует сессию; storage сохраняет исходное.
Контракты между модулями меняет один назначенный владелец, остальные получают новый SHA.

Поток: BLE callback → ограниченная очередь → raw writer → decoder → session analysis → UI.
Callback не блокировать диском. Переполнение очереди — явный gap/event; оно не должно
тихо отбрасывать samples. UI может получать редкие обновления, запись — весь доступный поток.
Обработка после завершения тренировки разрешена и предпочтительна для первого алгоритма.

## Контракт записи (требования; схема будет зафиксирована до реализации)

- Session: schema version, UUID, pseudonymous participant ID, activity, mounting position,
  phone/OS, sensor model/firmware, app build, конфигурация/калибровка, wall-clock начала.
- Packet: исходные bytes, characteristic, monotonic receive time, connection epoch;
  device time/sequence nullable, только если подтверждены протоколом.
- Sample: SI channels, coordinate frame, sample-time origin/uncertainty, ссылка на packet.
  Асинхронные каналы не выдавать за синхронные; при выравнивании фиксировать метод.
- QualityEvent: disconnect/reconnect, gaps, overflow, clipping, clock reset, storage failure.
- Result: algorithm/config version, input hash, границы события, height nullable,
  validity/reasons, estimated uncertainty при наличии проверенной модели неопределённости.

Разрыв делит запись на сегменты. Не интегрировать через разрыв и не считать потерянную
часть сессии отсутствием прыжков. При crash сохранять пригодные завершённые блоки raw,
помечать сессию interrupted. Удаление тренировки удаляет её raw и индексы.
MAC и видео не попадают в обычный export/логи; диагностический export требует явного действия.
Локальность включает Android Auto Backup и перенос на другое устройство: в JG-001
явно настроить backup/data-extraction rules, исключив записи, базу и диагностические
экспорты из автоматического облачного копирования и переноса. Проверить поведение
для поддерживаемых Android; отсутствие собственного backend само по себе этого не гарантирует.

## Что пока не нужно

Docker, backend, аккаунты, микросервисы, Kubernetes, облачная аналитика и ML-классификация.
Для MVP достаточно одного репозитория. Усложнение — по измеренной необходимости.
