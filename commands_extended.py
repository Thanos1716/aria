
    @command(aliases=["m"])
    async def map(self, ctx, seed: str = None):
        if seed:
            seed = seed.zfill(4)[:4]
            try:
                file = discord.File(
                    f"saves/{file_manager.savename}/{seed}.png")
            except FileNotFoundError:
                await ctx.send(embed=discord.Embed(title="Generating Map...", colour=0x001A67))
                file_manager.create_map(seed)
                file = discord.File(
                    f"saves/{file_manager.savename}/{seed}.png")
            e = discord.Embed(colour=0x001A67)
            e.set_image(url=f"attachment://{seed}.png")
            await ctx.send(file=file, embed=e)
        else:
            await ctx.send(embed=discord.Embed(title="Missing argument",
                                               description=f"Correct usage: `{get_prefix(bot, ctx)}map <seed>`",
                                               colour=0xBB0000))


    @command(aliases=["t"])
    async def test(self, ctx):
        with open("datapacks/default_datapack/resourcepacks/default 64bit/mossy_rock.png", "rb") as f:
            try:
                await ctx.guild.me.edit(nick=(ctx.author.nick if ctx.author.nick else ctx.author.name))
                await bot.user.edit(avatar=f.read())
            except discord.errors.HTTPException:
                pass
        await ctx.send("LOL MUCH EPIC")


    @command(aliases=["i"])
    async def inventory(self, ctx, target: Union[discord.Member, str, None], *, item: str = None):

        # If first word isn't a member, add the target field to the item field and set the target player to author
        if not isinstance(target, discord.Member):
            if target and (item is None):
                item = target
            elif target and item:
                item = f"{target} {item}"
            target = ctx.author

        # If item field exists, if found, send item as embed otherwise send item not found embed
        if item:
            found = False
            for o in object_list:
                if o.location == str(target.id) and o.name == item:
                    await ctx.send(embed=o.embed_item())
                    found = True
                    break

            if not found:
                await ctx.send(
                    embed=discord.Embed(title="Item Not Found",
                                        description="The item {} is not in {} inventory".format(
                                            item, target.display_name + "'s" if target != ctx.author else "your"),
                                        colour=0xFF8800))

        # Otherwise, send full target inventory embed
        else:
            found = False
            for p in object_list:
                if p.object_class == "players" and p.class_id == target.id:
                    await ctx.send(embed=discord.Embed(
                        title=("Your" if p.class_id ==
                               target.id else p.name + "'s") + " Inventory",
                        description=p.embed_contents(), colour=0xFF8800))
                    found = True
            if not found:
                await ctx.send(embed=discord.Embed(
                    title="Search by ID",
                    description="Currently not supported, please use `<@target>` instead", colour=0xFF8800))


    @command()
    @is_owner()
    async def sql(self, ctx, *, code):
        await ctx.send(embed=discord.Embed(title="Output:", description=str(
            exec_sql("datapacks/default_datapack/default_items.db", code)), colour=0xFFFFFE))

    @sql.error
    async def sql_error(self, ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send(embed=discord.Embed(title="Permission Denied",
                                               description="You must be the owner of this bot to use this command",
                                               colour=0xBB0000))
        else:
            raise


            if action in ("select", "s"):
                if name:
                    old_char = find_object(name=name, owner_id=ctx.author.id, selected=True, instance=Character)
                    new_char = find_object(name=name, owner_id=ctx.author.id, instance=Character)

                    if new_char:
                        if new_char.selected == True:
                            await ctx.send(embed=discord.Embed(title="Character Selected", description=f"{name} is already selected"))
                        else:
                            new_char.selected = True
                            if old_char:
                                old_char.selected = False
                        await ctx.send(embed=discord.Embed(title="Character Selected", description=f"{name} has been selected"))
                    else:
                        await ctx.send(embed=discord.Embed(title="Character Not Found", description=f"Character {name} does not exist"))


    # object_ids = exec_sql(save_db_filepath, "SELECT object_id, object_class FROM objects")
    # print(object_ids)
    # for i in range(len(object_ids)):
    #     if object_ids[i][1] == "items":
    #         object_list.append(Item(object_ids[i][0]))
    #         print(object_list[i])#.location)
    #     elif object_ids[i][1] == "players":
    #         object_list.append(Character(object_ids[i][0]))






# import math
# import sqlite3
# import numpy as np
# from noise import snoise2  # pnoise2, ???
# from PIL import Image


# def get_temp(x, y):
#     t_octaves = 8
#     t_freq = 512
#     return int(snoise2(x / t_freq, y / t_freq, t_octaves) * 128) + 127  # Temp


# def get_elevation(x, y, x_max, y_max):
#     e_octaves = 6
#     e_freq = 32 * e_octaves
#     grad_max = 191
#     grad_min = 63
#     max_dist = math.sqrt(x_max ** 2 + y_max ** 2)
#     grad = int(grad_max - math.sqrt(
#         ((((x_max / 2) - (x % x_max)) / max_dist) * ((grad_max - grad_min) * 2)) ** 2 + (
#                 (((y_max / 2) - (y % y_max)) / max_dist) * ((grad_max - grad_min) * 2)) ** 2))
#     grad += int(snoise2(x / e_freq, y / e_freq, e_octaves) * 64)  # Elevation noise
#     return grad


# def get_humidity(x, y):
#     h_octaves = 2
#     h_freq = 256
#     return int(snoise2(x / h_freq, y / h_freq, h_octaves) * 128) + 127  # Humidity


# # def get_adjacent(x, y, img, rec):
# #     img[x, y] = [30, rec*20, rec*20, 255]
# #     found = 0
# #     inds = 0
# #     for i in range(-1, 2):
# #         for j in range(-1, 2):
# #             if get_elevation(x + j, y + i) < get_elevation(x, y) and rec > 0:
# #                 if get_elevation(x + j, y + i) == min(min(
# #                 get_elevation(x + k, y + l) for k in range(-1, 2)) for l in range(-1, 2)):
# #                     get_adjacent(x + j, y + i, img, rec-1)
# #                     print("Recursion", rec, end="\n")
# #                     found += 1
# #                 else:
# #                     img[x + j, y + i] = [30, rec * 20, rec * 20, 255]
# #                     print("Spread", end=" ")
# #                     inds += 1
# #     if found >= 1:
# #         img[x, y] = [200, 200, 0, 255]
# #
# #     if inds >= 1:
# #         img[x, y] = [255, 0, 255, 255]
# #
# #     if found >= 1 and inds >= 1:
# #         img[x, y] = [0, 0, 0, 255]


# def create_map(seed):
#     y_max = 512
#     x_max = y_max

#     seed = list(str(seed))
#     x_add, y_add = int(seed[0] + seed[1]) * x_max, int(seed[2] + seed[3]) * y_max
#     seed = "".join(seed)

#     arr = np.zeros([x_max, y_max, 4], dtype=np.uint8)
#     arr[:, :, 3] = 255

#     y_max, x_max = arr.shape[:2]

#     for y in range(y_max):
#         for x in range(x_max):
#             val = [0, 0, 0, 255]

#             temp = get_temp(x + x_add, y + y_add)  # Temp
#             elevation = get_elevation(x + x_add, y + y_add, x_max, y_max)
#             humidity = get_humidity(x + x_add, y + y_add)

#             # if val[1] < 128:
#             #     val = [0, 36, 69, 255]
#             # elif val[0] > 128 and val[2] > 128:
#             #     val = [67, 213, 82, 255]
#             # elif val[0] > 128:
#             #     val = [210, 194, 12, 255]
#             # else:
#             #     pass

#             if elevation < 127:  # Ocean
#                 val = [0, 36, 69, 255]

#             elif 148 > elevation and temp > 148:  # Beach
#                 val = [255, 191, 0, 255]

#             elif elevation > 174 and temp < 88:  # Snow
#                 val = [255, 255, 255, 255]

#             elif humidity + int(snoise2(x, y, 100) * 128 + 127) > 255:  # Trees
#                 val = [0, 63, 0, 255]  # [0, 63, 0, 255]

#             else:
#                 val = [0, 127, 0, 255]

#             if int(snoise2(x, y, 100) * 128 + 127) > 226 and elevation >= 127:  # Villages
#                 val = [0, 0, 0, 255]

#             # if int(snoise2(x, y, 100) * 128 + 127) > 226 and elevation >= 175:  # Springs
#             #     val = [255, 0, 0, 255]
#             #     print("Elevation: " + str(elevation))

#             if x == 245 and y == 245:
#                 val = [255, 0, 0, 255]

#             # val = [temp, elevation, humidity, 255]

#             for i in range(4):
#                 if val[i] > 255 or val[i] < 0:
#                     pass
#                     raise ValueError(f"List index out of range where x = {x} and y = {y}, val = {val}")

#             # val = [elevation, 0, 0, 255]

#             arr[y, x] = val

#     # for y in range(y_max):
#     #     for x in range(x_max):
#     #         print(list(arr[y, x, :]))
#     # if list(arr[y, x]) == [255, 0, 0, 255]:
#     #     print(x, y)
#     #     get_adjacent(x, y, arr, 19)

#     img = Image.fromarray(arr, 'RGBA')
#     img.save(f'saves/{savename}/{seed}.png')


# def exec_sql(path, *code):
#     try:
#         with sqlite3.connect(path) as conn:
#             cur = conn.cursor()
#             rows = []

#             for arguments in range(len(code)):
#                 cur.execute(code[arguments])
#                 rows += cur.fetchall()
#             for x in range(len(rows)):
#                 for cols in range(len(rows)):
#                     if len(rows[cols]) == 1:
#                         rows[cols] = rows[cols][0]
#                 if len(rows) == 1:
#                     rows = rows[0]
#                 conn.commit()

#         return rows
#     except sqlite3.Error as error:
#         raise Exception(f"SQLError: {error} in code '{code}'")


    # @command(aliases=["char"])
    # async def character(self, ctx, action: Union[str, None], name: Union[str, None], key: Union[str, None], value: Union[str, None], value2: Union[str, None]):
    #     if action:
    #         if action in ("new", "n"):
    #             if name:
    #                 world.contents.append(Character(name, ctx.author.id))
    #                 save(world, "save")
    #                 await ctx.send(embed=discord.Embed(title="New Character Created", description=f"Character {name} was sucessfully created."))#\nTo select {name}, type `{get_prefix(bot, ctx)}character select '{name}'`"))
    #             else:
    #                 await ctx.send(embed=discord.Embed(title="Error", description="Character name is a required argument"))

    #         elif action in ("delete",):
    #             if name:
    #                 if world.find_object(name=name, delete=True):
    #                     await ctx.send(embed=discord.Embed(title="Character Deleted", description=f"Character {name} was successfully deleted"))
    #                 else:
    #                     await ctx.send(embed=discord.Embed(title="Character Not Found", description=f"Character {name} does not exist"))

    #         elif action in ("edit", "e"):
    #             character = world.find_object(name=name)
    #             if character:
    #                 if key in ("name",):
    #                     await ctx.send(embed=discord.Embed(title="Character Updated", description=f"{character.name} has been renamed to {value}"))
    #                     character.name = value

    #                 elif key in ("description",):
    #                     character.description = value
    #                     await ctx.send(embed=discord.Embed(title="Character Updated", description=f"{name}'s description has been updated"))

    #                 elif key in ("stats",):
    #                     character.stats[value] = value2

    #                 else:
    #                     await ctx.send(embed=discord.Embed(title="Invalid Argument", description=f"Argument `key` is invalid. Must be one of `<name|description|stats>`"))

    #                 save(world, "save")

    #             else:
    #                 await ctx.send(embed=discord.Embed(title="Character Not Found", description=f"Character {name} does not exist"))


    #         elif action in ("list", "ls", "l"):
    #             out = ""
    #             print(world)
    #             for c in world.contents:
    #                 if isinstance(c, Character):
    #                     # if c.owner == ctx.author:
    #                     out += c.name + "\n"
    #             if out:
    #                 await ctx.send(embed=discord.Embed(title="Your Characters", description=out, colour=0x0033FF))
    #             else:
    #                 await ctx.send(embed=discord.Embed(title="No Characters Available", description=f"You have not created a character yet.\nCreate one with `{get_prefix(bot, ctx)}newcharacter <name>` ", colour=0x0033FF))

    #     else:
    #         await ctx.send(embed=discord.Embed(title="Missing Argument", description=f"Arguments should bo formatted as such:\n`{get_prefix(bot, ctx)}character <select|new|delete|edit|list>`"))
