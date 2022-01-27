from os import path
from shutil import copy


def copie_css(chemin_destination):
    try:
        copy("./css/site.css ", path.abspath(chemin_destination + "/site/css"))
    except:
        pass
    return


def copie_images(chemin_entree, chemin_destination, liste_element):
    try:
        copy("./images/Privilegier_le_parcours_1.png",
             path.abspath(chemin_destination + "/site/images"))
    except:
        pass
    for element in liste_element:
        if element.image:
            try:
                copy(path.abspath(path.dirname(chemin_entree) + "/" + element.contenu),
                     path.abspath(chemin_destination + "/site/images"))
                element.contenu = "./images/" + path.basename(element.contenu)
            except:
                pass
    return