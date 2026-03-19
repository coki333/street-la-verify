import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# === SERVIDOR WEB PARA RENDER ===
app = Flask('')
@app.route('/')
def home():
    return "<h1>STREET LA - VERIFICATION SYSTEM</h1>"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === CONFIGURACIÓN DEL BOT ===
TOKEN = "MTQ4NDAwNzI5MDI1MTEyMDczMQ.G0I86k.vf0wcNjqaMqiSfUxjoFtJu-RIt2X4yrcM_OWOY"
ROLE_ID = 1432937819030159360 
EMOJI_VERIFICAR = "☠️" 
FOTO_LOCAL = "9c4a502946ce915d8d43e4d7ce68917e.jpg"
WEBHOOK_URL = "https://discord.com/api/webhooks/1479847656812712022/zUSdFk-FD9KWlSDhP-iUUbOMcPBw1pQ7_gryDbeQiFfyu4ZTF27IHzzCerMXPkQCvb6X"

# IMPORTANTE: Activar todos los intents para que lea el comando
intents = discord.Intents.all() 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"--- BOT STREET LA ONLINE: {bot.user} ---")
    print(f"--- VERIFICACIÓN ACTIVADA PARA SERVIDOR FIVEM: STREET LA ---")

@bot.command()
async def setup(ctx):
    # Intentará borrar tu mensaje de !setup para limpiar
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="🏙️ STREET LA VERIFICATION SYSTEM 🏙️",
        description=(
            "**ES:** Reacciona al emoji de abajo para verificar tu acceso.\n"
            "**EN:** React to the emoji below to verify and gain access.\n\n"
            "**🎮 SERVIDOR FIVEM: STREET LA**"
        ),
        color=0x000000 
    )
    embed.set_footer(text="Verified by Street LA System")
    
    # Imagen en GRANDE
    if os.path.exists(FOTO_LOCAL):
        file = discord.File(FOTO_LOCAL, filename="banner.jpg")
        embed.set_image(url="attachment://banner.jpg")
        msg = await ctx.send(file=file, embed=embed)
    else:
        print("No encontré la foto, mandando solo el texto...")
        msg = await ctx.send(embed=embed)
    
    await msg.add_reaction(EMOJI_VERIFICAR)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if str(payload.emoji) == EMOJI_VERIFICAR:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(1483637366047641641)
        
        if role:
            member = guild.get_member(payload.user_id)
            if member:
                try:
                    await member.add_roles(role)
                    print(f"✅ {member.name} se ha verificado en Street LA")
                    
                    # Enviar notificación al webhook
                    await enviar_webhook(member)
                    
                except Exception as e:
                    print(f"Error dando rol: {e}")

async def enviar_webhook(member):
    """Envía una notificación al webhook cuando alguien se verifica"""
    try:
        webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
        
        embed = discord.Embed(
            title="✅ NUEVA VERIFICACIÓN - STREET LA",
            description=f"**Usuario:** {member.mention}\n**ID:** {member.id}\n**Tag:** {member.name}#{member.discriminator}",
            color=0x00ff00
        )
        embed.set_footer(text="Bienvenido a Street LA")
        embed.timestamp = discord.utils.utcnow()
        
        webhook.send(embed=embed)
        
    except Exception as e:
        print(f"Error enviando webhook: {e}")

if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        bot.run(TOKEN)