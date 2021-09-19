import discord
import random

missing = object()
chars = tuple(r"""0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz""")


class Object:
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', uuid={self.uuid})"

    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.uuid = args[1]
        self.colour = None
        # self.object_class, self.object_id, self.class_id, self.location, self.column_name = \
        #     exec_sql(save_db_filepath, f"SELECT object_class, object_id, class_id, location, column_name FROM objects "
        #     f"WHERE object_id = {object_id}")


class Item(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = {}
        # self.name, self.description, self.weight, self.size, self.emoji, self.image = \
        #     exec_sql(save_db_filepath, f"SELECT name, description, weight, size, emoji, image_link "
        #                                f"FROM {self.object_class} WHERE {self.column_name} = {self.class_id}")

    # def embed_item(self):
    #     out = discord.Embed(title=self.name, description=self.description, colour=0x88FF42)
    #     if isinstance(self.image, str):
    #         out.set_thumbnail(url=self.image)
    #     return out

        # else:
        #     raise Exception("{} not in {}".format(target, filepath))


class Container:
    def __init__(self, size=10) -> None:
        self.size = size
        self.contents = []

    def add_object(self, obj) -> None:
        if len(self.contents) < self.size:
            self.contents.append(obj)
        else:
            raise ValueError("container full")

    def find_object(self, instance=missing, **kwargs):
        """Returns the first instance of an object where attributes match all the key word aruments
        "instance=`class'" can be used to typecheck the object
        will ignore """
        for obj in self.contents:
            if not (instance is missing) and not (type(self) == instance):
                continue
            for key, val in kwargs.items():
                try:
                    if not getattr(obj, key) == val:
                        break
                except AttributeError:
                    break
            else:
                return obj
        raise ValueError("object matching all key word arguments could not be found")

    def find_objects(self, instance=missing, **kwargs) -> tuple:
        pass

    def remove_object(self, obj):
        self.contents.remove(obj)
        return obj

    def follow_path(self, path: list):
        # out = self
        for name in path:
            self = self.find_object(name=name)
        return self

    def return_all(self):
        out = ""
        # print(objs.name)
        for obj in self.contents:
            # print("->", obj.name, hasattr(obj, "contents"))
            out += obj.name + "\n"
            if hasattr(obj, "contents"):
                # print(return_all(obj).split("\n")[:-1])
                out += "- - " + "\n- - ".join(obj.return_all().split("\n")[:-1]) + "\n"
        return out


        # else:
            # raise IndexError("container too small")

    # def embed_contents(self):
    #     description = ""
    #     for i in self.contents:
    #         description += str(i.name) + " " + str(i.emoji) + "\n"
    #     print(description)
    #     return description

class Box(Item, Container):
    def __init__(self, name, uuid, size=3):
        Object.__init__(self, name, uuid)
        Container.__init__(self, size=size)
        self.contents = [Item("Silver Dagger", "123"), Item("Ball", "456")]


class World(Container):
    def __init__(self, name, *args):
        Container.__init__(self, size=256)
        self.name = name
        self.uuids = []

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"#, owner_id='{self.owner_id}')"

    @staticmethod
    def generate_uuid() -> str:
        uuid = ""
        for _ in range(8):
            uuid += random.choice(chars)
        return uuid

    def new_uuid(self) -> str:
        uuid = self.generate_uuid()
        while uuid in self.uuids:
            uuid = self.generate_uuid()



class Character(Object, Container):
    def __init__(self, name: str, uuid) -> None: #  owner_id: str
        Object.__init__(self, name, uuid)
        Container.__init__(self, size=32)
        # self.owner_id = owner_id
        self.species = None
        self.stats = {}
        # self.selected = False

    # def __repr__(self):
        # return f"{self.__class__.__name__}(name='{self.name}')"#, owner_id='{self.owner_id}')"

    # def move_item(self, item, target):
        # pass
        # for i in self.contents:
        #     if i == item:
        #         # pass
        #     # if True:
        #         i.location = target
        #         target.contents.append(i)
        #         self.contents.remove(item)
        #         break

        # if target in execute_sql(filepath, "SELECT COUNT(1) FROM objects WHERE location={} AND object_id={};".format(
        # self.location, self.object_id)):
        # print(execute_sql(filepath, "select location from objects where object_id = {}".format(self.object_id)))
        # exec_sql(save_db_filepath, f"UPDATE objects SET location = '{target}' WHERE object_id = {self.object_id}")
        # print(execute_sql(filepath, "select location from objects where object_id = {}".format(self.object_id)))

            # print(i.name, item)

        # self.name, self.hunger, self.thirst, self.health, self.stamina, self.strength = exec_sql(
            # save_db_filepath, f"SELECT name, hunger, thirst, health, stamina, strength FROM players "
                              # f"WHERE player_id = {self.class_id}")


# class Vehicle(Object):
#     pass
#
#
# class Abstract:
#     pass
#
#
# class NonPlayerCharacter:
#     pass
#
#
# class Location:
#     pass
