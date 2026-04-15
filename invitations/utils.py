import random
import string
from django.conf import settings
import qrcode
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Invitation

def generate_code_invit():
    code = ''.join(random.choices(string.ascii_uppercase, k=10))
    while Invitation.objects.filter(code_invit=code).exists():
        code = ''.join(random.choices(string.ascii_uppercase, k=10))
    return code

def qr_code_generator(data):
    # Vérifiez que les données ne sont pas vides
    if not data:
        raise ValueError("Les données à encoder dans le QR code ne peuvent pas être vides.")

    logo_path = str(settings.STATIC_ROOT) + '/eventplanlogo/logo_plan_event.png'
    # Créer un objet QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Ajouter les données au code QR
    qr.add_data(data)
    qr.make(fit=True)

    # Créer une image du code QR
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Ouvrir l'image du logo
    try:
        logo = Image.open(logo_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier logo n'a pas été trouvé à l'emplacement : {logo_path}")

    # Redimensionner le logo pour qu'il s'adapte au centre du code QR
    logo_size = qr_img.size[0] // 5
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Convertir l'image JPEG en une image avec un canal alpha
    if logo.mode in ("RGBA", "LA") or (logo.mode == "P" and "transparency" in logo.info):
        # Si l'image a déjà un canal alpha, on la garde telle quelle
        logo_with_alpha = logo
    else:
        # Sinon, on crée un masque de transparence
        logo_with_alpha = logo.convert("RGBA")
        datas = logo_with_alpha.getdata()

        new_data = []
        for item in datas:
            # changer tous les pixels blancs en pixels transparents
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        logo_with_alpha.putdata(new_data)

    # Calculer la position pour placer le logo au centre
    position = ((qr_img.size[0] - logo_with_alpha.size[0]) // 2, (qr_img.size[1] - logo_with_alpha.size[1]) // 2)

    # Coller le logo sur l'image du code QR
    qr_img.paste(logo_with_alpha, position, logo_with_alpha)

    # Créer un fichier en mémoire
    image_io = BytesIO()
    qr_img.save(image_io, format='PNG')
    image_io.seek(0)

    # Créer une instance de InMemoryUploadedFile
    image_file = InMemoryUploadedFile(
        image_io, None, f'{data}.png', 'image/png', sys.getsizeof(image_io), None
    )

    return image_file

def send_invitation_email(invitation):
    # Générer le code QR
    qr_code = qr_code_generator(invitation.code_invit)

    # Enregistrer l'image combinée dans un objet BytesIO
    buf = BytesIO()
    qr_code.save(buf, format='JPEG')
    buf.seek(0)

    # Construire le corps de l'email
    context = {
        'invitation': invitation,
    }
    html_content = render_to_string('invitation_email.html', context)

    # Créer l'objet EmailMessage
    subject = f"Code QR pour l'événement {invitation.event.name}"
    from_email = settings.EMAIL_HOST_USER
    to = [invitation.email]
    msg = EmailMessage(subject, html_content, from_email, to)
    msg.content_subtype = "html"  # Définir le type MIME sur text/html

    # Attacher l'image en tant que pièce jointe
    msg.attach("code_qr.jpg", buf.getvalue(), "image/jpeg")

    # Envoyer l'email
    msg.send()

    # Fermer l'objet BytesIO
    buf.close()