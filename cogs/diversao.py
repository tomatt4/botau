import random

# ==========================================
# COMANDO DE JOGAR TOMATE 🍅
# ==========================================
@commands.command(
    name="tomate", 
    help="Joga um tomate aleatoriamente em uma das 5 mensagens mais recentes."
)
async def tomate(self, ctx):
    # Apaga a mensagem do comando para a cena ficar limpa (opcional)
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    # Pega as últimas 5 mensagens do canal (excluindo a mensagem do comando se não foi deletada)
    mensagens = []
    async for message in ctx.channel.history(limit=5):
        mensagens.append(message)

    if not mensagens:
        return await ctx.send("❌ Não encontrei nenhuma mensagem recente para jogar o tomate!", delete_after=5)

    # Escolhe uma mensagem aleatoriamente entre as 5 obtidas
    mensagem_alvo = random.choice(mensagens)

    try:
        # Reage com o emoji de tomate na mensagem escolhida
        await mensagem_alvo.add_reaction("🍅")
        await ctx.send(
            f"🍅 {ctx.author.mention} jogou um tomate em {mensagem_alvo.author.mention}!",
            delete_after=7
        )
    except discord.HTTPException:
        await ctx.send("❌ Ocorreu um erro ao tentar jogar o tomate.", delete_after=5)
