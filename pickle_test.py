# # import discord
# # import pickle
# # from commands import save, load
# # from objects import Character


# # member = discord.Member
# # chars = []

# # for i in range(5):
# #     chars.append(Character("Bob", member))

# # save(chars)

# # out = load()
# # print(out)
# # import ctypes

# # # list object which is referenced by
# # # my_list
# # my_list = [1, 2, 3]

# # my_list2 = my_list

# # # finding the id of list object
# # my_list_address = id(my_list)

# # # finds reference count of my_list
# # ref_count = ctypes.c_long.from_address(my_list_address).value

# # print(f"Reference count for my_list is: {ref_count}")

# # lst = [1, 2, 3, 4, 5, 6]

# # for i in lst:
# #     if i == 4:
# #         lst.remove(i)

# # print(lst)

# # lst = ["a", "b", "c"]
# # print(lst.pop(0))
# # print(lst)
# # for i in lst:
# #     print(i)

# from objects import *

# obj = Character("Jeff", "1234")
# obj.add_object(Container(size=10))

# print(obj.find_object(size=10))

# # print(help(obj.find_object()))


import discord

print(help(discord.Embed))
