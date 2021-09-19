# def format_command(command):
#     args = command.split(" ")


# command = "6d5"
# format_command(command)


# # import re
# # import random

# # string = "10d100d1"


# class Dice:
#     def __init__(self, name, values):
#         self.name = name
#         self.values = values

#     def roll(self):
#         return random.choice(self.values)


# dice = []


# dice.append("lol")


# command_map = {
#     "": 1,
#     "d": 6,
#     "dl": 0,
#     "dh": 0,
#     "min": None,
#     "max": None,
#     "r": None
# }

# find_numbers = re.compile(r"\d+")
# find_count = re.compile(r"\A\d+")
# find_dice = re.compile(r"d\d+")

# count = find_count.findall(string)
# dice = find_dice.findall(string)

# if not 0 < len(dice) < 2 or not 0 < len(count) < 2:
#     raise Exception()

# dice_range = [1, int(find_numbers.search(dice[0]).group())]

# output = []
# for i in range(int(find_numbers.search(count[0]).group())):
#     output.append(random.randint(*dice_range))

# print(output, len(output))
# for j in command_map:
# string.find(j)


# import file_manager
# file_manager.create_map("2200")
# import discord
# import asyncio
# from discord.ext.commands import Bot
# from discord.ext.commands import Bot, has_permissions, CheckFailure
#
#
# client = Bot(description="My Cool Bot", command_prefix=";")
#
#
# @client.event
# async def on_ready():
#     print("Bot is ready!")
#
#
# @client.command(pass_context=True)
# @has_permissions(administrator=False)
# async def whoami(ctx):
#     msg = "You're an admin {}".format(ctx.message.author.mention)
#     await ctx.send(msg)
#
#
# @whoami.error
# async def whoami_error(ctx, error):
#     print("error", error, ctx)
#     if isinstance(error, CheckFailure):
#         msg = "You're an average joe {}".format(ctx.message.author.mention)
#         await ctx.send(msg)
#     else:
#         raise
#
#
# client.run("")
