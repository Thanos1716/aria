from commands import General, Admin, Game, bot
import os


def main():
    bot.add_cog(General(bot))
    bot.add_cog(Admin(bot))
    bot.add_cog(Game(bot))

    if os.path.isdir("/home/runner"):  # Checks if running on a replit server
        import keep_alive
        keep_alive.keep_alive()
    else:
        import dotenv
        dotenv.load_dotenv()

    bot.run(os.getenv("Consciousness"))


if __name__ == "__main__":
    main()
