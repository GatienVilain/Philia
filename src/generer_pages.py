import os
from extraction_mind_map import *
from copie_image import *


def generer_page(chemin_destination, liste_element):
    contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>" + \
        liste_element[0].contenu + "</title>\n</head>\n<body>\n<h1>" + \
        liste_element[0].contenu + "</h1>\n"

    section_ouvert = False
    if len(liste_element) > 1:
        for index in range(1, len(liste_element)):
            element = liste_element[index]
            if element.sous_titre:
                if section_ouvert:
                    contenu_html += "\n</section>"
                contenu_html += "<section id=\"" + element.contenu + \
                    "\">\n\t<h2>" + element.contenu + "</h2>\n\t"
                section_ouvert = True
            elif element.image:
                contenu_html += "<img src=\"" + element.contenu + "\">"
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
    contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>" + \
        liste_element[0][0].contenu + "</title>\n</head>\n<body>\n<h1>" + \
        liste_element[0][0].contenu + "</h1>\n<ul>\n"

    for index in range(2, len(liste_element)):
        contenu_html += "\t<li><a href=" + liste_element[index][0].contenu.replace(
            " ", "_") + ".html\">" + liste_element[index][0].contenu + "</a></li>\n"

    contenu_html += "\n</body>\n</html>"
    f = open(chemin_destination + "/site/index.html", 'w', encoding='utf8')
    f.write(contenu_html)
    f.close()

    return True


def generer_pages(chemin_entree, chemin_destination):
    fichier_entree = extraction_texte(chemin_entree)

    if not os.path.exists(chemin_destination + "site"):
        os.mkdir(chemin_destination + "site")
        os.mkdir(chemin_destination + "site/css")
        os.mkdir(chemin_destination + "site/images")

    copie_images(chemin_entree, chemin_destination, fichier_entree)

    fichier_entree = decoupage(fichier_entree)

    generer_page_accueil(chemin_destination, fichier_entree)
    for page in range(1, len(fichier_entree)):
        generer_page(chemin_destination, fichier_entree[page])

    return True


# ---- TEST -------
if __name__ == '__main__':
    generer_pages(
        r"C:\Users\gatie\source\repos\GatienVilain\projet-info\TEST.mm", "./")
