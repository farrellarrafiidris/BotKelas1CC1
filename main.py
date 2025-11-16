import os 
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv() 

# intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!", intents=intents)

CREATE_CHANNEL_ID = 1439444648782467195  # ganti angka channel ID lo

@bot.event
async def on_voice_state_update(member, before, after):
    # user join trigger channel
    if after.channel and after.channel.id == CREATE_CHANNEL_ID:
        guild = member.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True)
        }

        # bikin channel private
        new_channel = await guild.create_voice_channel(
            f"Kamar {member.name}",
            overwrites=overwrites,
            category=after.channel.category
        )

        # pindahin user ke channel baru
        await member.move_to(new_channel)

    # hapus channel jika kosong dan bukan trigger channel
    if before.channel:
        if (
            before.channel.id != CREATE_CHANNEL_ID
            and len(before.channel.members) == 0
        ):
            await before.channel.delete()

bot.run(TOKEN)
