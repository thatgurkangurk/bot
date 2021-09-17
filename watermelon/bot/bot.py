from __future__ import annotations
import os

from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from watermelon import __version__

import hikari
import logging
import lightbulb


class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self._extensions = [
            p.stem for p in Path("./watermelon/bot/extensions/").glob("*.py")
        ]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read()

        super().__init__(
            prefix="-",
            insensitive_commands=True,
            token=token,
            intents=hikari.Intents.ALL,
        )

    def run(self) -> None:

        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.MessageCreateEvent, self.on_message_create)

        super().run(
            activity=hikari.Activity(
                name="https://www.watermelonbot.ml", type=hikari.ActivityType.WATCHING
            ),
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        logging.info("Loading extensions...")
        for ext in self._extensions:
            self.load_extension(f"watermelon.bot.extensions.{ext}")
            logging.info(f" {ext} extension loaded")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        logging.info("BOT READY")
        self.scheduler.start()
        self.event_manager.unsubscribe(hikari.StartedEvent, self.on_started)

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        logging.info("shutting down")
        self.scheduler.shutdown()

    async def on_message_create(self, event: hikari.MessageCreateEvent) -> None:
        if isinstance(event.message.channel_id, hikari.DMChannel):
            return
