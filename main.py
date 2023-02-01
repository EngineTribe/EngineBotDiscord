from nextcord import (
    Interaction
)
from nextcord.ext import commands

from config import *
import api
from activates import (
    Register
)
from locales import (
    get_locale_model
)

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(
    description="Register in SMM:WE (Engine Tribe)",
    guild_ids=GUILD_IDS,

)
async def register(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' in user_info_response:
        await interaction.response.send_modal(
            Register(
                locale_model=locale_model
            )
        )
    else:
        await interaction.send(
            locale_model.ALREADY_REGISTERED
        )


@bot.slash_command(
    description="Change password",
    guild_ids=GUILD_IDS,
)
async def password(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' in user_info_response:
        await interaction.send(
            locale_model.NOT_REGISTERED
        )
    else:
        pass  # TODO


bot.run(BOT_TOKEN)
