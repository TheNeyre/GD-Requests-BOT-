import discord
from discord import app_commands
from discord.ext import commands
from discord import Permissions
from config import Config

req_channel_id = Config.req_channel_id
req_result_channel_id = Config.req_result_channel_id
token = Config.token
REQ_Moderator_ID = Config.REQ_Moderator_ID

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix = "v.", intents = intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}.")
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = discord.Embed(
                title='Ошибка!',
                description=f'`У вас недастаточно прав для использования этой команды!'))
        else: await ctx.reply(error, ephemeral = True)


bot = Bot()
bot.remove_command('help')

@bot.event
async def on_ready():
	print('connect')

class ReqQuestion(discord.ui.Modal, title='Анкета для отправки реквестов'):
    GDNickName = discord.ui.TextInput(label='Ваш ник в Geometry Dash',
                                      placeholder='BestNickName')
    
    GDLevelID = discord.ui.TextInput(label='ID Вашего Реквест-Уровня',
                                     placeholder='12345678')
    
    GDShowCase = discord.ui.TextInput(label='Ссылка на Showcase вашего уровня',
                                     placeholder='www.youtube.com/... (необязательно)')

    GDStars = discord.ui.TextInput(label='Сложность уровня в звёздах', placeholder='x')
    
    GDLevelMode = discord.ui.TextInput(label='Режим игры',
                                     placeholder='Классика/Платформер')


    async def on_submit(self, interaction: discord.Interaction):
        channel = bot.get_channel(req_result_channel_id)
        await channel.send(f'''
# REQ SEND <@{REQ_Moderator_ID}>
Member: <@{interaction.user.id}>
`info:`
- GD NICK: {self.GDNickName}
- ID: {self.GDLevelID}
- Showcase: {self.GDShowCase}
- Stars: {self.GDStars}
- Mode: {self.GDLevelMode}
''')
        text = f'''
- GD NICK: {self.GDNickName}
- ID: {self.GDLevelID}
- Showcase: {self.GDShowCase}
- Stars: {self.GDStars}
- Mode: {self.GDLevelMode}
'''
        await interaction.response.defer()
        await interaction.followup.send('# Реквест отправлен!' + '\n' + text, ephemeral=True)

@bot.tree.command(name='send-req-form')
@app_commands.checks.has_permissions(administrator=True)
async def req_form(inter: discord.Interaction):
    channel = bot.get_channel(req_channel_id)
    button = discord.ui.Button(label='Отправить Реквест', style=discord.ButtonStyle.green, custom_id='req')
    embed = discord.Embed(title='Отправка реквестов',
                          description= 'Тут вы можете отправить ваш уровень нашему модератору, а тот перекинет уровень GD-модераторам на оценку!\n```Правила реквестов```\n- Ваш уровень должен соответствовать как правилам проекта, так и правилам игры\n- Нельзя пользоватся данной системой не в серьёз. За ложный реквест вы получите наказание, а позже и блокировку доступа к системе!\n- Вы получите такое-же наказание как и за прошлый пункт, если вы отправите в анкете рофл-уровень!\n- Не используйте систему чрезмерно часто!',
                          color=discord.Color.green())
    view = discord.ui.View().add_item(button)
    await channel.send(embed=embed, view=view)
    await ctx.reply('end!')

@bot.event
async def on_interaction(interaction: discord.Interaction):
    async def give_req_form(interaction: discord.Interaction):
        modal = ReqQuestion()
        await interaction.response.send_modal(modal) # make a code...
        await modal.wait()
    if interaction.data['custom_id'] == 'req':
        await give_req_form(interaction)


bot.run(token)
