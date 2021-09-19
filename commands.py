import discord
from discord.ext.commands import Bot, Cog, command, has_permissions, is_owner, MinimalHelpCommand, MissingPermissions
from file_manager import save, load, get_prefix
from objects import World, Character, Item, Box, Container
from typing import Union
import requests
import random
import json
import re


object_map = {
    ("world"): World,
    ("character", "char", "characters", "chars"): Character,
    ("item", "items"): Item,
    ("box", "boxes"): Box
}

bot = Bot(command_prefix=get_prefix)

save_name = "save.pickle"


def try_load(save_name):
    try:
        worlds = load(save_name)
        try:
            world = worlds.find_object(name="world")
        except ValueError:
            world = World("world")
            worlds.add_object(world)
        try:
            deleted = worlds.find_object(name="deleted")
        except ValueError:
            deleted = World("deleted")
            worlds.add_object(deleted)
    except (FileNotFoundError, EOFError):
        worlds = Container()
        world = World("world")
        deleted = World("deleted")
        worlds.add_object(world)
        worlds.add_object(deleted)
    return worlds, world, deleted


worlds, world, deleted = try_load(save_name)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        print(f"- {guild.id} ({guild.name})")
    print(f"{bot.user.display_name} is in {str(len(bot.guilds))} guild" +
          ("." if len(bot.guilds) == 1 else "s."))


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ";"

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    del prefixes[str(guild.id)]

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=4)


class Game(Cog):
    @command(aliases=["i", "information"])
    async def info(self, ctx, *path: Union[str, None]):
        all_info = False
        if path[-1] == "all":  # Losing path with "all" as last name, minor
            all_info = True
            path = path[:-1]
        path = list(path)
        if path:
            try:
                worlds.find_object(name=path[0])
            except ValueError:
                path.insert(0, world.name)

            try:
                obj = worlds.follow_path(path)
            except ValueError:
                await ctx.send(embed=discord.Embed(title="Invalid Path", description="The path to the specified object is invalid", colour=0xdd0000))
                return

            info = f"**Class:** {obj.__class__.__name__}\n\n"
            colour = 0xfffffe
            thumbnail = None
            image = None
            footer_text = "‏‏‎ ‎"
            footer_icon = None

            for attr, value in obj.__dict__.items():

                if (attr == "species") and value:
                    info += "**Species: **" + obj.species + "\n\n"

                elif (attr == "description") and value:
                    info += f"**Description:**\n"
                    for key, val in value.items():
                        info += "__" + str(key) + ":__ " + str(val) + "\n"
                    info += "\n"

                elif (attr == "contents") and value:
                    if isinstance(obj, Character):
                        info += f"**Inventory:**\n"
                    else:
                        info += f"**Contents:**\n"

                    for o in value:
                        try:
                            info += " - " + str(o.name) + "\n"
                        except AttributeError:
                            info += " - NO NAME: " + str(o) + "\n"
                    info += "\n"

                elif (attr == "colour") and value:
                    colour = discord.Colour(int(value, 16))

                elif (attr == "thumbnail") and value:
                    thumbnail = value

                elif (attr == "image") and value:
                    image = value

                elif (attr == "footer_text") and value:
                    footer_text = value

                elif (attr == "footer_icon") and value:
                    footer_icon = value

                elif isinstance(value, list) and value:
                    info += f"**{attr.title()}:**\n"
                    for o in value:
                        info += " - " + str(o) + "\n"
                    info += "\n"

                elif isinstance(value, dict) and value:
                    info += f"**{attr.title()}:**\n"
                    for key, val in value.items():
                        info += " - " + str(key) + ": " + str(val) + "\n"
                    info += "\n"

                # elif (attr == "contents") and value:
                #     info += "**Contents:**\n"
                #     for o in obj.contents:
                #         info += " - " + o.name + "\n"
                #     info += "\n"

                else:
                    if all_info:
                        info += "**" + attr.title() + ":** " + str(value) + "\n\n"

            info_embed = discord.Embed(title=obj.name, description=info, colour=colour)
            # info_embed.set_author(name=ctx.author.name, icon_url="https://cdn.discordapp.com/attachments/862716323394224158/863141970427117598/Nughilug.png")
            # info_embed.set_image(url="https://cdn.discordapp.com/attachments/862716323394224158/866039340593315860/unknown.png")
            print("Thumbnail:", thumbnail)
            if thumbnail:
                info_embed.set_thumbnail(url=thumbnail)
            if image:
                info_embed.set_image(url=image)
            # if footer_text:
            if footer_icon:
                try:
                    requests.get(footer_icon)
                    info_embed.set_footer(text=footer_text, icon_url=footer_icon)
                except requests.exceptions.MissingSchema:
                    if footer_text != "‏‏‎ ‎":  # Lose unicode whitespace character possibility, oh well
                        info_embed.set_footer(text=footer_text)

            # info_embed.add_field(name=obj.name, value=info)
            # info_embed.set_footer(text="Footer text", icon_url="https://cdn.discordapp.com/attachments/862716323394224158/863141970427117598/Nughilug.png")

            print(info)
                # description += str(key) + ": " + str(val) + "\n"
            # if hasattr(obj, "description"):
            #     if obj.description:
            #         description += "Description: \n" + obj.description + "\n"
            # if hasattr(obj, "stats"):
            #     if obj.stats:

            await ctx.send(embed=info_embed)
        else:
            await ctx.send(embed=discord.Embed(title="Character Not Found", description=f"Character {name} does not exist"))

    @command(aliases=["n"])
    async def new(self, ctx, object_type: Union[str, None], name: Union[str, None], *args: Union[str, None]):
        if args:
            for arg in args:
                pass
        else:
            for key, val in object_map.items():
                if object_type in key:
                    world.add_object(val(name, world.new_uuid()))
                    save(worlds, save_name)
                    await ctx.send(embed=discord.Embed(title=f"{val.__name__} Added", description=f"{val.__name__} `{name}` successfully created"))
                    break
            else:
                await ctx.send(embed=discord.Embed(title="Object Error", description=f"Object of type '{object_type}' does not exist"))

    @command(aliases=["e"])
    async def edit(self, ctx, path: Union[str, None], *args: Union[str, None]):
        """;edit Bob locket add description Bob is a fierce warrior"""
        path = [path]
        args = list(args)
        add = ("add", "new")
        edit = ("edit", "modify", "mod", "set")
        delete = ("delete", "del")
        if path:
            print("args", args)
            for arg in args:
                print(arg)
                if arg in (add + edit + delete):
                    args = args[len(path) - 1:]
                    try:
                        worlds.find_object(name=path[0])
                    except ValueError:
                        path.insert(0, world.name)

                    try:
                        obj = worlds.follow_path(path)
                    except ValueError:
                        await ctx.send(embed=discord.Embed(title="Path Invalid", description="The path to the specified object is invalid."))
                        return

                if arg in add:
                    try:
                        classtype = args[1]
                    except IndexError:
                        await ctx.send(embed=discord.Embed(title="Missing Argument", description="The type of class is a required argument (can be one of `str`, `dict`, or `list`)"))
                        return

                    try:
                        attr = " ".join(args[2:])
                    except IndexError:
                        await ctx.send(embed=discord.Embed(title="Missing Argument", description="The attribute name is a required argument"))
                        return

                    if classtype == "str":
                        setattr(obj, attr, "")

                    elif classtype == "dict":
                        setattr(obj, attr, {})

                    elif attr == "list":
                        setattr(obj, attr, [])

                    else:
                        print(attr)
                        await ctx.send(embed=discord.Embed(title="Invalid Argument", description="The type of class must be one of `str`, `dict`, or `list`"))
                        return

                    await ctx.send(embed=discord.Embed(title="Attribute Added", description=f"The {classtype} `{attr}` was successfully added to `{obj.name}`"))
                    return

                elif arg in edit:
                    try:
                        attr = args[1]
                    except IndexError:
                        await ctx.send(embed=discord.Embed(title="Missing Argument", description="The name of the attribute is a required argument"))
                        return

                    print("path:", path, "args", args)
                    print("object:", obj)
                    try:
                        value = getattr(obj, attr)
                    except AttributeError:
                        await ctx.send(embed=discord.Embed(title="Attribute Missing", description="`{}` does not have the specified attribute. If you would like to create a new attribute, use `{}edit {} new <dict|list|str> <attrname>`".format(obj.name, get_prefix(bot, ctx), " ".join(path))))
                        return
                    print("value:", value)
                    # if attr == "colour":
                    #     setattr(obj, attr, discord.Colour(int(" ".join(args[2:]))))
                    if attr == "uuid":
                        await ctx.send(embed=discord.Embed(title="Error", description="You cannot modify the uuid of an object"))
                        return

                    elif isinstance(value, dict):
                        print("dis is dict", args[2], " ".join(args[3:]))
                        value[args[2]] = " ".join(args[3:])
                        print(value)
                        print(getattr(obj, attr))

                    elif isinstance(value, list):
                        value.append(" ".join(args[2:]))

                    else:
                        setattr(obj, attr, " ".join(args[2:]))

                    await ctx.send(embed=discord.Embed(title="Edit Complete", description=f"Attribute `{attr}` was successfully modified"))
                    break

                elif arg in delete:
                    try:
                        attr = args[1]
                    except IndexError:
                        await ctx.send(embed=discord.Embed(title="Missing Argument", description="The name of the attribute is a required argument"))
                        return

                    value = getattr(obj, attr)

                    if attr == "uuid":
                        await ctx.send(embed=discord.Embed(title="Error", description="You cannot delete the uuid of an object"))
                        return

                    if attr == "name":
                        await ctx.send(embed=discord.Embed(title="Error", description="You cannot delete the name of an object"))
                        return

                    if isinstance(value, dict):
                        key = " ".join(args[2:])
                        try:
                            del value[key]
                        except KeyError:
                            await ctx.send(embed=discord.Embed(title="Key Not Found", description=f"The key `{key}` could not be found in `{attr}`"))
                            return

                    elif isinstance(value, list):
                        await ctx.send(embed=discord.Embed(title="", description=f"attribute ... was successfully deleted"))
                        # obj.find_object()

                    else:
                        delattr(obj, attr)

                    await ctx.send(embed=discord.Embed(title="ddd", description="dd"))
                    break

                else:
                    path.append(arg)
                    print("Path:", path, "args:", args)

                # try:
                #     world.find_object(name=name)
                #     await ctx.send(embed=discord.Embed(title=f"{object_type.title()} ", description=f"{object_type.title()} {name} successfully created"))
                # except KeyError:
                #     await ctx.send(embed=discord.Embed(title="Object Error", description=f"Object of type '{object_type}' does not exist"))

            save(worlds, save_name)

        else:
            print("no path")

    @command(aliases=["del", "rm"])
    async def delete(self, ctx, *path: Union[str, None]):
        path = list(path)
        if path:
            try:
                worlds.find_object(name=path[0])
            except ValueError:
                path.insert(0, world.name)

            try:
                container = worlds.follow_path(path[:-1])
            except ValueError:
                await ctx.send(embed=discord.Embed(title="Path Invalid", description=f"The path to the specified object is invalid.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                return

            try:
                obj = container.find_object(name=path[-1])
                print(obj.contents)
                worlds.find_object(name="deleted").add_object(obj)
                print(deleted.find_object(name=obj.name).contents)
                container.remove_object(obj)
            except ValueError as e:
                print(e)
                await ctx.send(embed=discord.Embed(title="Invalid Name", description=f"An object called `{path[-1]}` could not be found" + (f" in `{path[-2]}`" if len(path) >= 2 else "") + f".\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                return
            save(worlds, save_name)
            await ctx.send(embed=discord.Embed(title="Object Deleted", description=f"The object `{path[-1]}` was sucessfully deleted", colour=0xdd0000))
        else:
            await ctx.send(embed=discord.Embed(title="Missing Argument", description="Path is a required argument"))

    @command(aliases=["mv"])
    async def move(self, ctx, old_path: Union[str, None], *args: Union[str, None]):
        old_path = [old_path]
        args = list(args)
        if old_path:
            for arg in args:
                if arg in ("to",):
                    new_path = args[len(old_path):]
                    for path in (old_path, new_path):
                        try:
                                worlds.find_object(name=path[0])
                        except (ValueError, IndexError) as error:
                            if isinstance(error, ValueError):
                                path.insert(0, world.name)
                            else:
                                await ctx.send(embed=discord.Embed(title="Path Not Found", description=f"The destination path appears to be missing.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                                return

                    print("Old path, new path:", old_path, new_path)
                    try:
                        old_container = worlds.follow_path(old_path[:-1])
                        print(old_container)
                    except ValueError:
                        await ctx.send(embed=discord.Embed(title="Path invalid", description=f"The path to the specified object is invalid.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                        return
                    # print("Old container:", old_container, old_container.contents)
                    try:
                        obj = old_container.find_object(name=old_path[-1])
                    except ValueError:
                        await ctx.send(embed=discord.Embed(title="Path invalid", description=f"The name of the specified object is incorrect or does not exist.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                        return
                    old_container.remove_object(obj)
                    # print("Old container", old_container, old_container.contents)
                    try:
                        new_container = worlds.follow_path(new_path)
                        print("new container:", new_container)
                    except ValueError:
                        old_container.add_object(obj)
                        await ctx.send(embed=discord.Embed(title="Path invalid", description=f"The destination path is invalid.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                        return
                    try:
                        new_container.add_object(obj)
                    except AttributeError:
                        old_container.add_object(obj)
                        await ctx.send(embed=discord.Embed(title="Object invalid", description=f"'{new_container.name}' is not a container.\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                        return
                    # print("new container", new_container.name, new_container.contents)
                    # print("new container", new_container.name, new_container.contents)

                    await ctx.send("Done")
                    break

                else:
                    old_path.append(arg)

            else:
                await ctx.send(embed=discord.Embed(title="Path Not Found", description=f"The destination path appears to be missing.\nTry separating the object path and the destination path with the keyword `to`\nSee `{get_prefix(bot, ctx)}help move` for more information"))
                return
            save(worlds, save_name)

        else:
            print("no path")

    @command(aliases=["cp"])
    async def copy(self, ctx, *path):
        try:
            container = worlds.follow_path(path[:-1])
        except ValueError as e:
            # raise e
            return

        try:
            obj = container.find_object(name=path[-1])
        except ValueError as e:
            raise e
            return

        container.add_object(obj)
        await ctx.send(embed=discord.Embed(title="Object Copied", description=f"The object `{obj.name}` was successfully copied"))

    @command(aliases=["ls"])
    async def list(self, ctx, *path: Union[str, None]):  # add type filters?
        path = list(path)
        if path:
            try:
                worlds.find_object(name=path[0])
            except ValueError:
                path.insert(0, world.name)

            obj = worlds.follow_path(path)

            try:
                await ctx.send(embed=discord.Embed(title=obj.name + ":", description="\n" + obj.return_all(), colour=0x0044aa))
            except AttributeError:
                await ctx.send(embed=discord.Embed(title="Invalid Object", description=f"The object `{obj.name}` is not a container"))

        else:
            description = worlds.return_all()
            # print(description)
            await ctx.send(embed=discord.Embed(title="World:", description="\n" + description, colour=0x0044aa))

    @command(aliases=["r"])
    async def roll(self, ctx, string: Union[str, None]):
        if string:
            find_numbers = re.compile(r"\d+")
            find_count = re.compile(r"\A\d+")
            find_dice = re.compile(r"d\d+")

            count = find_count.findall(string)
            dice = find_dice.findall(string)

            if (dicelen := len(dice)) == 0:
                message = discord.Embed(
                    title="Error", description="Dice type required, for example: `d6`", colour=0xDD0000)

            elif dicelen > 1:
                message = discord.Embed(
                    title="Error", description="Too many dice type arguments", colour=0xDD0000)

            elif (countlen := len(count)) > 1:
                message = discord.Embed(
                    title="Error", description="Too many dice count arguments", colour=0xDD0000)

            else:
                if countlen == 0:
                    count.append("1")

                dice_range = [1, int(find_numbers.search(dice[0]).group())]
                rolls = []
                for i in range(int(find_numbers.search(count[0]).group())):
                    rolls.append(random.randint(*dice_range))

                message = discord.Embed(
                    title=f":game_die: {string} :game_die:", description="Rolls: `{}`".format(", ".join([str(i) for i in rolls])) + (f"\nTotal: `{sum(rolls)}`" if len(rolls) > 1 else ""), colour=0x44AA00)

        else:
            message = discord.Embed(
                title="Missing Arguments", description=f"Dice type is a required argument, try `{get_prefix(bot, ctx)}roll d6`", colour=0xDD0000)

        await ctx.send(embed=message)

    @command(aliases=["s", "export"])
    async def save(self, ctx, *args: Union[str, None]):
        save(worlds, save_name)
        await ctx.send(file=discord.File(save_name))

    @command(aliases=["l", "import"])
    async def load(self, ctx, url: Union[str, None]):
        with open(save_name, "wb") as f:
            f.write(requests.get(url).content)
        global worlds, world, deleted
        worlds, world, deleted = try_load(save_name)
        # save()
        # load(worlds, save_name)
        # await ctx.send(file=discord.File(save_name))


class Admin(Cog):
    @command(aliases=['p'])
    @has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str = None):
        if new_prefix:
            with open("prefixes.json", 'r') as f:
                prefixes = json.load(f)
            if prefixes[str(ctx.guild.id)] != new_prefix:
                prefixes[str(ctx.guild.id)] = new_prefix

                with open("prefixes.json", 'w') as f:
                    json.dump(prefixes, f, indent=4)

                await ctx.send(embed=discord.Embed(title="Command Prefix Updated",
                                                   description=f"{ctx.author.mention} has changed {bot.user.mention}'s "
                                                               f"command prefix to '{new_prefix}'",
                                                   colour=0xFFFFFE))
            else:
                await ctx.send(embed=discord.Embed(title="Command Prefix Reassignment",
                                                   description=f"{bot.user.mention}'s command prefix is already "
                                                               f"'{new_prefix}'",
                                                   colour=0xBB0000))
        else:
            await ctx.send(embed=discord.Embed(title="Missing Argument",
                                               description=f"Correct usage: `{get_prefix(bot, ctx)}prefix "
                                                           f"<new_prefix>`",
                                               colour=0xBB0000))

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Permission Denied",
                                               description="You do not have administrator permissions",
                                               colour=0xBB0000))
        else:
            raise


class General(Cog):
    @command(aliases=["emoj"])
    async def emojis(self, ctx):
        emojis_list = ""
        for emoji in ctx.guild.emojis:
            for i in range(2):
                if emoji.animated:
                    emojis_list += "<a:"
                else:
                    emojis_list += "<:"
                emojis_list += emoji.name + ":" + str(emoji.id) + ">"
                if i == 0:
                    emojis_list += ": "
                emojis_list += "`"
            emojis_list += "\n"
        await ctx.send(embed=discord.Embed(title="Emojis:", description=emojis_list, colour=0xDDDD00))


class Help(MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            help_embed = discord.Embed(
                title="Help:", description=page, colour=0x3388DD)
            await destination.send(embed=help_embed)


bot.help_command = Help()
