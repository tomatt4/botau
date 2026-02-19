import discord
from discord.ext import commands
from datetime import timedelta
from db import get_conn

CARGO_ID = 1473878349775507579
EXCLUSIVE_ROLE_ID = 1447395230646140999

# =========================
# VIEW DO TICKET PARA PRIMEIRA DAMA
# =========================
class PrimeiraDamaView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Verificar", style=discord.ButtonStyle.success, emoji="🔍")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction)

    async def create_ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        member = guild.get_member(user.id)

        if not guild or not member:
            await interaction.response.send_message(
                "Não consegui te encontrar no servidor.",
                ephemeral=True
            )
            return

        category = discord.utils.get(guild.categories, name="𝐈𝐧𝐟𝐨𝐫𝐦𝐚çõ𝐞𝐬")
        if not category:
            category = await guild.create_category("𝐈𝐧𝐟𝐨𝐫𝐦𝐚çõ𝐞𝐬")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        # Permissões para admins
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                )

        channel_name = f"primeira-dama-{user.name}"
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        # Salvar no banco
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tickets (user_id, channel_id, type) VALUES (%s, %s, %s)",
                (str(user.id), str(channel.id), "Primeira Dama")
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

        await interaction.response.send_message(
            f"Ticket criado: {channel.mention}", ephemeral=True
        )

        exclusive_role_mention = f"<@&{EXCLUSIVE_ROLE_ID}>"
        await channel.send(
            f"{user.mention} {exclusive_role_mention}\n\n"
            f"***Boas vindas ao seu Ticket de Primeira Dama!***\n"
            f"Aqui a staff irá verificar seu print do perfil.\n"
            f"Apenas **administradores** podem visualizar este canal.\n\n"
            f"Envie o print do seu perfil com o **/sph** na sua bio quando estiver pronto."
        )


# =========================
# COG PRIMEIRA DAMA
# =========================
class PrimeiraDama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def primeiradama(self, ctx):
        embed = discord.Embed(
            title="Cargo Primeira Dama",
            description=(
                "O cargo **Primeira Dama** é um cargo especial para quem ajuda "
                "a divulgar o servidor.\n\n"
                "Clique em **Verificar** abaixo para abrir um ticket e enviar seu print do perfil. "
                "A staff irá analisar e conceder o cargo."
            ),
            color=0xFFFFFF
        )

        embed.add_field(
            name="Benefícios",
            value=(
                "3x EXP\n"
                "Pode conceder o cargo para até 2 pessoas\n"
                "GIFs, áudios e anexos liberados\n"
                "Prioridade de voz nas calls"
            ),
            inline=False
        )

        embed.add_field(
            name="Como obter",
            value=(
                "• Clique em **Verificar**\n"
                "• Abra um ticket e envie o print do seu perfil\n"
                "• A staff irá conferir e conceder o cargo"
            ),
            inline=False
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1457448153174376708/1474084563184648333/Logomarca_loja_de_moda_feminina_moderno_vermelho_20260219_133148_0000.png?ex=69988fbb&is=69973e3b&hm=7e174c95aa7a4666c8158c3479d85946d5d6c85ac863a7a5f970a0b29b131556&=&format=webp&quality=lossless&width=1214&height=759")
        await ctx.send(embed=embed, view=PrimeiraDamaView(self.bot))


async def setup(bot):
    await bot.add_cog(PrimeiraDama(bot))
