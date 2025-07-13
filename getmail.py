from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header
import pickle
from smtplib import SMTP
import random


def functie_nume_si_parola():

    with open("date.txt","r") as fisier:

        parola = fisier.readline()
        nume_mail = fisier.readline()
        
    return nume_mail,parola

#aici am luat numele si parola din fisierul date.txt
    
def spatiu_sageti():
    print("------------------------------------------------------------------------------")
        
#liniiii

def decodare_mesaj(mesaj):

    subiect = decode_header(mesaj["Subject"])[0][0]

    from_ = decode_header(mesaj.get("From"))[0][0]

    data = decode_header(mesaj.get("Date"))[0][0]
    
    return subiect, from_, data

#aici decodez datele din mesaj

def functie_mail(username, parola, limita=1):
    lista_mesaj_mail_subiect = []
    lista_mesaj_mail_from_ = []
    lista_mesaj_mail_data = []
    lista_mesaj_mail_corp = []  # Adăugat pentru a stoca corpul e-mailurilor

    with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
        mail.login(username, parola) 
        mail.select("inbox")
        reusita, mesaje = mail.search(None, "ALL")
        mesaj_id = mesaje[0].split()
        mesaj_id = mesaj_id[-limita:]

        for id in mesaj_id:
            reusita, msg_data = mail.fetch(id, "(RFC822)")
            if reusita == "OK":
                mesaj = email.message_from_bytes(msg_data[0][1])
                subiect, from_, data = decodare_mesaj(mesaj)

                if mesaj.is_multipart():
                    for part in mesaj.walk():
                        if part.get_content_type() == "text/plain":
                            corp = part.get_payload(decode=True).decode()
                            lista_mesaj_mail_corp.append(corp)
                            break
                else:
                    corp = mesaj.get_payload(decode=True).decode()
                    lista_mesaj_mail_corp.append(corp)
                
                lista_mesaj_mail_subiect.append(subiect)
                lista_mesaj_mail_from_.append(from_)
                lista_mesaj_mail_data.append(data)

    return lista_mesaj_mail_subiect, lista_mesaj_mail_from_, lista_mesaj_mail_data, lista_mesaj_mail_corp



def verificare_mail_nou():

    nume_mail,parola = functie_nume_si_parola()
    emailuri_noi = functie_mail(nume_mail, parola)

    with open("fisier_email.pkl","rb") as fisier:
        emailuri_vechi=pickle.load(fisier)

    if emailuri_noi != emailuri_vechi:

        with open("fisier_email.pkl","wb") as fisier:
            pickle.dump(emailuri_noi,fisier)

        return True


def trimitere_mail(nume_receptioner_mail,subiect_mesaj,*,corp_mesaj):

    sender,parola=functie_nume_si_parola()

    mesaj_mail=MIMEMultipart()
    mesaj_mail["From"]=sender
    mesaj_mail["To"]=nume_receptioner_mail
    mesaj_mail["Subject"]=subiect_mesaj
    mesaj_mail.attach(MIMEText(corp_mesaj,"plain"))

    with SMTP("smtp.gmail.com",587) as server:

        server.starttls()
        server.login(sender,parola)
        server.sendmail(sender,nume_receptioner_mail,mesaj_mail.as_string())
    
    print("Succes trimitre mesaj!")


def aprindere_bot(bot):

    with open("token.txt") as token_discord:
        token_bot=token_discord.readline()

    bot.run(token_bot)



def sfaturi_de_viata():
    
    with open("sfaturi.txt","r") as fisier_sfaturi:

        lista_sfaturi=fisier_sfaturi.readline()
        print(lista_sfaturi)

    emoji_sfaturi_de_viata = [
    "📚🌱", "🙏💙", "💖🎁", "⏳🚀", "🌈🌌", "💰❌", "🤲🤝", "📜🔍", "😊🌟", 
    "🌱🌎", "🎯🎭", "🔄🔍", "🚀🌈", "🌱🌼", "💡🧠", "🌍💚", "👫🌟", "😄🌈", "🎯🌟",
    "💡🤝", "🌟🚀", "🎭👥", "🧠🤲", "🌟🏆", "🔍🧘", "🤝👂", "🌟🌳", "🤲💕", "🚀🏞️",
    "🔄🌅", "👫🌈", "🤝📈", "💕🎵", "🌅🌻", "💚👂", "📚🌠", "🌱🚶", "🚀💼", "🏆💖",
    "💼🌟", "🌍🤲", "🌼🌞", "💖🌍", "🌞💡", "🌎📈", "🤔👂", "🌈🚀", "🏞️🔄", "💡💬",
    "🚀🔍", "🕊️🌟", "🔍💪", "🚀💪", "🎶🕊️", "💚🔍", "🔍👥", "💖🌱", "🎨💖", "📈🎈"
]

    numar_random=random.randint(0,len(lista_sfaturi)-1)

    sfat_de_viata=lista_sfaturi[numar_random],emoji_sfaturi_de_viata[numar_random]

    return sfat_de_viata


nume_mail,parola_mail=functie_nume_si_parola()

lista_mesaj_mail_subiect,lista_mesaj_mail_from_,lista_mesaj_mail_data=functie_mail(nume_mail, parola_mail)





