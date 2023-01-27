
from discord.utils import get
import discord
from discord import ui
from discord.ui import Select, View
import mysql.connector
from io import BytesIO
import time



async def ready(bot):
    await bot.tree.sync()
    print("Bot rodando")

async def visitante(member):
    visitante = get(member.guild.roles, name="❌┃Visitante")
    await member.add_roles(visitante)

async def banco(sql):
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "creative",
        port = 3306

    )
    cursor = db.cursor()
    cursor.execute(sql)
    resposta = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return resposta

#-----------------------------------------------------------WHITELIST-------------------------------------------------

class BtWl(View):
    @discord.ui.button(label="Iniciar whitelist",style=discord.ButtonStyle.green)
    async def test(self,interaction: discord.Interaction,Button:discord.ui.Button):
        
        if interaction.channel.name == "🆔・whitelist":
            
            dc = interaction.user.id
            sql = f"SELECT * FROM bot_respostas WHERE dc = {dc}"
            
            resposta = await banco(sql=sql)
            if(resposta):
                if(resposta[7]):
                    await interaction.response.send_message("Voce ja está em analise! Se achar que ha um erro entre em contato no suporte.",ephemeral=True,delete_after=5.0)
                else:
                    await interaction.response.send_modal(FormWhitelistModal2(timeout=None))
            else:
                await interaction.response.send_modal(FormWhitelistModal(timeout=None))
            
            
class BtWl2(View):
        
    @discord.ui.button(label="Proximas perguntas",style=discord.ButtonStyle.blurple)
    async def test(self,interaction: discord.Interaction,Button:discord.ui.Button):
        
        if interaction.channel.name == "🆔・whitelist":
            
            await interaction.response.send_modal(FormWhitelistModal2(timeout=None))
            
          
class BtAprovar(View):
    
    @discord.ui.button(label="Aprovar Whitelist",style=discord.ButtonStyle.green)
    async def test(self,interaction: discord.Interaction,Button:discord.ui.Button):
        msg = interaction.message.content.split()
        id_five = int(msg[2]) 
        id_dc = msg[5]
        
        sql = f"UPDATE accounts SET whitelist = 1 WHERE id = {id_five}"
        await banco(sql)

        sql = f"DELETE FROM bot_respostas WHERE id_five = {id_five}"
        await banco(sql)
        

        tag_visitante = discord.utils.get(interaction.user.guild.roles, name='❌┃Visitante')
        tag_cidadao = discord.utils.get(interaction.user.guild.roles, name='🏡┃Cidadão Capital')
        member = interaction.user.guild.get_member(int(id_dc))
        await member.add_roles(tag_cidadao)
        await member.remove_roles(tag_visitante)
        await interaction.message.delete()
        await interaction.response.send_message("Cidadão Aprovado")
        canal = discord.utils.get(interaction.user.guild.text_channels, name="🚩・resultado")
        embed = discord.Embed(title="Aprovado ✅", description=f"O cidadão <@{id_dc}> foi aprovado!")
        await canal.send(embed=embed)
        
        #
    @discord.ui.button(label="Reprovar Whitelist",style=discord.ButtonStyle.red)
    async def test2(self,interaction: discord.Interaction,Button:discord.ui.Button):
        uid = interaction.message.content.split()
        id_five = uid[2]
        id_dc = uid[5]
        
        sql = f"DELETE FROM bot_respostas WHERE id_five = {id_five}"
        await banco(sql)
        await interaction.message.delete()
        await interaction.response.send_message("Cidadão Reprovado")
        canal = discord.utils.get(interaction.user.guild.text_channels, name="🚩・resultado")
        embed = discord.Embed(title="Reprovado ❌", description=f"O cidadão <@{id_dc}> foi reprovado!")
        await canal.send(embed=embed)
        
class FormWhitelistModal(ui.Modal, title=f"Whitelist Capital 📄"):

    uid = ui.TextInput(label="Responda 👇",placeholder="Qual o ID apresentado ao entrar na cidade?",style=discord.TextStyle.short)
    p1 = ui.TextInput(label="Responda 👇",placeholder="O que você considera como anti-rp?",style=discord.TextStyle.short)
    p2 = ui.TextInput(label="Responda 👇",placeholder="O que você considera como power-gamming?",style=discord.TextStyle.short)    
    p3 = ui.TextInput(label="Responda 👇",placeholder="O que você considera como meta-gamming?",style=discord.TextStyle.short)    
    p4 = ui.TextInput(label="Responda 👇",placeholder="Você está na rua e é abordado por 2 pessoas armadas, e você está armado, oque você faria?" ,style=discord.TextStyle.long)    
    
    
    async def on_submit(self, interaction: discord.Interaction):
        
        dc = interaction.user.id
        sql = f"INSERT INTO bot_respostas (id_five,dc,p1,p2,p3,p4) VALUES ({self.uid},'{dc}','{self.p1}','{self.p2}','{self.p3}','{self.p4}')"
        await banco(sql)
        bed = discord.Embed(title="Segunda Parte", description="Clique no botão abaixo para as proximas perguntas")
        await interaction.response.send_message(embed=bed,view=BtWl2(timeout=None),ephemeral=True,delete_after=5.0)
        
           
class FormWhitelistModal2(ui.Modal, title="Whitelist Capital 📄"):
    
    p5 = ui.TextInput(label="Responda 👇",placeholder="Qual é a historia do seu personagem?" ,style=discord.TextStyle.long)    
    
    async def on_submit(self, interaction: discord.Interaction):
        dc = interaction.user.id
        sql = f"UPDATE bot_respostas SET p5 = '{self.p5}' WHERE dc = {dc}"
        await banco(sql)
        
        sql = f"SELECT * FROM bot_respostas WHERE dc = {dc}"
        resposta =  await banco(sql)
        
        if(resposta):
            
            canal = discord.utils.get(interaction.user.guild.text_channels, name="📑・avaliar-wl")
            bed = discord.Embed(title="Analise de whitelist",description=f"Formulario feito por: <@{interaction.user.id}>")
            bed.add_field(name="Qual o ID apresentado ao entrar na cidade?",value=f"{resposta[1]}",inline=False)
            bed.add_field(name="O que você considera como anti-rp?",value=f"{resposta[3]}",inline=False)
            bed.add_field(name="O que você considera como power-gamming?",value=f"{resposta[4]}",inline=False)
            bed.add_field(name="O que você considera como meta-gamming?",value=f"{resposta[5]}",inline=False)
            bed.add_field(name="Você está na rua e é abordado por 2 pessoas armadas, e você está armado, oque você faria?",value=f"{resposta[6]}",inline=False)
            as_bytes = map(str.encode,resposta[7])
            content = b"".join(as_bytes)
            await canal.send(f"Historia de <@{interaction.user.id}>",file=discord.File(BytesIO(content),"historia.txt"))
            await canal.send(f"ID cidadão: {resposta[1]} ID discord: {interaction.user.id}",embed=bed,view=BtAprovar(timeout=None))

        await interaction.response.send_message("Concluido, Por favor aguarde até ser aprovado!",ephemeral=True,delete_after=10.0)        
        
        
#-----------------------------------------------------------tICKET-------------------------------------------------

class Ticket(View):
    @discord.ui.select(
        placeholder="Abra um ticket!",
        options=[
            discord.SelectOption(label="Denuncias",description="Aconteceu algum ANTI-RP? Clique aqui.",value="1",emoji="🚨"),
            discord.SelectOption(label="Doações",description="Ja pensou em sair com um carrão? Só clicar aqui.",value="2",emoji="💰"),
            discord.SelectOption(label="Suporte",description="Está precisando de ajuda? Clique aqui.",value="3",emoji="🛠️"),
            discord.SelectOption(label="Bug",description="Está com problemas de bug? Clique aqui.",value="4",emoji="🐛"),
        ]
    )

    async def select_callback(self,interaction,select):
        select.disabled=True
        guild = interaction.guild
        cat_sup = discord.utils.get(interaction.guild.categories, name="[SUPORTE]")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        if select.values[0] == "1":
            canal = await guild.create_text_channel(name=f"🚨 Denuncia-{interaction.user.display_name}",category=cat_sup,overwrites=overwrites)
            await canal.send("🚨 Obrigado por sua denuncia, nossa equipe fará o máximo para te atender. Para adiantar seu atendimento, Por favor mande aqui sua denuncia!",view=BtFecharTiket(timeout=None))
        if select.values[0] == "2":
            canal = await guild.create_text_channel(name=f"💰 Doação-{interaction.user.display_name}",category=cat_sup,overwrites=overwrites)
            await canal.send("💰 Obrigado por sua doação, Pessoas como você são o alicerce desta cidade, nossa equipe terá sempre uma gratidão especial com você. Para adiantar seu atendimento, Por favor mande aqui um resumo!",view=BtFecharTiket(timeout=None))
        if select.values[0] == "3":
            canal = await guild.create_text_channel(name=f"🛠️ Suporte-{interaction.user.display_name}",category=cat_sup,overwrites=overwrites)
            await canal.send("🛠️ Para adiantar seu atendimento, Por favor mande aqui o motivo de sua solicitação!",view=BtFecharTiket(timeout=None))
        if select.values[0] == "4":
            canal = await guild.create_text_channel(name=f"🐛 Bug-{interaction.user.display_name}",category=cat_sup,overwrites=overwrites)
            await canal.send("🐛 Olá, obrigado por se preocupar com nossa cidade, nossa equipe esta trabalhando duro para resolver qualquer tipo de bug. Para adiantar seu atendimento, Por favor mande aqui o motivo de sua solicitação!",view=BtFecharTiket(timeout=None))

        await interaction.response.send_message(f"<a:Verify:1064383261834485901> Ticker aberto em nome de {interaction.user.display_name}, essa mensagem será excluida em breve!",ephemeral=True,delete_after=10.0)  

class BtFecharTiket(View):
        
    @discord.ui.button(label="Fechar Ticket",style=discord.ButtonStyle.red)
    async def test(self,interaction: discord.Interaction,Button:discord.ui.Button):
        adm = discord.utils.get(interaction.user.guild.roles, name='👨‍💼┃Administrador')

        if adm in interaction.user.roles:
            canal = interaction.channel
            await interaction.response.send_message("Este canal será excluido em breve!")

            await canal.delete()
        else:
            await interaction.response.send_message("<a:alert:1064383256037969960> Alerta: Apenas um administrador poderá encerrar seu Ticket",ephemeral=True,delete_after=10.0)
