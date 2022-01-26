from os import path
from shutil import copy


def copie_css(chemin_destination):
    copy("./src/css/site.css ", path.abspath(chemin_destination + "/site/css"))
    return


def copie_images(chemin_entree, chemin_destination, liste_element):
    copy("./src/images/Privilegier_le_parcours_1.png", path.abspath(chemin_destination + "/site/images"))
    for element in liste_element:
        if element.image:
            copy(path.abspath(path.dirname(chemin_entree) + "/" + element.contenu), path.abspath(chemin_destination + "/site/images"))
            element.contenu = "./images/" + path.basename(element.contenu)
    return
