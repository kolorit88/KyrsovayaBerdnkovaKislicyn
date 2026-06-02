from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)


class SchedulerManager:
    """Централизованное управление периодическими задачами."""

    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    def add_interval_job(self, func, job_id: str, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs):
        """
        Добавить задачу с фиксированным интервалом.

        Args:
            func: асинхронная функция задачи
            job_id: уникальный идентификатор задачи
            hours: часы (по умолчанию 0)
            minutes: минуты (по умолчанию 0)
            seconds: секунды (по умолчанию 0)
            **kwargs: дополнительные аргументы для add_job (например, args, kwargs)
        """
        if hours == 0 and minutes == 0 and seconds == 0:
            raise ValueError("Укажите хотя бы один положительный интервал (hours, minutes или seconds)")

        trigger = IntervalTrigger(hours=hours, minutes=minutes, seconds=seconds)
        self._scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            **kwargs
        )
        logger.info(f"Задача {job_id} запланирована с интервалом {hours}ч {minutes}м {seconds}с")

    def add_cron_job(self, func, cron_expression: str, job_id: str, **kwargs):
        """
        Добавить задачу по cron-выражению (для сложных расписаний).

        Args:
            func: асинхронная функция задачи
            cron_expression: строка cron ("минуты часы дни месяцы дни_недели")
            job_id: уникальный идентификатор задачи
            **kwargs: дополнительные аргументы для add_job
        """
        trigger = CronTrigger.from_crontab(cron_expression)
        self._scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            **kwargs
        )
        logger.info(f"Задача {job_id} запланирована: {cron_expression}")

    def start(self):
        """Запуск планировщика."""
        self._scheduler.start()
        logger.info("Планировщик запущен")

    def shutdown(self, wait: bool = False):
        """Остановка планировщика."""
        self._scheduler.shutdown(wait=wait)
        logger.info("Планировщик остановлен")