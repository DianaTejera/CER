import cloudscraper
import re
from database import insertar_cambio
import sched, time

def obtener_cambio():
#Función que extrae el dato de la página web
	scraper = cloudscraper.create_scraper(delay=10, browser={'custom':'ScraperBot/1.0', })
	url = 'https://es.investing.com/currencies/eur-usd'
	resp = scraper.get(url)

	if resp.status_code == 200:
		html = resp.text
		pattern = 'data-test="instrument-price-last">(\d+\,\d+)</span>'
		match = re.search(pattern, html)
		if match:
			valor = float(match.group(1).replace(',','.'))
			insertar_cambio(valor)
			print('Nuevo valor')
			return match.group(1)
		else:
			return "N/A"
	else:
		print('code',resp.status_code)
		return "Could not connect to es.investing.com"

	s.enter(120,1,obtener_cambio)

if __name__ == "__main__":
	try:
		s = sched.scheduler(time.time, time.sleep)
#		s.enter(120,1,obtener_cambio)
		s.run()
	except KeyboardInterrupt:
			exit()



#	while(True):
#		schedule.run_pending()
#		time.sleep(120)
#		if (KeyboardInterrupt):
#			exit

