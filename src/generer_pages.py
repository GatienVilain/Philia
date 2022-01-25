import os
from extraction_mind_map import *


def generer_section_1_colonne(contenu_html, titre, element):
    contenu_html += "<section id=\"" + titre + ">\n\t<h2>" + titre + "</h2>\n\t"
    if element.image:
        contenu_html += "<img src=\"" + element.texte + "\">"
    else:
        contenu_html += "<p>" + element.texte + "</p>"
    contenu_html += "\n</section>"
    return contenu_html


def generer_section_2_colonne(contenu_html, titre, element_1, element_2):
    contenu_html += "<section id=\"" + titre + ">\n\t<h2>" + titre + "</h2>\n\t"
    if element_1.image:
        contenu_html += "<img src=\"" + element.texte + "\">"
    else:
        contenu_html += "<p>" + element.texte + "</p>"
    if element_2.image:
        contenu_html += "<img src=\"" + element.texte + "\">"
    else:
        contenu_html += "<p>" + element.texte + "</p>"
    contenu_html += "</section>"
    return contenu_html


def generer_page(chemin_destination, liste_element):
    if not os.path.exists(path):
        os.mkdir(chemin_destination + "site")

    contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>" + liste_element[0].texte + "</title>\n</head>\n<body>"

    # boucle d'élément qui génère les pages
    # ------
    nombre_element = 0
    for element in liste_element:
        if liste_element.title:
            if nombre_element == 1:
                generer_section_1_colonne(contenu_html, titre, element_1)
            elif nombre_element == 2:
                generer_section_2_colonne(
                    contenu_html, titre, element_1, element_2)

            titre = liste_element.texte
            nombre_element = 0
        elif nombre_element == 0:
            element_1 = liste_element.texte
            nombre_element += 1
        else:
            element_2 = liste_element.texte
            nombre_element += 1

    # ------

    contenu_html += "\n</body>\n</html>"
    f = open(chemin_destination + "/" + liste_element[0].texte + 'index.html', 'w')
    f.write(contenu_html)
    f.close()
    return True


l = extraction_texte('./src/TITRE.mm')
generer_page("./", l)
