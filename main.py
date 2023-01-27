import discord
from discord.ext import commands
from discord.utils import get
from discord.ui import Select, View
from discord import app_commands
import Modulos.Gerente as gerente

from decouple import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

activity = discord.Game(name="Capital Roleplay")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity, status=discord.Status.online)

#gerente

@bot.event
async def on_ready():
   await gerente.ready(bot)    

@bot.event
async def on_member_join(member):
    await gerente.visitante(member)

#comandos
@bot.tree.command(name="whitelist",description="Cria um botão de whitelist em um canal")
async def whitelist(interaction: discord.Integration):

    adm = discord.utils.get(interaction.user.guild.roles, name='👨‍💼┃Administrador')

    if adm in interaction.user.roles:
       bed = discord.Embed(title="<a:Verify:1064383261834485901>   Formulario para Whitelist",description="Selecione um botão abaixo para iniciar o seu formulario") 
       await interaction.response.send_message(embed=bed,view=gerente.BtWl(timeout=None))
        

    else:
        #TODO MANDAR PARA O CANAL DE LOG

        await interaction.response.send_message("Epa, você não tem permissão para isso. nossa equipe foi avisada dessa tentativa!",delete_after=10.0, ephemeral=True)

@bot.tree.command(name="ticket",description="Cria um menu para abrir ticket")
async def ticket(interaction: discord.Interaction):
    
    adm = discord.utils.get(interaction.user.guild.roles, name='👨‍💼┃Administrador')
    
    if adm in interaction.user.roles:
       bed = discord.Embed(title="<a:Verify:1064383261834485901>   Sistema de Tickets",description="Selecione abaixo o método de atendimento") 
       await interaction.response.send_message(embed=bed,view=gerente.Ticket(timeout=None))


@bot.tree.command(name="teste")
async def teste(interaction: discord.Interaction):
    emoji = "\:Verify:"
    await interaction.response.send_message(emoji)
bot.run(config("TOKEN"))