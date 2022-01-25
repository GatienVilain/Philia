from xml.dom import minidom


class texte:
    def __init__(self):
        self.contenu = ""  # contenu du bloc
        self.numero = ""  # numero d'emplacement
        self.image = False  # etat image
        self.titre = False  # etat titre
        # sinon texte


def charge_fichier(nom):  # nom = chemin du fichier
    L = []
    file = open(nom, "r")  # r pour mode lecture
    file.readline()  # creÃ© une liste file ou chaque elements est une ligne
    for line in file:
        L.append(line)
    return L


def extraction_texte(nom_fichier):
    Liste_text = []  # creation liste, chaque elem est un bloc du xml
    cpt_img = 0  # compteur pour avancer dans la lecture des images
    # decoupage du fichier en bloc pour connaitre le nombre de lectures a effectuer
    L = charge_fichier(nom_fichier)
    # mise en memoire du XML a travers la bibliotheque minidom
    file = minidom.parse(nom_fichier)
    for i in range(len(L)):
        textetampon = texte()
        try:  # si element texte existe dans la node, alors on le met en memoire comme contenu
            textetampon.contenu = file.getElementsByTagName(
                'node')[i].attributes['TEXT'].value
            textetampon.numero = i
            Liste_text.append(textetampon)

        except:  # sinon on verifie si ce n'est pas une image avant de passer Ã  la node suivante
            try:
                textetampon.contenu = file.getElementsByTagName(
                    'img')[cpt_img].attributes['src'].value
                # on incremente le compteur d'image pour lire limage suivante au prochain tour
                cpt_img = cpt_img+1
                textetampon.numero = i            # on la place a la bonne position parmis le texte
                # on indique que c'est une image (pour la gÃ©nÃ©ration html)
                textetampon.image = True
                Liste_text.append(textetampon)

            except:
                pass  # si la node est vide on passe
    Liste_text = detection_titre(Liste_text)
    return(Liste_text)


def detection_titre(L):
    L_triee = []  # on cree une liste triee qui sera renvoyÃ©e en sortie de fct
    for elem in L:
        if elem.contenu[0] == '-' and elem.contenu[-1] == '-':  # detection titre
            elem.contenu = elem.contenu.replace(
                "-", "")  # supression des tirets
            elem.titre = True  # on indique que l'element est un titre
            L_triee.append(elem)
        else:
            L_triee.append(elem)  # sinon on ne modifie pas l'element

    return(L_triee)
