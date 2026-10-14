import json
import re

CAMPOS = {
    "nic": r"(?:NIC|N[uú]mero de cliente|Cuenta)\s*[:#]?\s*(\d{6,12})",
    "nombre": r"Nombre\s*:\s*(.+)",
    "cedula": r"(?:C[eé]dula|RUC)\s*:\s*([\w\-]+)",
    "telefono": r"(?:Tel[eé]fono|Celular)\s*:\s*([\d\-\s\+]{7,15})",
    "direccion": r"Direcci[oó]n\s*:\s*(.+)",
    "tipo_caso": r"(?:Tipo de caso|Motivo)\s*:\s*(.+)",
}
OBLIGATORIOS = ["nic", "nombre", "telefono", "tipo_caso"]


def limpiar(texto):
    texto = re.sub(r"<br\s*/?>|</p>", "\n", texto or "", flags=re.I)
    return re.sub(r"<[^>]+>", " ", texto)


def validar(asunto, cuerpo):
    texto = f"{asunto or ''}\n{limpiar(cuerpo)}"
    datos = {}
    for campo, patron in CAMPOS.items():
        m = re.search(patron, texto, re.IGNORECASE)
        datos[campo] = m.group(1).strip() if m else None
    faltantes = [c for c in OBLIGATORIOS if not datos.get(c)]
    return json.dumps(
        {"datos": datos, "faltantes": faltantes, "completo": not faltantes},
        ensure_ascii=False,
    )
