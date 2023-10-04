from . import app
from swibots import CommandEvent, BotContext
from swibots import InlineKeyboardButton, InlineMarkup
from .callback import addToConvo

HELP = """🤖 *Archive Bot*

🌄 <b>Bots Archive</b> is a place where you can showcase your bot or find variety of <b>cool bots</b>!"""


@app.on_command("start")
async def on_start(ctx: BotContext[CommandEvent]):
    user = ctx.event.message.user
    await ctx.event.message.reply_text(
        f"Hi <b>{user.name}</b>!\nYou can submit your bots to bots archive using me!",
        inline_markup=InlineMarkup(
            [[InlineKeyboardButton("🤖 Submit Bot", callback_data=r"submit")]]
        ),
    )


@app.on_command("help")
async def helpMessage(ctx: BotContext[CommandEvent]):
    """Send a attractive help message on help command"""
    m = ctx.event.message
    await m.reply_text(
        HELP,
        inline_markup=InlineMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bots Archive 🔗", url="https://switch.click/bots"
                    ),
                    InlineKeyboardButton(
                        "🐍 Swibots Library",
                        url="https://github.com/switchcollab/Switch-Bots-Python-Library",
                    ),
                ],
            ]
        ),
    )


@app.on_command("submit")
async def submitBot(ctx: BotContext[CommandEvent]):
    await addToConvo(ctx)
