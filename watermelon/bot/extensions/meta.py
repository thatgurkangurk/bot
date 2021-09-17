import hikari
import lightbulb
from watermelon.bot.bot import Bot


class Meta(lightbulb.Plugin):
    def __init__(self):
        super().__init__()

    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f}ms")


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")
