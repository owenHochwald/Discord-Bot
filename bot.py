import discord
import os
import random
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix=".")
client.remove_command("help")
status = cycle([
    'executing commands',
    'contemplating life',
    'doing bot things'
])

filtered_words = ["cunt", "nigger", "nigga"]


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('taking commands'))
    change_status.start()
    print('Bot is ready and online')
# ping command


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# loading cogs


@client.command()
@commands.has_role("El Jefe")
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.has_role("El Jefe")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.has_role("El Jefe")
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
# ----------
# changing task


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
# removing .py

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# adding commands from discordbot.py


@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likley.',
                 'Outlook good.',
                 'Yes.',
                 'Sign point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tel you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Dont count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# ////////////////moderation
# clear command


@client.command()
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)

# banning unabnning


@client.command()
@commands.has_role("El Jefe")
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


@client.command()
@commands.has_role("El Jefe")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
@commands.has_role("El Jefe")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# auto mod


@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)


@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="Help", description="Use .help (command) for extended info on a command.", color=ctx.author.color)
    em.add_field(name="Moderation ('Dont try these only Mod's have access to them)",
                 value="kick, ban, unban, clear, load, unload, reload")
    em.add_field(name="Entertainment (anyone can use these commands)",
                 value="8ball, eightball, ping, test")

    await ctx.send(embed=em)

client.run('ODQ3NjE5OTQ2OTAxMjc0NjQ0.YLAtlw.5vLifKHkTPpSNQqcCOZFgX-H6LM')
