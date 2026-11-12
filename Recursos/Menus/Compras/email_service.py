import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def enviar_factura(destinatario, asunto, mensaje, archivo_pdf):

    try:

        remitente = "farmaciascruzazul.05@gmail.com"

        # CONTRASEÑA DE APLICACIÓN
        password = "bkmxdrmajdnouhmq"

        # =========================
        # CREAR MENSAJE
        # =========================
        msg = MIMEMultipart()

        msg["From"] = remitente
        msg["To"] = destinatario
        msg["Subject"] = asunto

        msg.attach(MIMEText(mensaje, "plain"))

        # =========================
        # ADJUNTAR PDF
        # =========================
        nombre_archivo = os.path.basename(archivo_pdf)

        with open(archivo_pdf, "rb") as archivo:

            parte = MIMEBase("application", "octet-stream")

            parte.set_payload(archivo.read())

        encoders.encode_base64(parte)

        parte.add_header(
            "Content-Disposition",
            f"attachment; filename={nombre_archivo}"
        )

        msg.attach(parte)

        # =========================
        # CONEXIÓN SMTP
        # =========================
        servidor = smtplib.SMTP("smtp.gmail.com", 587)

        servidor.ehlo()

        servidor.starttls()

        servidor.ehlo()

        servidor.login(remitente, password)

        servidor.sendmail(
            remitente,
            destinatario,
            msg.as_string()
        )

        servidor.quit()

        print("Correo enviado correctamente")

    except Exception as e:

        print("Error enviando correo:")
        print(e)

def enviar_correo_proveedor(destinatario, productos,direccion):

    try:

        remitente = "farmaciascruzazul.05@gmail.com"

        # CONTRASEÑA DE APLICACIÓN
        password = "bkmxdrmajdnouhmq"

        # =========================
        # CREAR MENSAJE
        # =========================
        msg = MIMEMultipart()

        msg["From"] = remitente
        msg["To"] = destinatario
        msg["Subject"] = f"Querido proveedor. Socicito tus productos"

        cuerpo = "Le solicito de manera más atenta los siguientes productos \n\n"
        for item in productos:
             producto = f"- {item['nombre']} | Cantidad: {item['cantidad']} | Precio: ${item['precio']}\n"
             cuerpo += producto
        cuerpo += f"\n\nEnviar a la sucursal: {direccion}"
        cuerpo += "\n\nLe agradezco de manera más atenta su colaboración"
          
        
        msg.attach(MIMEText(cuerpo, "plain"))

        """# =========================
        # ADJUNTAR PDF
        # =========================
        nombre_archivo = os.path.basename(archivo_pdf)

        with open(archivo_pdf, "rb") as archivo:

            parte = MIMEBase("application", "octet-stream")

            parte.set_payload(archivo.read())

        encoders.encode_base64(parte)

        parte.add_header(
            "Content-Disposition",
            f"attachment; filename={nombre_archivo}"
        )

        msg.attach(parte)"""

        # =========================
        # CONEXIÓN SMTP
        # =========================
        servidor = smtplib.SMTP("smtp.gmail.com", 587)

        servidor.ehlo()

        servidor.starttls()

        servidor.ehlo()

        servidor.login(remitente, password)

        servidor.sendmail(
            remitente,
            destinatario,
            msg.as_string()
        )

        servidor.quit()

        print("Correo enviado al proveedor correctamente")

    except Exception as e:

        print("Error enviando correo al proveedor:")
        print(e)