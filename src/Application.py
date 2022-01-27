from tkinter import*  # Pour l'interface graphique
import tkinter.filedialog as FD  # Utilisé pour les chemins des fichiers et dossiers
import tkinter.ttk as ttk  # Pour avoir plus d'options sur les widgets

from webbrowser import open  # Pour ouvrir un page web
from pathlib import Path  # Pour récupérer l'adresse du dossier download
from os import startfile

# Pour importer le programme servant à générer le site web
from programmes.generer_pages import generer_pages_liste
from programmes.objet import generer_pages_objets

# Début class PathEntry


class PathEntry (ttk.Frame):

    # Début def
    def __init__(self, master=None, texteLabel="Defaut"):  # Initialisation de l'objet PathEntry

        self.master = master
        self.texteLabel = texteLabel

        # Initialisation de l'objet Frame
        ttk.Frame.__init__(self, master)

        # Initialisation des widgets

        self.init_widget(texteLabel)

    # Fin def

    # Début def
    def init_widget(self, texteLabel):  # Initialisation des widgets

        # component inits

        # Création d'un objet Label
        self.label = ttk.Label(

            self,

            text=texteLabel

        )

        # Création d'une variable StrinVar
        self.file_path = StringVar()

        # Création d'un objet Entry
        self.entry = Entry(

            self,

            textvariable=self.file_path,

            # On désactive entry (on ne peut plus écrire dedans)
            state=DISABLED,

            disabledbackground="WHITE",  # Couleur du fond quand entry est désactivé

            disabledforeground='BLACK'  # Couleur du texte quand entry est désactivé

        )

        # Création d'un bouton
        self.boutonParcourir = ttk.Button(

            self,

            text="Parcourir",

            command=self.slot_browse,  # Commande exécutée quand on appuie sur le bouton

            underline=0

        )

        # On initialise la position des widgets de l'objet PathEntry

        self.label.pack(side=LEFT, expand=0, fill=X)

        self.entry.pack(side=LEFT, expand=1, fill=X)

        self.boutonParcourir.pack(side=LEFT, expand=0, fill=NONE, padx=5)

    # Fin def

    # Début def

    def get_path(self):

        return self.file_path.get()  # On récupère la valeur de l'attribut file_path

    # Fin def

    # Début def

    def set_path(self, path):
        # On modfie le contenu de l'attribut file_path par path
        self.file_path.set(path)

    # Fin def

# Fin class PathEntry


# Début class FileEntry
class FileEntry(PathEntry):  # La class FileEntry hérite de la class PathEntry

    def __init__(self, master=None, texteLabel=""):  # On initialise l'objet FileEntry
        PathEntry.__init__(self, master, texteLabel)

    def slot_browse(self):

        # On parcourt les fichiers et on récupère l'adresse du fichier voulu
        fpath = FD.askopenfilename(
            filetypes=[("Fichier mind map", ".mm"), ("All types", ".*")])  # On autorise différents types de fichiers

        # On met à jour l'adresse du fichier
        self.set_path(fpath)

    # Fin def

# Fin class FileEntry


# Début class FolderEntry
class FolderEntry(PathEntry):  # La class FolderEntry hérite de la class PathEntry

    # Début def
    def __init__(self, master=None, texteLabel=""):  # On initialise l'objet FolderEntry
        PathEntry.__init__(self, master, texteLabel)
    # Fin def

    # Début def
    def slot_browse(self):

        # On parcourt les dossier et on récupère l'adresse du dossier voulu
        fpath = FD.askdirectory(title="Répertoire de travail")

        # On met à jour l'adresse du dossier
        self.set_path(fpath)

    # Fin def

# Fin class FolderEntry


# Début def

# Fonction qui cache le widget passé en paramètre
def dissimuler(widget):
    widget.forget()  # On cache le widget
# Fin def


# Début def

# Fonction qui affiche le widget passé en paramètre
def afficher(widget):
    widget.pack()  # Affichage du widget
# Fin def


# Début def

# Fonction qui vérifie que le fichier MindMap entré par l'utilisateur est correct
def verificationFichierMindMap(cadreInitial, cadreChoixMode, boutonGenerer, labelErreur, adresseMindMap):

    if(adresseMindMap[-3:] == ".mm"):  # On vérifie qu'il s'agit d'un fichier MindMap
        # On change le style du boutonGenerer pour passer en mode 'Normal'
        boutonGenerer['style'] = 'BoutonNormal.TButton'
        dissimuler(labelErreur)  # On cache le label erreur
        dissimuler(cadreInitial)  # On cache le cadre initial
        # afficher(cadreFinal) #On affiche le cadre final
        cadreInitial.master.geometry("200x60")
        afficher(cadreChoixMode)
        # genererSite(cadreInitial, cadreFinal, adresseMindMap, folderEntry.get_path()) #On appelle la fonction genererSite

    else:
        # En cas de fichier incorrect on passe le bouton en mode 'Erreur'
        boutonGenerer['style'] = 'BoutonErreur.TButton'
        # On affiche le label erreur et on le positionne en dessous du bouton Generer
        labelErreur.pack(side=BOTTOM, fill=BOTH)
# Fin def


# Début def

# La fonction démarre la génération du site en mode Objet
def genererSiteObjets(adresseMindMap, adresseSite):

    if adresseSite == "":  # Si l'utilisateur n'a pas entré d'adresse de stockage, on charge une adresse par défaut
        adresseSite = str(Path.home() / "Downloads")

    # On démarre la création du site à l'adresse souhaitée avec le programme objet
    generer_pages_objets(adresseMindMap, adresseSite)
# Fin def


# Début def

# La fonction démarre la génération du site avec le mode Liste
def genererSiteListes(adresseMindMap, adresseSite):

    if adresseSite == "":
        adresseSite = str(Path.home() / "Downloads")

    # On démarre la création du site avec le programme sans objet
    generer_pages_liste(adresseMindMap, adresseSite)
# Fin def


# Début def

# La fonction permet d'ouvrir le site Web
def ouvrirSite(adresse):
    if(adresse == ""):  # Si l'utilisateur n'a pas entré d'adresse de stockage, on charge l'adresse par défaut
        adresse = str(Path.home() / "Downloads")

    adresse = adresse + "/site/index.html"
    open("file:///" + adresse)  # Ouverture du site web
# Fin def


# Début def
def creerCadreInitial(cadreInitial, cadreFinal, cadreChoixMode):

    ########### Création et initialisation des différents styles pour les widgets ###########

    styleCadreHaut = ttk.Style()  # Création d'un objet style pour la frame CadreHaut

    # Configuration du style
    styleCadreHaut.configure('cadreHaut.TFrame',

                             background='ivory')

    styleLabelErreur = ttk.Style()
    styleLabelErreur.configure('labelErreur.TLabel',

                               font=('calibri', 12, 'bold'),

                               relief=FLAT)

    styleBoutonErreur = ttk.Style()
    styleBoutonErreur.configure('BoutonErreur.TButton',

                                font=('calibri', 15, 'bold'),

                                foreground='RED',

                                width=14)

    styleBoutonNormal = ttk.Style()
    styleBoutonNormal.configure('BoutonNormal.TButton',

                                font=('calibri', 15, 'bold'),

                                foreground='BLACK',

                                width=14)

    ########### Fin de la création et initialisation du style des widgets ###########

    ########### Création des widgets composant le cadre initial ###########

    # Création d'une frame en définissant le maitre, la taille et le style
    cadreHaut = ttk.Frame(cadreInitial, width=400,
                          height=130, style='cadreHaut.TFrame')

    cadreBas = ttk.Frame(cadreInitial, width=400, height=70)

    cadreBouton = ttk.Frame(cadreInitial, width=80, height=30)

    global fileEntry
    # Création objet FileEntry
    fileEntry = FileEntry(cadreInitial, texteLabel="Fichier .mm :")

    global folderEntry
    # Création objet FolderEntry
    folderEntry = FolderEntry(cadreInitial, texteLabel="Enregistrer    :")

    # Création d'un bouton
    boutonGenerer = ttk.Button(cadreBouton,

                               text='Générer',

                               style='BoutonNormal.TButton',

                               # Commande exécutée quand on clique sur le bouton
                               command=lambda: verificationFichierMindMap(cadreInitial, cadreChoixMode, boutonGenerer,
                                                                          labelErreur, fileEntry.get_path())

                               )

    labelErreur = ttk.Label(cadreBouton, text="Fichier .mm incorrect",
                            style='labelErreur.TLabel')  # Création d'un label

    ########### Fin création des widgets ###########

    ########### Affichage des widgets dans le cadre initial ###########

    # On positionne le widget en haut du cadre initial et il doit remplir toute la place disponible
    cadreHaut.pack(side=TOP, fill=BOTH)
    cadreBas.pack(side=BOTTOM)
    # On positionne le widget à une position précise
    cadreBouton.place(x=125, y=138)
    fileEntry.place(x=55, y=30)
    folderEntry.place(x=55, y=70)
    boutonGenerer.pack(fill=BOTH)

    ########### Fin affichage ###########

# Fin def


# Début def
def creerCadreFinal(cadreFinal, cadreInitial):

    ########### Création et initialisation des différents styles pour les widgets ###########

    styleCadreHaut = ttk.Style()
    styleCadreHaut.configure('cadreHaut.TFrame',

                             background='ivory')

    styleLabel = ttk.Style()  # Création d'un objet style pour le label

    # Configuration du style
    styleLabel.configure('label.TLabel',

                         font=('calibri', 12, 'bold'),

                         relief=GROOVE)

    styleBoutonsEcranFinal = ttk.Style()
    styleBoutonsEcranFinal.configure('Bouton.TButton',

                                     font=('calibri', 12, 'bold'),

                                     foreground='BLACK',

                                     width=10)

    ########### Fin de la création et initialisation du style des widgets ###########

    ########### Création des widgets composant le cadre initial ###########

    cadreHaut = ttk.Frame(cadreFinal, width=400,
                          height=130, style='cadreHaut.TFrame')

    # Création d'une frame en définissant son maitre et sa taille
    cadreBas = ttk.Frame(cadreFinal, width=400, height=70)

    label = ttk.Label(cadreHaut, text="Site Web généré", style='label.TLabel')

    # Chargement d'une image
    imageValider = PhotoImage(file='./images/valider.png')
    canvas = Canvas(cadreHaut, width=45, height=45)
    # Créer un cadre permettant d'insérer une image
    canvas.create_image(0, 0, anchor=NW, image=imageValider)
    canvas.image = imageValider  # On insère l'image dans le canvas

    boutonVisualiser = ttk.Button(cadreBas,

                                  text='Visualiser',

                                  style="Bouton.TButton",

                                  command=lambda: ouvrirSite(folderEntry.get_path()))

    # Création du bouton Redemarer
    boutonRedemarer = ttk.Button(cadreBas,

                                 text='Redémarrer',  # Texte affiché sur le bouton

                                 style="Bouton.TButton",  # Style du bouton défini

                                 command=lambda: [dissimuler(cadreFinal), afficher(cadreInitial)])  # Commande exécutée quand on clique sur le bouton

    boutonModifier = ttk.Button(cadreBas,

                                text='Modifier',  # Texte affiché sur le bouton

                                style="Bouton.TButton",  # Style du bouton défini

                                command=lambda: [startfile(fileEntry.get_path()), afficher(cadreInitial), dissimuler(cadreFinal)])  # Commande exécutée quand on clique sur le bouton

    ########### Fin création des widgets ###########

    ########### Affichage des widgets dans le cadre initial ###########

    cadreHaut.pack(side=TOP, fill=BOTH)
    # On positionne le widget en bas du cadre initial
    cadreBas.pack(side=BOTTOM)
    label.place(x=145, y=30)
    # On positionne le widget à une position x et y précise
    canvas.place(x=175, y=65)
    boutonVisualiser.place(x=280, y=20)
    boutonRedemarer.place(x=30, y=20)
    boutonModifier.place(x=156, y=20)

    ########### Fin affichage ###########

# Fin def


# Début def
def creerCadreChoixMode(cadreInitial, cadreFinal, cadreChoixMode):

    ########### Création et initialisation des différents styles pour les widgets ###########

    styleBouton = ttk.Style()
    styleBouton.configure('Bouton.TButton',

                          font=('calibri', 12, 'bold'),

                          foreground='BLACK',

                          width=10,
                          )

    ########### Fin de la création et initialisation du style des widgets ###########

    ########### Création des widgets composant le cadre initial ###########

    boutonModeObjet = ttk.Button(cadreChoixMode,

                                 text='Objet',  # Texte affiché sur le bouton

                                 style="Bouton.TButton",  # Style du bouton défini

                                 command=lambda: [genererSiteObjets(fileEntry.get_path(), folderEntry.get_path()), afficher(cadreFinal), dissimuler(cadreChoixMode), cadreInitial.master.geometry("400x200")])  # Commande exécutée quand on clique sur le bouton

    boutonModeNormal = ttk.Button(cadreChoixMode,

                                  text='Liste',  # Texte affiché sur le bouton

                                  style="Bouton.TButton",  # Style du bouton défini

                                  command=lambda: [genererSiteListes(fileEntry.get_path(), folderEntry.get_path()), afficher(cadreFinal), dissimuler(cadreChoixMode), cadreInitial.master.geometry("400x200")])  # Commande exécutée quand on clique sur le bouton

    ########### Fin création des widgets ###########

    ########### Affichage des widgets dans le cadre initial ###########

    # On affiche le boutonModeNormal dans la frame cadreChoixMode
    boutonModeNormal.pack(side=TOP)
    boutonModeObjet.pack(side=BOTTOM)

    ########### Fin affichage ###########

# Fin def


# Début def

def creerApplication(titreApplication):

    ########### Création fenêtre application ###########

    window = Tk()  # Création d'une fenêtre
    window.title(titreApplication)  # On défini le titre de la fenêtre
    window.geometry("400x200")  # Choix de la taille de l'application
    # Ajout d'une icone personnalisée
    window.iconphoto(False, PhotoImage(file="./images/icon.png"))
    # On désactive la possibilité de modifier la taille de l'application pour l'utilisateur
    window.resizable(width=0, height=0)

    ########### Fin création fenêtre application ###########

    cadreFinal = ttk.Frame(window)  # Création d'un objet Frale
    cadreInitial = ttk.Frame(window)
    cadreChoixMode = ttk.Frame(window)
    creerCadreChoixMode(cadreInitial, cadreFinal, cadreChoixMode)
    # Création du cadre initial et récupération de l'adresse du site Web
    creerCadreInitial(cadreInitial, cadreFinal, cadreChoixMode)
    creerCadreFinal(cadreFinal, cadreInitial)
    afficher(cadreInitial)  # Affichage du cadre initial

    window.mainloop()  # Affiche la fenêtre et attend une action de la part de l'utilisateur

# Fin def


creerApplication('Philia')  # Création de l'application
