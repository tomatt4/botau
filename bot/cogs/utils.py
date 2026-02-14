import discord
import random
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /limpar
    @commands.hybrid_command(name="limpar", description="Limpa mensagens do canal")
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx: commands.Context, quantidade: int):
        if quantidade > 3000:
            await ctx.send("<:warning:1457445890360086601> **ERRO** | O máximo é **3000** mensagens.")
            return

        await ctx.channel.purge(limit=quantidade + 1)
        msg = await ctx.send(f"<a:verificado:1457792350108647435> | **{quantidade}** mensagens apagadas.")
        await msg.delete(delay=5)

    # /ping
@commands.hybrid_command(name="ping", description="Mostra a latência do bot")
async def ping(self, ctx):  # removeu a anotação
    # 1 em 10.000 chances (0,01%)
    if random.randint(1, 10000) == 1:
        latencia = -1
    else:
        latencia = round(self.bot.latency * 1000)
    
    await ctx.send(f"Pong! Meu tempo de resposta é de `{latencia} milisegundos`")

    # /avatar
    @commands.hybrid_command(name="avatar", description="Mostra o avatar de um usuário")
    async def avatar(self, ctx: commands.Context, usuario: discord.Member = None):
        usuario = usuario or ctx.author
        embed = discord.Embed(title=f"Avatar de {usuario.name}", color=discord.Color.blurple())
        embed.set_image(url=usuario.display_avatar.url)
        await ctx.send(embed=embed)

    # /userinfo
    @commands.hybrid_command(name="userinfo", description="Mostra informações de um usuário")
    async def userinfo(self, ctx: commands.Context, usuario: discord.Member = None):
        usuario = usuario or ctx.author
        roles = [role.mention for role in usuario.roles[1:]]
        embed = discord.Embed(title=f"Informações de {usuario.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=usuario.display_avatar.url)
        embed.add_field(name="ID", value=usuario.id, inline=True)
        embed.add_field(name="Nickname", value=usuario.nick or "Nenhum", inline=True)
        embed.add_field(name="Conta Criada", value=usuario.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Entrou no Servidor", value=usuario.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join(roles) if roles else "Nenhum", inline=False)
        await ctx.send(embed=embed)

    # /serverinfo
    @commands.hybrid_command(name="serverinfo", description="Mostra informações do servidor")
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        membros = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humanos = membros - bots
        canais = len(guild.channels)
        categorias = len(guild.categories)
        meta = 1000
        faltando = max(0, meta - membros)

        embed = discord.Embed(
            title=f"Informações do Servidor: {guild.name}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Quantidade de canais", value=canais, inline=True)
        embed.add_field(name="Quantidade de categorias", value=categorias, inline=True)
        embed.add_field(name="Quantos bots", value=bots, inline=True)
        embed.add_field(name="Quantos membros", value=membros, inline=True)
        embed.add_field(name="Meta de 1000 membros", value=f"Faltam **{faltando}** membros", inline=False)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        await ctx.send(embed=embed)
        
    # /help
    @commands.hybrid_command(name="help", description="Mostra informações do bot")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Seus comandos",
            description=(
                "# Comandos Disponíveis:\n\n"

                "- /ship \n"
                "- /mute \n"
                "- /ban \n"
                "- /expulsar \n"
                "- /afk \n"
                "- /assumir \n"
                "- /painel \n"
                "- /avatar \n"
                "- /help \n"
                "- /casar \n"
                "- /namorar \n"
                "- /beijar \n"
                "- /limpar \n"
                "- /lembrete\n"
                "- /presentear |\n"
                "- /ping \n"
                "- /restaurar \n"
                "- /warn \n"
                "- /userinfo \n"
                "- /serverinfo \n"
                "- /numero\n"
            ),
            color=0x000000
        )
        embed.set_footer(text="Cada comando, cada sistema no bot tem a assinatura do Salva. Fazer um bot desses NÃO é fácil!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utils(bot))
