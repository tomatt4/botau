import discord
from discord.ext import commands
import requests
import os

VT_API_KEY = "75bcda2dec798a0d9e4d7eafd4531e978d8a8002c7e183bf71d9b81d61ce844e"

class VirusTotal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx, url: str):
        """.check url https://exemplo.com"""
        headers = {
            "x-apikey": VT_API_KEY
        }
        data = {"url": url}
        response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
        if response.status_code != 200:
            await ctx.send("Erro ao consultar VirusTotal.")
            return
        
        url_id = response.json()["data"]["id"]
        result = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers).json()
        malicious = result["data"]["attributes"]["last_analysis_stats"]["malicious"]
        if malicious > 0:
            await ctx.send(f"**PERIGO** | A URL {url} é perigosa, e foi marcada como perigosa por **{malicious}** motores.")
        else:
            await ctx.send(f"**SEGURO** | A seguinte URL {url} é seguro.")

async def setup(bot):
    await bot.add_cog(VirusTotal(bot))
