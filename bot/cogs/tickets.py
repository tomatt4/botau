import discord
from discord.ext import commands


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="support",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_support"
    )
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Abrindo seu ticket...", ephemeral=True
        )


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.add_view(TicketView())

    @commands.hybrid_command(name="painel")
    async def painel(self, ctx):

        embed = discord.Embed(
            title="Support - Angel's",
            description=(
                ":angels~5: solicite um ticket para denúncias, dúvidas, solicitar cargos, "
                "parcerias ou outros. Basta solicitar algumas das opções e aguardar "
                "um dos adm ou a própria dona."
            ),
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_thumbnail(
    url="https://images-ext-1.discordapp.net/external/hlM6hn4gGRJQaCfShD8vpSxhblrcsKJGag2NWdmjucs/%3Fsize%3D128/https/cdn.discordapp.com/icons/1468775595650318543/a_f1303771b8ed3b822230cf4f0dcab192.gif"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1470128118390984776/1477831994888028190/IMG_5522.jpg"
        )

        await ctx.send(embed=embed, view=TicketView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
