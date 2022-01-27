import xml.etree.ElementTree as et
from os import path, mkdir
from shutil import copy


class Map():
    def __init__(self, node):
        self.information = node
        self.description = ''
        self.pere = None
        self.fils = []
        for node_fils in node.findall('node'):
            if node_fils.attrib['CREATED'] != '':
                item_fils = Titre(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = node

    def generer(self, chemin_entree, chemin_destination):
        for index in self.fils:
            index.generer(chemin_entree, chemin_destination)
            for page in index.fils:
                page.generer(chemin_entree, chemin_destination)


class Titre():
    def __init__(self, node):
        self.information = node
        self.titre = node.attrib['TEXT']
        self.fils = []
        self.pere = ''
        for node_fils in node.findall('node'):
            if node_fils.attrib['CREATED'] != '':
                item_fils = Page(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = self

    def generer(self, chemin_entree, chemin_destination):
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


class Page():
    def __init__(self, node):
        self.page = node.attrib['TEXT']
        self.information = node
        self.pere = ''
        self.fils = []
        for node_fils in node.findall('node'):
            if node_fils.attrib['CREATED'] != '':
                item_fils = Sous_titre(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = self

    def generer(self, chemin_entree, chemin_destination):
        contenu_html = "<!DOCTYPE html><html lang=\"fr\">\n<head>\n<meta charset=\"UTF-8\">\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t\n\t<link rel=\"stylesheet\" href=\"./css/site.css\">\n\t<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"></head>\n<body>\n\t<a href=\"./index.html\"><i class=\"material-icons\">house</i></a>\n\t<title>" + \
            self.page + "</title>\n</head>\n<body>\n<h2>" + self.page + "</h2>\n"

        for sous_titre in self.fils:
            contenu_html = sous_titre.generer(
                contenu_html, chemin_entree, chemin_destination)

        contenu_html += "<p id=\"to_top\"><a href=\"#top\">▲</p>\n</body>\n</html>"
        f = open(chemin_destination + "/site/" +
                 self.page.replace(" ", "_") + '.html', 'w', encoding='utf8')
        f.write(contenu_html)
        f.close()


class Sous_titre():
    def __init__(self, node):
        self.sous_titre = node.attrib['TEXT']
        self.information = node
        self.pere = ''
        self.fils = []
        for node_fils in node.findall('node'):
            if node_fils.attrib['CREATED'] != '':
                item_fils = Bloc(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = self

    def generer(self, contenu_html, chemin_entree, chemin_destination):
        contenu_html += "<section id=\"" + self.sous_titre + "\">\n\t<h3 id=\"" + \
            self.sous_titre.replace(" ", "-") + "\">" + \
            self.sous_titre + "</h3>\n\t"

        for bloc in self.fils:
            contenu_html = bloc.generer(
                contenu_html, chemin_entree, chemin_destination)

        contenu_html += "\n</section>"
        return contenu_html


class Bloc():
    def __init__(self, node):
        self.bloc = ''
        self.image = ''
        self.information = node
        self.pere = ''
        self.fils = []
        for node_fils in node.findall('node'):
            if node_fils.attrib['CREATED'] != '':
                item_fils = Bloc(node_fils)
                self.fils.append(item_fils)
                item_fils.pere = self
        try:
            self.bloc = node.attrib['TEXT']
        except:
            try:
                self.image = node.find('richcontent').find(
                    'html').find('body').find('img').attrib['src']
            except:
                print("Veuillez ne pas mettre de texte sous les images")

    def generer(self, contenu_html, chemin_entree, chemin_destination):
        if self.image != '':
            copy(path.abspath(path.dirname(chemin_entree) + "/" + self.image),
                 path.abspath(chemin_destination + "/site/images"))
            self.image = "./images/" + path.basename(self.image)
            contenu_html += "<center><img id=\"" + path.basename(self.image).replace(
                " ", "-") + "\" src=\"" + self.image + "\" style = \"width:30%\"></center>"
        if self.bloc != '':
            contenu_html += "<p>" + self.bloc + "</p>"
        return contenu_html


def generer_pages(chemin_entree, chemin_destination):
    if not path.exists(chemin_destination + "/site"):
        mkdir(chemin_destination + "/site")
        mkdir(chemin_destination + "/site/css")
        mkdir(chemin_destination + "/site/images")

    doc = et.parse(chemin_entree)
    root = doc.getroot()
    site = Map(root)
    site.generer(chemin_entree, chemin_destination)

    copy("./css/site.css ", path.abspath(chemin_destination + "/site/css"))

    return True


# ----- TEST -----
if __name__ == '__main__':
    doc = et.parse('TITRE.mm')

    root = doc.getroot()

    Mapazerty = Map(root)

    for Title in Mapazerty.fils:
        print(Title.titre)
        for pages in Title.fils:
            print(pages.page)
            for subtitles in pages.fils:
                print(subtitles.sous_titre)
                for blok in subtitles.fils:
                    print(blok.bloc, blok.image)
