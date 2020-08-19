import discord
from discord import utils

POST_ID = '745618105983828008' #post id to read reactions from

#roles list according to emotes
ROLES = {
	'💙': '745583364068737076',
	'💚': '745634951852195961',
	'💛': '745634956063146085',
	'💜': '745634959422914632'
}

#exclude this roles from counting
EXCROLES = ()

MAX_ROLES_PER_USER = 5 #max ammount of roles a user can have

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_raw_reaction_add(self, payload):
		channel = self.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=int(ROLES[emoji])) # объект выбранной роли (если есть)
			
			await member.add_roles(role)
			print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
			
		except KeyError as e:
			print('[ERROR] KeyError, no role found for ' + emoji)
		except Exception as e:
			print(repr(e))

	async def on_raw_reaction_remove(self, payload):
		channel = self.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=int(ROLES[emoji])) # объект выбранной роли (если есть)

			await member.remove_roles(role)
			print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

		except KeyError as e:
			print('[ERROR] KeyError, no role found for ' + emoji)
		except Exception as e:
			print(repr(e))

client = MyClient()
client.run('token')
