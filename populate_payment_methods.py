import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Reemplaza 'nombre_proyecto' con el nombre de tu proyecto.
django.setup()

from factus.models import PaymentMethod  # Importa el modelo de tu aplicación.

def populate_payment_methods():
    payment_methods = [
        ("10", "Efectivo"),
        ("42", "Consignación"),
        ("20", "Cheque"),
        ("46", "Transferencia Débito Interbancario"),
        ("47", "Transferencia"),
        ("71", "Bonos"),
        ("72", "Vales"),
        ("ZZZ", "Otro*"),
        ("1", "Medio de pago no definido"),
        ("49", "Tarjeta Débito"),
        ("3", "Débito ACH"),
        ("25", "Cheque certificado"),
        ("26", "Cheque Local"),
        ("24", "Nota cambiaria esperando aceptación"),
        ("64", "Nota promisoria firmada por el banco"),
        ("65", "Nota promisoria firmada por un banco avalada por otro banco"),
        ("66", "Nota promisoria firmada"),
        ("67", "Nota promisoria firmada por un tercero avalada por un banco"),
        ("2", "Crédito ACH"),
        ("95", "Giro formato abierto"),
        ("13", "Crédito Ahorro"),
        ("14", "Débito Ahorro"),
        ("39", "Crédito Intercambio Corporativo (CTX)"),
        ("4", "Reversión débito de demanda ACH"),
        ("5", "Reversión crédito de demanda ACH"),
        ("6", "Crédito de demanda ACH"),
        ("7", "Débito de demanda ACH"),
        ("9", "Clearing Nacional o Regional"),
        ("11", "Reversión Crédito Ahorro"),
        ("12", "Reversión Débito Ahorro"),
        ("18", "Desembolso (CCD) débito"),
        ("19", "Crédito Pago negocio corporativo (CTP)"),
        ("21", "Proyecto bancario"),
        ("22", "Proyecto bancario certificado"),
        ("27", "Débito Pago Negocio Corporativo (CTP)"),
        ("28", "Crédito Negocio Intercambio Corporativo (CTX)"),
        ("29", "Débito Negocio Intercambio Corporativo (CTX)"),
        ("30", "Transferencia Crédito"),
        ("31", "Transferencia Débito"),
        ("32", "Desembolso Crédito plus (CCD+)"),
        ("33", "Desembolso Débito plus (CCD+)"),
        ("34", "Pago y depósito pre acordado (PPD)"),
        ("35", "Desembolso Crédito (CCD)"),
        ("36", "Desembolso Débito (CCD)"),
        ("48", "Tarjeta Crédito"),
        ("44", "Nota cambiaria"),
        ("23", "Cheque bancario de gerencia"),
        ("61", "Nota promisoria firmada por el acreedor"),
        ("62", "Nota promisoria firmada por el acreedor, avalada por el banco"),
        ("63", "Nota promisoria firmada por el acreedor, avalada por un tercero"),
        ("60", "Nota promisoria"),
        ("96", "Método de pago solicitado no usado"),
        ("91", "Nota bancaria transferible"),
        ("92", "Cheque local transferible"),
        ("93", "Giro referenciado"),
        ("94", "Giro urgente"),
        ("40", "Débito Intercambio Corporativo (CTX)"),
        ("41", "Desembolso Crédito plus (CCD+)"),
        ("43", "Desembolso Débito plus (CCD+)"),
        ("45", "Transferencia Crédito Bancario"),
        ("50", "Postgiro"),
        ("51", "Telex estándar bancario"),
        ("52", "Pago comercial urgente"),
        ("53", "Pago Tesorería Urgente"),
        ("15", "Bookentry Crédito"),
        ("16", "Bookentry Débito"),
        ("17", "Desembolso Crédito (CCD)"),
        ("70", "Retiro de nota por el acreedor"),
        ("74", "Retiro de nota por el acreedor sobre un banco"),
        ("75", "Retiro de nota por el acreedor, avalada por otro banco"),
        ("76", "Retiro de nota por el acreedor, sobre un banco avalada por un tercero"),
        ("77", "Retiro de una nota por el acreedor sobre un tercero"),
        ("78", "Retiro de una nota por el acreedor sobre un tercero avalada por un banco"),
        ("37", "Pago Negocio Corporativo Ahorros Crédito (CTP)"),
        ("38", "Pago Negocio Corporativo Ahorros Débito (CTP)"),
        ("97", "Clearing entre partners"),
    ]

    for code, description in payment_methods:
        PaymentMethod.objects.get_or_create(code=code, description=description)

if __name__ == "__main__":
    populate_payment_methods()
    print("¡Métodos de pago poblados exitosamente!")
