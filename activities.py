from nextcord.ui import (
    TextInput,
    Modal,

)
from nextcord import (
    Interaction
)

from locales import *
import api
from utils import (
    calculate_password_hash
)


class Register(Modal):
    def __init__(self, locale_model: LocaleModel):
        self.locale_model = locale_model
        super().__init__(
            self.locale_model.REGISTER_TITLE,
            timeout=5 * 60
        )
        self.register_username = TextInput(
            placeholder=self.locale_model.USERNAME,
            label=self.locale_model.USERNAME,
            min_length=3,
            max_length=25
        )
        self.register_password = TextInput(
            placeholder=self.locale_model.PASSWORD,
            label=self.locale_model.PASSWORD,
            min_length=7,
            max_length=30
        )
        self.register_confirm_password = TextInput(
            placeholder=self.locale_model.CONFIRM_PASSWORD,
            label=self.locale_model.CONFIRM_PASSWORD,
            min_length=7,
            max_length=30
        )
        self.add_item(self.register_username)
        self.add_item(self.register_password)
        self.add_item(self.register_confirm_password)

    async def callback(self, interaction: Interaction):
        if self.register_password.value != self.register_confirm_password.value:
            await interaction.response.send_message(
                self.locale_model.PASSWORD_MISSMATCH
            )
            return
        elif (not self.register_username.value.isalnum()) or ' ' in self.register_username.value:
            await interaction.response.send_message(
                self.locale_model.ALPHANUMERIC_USERNAME
            )
            return
        elif (not self.register_password.value.isalnum()) or ' ' in self.register_password.value:
            await interaction.response.send_message(
                self.locale_model.ALPHANUMERIC_PASSWORD
            )
            return
        else:
            try:
                response_json = await api.user_register(
                    username=self.register_username.value,
                    im_id=interaction.user.id,
                    password_hash=calculate_password_hash(
                        self.register_password.value
                    )
                )
                if 'success' in response_json:
                    await interaction.send(
                        f'✅ **{self.register_username.value}** {self.locale_model.REGISTER_SUCCESS}'
                    )
                else:
                    if response_json['error_type'] == '035':
                        await interaction.send(
                            f'{self.locale_model.ALREADY_REGISTERED}'
                            f'{self.locale_model.YOUR_USERNAME_IS} **{response_json["username"]}**'
                        )
                    elif response_json['error_type'] == '036':
                        await interaction.send(
                            self.locale_model.USERNAME_ALREADY_TAKEN
                        )
                    else:
                        await interaction.send(
                            self.locale_model.UNKNOWN_ERROR + '\n' +
                            f"{response_json['error_type']} - {response_json['message']}"
                        )
            except Exception as e:
                await interaction.send(
                    self.locale_model.UNKNOWN_ERROR + '\n' + str(e)
                )


class ChangePassword(Modal):
    def __init__(self, locale_model: LocaleModel):
        self.locale_model = locale_model
        super().__init__(
            self.locale_model.PASSWORD,
            timeout=5 * 60
        )
        self.password = TextInput(
            placeholder=self.locale_model.PASSWORD,
            label=self.locale_model.PASSWORD,
            min_length=7,
            max_length=30
        )
        self.confirm_password = TextInput(
            placeholder=self.locale_model.CONFIRM_PASSWORD,
            label=self.locale_model.CONFIRM_PASSWORD,
            min_length=7,
            max_length=30
        )
        self.add_item(self.password)
        self.add_item(self.confirm_password)

    async def callback(self, interaction: Interaction):
        if self.password.value != self.confirm_password.value:
            await interaction.response.send_message(
                self.locale_model.PASSWORD_MISSMATCH
            )
            return
        elif (not self.password.value.isalnum()) or ' ' in self.password.value:
            await interaction.response.send_message(
                self.locale_model.ALPHANUMERIC_PASSWORD
            )
            return
        else:
            try:
                response_json = await api.update_password(
                    user_identifier=interaction.user.id,
                    im_id=interaction.user.id,
                    password_hash=calculate_password_hash(
                        self.password.value
                    )
                )
                if 'success' in response_json:
                    await interaction.send(
                        self.locale_model.PASSWORD_CHANGE_SUCCESS
                    )
                else:
                    if response_json['error_type'] == '006':
                        await interaction.send(
                            self.locale_model.UNKNOWN_USER
                        )
                    else:
                        await interaction.send(
                            self.locale_model.UNKNOWN_ERROR + '\n' +
                            f"{response_json['error_type']} - {response_json['message']}"
                        )
            except Exception as e:
                await interaction.send(
                    self.locale_model.UNKNOWN_ERROR + '\n' + str(e)
                )
