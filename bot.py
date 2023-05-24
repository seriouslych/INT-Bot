import os
import asyncio
from asyncio import sleep #не забываем
import discord
from discord.ext import commands,tasks

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
  guilds = len(bot.guilds)
  info = "."
  print("Иш сука!".format(info)) #в командную строку идёт инфа о запуске
  while True:
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = f'.хелп', type = discord.ActivityType.playing)) #Идёт инфа о команде помощи (префикс изменить)
    await asyncio.sleep(15)
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = f'за {len(bot.guilds)} серверами', type = discord.ActivityType.watching)) #Инфа о количестве серверов, на котором находится бот.
    await asyncio.sleep(15)
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = f'Иш сука!', type = discord.ActivityType.playing))
    await asyncio.sleep(15)

@bot.command(help='Эта команда повторяет ваше сообщение')
async def эхо(ctx, *, message: str):
    await ctx.send(message)

@bot.command(help='Эта команда позволяет банить пользователя')
@commands.has_permissions(ban_members=True)
async def бан(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"{member.name} был забанен.")


@bot.command(help='Эта команда удаляет определённое количество сообщений')
@commands.has_permissions(manage_messages=True)
async def очистить(ctx, amount=5):
    if amount > 1000:
        await ctx.send("Вы превысили лимит удаления сообщений! Лимит: 1000 сообщений")
        return

    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Удалено {amount} сообщений.")

@bot.command(help='Эта команда показывает аватар пользователя')
async def аватар(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    embed = discord.Embed(title=f"Аватар {member.name}", color=discord.Color.red()) # изменяем цвет на красный
    embed.set_image(url=member.avatar.url)

    await ctx.send(embed=embed)

@bot.command(help='Эта команда показывает информацию про сервер')
async def сервер(ctx):
    server = ctx.guild

    embed = discord.Embed(title=f"Сервер {server.name}", color=discord.Color.red()) # изменяем цвет на красный

    # проверяем, что сервер имеет иконку
    if server.icon:
        embed.set_thumbnail(url=server.icon.url)

    embed.add_field(name="ID", value=server.id, inline=False)
    embed.add_field(name="Создан", value=server.created_at.strftime('%d.%m.%Y %H:%M'))
    embed.add_field(name="Владелец", value=f"{server.owner.mention} ({server.owner.name}#{server.owner.discriminator})")
    embed.add_field(name="Количество участников", value=server.member_count, inline=False)
    embed.add_field(name="Роли", value=", ".join([role.mention for role in server.roles]), inline=False)

    await ctx.send(embed=embed)

@bot.command(help='Эта команда позволяет мьютить пользователя')
@commands.has_permissions(manage_roles=True)
async def мьют(ctx, *members: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Под арестом")

    if not mute_role:
        await ctx.send("Роль 'Muted' не найдена. Создайте эту роль и попробуйте снова.")
        return

    for member in members:
        await member.add_roles(mute_role)

    await ctx.send(f"Участник {', '.join([member.mention for member in members])} замучен.")

@bot.command(help='Эта команда позволяет размьютить пользователя')
@commands.has_permissions(manage_roles=True)
async def размьют(ctx, *members: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Под арестом")

    if not mute_role:
        await ctx.send("Роль 'Muted' не найдена. Создайте эту роль и попробуйте снова.")
        return

    for member in members:
        await member.remove_roles(mute_role)

    await ctx.send(f"Участник {', '.join([member.mention for member in members])} размучен.")

@bot.command(help='Эта команда позволяет кикать пользователя')
@commands.has_permissions(kick_members=True)
async def кик(ctx, member: discord.Member, *, reason=""):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был кикнут с сервера.")

@bot.command(help='Эта команда показывает список команд')
async def хелп(ctx):
    embed = discord.Embed(
        title="Список команд",
        description="Список команд, которые я могу выполнить",
        color=discord.Color.red()
    )

    commands_list = []
    for command in bot.commands:
        # Получаем описание команды
        help_text = command.help or "Описание отсутствует."

        # Получаем аргументы команды
        signature = f"{ctx.prefix}{command.name} {command.signature}"

        # Сохраняем информацию о команде в список
        commands_list.append(f"**{signature}** - {help_text}")

    # Добавляем список команд в embed
    embed.add_field(name="Команды", value="\n".join(commands_list), inline=False)

    # Отправляем embed
    await ctx.send(embed=embed)

bot.run('ADD_BOT_TOKEN_HERE')
