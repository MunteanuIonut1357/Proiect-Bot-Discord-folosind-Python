import openai
from getmail import functie_mail, functie_nume_si_parola

openai.api_key = 'your-openai-api-key'

def is_email_a_task(email_content):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Este acest text un task? Text: {email_content}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

nume_mail, parola = functie_nume_si_parola()

lista_mesaj_mail_subiect, lista_mesaj_mail_from_, lista_mesaj_mail_data = functie_mail(nume_mail, parola)


for email_content in lista_mesaj_mail_subiect:
    if is_email_a_task(email_content):
        print("Acest e-mail conține un task.")
    else:
        print("Acest e-mail nu conține un task.")
