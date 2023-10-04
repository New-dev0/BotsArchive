import asyncio, os, requests
from io import BytesIO
from . import app, AskMode, GroupInfo, PostInfo
from urllib.parse import urlparse
from swibots import CallbackQueryEvent, regexp, BotContext, MessageEvent
from swibots import User, Message
from swibots import EmbeddedMedia, EmbedInlineField
from swibots import InlineMarkup, InlineKeyboardButton, InlineMarkupRemove
from PIL import Image, ImageChops, ImageDraw, ImageFont
from secrets import token_hex


def create_round_image(image):
    bigsize = (image.size[0] * 3, image.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(image.size)
    image.putalpha(mask)
    return image, mask


def generateBotPreview(bot: User):
    new = Image.open("assets/abstract.jpg")
    font = ImageFont.truetype("assets/fonts/BRITANIC.TTF", size=45)
    draw = ImageDraw.Draw(new)
    botImg = None
    if bot.image_url:
        req = requests.get(bot.image_url)
        if req.status_code == 200:
            botImg = Image.open(BytesIO(req.content))
    if not botImg:
        botImg = Image.open("assets/bot.jpg")
    botImg = botImg.resize((230, 230))

    im, _ = create_round_image(botImg)

    cwidth = (new.width // 2) - (botImg.width // 2)

    new.paste(
        im,
        (
            cwidth,
            60,
        ),
        im,
    )
    draw.text(
        (new.width // 2, im.height + 100),
        bot.name,
        anchor="mm",
        fill="white",
        font=font,
    )

    draw.text(
        (new.width // 2, im.height + 140),
        f"@{bot.username}",
        anchor="mm",
        fill="whitesmoke",
        font=ImageFont.truetype("./assets/fonts/PixelifySans.ttf", size=24),
    )
    name = f"{token_hex(8)}.png"
    new.save(name)
    return name


async def sendBotEmbed(bot_username):
    bot = await app.get_user(username=bot_username)
    thumb = generateBotPreview(bot)
    msg = await app.send_message(
        bot.name,
        group_id=PostInfo.id,
        community_id=PostInfo.community_id,
        embed_message=EmbeddedMedia(
            thumbnail=thumb,
            header_name=PostInfo.name,
            description=bot.bio or "Check @bots for more such cool bots! 🎉",
            footer_icon="https://img.icons8.com/?size=256&id=8ujYtGLeAGzW&format=png",
            header_icon="https://img.icons8.com/?size=256&id=59023&format=png",
            footer_title=f"Use @{app.user.user_name} to submit your bots!",
            title=bot.name,
            inline_fields=[[]],
        ),
        inline_markup=InlineMarkup(
            [[InlineKeyboardButton("View bot 🔗", url=bot.link)]]
        ),
    )
    os.remove(thumb)
    return msg


async def addToConvo(ctx):
    """Check for bot username"""
    m: Message = ctx.event.message
    chat_id = m.user_session_id or m.channel_id or m.group_id or m._get_receiver_id()
    AskMode.add(chat_id)
    await m.send("🥳 Send me the bot username to add it to the *Bots Archive 🤖*")
    """
    await asyncio.sleep(3 * 60)
    if chat_id in AskMode:
        await m.send(
            "❌ Too long to respond!!\nRe-Initiate conversation to submit bot 🤖!"
        )
        AskMode.remove(chat_id)
    """


@app.on_callback_query(regexp(r"submit"))
async def submitBot(ctx: BotContext[CallbackQueryEvent]):
    """Handle callback query to ask bot username!"""
    await addToConvo(ctx)


@app.on_callback_query(regexp(r"delete"))
async def deleteMessage(ctx: BotContext[CallbackQueryEvent]):
    await ctx.event.message.delete()


@app.on_callback_query(regexp(r"app(.*)"))
async def approveBot(ctx: BotContext[CallbackQueryEvent]):
    username = ctx.event.callback_data[3:]
    await sendBotEmbed(username)
    await ctx.event.message.edit_text(
        f"@{username} was approved!", inline_markup=InlineMarkupRemove()
    )


@app.on_message()
async def checkUserMessages(ctx: BotContext[MessageEvent]):
    """Check user messages for bot usernames!"""
    m = ctx.event.message
    chat_id = m.user_session_id or m.channel_id or m.group_id or m.user_id
    if chat_id not in AskMode:
        return
    message = m.message
    if not message:
        return
    parse = urlparse(message)
    if parse.netloc and parse.scheme:
        return await m.reply_text(
            "⚠️ Send me bot username (and not bot link) to submit your bot 🤖!"
        )
    user = await app.get_user(username=m.message)
    if not (user and user.is_bot):
        AskMode.remove(chat_id)
        await m.reply_text("🌋 Invalid Bot username provided!")
        return
    await m.reply_text("🎉 Your bot has been submitted! ✅")
    AskMode.remove(chat_id)
    await app.send_message(
        f"{m.user.name} [{m.user.id}] has submitted a bot to review!\n- {user.name} [<copy>{user.username}</copy>]",
        group_id=GroupInfo.id,
        community_id=GroupInfo.community_id,
        inline_markup=InlineMarkup(
            [
                [InlineKeyboardButton("View Bot 🔗", url=user.link)],
                [
                    InlineKeyboardButton(
                        "✅ Approve", callback_data=f"app{user.username}"
                    ),
                    InlineKeyboardButton("Reject ❌", callback_data=f"delete"),
                ],
            ]
        ),
    )
