import xml.etree.ElementTree as et
from os import path, mkdir
from shutil import copy

#classe générique
class Item():
    def __init__(self, node):
        self.information = node         #Information de la node conservé
        self.fils = []
        self.pere = None
        for node_fils in node.findall('node'):      # Création des fils directement dans la classe item
            if node_fils.attrib['CREATED'] != '':       # Condition d'arrêt sur la récursivité
                item_fils = Item(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = self
        try:        # Tri vers les différentes classes
            description = node.attrib['TEXT']
            if description[0] == '/':               # Sous-titres
                self.__class__ = Sous_titre
                self.sous_titre = description[1:]
            elif (description[0] == '-' and description[-1] == '-'):    # Pages
                self.__class__ = Page
                self.page = description[1:-1]
            elif (description[0] == '^'):   #Titre
                self.__class__ = Titre
                self.titre = description[1:]
            else:       # Bloc sans image
                self.__class__ = Bloc
                self.bloc = description
                self.image = ''
        except:
            try:        # Bloc avec image (avec texte sans implémentation)
                self.__class__ = Bloc
                self.image = node.find('richcontent').find('html').find(
                    'body').find('p').find('img').attrib['src']
                self.bloc = ''
            except:     # Bloc avec image sans texte en supplément
                self.__class__ = Bloc
                self.image = node.find('richcontent').find(
                    'html').find('body').find('img').attrib['src']
                self.bloc = ''

#Classe titre au sommet

class Titre(Item):
    def __init__(self, node):
        Item.__init__(self, node)   # Héritage de la classe Item
        self.titre = ''

    def generer_accueil(self, chemin_entree, chemin_destination):
        contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>" + \
            self.titre + "</title>\n\t<link rel=\"stylesheet\" href=\"./css/site.css\">\n\t<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"></head>\n<body>\n\t<a href=\"./index.html\"><i class=\"material-icons\">house</i></a>\n\t<h1>" + \
            self.titre + "</h1>\n<ul id=\"menu-deroulant\">\n"

        for page in self.fils:
            contenu_html += "\t<li><a href=\"" + page.page.replace(
                " ", "_") + ".html\">" + page.page + "</a>\n\t\t<ul>\n"
            for sous_titre in page.fils:
                contenu_html += "\n\t\t<li><a href=\"" + page.page.replace(
                    " ", "_") + ".html#" + sous_titre.sous_titre.replace(
                    " ", "-") + "\">" + sous_titre.sous_titre + "</a></li>\n"
            contenu_html += "\n\t\t</ul>\n\t</li>"

        contenu_html += "\n\t</ul>\n\t<br>\n\t<div id =\"imageprinc\"><img src=\"./images/Privilegier_le_parcours_1.png\"></div>\n</body>\n</html>"
        copy("./images/Privilegier_le_parcours_1.png",
             path.abspath(chemin_destination + "/site/images"))
        f = open(chemin_destination + "/site/index.html", 'w', encoding='utf8')
        f.write(contenu_html)
        f.close()

    def generer(self, chemin_entree, chemin_destination):
        self.generer_accueil(chemin_entree, chemin_destination)
        for page in self.fils:
            page.generer(chemin_entree, chemin_destination)

#Classe Page
class Page(Item):
    def __init__(self, node):
        Item.__init__(self, node)               # Héritage de la classe Item
        self.page = ''

    def generer(self, chemin_entree, chemin_destination):
        contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t\n\t<link rel=\"stylesheet\" href=\"./css/site.css\">\n\t<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"></head>\n<body>\n\t<a href=\"./index.html\"><i class=\"material-icons\">house</i></a>\n\t<title>" + \
            self.page + "</title>\n</head>\n<body>\n<h2>" + self.page + "</h2>\n"

        for sous_titre in self.fils:
            contenu_html = sous_titre.generer(
                contenu_html, chemin_entree, chemin_destination)

        contenu_html += "\n\t<div id=\"myModal\" class=\"modal\">\n\t\t<span class=\"close\">&times;</span>\n\t\t<img class=\"modal-content\" id=\"img01\">\n\t\t<div id=\"caption\"></div>\n\t</div>\n\t<script>\n\t\tfunction agrandir(id_item) {\n\t\t\tvar modal = document.getElementById(\"myModal\");\n\t\t\tvar img = document.getElementById(id_item);\n\t\t\tvar modalImg = document.getElementById(\"img01\");\n\t\t\tvar captionText = document.getElementById(\"caption\");\n\n\t\t\timg.onclick = function() {\n\t\t\t\tmodal.style.display = \"block\";\n\t\t\t\tmodalImg.src = this.src;\n\t\t\t\tcaptionText.innerHTML = this.alt;\n\t\t\t}\n\n\t\t\tvar span = document.getElementsByClassName(\"close\")[0];\n\n\t\t\tspan.onclick = function() {\n\t\t\t\tmodal.style.display = \"none\";\n\t\t\t}\n\t\t}\n\t</script>\n\t<p id=\"to_top\"><a href=\"#top\">▲</p>\n</body>\n</html>"
        f = open(chemin_destination + "/site/" +
                 self.page.replace(" ", "_") + '.html', 'w', encoding='utf8')
        f.write(contenu_html)
        f.close()


class Sous_titre(Item):
    def __init__(self, node):
        Item.__init__(self, node)           # Héritage de la classe Item
        self.sous_titre = ''

    def generer(self, contenu_html, chemin_entree, chemin_destination):
        contenu_html += "<section id=\"" + self.sous_titre + "\">\n\t<h3 id=\"" + \
            self.sous_titre.replace(" ", "_") + "\">" + \
            self.sous_titre + "</h3>\n\t"

        for bloc in self.fils:
            contenu_html = bloc.generer(
                contenu_html, chemin_entree, chemin_destination)

        contenu_html += "\n</section>"
        return contenu_html

# Classe bloc
class Bloc(Item):
    def __init__(self, node):
        Item.__init__(self, node)       # Héritage de la classe Item
        self.bloc = ''          # Texte
        self.image = ''         # Chemin d'accès de l'image

    def generer(self, contenu_html, chemin_entree, chemin_destination):
        if self.image != '':
            copy(path.abspath(path.dirname(chemin_entree) + "/./" + self.image),
                 path.abspath(chemin_destination + "/site/images/" + path.basename(self.image).replace(" ", "_")))
            self.image = "./images/" + \
                path.basename(self.image).replace(" ", "_")
            contenu_html += "<center><a href=\"javascript:agrandir(\'" + path.basename(self.image).replace(
                " ", "_") + "\')\"><img id=\"" + path.basename(self.image).replace(
                " ", "_") + "\" src=\"" + self.image + "\" style = \"width:30%\"></a></center>"
        if self.bloc != '':
            contenu_html += "<p>" + self.bloc + "</p>"
        return contenu_html


def generer_pages_heritage(chemin_entree, chemin_destination):
    if not path.exists(chemin_destination + "/site"):
        mkdir(chemin_destination + "/site")
        mkdir(chemin_destination + "/site/css")
        mkdir(chemin_destination + "/site/images")

    doc = et.parse(chemin_entree)
    root = doc.getroot()
    site_root = root.findall('node')[0]         # On skip la map pour prendre le titre directement
    site = Item(site_root)

    site.generer(chemin_entree, chemin_destination)

    copy("./css/site.css ", path.abspath(chemin_destination + "/site/css"))

    return True


# ----- TEST -----
if __name__ == '__main__':
    doc = et.parse('TEST.mm')

    root = doc.getroot()

    titre_oui = root.findall('node')[0]

    title = Item(titre_oui)

    for pages in title.fils:
        print(pages.page)
        for soustitres in pages.fils:
            print(soustitres.sous_titre)
            for blocs in soustitres.fils:
                print(blocs.bloc, blocs.image)
