# src/discord_bot/bot.py
import discord
from discord.ext import commands
from src.core.chatbot import chat_once
import os

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(command_prefix="!", intents=INTENTS)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, query: str):
    workspace = f"discord:{ctx.guild.id}:{ctx.channel.id}"
    user_id = str(ctx.author.id)
    await ctx.channel.typing()
    reply = chat_once(workspace, user_id, query)
    await ctx.reply(reply[:1900])  # keep under Discord limit

bot.run(os.getenv("DISCORD_TOKEN"))
