import discord
from discord import app_commands
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service_port = 3000  # muda se quiser

    def qualidade_conexao(self, ping: int) -> str:
        if ping < 10:
            return "🟢 Perfeita"
        elif ping < 100:
            return "🟢 Estável"
        elif ping < 200:
            return "🟡 Média"
        elif ping < 500:
            return "🟠 Ruim"
        elif ping < 700:
            return "🔴 Horrível"
        else:
            return "💀 Inutilizável"

    @app_commands.command(name="status", description="Mostra o status geral do bot")
    async def status(self, interaction: discord.Interaction):
        ping = round(self.bot.latency * 1000)

        websocket_status = "🟢 Conectado" if self.bot.is_ready() else "🔴 Desconectado"
        gateway_status = "🟢 OK" if ping < 300 else "🔴 Ruim"
        qualidade = self.qualidade_conexao(ping)

        shard_info = (
            f"Shard {interaction.guild.shard_id}"
            if interaction.guild and interaction.guild.shard_id is not None
            else "Shard principal"
        )

        embed = discord.Embed(
            title="📡tatus do Sistema",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Hospedagem 24/7",
            value="Render + UptimeRobot",
            inline=False

        )
        embed.add_field(
            name="Servidor Interno",
            value=shard_info,
            inline=True
        )
        embed.add_field(
            name="Porta de Serviço",
            value=str(self.service_port),
            inline=True
        )
        embed.add_field(
            name="WebSocket",
            value=websocket_status,
            inline=True
        )
        embed.add_field(
            name="Gateway Discord",
            value=gateway_status,
            inline=True
        )
        embed.add_field(
            name="Ping",
            value=f"{ping} ms",
            inline=True
        )
        embed.add_field(
            name="Qualidade da Conexão",
            value=qualidade,
            inline=False
        )

        embed.set_footer(text="")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))
