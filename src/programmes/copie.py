import os

def copie_css(chemin_destination):
    os.system("powershell copy ./src/css/site.css " + chemin_destination + "/site/css -erroraction 'silentlycontinue'")
    return

def copie_images(chemin_entree, chemin_destination, liste_element):
    os.system("powershell copy ./src/images/Privilegier_le_parcours_1.png " + chemin_destination + "/site/images -erroraction 'silentlycontinue'")
    for element in liste_element:
        if element.image:
            os.system("powershell copy " + chemin_entree + "/" + element.contenu +
                      " " + chemin_destination + "/site/images -erroraction 'silentlycontinue'")
            element.contenu = "./site/images/" + os.path.basename(element.contenu)
    return
