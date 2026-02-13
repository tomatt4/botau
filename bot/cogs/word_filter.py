import discord
from discord.ext import commands

class WordFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Palavras proibidas
        self.bad_words = ["nigger", "niggar", "niggers", "niggars", "Nigger", "Niggars", "Niggers", "Niggar", "niggar", "Niggar"]
        # Cargos que podem falar livremente
        self.allowed_roles = ["/salva", "✦  𝐒𝐭𝐚𝐟𝐟", "✦ 𝐀𝐝𝐦𝐢𝐧", "✦ 𝐆𝐞𝐫𝐞𝐧𝐭𝐞", "Lumi", "𝐕𝐢𝐜𝐞 𝐃𝐨𝐧𝐨", "𝐃𝐨𝐧𝐚😴"]  # coloque os nomes exatos dos cargos
        self.staff_channel_name = "geral"  # canal que vai receber os avisos

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Usuário tem cargo liberado? Não punir
        if any(role.name in self.allowed_roles for role in message.author.roles):
            return

        # Verifica palavras proibidas
        if any(word.lower() in message.content.lower() for word in self.bad_words):
            await message.delete()
          
            # Envia aviso para o canal de staff
            staff_channel = discord.utils.get(message.guild.text_channels, name=self.staff_channel_name)
            if staff_channel:
                await staff_channel.send(
                    f"**AVISO** | {message.author.mention} usou palavra proibida: `{message.content}`\n"
                )

async def setup(bot):
    await bot.add_cog(WordFilter(bot))
