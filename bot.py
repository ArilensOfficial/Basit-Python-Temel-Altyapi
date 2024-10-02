import discord
from discord.ext import commands

# Bot'un ihtiyaç duyduğu yetkiler
intents = discord.Intents.default()
intents.members = True  # Üyeler üzerinde işlem yapmak için gerekli izinler

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot hazır olduğunda
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')
    # Komutları sunucuya kaydet
    await bot.tree.sync()
    print("Slash komutları sunucuya kaydedildi.")

# Ping komutu (slash)
@bot.tree.command(name="ping", description="Botun gecikmesini gösterir.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Gecikme: {round(bot.latency * 1000)}ms')

# Ban komutu (slash)
@bot.tree.command(name="ban", description="Bir kullanıcıyı sunucudan yasaklar.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member.mention} sunucudan yasaklandı. Sebep: {reason}')
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok.")

# Kick komutu (slash)
@bot.tree.command(name="kick", description="Bir kullanıcıyı sunucudan atar.")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.mention} sunucudan atıldı. Sebep: {reason}')
    else:
        await interaction.response.send_message("Bu komutu kullanmak için yetkiniz yok.")

# Mute komutu (slash)
@bot.tree.command(name="mute", description="Bir kullanıcıyı susturur.")
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await interaction.response.send_message(f'{member.mention} susturuldu. Sebep: {reason}')

# Unmute komutu (slash)
@bot.tree.command(name="unmute", description="Bir kullanıcının susturmasını kaldırır.")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await interaction.response.send_message(f'{member.mention} susturması kaldırıldı.')
    else:
        await interaction.response.send_message(f'{member.mention} zaten susturulmamış.')

# Clear (mesaj temizleme) komutu (slash)
@bot.tree.command(name="temizle", description="Belirtilen miktarda mesajı siler.")
async def temizle(interaction: discord.Interaction, miktar: int):
    await interaction.channel.purge(limit=miktar)
    await interaction.response.send_message(f"{miktar} mesaj silindi.", ephemeral=True)

# Sunucu bilgisi komutu (slash)
@bot.tree.command(name="sunucu_bilgi", description="Sunucu bilgilerini gösterir.")
async def sunucu_bilgi(interaction: discord.Interaction):
    sunucu = interaction.guild
    bilgi = f"Sunucu adı: {sunucu.name}\nÜye sayısı: {sunucu.member_count}"
    await interaction.response.send_message(bilgi)

# Kullanıcı bilgisi komutu (slash)
@bot.tree.command(name="kullanıcı_bilgi", description="Bir kullanıcının bilgilerini gösterir.")
async def kullanıcı_bilgi(interaction: discord.Interaction, member: discord.Member):
    bilgi = f"Kullanıcı adı: {member.name}\nID: {member.id}\nKatılma tarihi: {member.joined_at}"
    await interaction.response.send_message(bilgi)

# Sunucu daveti oluşturma komutu (slash)
@bot.tree.command(name="davet", description="Sunucuya davet linki oluşturur.")
async def davet(interaction: discord.Interaction):
    davet_link = await interaction.channel.create_invite(max_uses=1, unique=True)
    await interaction.response.send_message(f'Davet linki: {davet_link}')

# Botu çalıştır
bot.run('TOKENINIZI KOYUN') # bot tokeniniz buraya

# Basit Python Temel Bot Altyapısı Pythondeki İlk Yaptığım projelerden ona göre yorum yapınız.