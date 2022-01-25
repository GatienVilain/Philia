import os


def copie_images(chemin_entree, chemin_destination, liste_element):
    for element in liste_element:
        if element.image:
            os.system("powershell copy " + chemin_entree + "/" + element.contenu +
                      " " + chemin_destination + "/site/images -erroraction 'silentlycontinue'")
    return
