import discord
from discord.ext import commands

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="a")
    async def cores_embed(self, ctx):
        embed = discord.Embed(
            title="",
            description=(
                "**ⵈ﹒ʀᴇsᴘᴇɪᴛᴏ⊹◄꯭** ``¡﹒﹒ⵗ``\n"
                "Trate todos com educação, sem ofensas, brigas ou preconceito! :3\n\n"

                "**⏝ᩙ ＞꯭sᴇᴍ ғʟᴏᴏᴅ / sᴘᴀᴍ ꩅ﹕❄**\n"
                "Não envie mensagens repetidas, links ou divulgações sem permissão...\n\n"

                "**¡ᩚᴅɪsᴄᴜssᴏ̃ᴇs ᴅᴇsɴᴇᴄᴇssᴀ́ʀɪᴀs︐＼ׂ Ꮼ ⢷𓈓🍇ᱬ︩︪͑**\n"
                "Evite discussões, provocações ou conflitos no chat, resolva no pv.\n\n"

                "**𐃆͡ ᩡ ᴄᴏɴᴛᴇᴜ́ᴅᴏ +𝟏𝟖﹍﹒ⵗ𖥔ׂ𓂂**\n"
                "Proibido nsfw, gore ou qualquer conteúdo impróprio!\n\n"

                "**ⵗⵗ◌﹐﹒ʀᴇsᴘᴇɪᴛᴇ ᴏs ᴀᴅᴍs 𐙚 💬＼ׂ**\n"
                "Siga as orientações da staff e evite discussões desnecessárias.\n\n"

                "**︵꯭︵＼🌷ᩧ𓈓ᱬ︩︪͑𝄒 ᴄʟɪᴍᴀ ᴀᴍɪɢᴀ́ᴠᴇʟ**\n"
                "Mantenha a house leve, divertida e confortável pra todo mundo!\n\n"

                "**ᩡ♡⃘﹒💢﹒ ᴘᴜɴɪᴄ̧ᴏ̃ᴇs 𓎟**\n"
                "O descumprimento das regras pode resultar em aviso, mute ou ban...\n\n"

                "**ᩡ♡⃘🍡﹍︒ ✿ᩧ  ᴍᴇɴsᴀɢᴇᴍ  ғɪɴᴀʟ  ⵗⵗ◌﹐﹒❥⃘**\n"
                "Esperamos que todos se sintam confortáveis, seguros e bem-vindos aqui ✿\n"
                "Respeite as regras, cuide dos outros membros e mantenha o clima leve e amigável.\n"
                "Assim todo mundo consegue se divertir, fazer amizades e aproveitar a house juntinhos (≧▽≦) 🌸"
            
            ),

            color=0xFFFFF
        )
        await ctx.send(embed=embed)
        embed.set_footer(text="")
        embed.set_image(url="https://i.postimg.cc/qM5bJhNC/d69820617738868f7b39dd1b09e1b19b.jpg")
        

async def setup(bot):
    await bot.add_cog(Embeds(bot))
