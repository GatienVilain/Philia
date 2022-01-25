from xml.dom import minidom


class texte:
    def __init__(self):
        self.contenu = ""
        self.numero = ""
        self.image = False


def charge_fichier(nom):  # nom = chemin du fichier
    L = []
    file = open(nom, "r")  # r pour mode lecture
    file.readline()  # creé une liste file ou chaque elements est une ligne

    for line in file:
        L.append(line)

    return L


def extraction_texte(nom_fichier):
    Liste_text = []
    cpt_img = 0
    L = charge_fichier(nom_fichier)
    file = minidom.parse(nom_fichier)
    for x in range(len(L)):

        textetampon = texte()
        try:
            textetampon.contenu = file.getElementsByTagName(
                'node')[x].attributes['TEXT'].value
            textetampon.numero = x
            Liste_text.append(textetampon)
            #print (textetampon.contenu)
        except:
            try:
                textetampon.contenu = file.getElementsByTagName(
                    'img')[cpt_img].attributes['src'].value
                cpt_img = cpt_img+1
                textetampon.numero = x
                textetampon.image = True
                Liste_text.append(textetampon)

            except:
                pass

    return(Liste_text)
