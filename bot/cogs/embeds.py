import discord
from discord.ext import commands

class Embeds(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command(name="cinco_embeds")
    async def cores_embed(self, ctx):
        # Criando os 5 embeds diferentes
        embed1 = discord.Embed(
            title="",
            description="# *<@&1447756713146056745>*\n\n"
            "- *Postar Icons e Banners na Categoria de Decorações*\n"
            "- *Voz Prioritária*\n"
            "- *Fotos, GIFs e áudios no chat*\n"
            "- *Desabafo e Aniversário Prioritário*\n"
            "- *Atendimento de Ticket Profissional*\n"
            "- *Cargo Personalizado*\n\n"
            "# Preço: 45.6K de Sonhos",
            color=0xFFD700
        )
        embed2 = discord.Embed(
            title="",
            description="# *<@&1474103671867310292>*\n\n"
            "- *Todas as permissões do <@&1447756713146056745>*\n"
            "- *Entrada Automática no Queridômetro*\n"
            "- *Gerenciar Figurinhas e Emojis*\n"
            "- *Autoridade Sobre os Membros*\n"
            "- *3.2x EXP na Loritta*\n"
            "- *Conceder o cargo Primeira Dama a 2 Membros*\n"
            
            "# Preço: 50K de Sonhos,
            color=0x000001
        )
        embed3 = discord.Embed(
            title="",
            description="# *<@&1474103441180721162>*\n\n"
            "- *Todas as permissões do <@&1474103671867310292>*\n"
            "- *Comando personalizado no Sukuna*\n"
            "- *Direito a dar o cargo Primeira Dama a 4 membros*\n"
            "- *Desconto de 5,8% nas Cores Personalizadas e Ícones Personalizados*\n\n"
            
            "# Preço: 58.5K de Sonhos",
            color=0xFFFF00
        )
        embed4 = discord.Embed(
            title="",
            description="# *<@&1474103543299575818>*\n\n"
            "- *Todas as permissões do <@&1474103441180721162>*\n"
            "- *Desconto de 10,5% nas Cores Personalizadas e Ícones Personalizados*\n"
            "- *Contato direto com o <@&1446602002246406279> a qualquer hora(na DM)*\n"
            "- *Sugestões com Prioridade*\n"
            "- *5x EXP na Loritta*\n\n"
            
            "# Preço: 65.1K de Sonhos",
            color=0x5865F2
        )
        embed5 = discord.Embed(
            title="",
            description="# *<@&1474103692264476762>*"
            "- *Todas as permissões do <@&1474103543299575818>*"
            "- *Desconto de 23% nas Cores Personalizadas e Ícones Personalizados*"
            "- *6x EXP na Loritta*",
            color=0xFFBF00
        )
        # Enviando todos
        for embed in [embed1, embed2, embed3, embed4, embed5]:
            await ctx.send(embed=embed)


# Para adicionar o cog no bot principal
def setup(bot):
    bot.add_cog(Embeds(bot))
