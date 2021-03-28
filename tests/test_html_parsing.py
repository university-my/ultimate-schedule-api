from bs4 import BeautifulSoup

def test_h4_tag_parsing():
	h4WithTags = '<h4>03.04.2021 <small>Субота </small><br/><span style="color:red;font-size: 16px;"> Перенесено з 6.5.2021</span></h4>'
	soup = BeautifulSoup(h4WithTags, "lxml")
	print(soup.h4.text.split()[0])

	h4 = "<h4>02.04.2021 <small>П'ятниця</small></h4>"
	soup = BeautifulSoup(h4, "lxml")
	print(soup.h4.text.split()[0])
	pass
	