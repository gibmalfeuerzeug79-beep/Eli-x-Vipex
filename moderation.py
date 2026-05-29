import discord
from discord.ext import commands
from datetime import timedelta

os.getenv(TOKEN)

ALLOWED_USERS = [
    662596869221908480, #Yuqii
    1159469934989025290, #Eli
    1280038439202590802, #Alicia
    1435760640475009117 #Vapexxxxx

]
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

def is_allowed():
    async def predicate(ctx):
        print("Author:", ctx.author.id)
        return ctx.author.id in ALLOWED_USERS

    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
@is_allowed()
async def to(ctx, member: discord.Member, minutes: int, *, reason="No Reason"):
    duration = timedelta(minutes=minutes)

    await member.timeout(duration, reason=reason)

    await ctx.send(
        f"{member.mention} was for {minutes} minutes timeoutet \nReason: {reason}"
    )

@bot.command(name="rto")
@is_allowed()
async def remove_timeout(ctx, member: discord.Member):

    await member.timeout(None)

    await ctx.send(
        f"Timeout from {member.mention} has been removed."
    )

@bot.command()
@is_allowed()
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send("got kicked")

@kick.error
async def kick_error(ctx, error):
    print(error)

    if isinstance(error, commands.CheckFailure):
        await ctx.send("No Permissions. Ask @yuqii.de for your Permissions!")

bot.run(TOKEN)
