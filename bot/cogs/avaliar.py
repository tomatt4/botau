# arquivo: avaliar.py
import discord
from discord.ext import commands

STAFF_ROLE_ID = 1447395230646140999  # ID do cargo de staff

class StaffEvaluation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avaliar_staff")
    async def avaliar_staff(self, ctx):
        """Envia a embed com botÃ£o para avaliar staff"""

        embed = discord.Embed(
            title="AvaliaÃ§Ã£o de Staff",
            description="Clique no botÃ£o abaixo para avaliar um membro da staff.",
            color=discord.Color.blue()
        )

        class AvaliarView(discord.ui.View):
            @discord.ui.button(label="Avaliar Staff", style=discord.ButtonStyle.green)
            async def avaliar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                # pega todos os membros com o cargo STAFF_ROLE_ID
                guild = interaction.guild
                staff_membros = [m for m in guild.members if any(r.id == STAFF_ROLE_ID for r in m.roles)]

                if not staff_membros:
                    await interaction.response.send_message(
                        "NÃ£o encontrei nenhum membro com o cargo de staff.", ephemeral=True
                    )
                    return

                # cria dropdown com os staffs
                options = [
                    discord.SelectOption(label=m.display_name, value=str(m.id))
                    for m in staff_membros
                ]

                class StaffSelect(discord.ui.View):
                    @discord.ui.select(
                        placeholder="Escolha o staff que deseja avaliar",
                        min_values=1,
                        max_values=1,
                        options=options
                    )
                    async def select_callback(self, select_interaction: discord.Interaction, select: discord.ui.Select):
                        staff_id = int(select.values[0])
                        staff_user = guild.get_member(staff_id)

                        if staff_user is None:
                            await select_interaction.response.send_message(
                                "NÃ£o consegui encontrar esse usuÃ¡rio.", ephemeral=True
                            )
                            return

                        try:
                            # envia DM para o usuÃ¡rio pedindo a avaliaÃ§Ã£o
                            await select_interaction.user.send(
                                f"VocÃª escolheu avaliar **{staff_user.display_name}**.\n"
                                "Por favor, envie sua avaliaÃ§Ã£o aqui. Depois de enviar, ela serÃ¡ encaminhada para o staff."
                            )

                            await select_interaction.response.send_message(
                                "Te enviei uma DM para enviar sua avaliaÃ§Ã£o!", ephemeral=True
                            )

                            # espera a resposta na DM
                            def check(m):
                                return m.author == select_interaction.user and isinstance(m.channel, discord.DMChannel)

                            msg = await self.bot.wait_for("message", check=check, timeout=300)  # 5 min

                            # envia a avaliaÃ§Ã£o para a DM do staff
                            try:
                                await staff_user.send(
                                    f"VocÃª recebeu uma avaliaÃ§Ã£o de {select_interaction.user.mention}:\n\n{msg.content}"
                                )
                                await select_interaction.user.send("Sua avaliaÃ§Ã£o foi enviada com sucesso âœ…")
                            except discord.Forbidden:
                                await select_interaction.user.send(
                                    "NÃ£o consegui enviar a avaliaÃ§Ã£o para o staff. Ele(a) pode estar com DMs bloqueadas."
                                )

                        except discord.Forbidden:
                            await select_interaction.response.send_message(
                                "NÃ£o consegui te enviar uma DM. Verifique suas configuraÃ§Ãµes de privacidade.", ephemeral=True
                            )
                        except discord.TimeoutError:
                            await select_interaction.user.send(
                                "VocÃª nÃ£o respondeu a tempo. Tente novamente clicando no botÃ£o."
                            )

                await interaction.response.send_message("Escolha um staff abaixo:", view=StaffSelect(), ephemeral=True)

        await ctx.send(embed=embed, view=AvaliarView())

def setup(bot):
    bot.add_cog(StaffEvaluation(bot))
