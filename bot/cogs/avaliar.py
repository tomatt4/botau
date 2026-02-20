# arquivo: avaliar.py
import discord
from discord.ext import commands
import asyncio

STAFF_ROLE_ID = 1447395230646140999  # ID do cargo de staff

class avaliar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avaliar_staff")
    async def avaliar_staff(self, ctx):
        """Envia a embed com botão para avaliar staff"""

        embed = discord.Embed(
            title="Avaliação de Staff",
            description="Clique no botão abaixo para avaliar um membro da staff.",
            color=discord.Color.blue()
        )

        class AvaliarView(discord.ui.View):
            @discord.ui.button(label="Avaliar Staff", style=discord.ButtonStyle.green)
            async def avaliar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                guild = interaction.guild
                staff_membros = [m for m in guild.members if any(r.id == STAFF_ROLE_ID for r in m.roles)]

                if not staff_membros:
                    await interaction.response.send_message(
                        "Não encontrei nenhum membro com o cargo de staff.", ephemeral=True
                    )
                    return

                # Criando a view com Select dinâmico
                class StaffSelect(discord.ui.View):
                    def __init__(self, staff_membros):
                        super().__init__()
                        options = [
                            discord.SelectOption(label=m.display_name, value=str(m.id))
                            for m in staff_membros
                        ]
                        select = discord.ui.Select(
                            placeholder="Escolha o staff que deseja avaliar",
                            min_values=1,
                            max_values=1,
                            options=options
                        )
                        select.callback = self.select_callback
                        self.add_item(select)

                    async def select_callback(self, select_interaction: discord.Interaction):
                        staff_id = int(select_interaction.data["values"][0])
                        staff_user = guild.get_member(staff_id)

                        if staff_user is None:
                            await select_interaction.response.send_message(
                                "Não consegui encontrar esse usuário.", ephemeral=True
                            )
                            return

                        # envia DM para o usuário pedindo avaliação
                        try:
                            await select_interaction.user.send(
                                f"Você escolheu avaliar **{staff_user.display_name}**.\n"
                                "Por favor, envie sua avaliação aqui. Depois de enviar, ela será encaminhada para o staff."
                            )

                            await select_interaction.response.send_message(
                                "Te enviei uma DM para enviar sua avaliação!", ephemeral=True
                            )

                            def check(m):
                                return m.author == select_interaction.user and isinstance(m.channel, discord.DMChannel)

                            msg = await self.bot.wait_for("message", check=check, timeout=300)  # 5 min

                            try:
                                await staff_user.send(
                                    f"Você recebeu uma avaliação de {select_interaction.user.mention}:\n\n{msg.content}"
                                )
                                await select_interaction.user.send("Sua avaliação foi enviada com sucesso ✅")
                            except discord.Forbidden:
                                await select_interaction.user.send(
                                    "Não consegui enviar a avaliação para o staff. Ele(a) pode estar com DMs bloqueadas."
                                )

                        except discord.Forbidden:
                            await select_interaction.response.send_message(
                                "Não consegui te enviar uma DM. Verifique suas configurações de privacidade.", ephemeral=True
                            )
                        except asyncio.TimeoutError:
                            await select_interaction.user.send(
                                "Você não respondeu a tempo. Tente novamente clicando no botão."
                            )

                await interaction.response.send_message("Escolha um staff abaixo:", view=StaffSelect(staff_membros), ephemeral=True)

        await ctx.send(embed=embed, view=AvaliarView())

def setup(bot):
    bot.add_cog(avaliar(bot))
