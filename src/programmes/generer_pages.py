import os
from programmes.extraction_mind_map import *
from programmes.copie import *


def generer_page(chemin_destination, liste_element):
    contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t\n\t<link rel=\"stylesheet\" href=\"./css/site.css\">\n\t<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"></head>\n<body>\n\t<a href=\"./index.html\"><i class=\"material-icons\">house</i></a>\n\t<title>" + \
        liste_element[0].contenu + "</title>\n</head>\n<body>\n<h2>" + \
        liste_element[0].contenu + "</h2>\n"

    section_ouvert = False
    if len(liste_element) > 1:
        for index in range(1, len(liste_element)):
            element = liste_element[index]
            if element.sous_titre:
                if section_ouvert:
                    contenu_html += "\n</section>"
                contenu_html += "<section id=\"" + element.contenu + \
                    "\">\n\t<h3 id=\"" + element.contenu.replace(" ", "-") + "\">" + element.contenu + "</h3>\n\t"
                section_ouvert = True
            elif element.image:
                contenu_html += "<center><img id=\"" + element.contenu.replace(" ", "-") + "\" src=\"" + element.contenu + "\" style = \"width:30%\"></center>"
            else:
                contenu_html += "<p>" + element.contenu + "</p>"
        if section_ouvert:
            contenu_html += "\n</section>"

    contenu_html += "\n</body>\n</html>"
    f = open(chemin_destination + "/site/" +
             liste_element[0].contenu.replace(" ", "_") + '.html', 'w', encoding='utf8')
    f.write(contenu_html)
    f.close()

    return True


def generer_page_accueil(chemin_destination, liste_element):
    contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>" + \
        liste_element[0][0].contenu + "</title>\n\t<link rel=\"stylesheet\" href=\"./css/site.css\">\n\t<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"></head>\n<body>\n\t<a href=\"./index.html\"><i class=\"material-icons\">house</i></a>\n\t<h1>" + \
        liste_element[0][0].contenu + "</h1>\n<ul id=\"menu-deroulant\">\n"

    for index in range(1, len(liste_element)):
        contenu_html += "\t<li><a href=\"" + liste_element[index][0].contenu.replace(
            " ", "_") + ".html\">" + liste_element[index][0].contenu + "</a>\n\t\t<ul>\n"
        for chapitre in range(1, len(liste_element[index])):
            if liste_element[index][chapitre].sous_titre:
                contenu_html += "\n\t\t<li><a href=\"" + liste_element[index][0].contenu.replace(
                    " ", "_") + ".html#" + liste_element[index][chapitre].contenu.replace(
                    " ", "-") + "\">" + liste_element[index][chapitre].contenu + "</a></li>\n"
        contenu_html += "\n\t\t</ul>\n\t</li>"

    contenu_html += "\n\t</ul>\n\t<br>\n\t<div id =\"imageprinc\"><img src=\"./images/Privilegier_le_parcours_1.png\"></div>\n</body>\n</html>"
    f = open(chemin_destination + "/site/index.html", 'w', encoding='utf8')
    f.write(contenu_html)
    f.close()

    return True


def generer_pages(chemin_entree, chemin_destination):
    fichier_entree = extraction_texte(chemin_entree)

    if not os.path.exists(chemin_destination + "/site"):
        os.mkdir(chemin_destination + "/site")
        os.mkdir(chemin_destination + "/site/css")
        os.mkdir(chemin_destination + "/site/images")

    copie_css(chemin_destination)
    copie_images(chemin_entree, chemin_destination, fichier_entree)

    fichier_entree = decoupage(fichier_entree)

    generer_page_accueil(chemin_destination, fichier_entree)
    for page in range(1, len(fichier_entree)):
        generer_page(chemin_destination, fichier_entree[page])

    return True


# ---- TEST -------
if __name__ == '__main__':
    generer_pages(
        r"C:/Users/gatie/Bureau/TEST.mm", "C:/Users/gatie/Bureau")
