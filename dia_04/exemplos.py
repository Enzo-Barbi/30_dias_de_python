import humanize as h

# Size
val=300
print(val)
h.naturalsize(val)

# Datas e tempo
from datetime import datetime, timedelta

#dias
h.naturalday(datetime.now() - timedelta(3))

#datas
h.naturaldate(datetime.now() + timedelta(365))

#distancia
h.naturaldelta(timedelta(365))

h.activate('pt_BR')
h.deactivate()

#numeros 
h.fractional(0.5)
h.scientific(1.12836782)
h.metric(10, 'km')
h.ordinal(10, gender='famale')
h.intcomma(5000.98)
h.intword(20_000)

#listas
h.natural_list([1,2,3])