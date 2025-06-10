import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

EMAIL = "nelly.sgn@gmail.com"
EMAIL_APP_PASSWORD = "brauymepehfjrpqd"


def send_email():
    msg = MIMEText("Une place pourrait être dispo ! Vérifie ici : https://widget.weezevent.com/ticket/revente-coucool25?locale=fr-FR")
    msg["Subject"] = "\u26a0\ufe0f Place dispo Coucool"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def check_weez():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://widget.weezevent.com/ticket/revente-coucool25?locale=fr-FR", timeout=60000)
        page.wait_for_timeout(15000)  # attendre le chargement JS
        content = page.content()
        nb_indispo = content.count("Indisponible")
        print(f"Nombre d'Indisponible détecté : {nb_indispo}")


        if nb_indispo < 7:
            send_email()

        browser.close()


if __name__ == "__main__":
    check_weez()
