import discord
from discord.ext import commands
from discord.ext import tasks
from getmail import functie_mail,functie_nume_si_parola,verificare_mail_nou,trimitere_mail,aprindere_bot
from getmail import sfaturi_de_viata

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
 

#comenzi bot

@bot.event
async def on_ready():
    print(f"Bot conectat ca {bot.user}")
    verifica_emailuri.start()


@bot.command()
async def ajutor(ctx):
    await ctx.send("Buna mersi ca ai ales Botul Salutator!\n")
    await ctx.send("Aici este lista comenzilor valabile:\n!test-este comanda de testare.\n!mail (numar_mesaje)-afiseaza mesaje primite pe mail.\n!trimite (nume_recevier) (subiect) (mesaj).\n!citat pentru a primi un sfat.")


@bot.command()
async def test(ctx):
    await ctx.send("Comanda test a funcționat!")

@bot.command()
async def mail(ctx,dimensiune):

    nume_mail,parola=functie_nume_si_parola()
    
    lista_mesaj_mail_subiect,lista_mesaj_mail_from_,lista_mesaj_mail_data=functie_mail(nume_mail,parola,int(dimensiune))
    
    for index in range(0,len(lista_mesaj_mail_subiect)):

        await ctx.send(f"Subiectul mesajului:{lista_mesaj_mail_subiect[index]}")
        await ctx.send(f"Provenienta mesajului:{lista_mesaj_mail_from_[index]}")
        await ctx.send(f"Data si ora mesajului:{lista_mesaj_mail_data[index]}")
        await ctx.send("----------------------------------------------------")


@bot.command()
async def trimite(ctx,nume_primitor,subiect_mesaj,*,corp_mesaj):
    trimitere_mail(nume_primitor,subiect_mesaj,corp_mesaj=corp_mesaj)
    await ctx.send("Mesajul a fost trimis cu succes!")


@bot.command()
async def citat(ctx):
    sfat=sfaturi_de_viata()

    await ctx.send(sfat[0])
    await ctx.send(sfat[1])

@tasks.loop(seconds=20)
async def verifica_emailuri():
    
    verificare=verificare_mail_nou()

    if verificare==True:
        canal = bot.get_channel(1176178364571201548) 
        await canal.send("BIP BAP BIP MAIL NOU!")


aprindere_bot(bot)
