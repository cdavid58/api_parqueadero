# import requests, json
# url = "http://127.0.0.1:9090/schedule/Get_Range_Fee/"
# payload = {}
# headers = {}
# response = requests.request("GET", url, headers=headers, data=payload)
# ranges_list = json.loads(response.text)


# minutes = 62
# found_range = None
# price_to_charge = None
# for r in ranges_list:
#     if r['time'][0] <= minutes <= r['time'][1]:
#         found_range = r
#         price_to_charge = r['price']
#         break

# if found_range:
#     # print(f"El valor {x} está en el rango [{found_range['time'][0]}, {found_range['time'][1]}].")
#     print(f"Se debe cobrar el precio: {price_to_charge}.")
# else:
#     print(f"El valor {minutes} no está dentro de ningún rango.")

import pytz
from datetime import datetime

# Obtener la zona horaria de Colombia
colombia_tz = pytz.timezone('America/Bogota')

# Obtener la hora actual en Colombia
hora_actual_colombia = datetime.now(colombia_tz)

# Formatear la hora actual para imprimir
formato = '%H:%M'  # Formato de fecha y hora
hora_actual_formateada = hora_actual_colombia.strftime(formato)

print("Hora actual en Colombia:", hora_actual_formateada)