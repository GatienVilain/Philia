from tkinter import*
import tkinter.filedialog as FD
import tkinter.messagebox as MB
import webbrowser
import os
from pathlib import Path

import tkinter.ttk as ttk
from programmes.generer_pages import *


class FileEntry (ttk.Frame):

    def __init__(self, master=None, nameButton="Parcourir", **kw):

        self.master = master
        self.nameButton = nameButton
        self.kw = kw

        # super class inits
        ttk.Frame.__init__(self, master)

        # widget inits

        self.init_widget(nameButton, **kw)

    # end def

    def init_widget(self, nameButton, **kw):

        # component inits

        self.label = ttk.Label(

            self,

            text=kw.get(

                "label",

                "Veuillez sélectionner un fichier, SVP:"
            )

        )

        self.file_path = StringVar()

        self.entry = Entry(

            self,

            textvariable=self.file_path,

            state=DISABLED,

            disabledbackground="WHITE",

            disabledforeground='BLACK'

        )

        self.button = ttk.Button(

            self,

            text=nameButton,

            command=self.slot_browse,

            underline=0,
        )

        # layout inits

        self.label.pack(side=LEFT, expand=0, fill=X)

        self.entry.pack(side=LEFT, expand=1, fill=X)

        self.button.pack(side=LEFT, expand=0, fill=NONE, padx=5)

    # end def

    def get_path(self):

        return self.file_path.get()

    # end def

    def slot_browse(self, tk_event=None, *args, **kw):

        # browse file path

        fpath = FD.askopenfilename(
            filetypes=[("Fichier mind map", ".mm"), ("All types", ".*")])
        # set entry's contents with file_path control variable

        self.file_path.set(fpath)

    # end def

    def get_path(self):

        return self.file_path.get()

    # end def

# end class FileEntry


class FolderEntry (ttk.Frame):

    def __init__(self, master=None, **kw):

        # super class inits

        ttk.Frame.__init__(self, master)

        # widget inits

        self.init_widget(**kw)

    # end def

    def init_widget(self, **kw):

        # component inits

        self.label = ttk.Label(

            self,

            text=kw.get(

                "label",

                "Veuillez sélectionner un dossier, SVP:"
            )
        )

        self.file_path = StringVar()

        self.entry = Entry(

            self,

            textvariable=self.file_path,

            state=DISABLED,

            disabledbackground="WHITE",

            disabledforeground='BLACK'
        )

        self.button = ttk.Button(

            self,

            text="Parcourir",

            command=self.slot_browse,

            underline=0,
        )

        # layout inits

        self.label.pack(side=LEFT, expand=0, fill=X, padx=4)

        self.entry.pack(side=LEFT, expand=1, fill=X)

        self.button.pack(side=LEFT, expand=0, fill=NONE, padx=5)

    # end def

    def slot_browse(self, tk_event=None, *args, **kw):

        # browse file path

        fpath = FD.askdirectory(title="Répertoire de travail")

        # set entry's contents with file_path control variable

        self.file_path.set(fpath)

    # end def

    def get_path(self):

        return self.file_path.get()

    # end def

# end class FolderOutput


def forget(widget):

    # This will remove the widget from toplevel
    # basically widget do not get deleted
    # it just becomes invisible and loses its position
    # and can be retrieve
    widget.forget()


def retrieve(widget):
    widget.pack()


def verificationFichier(adresse, cadreInitial, cadreFinal, boutonGenerer, labelErreur):
    if(adresse[-3:] == ".mm"):
        boutonGenerer['style'] = 'W2.TButton'
        forget(labelErreur)
        generer(cadreInitial, cadreFinal)

    else:
        boutonGenerer['style'] = 'W3.TButton'
        labelErreur.pack(side=BOTTOM, fill=BOTH)
        fileentry_sequence.entry.delete(0, END)


def generer(cadreInitial, cadreFinal):
    forget(cadreInitial)
    retrieve(cadreFinal)
    adresseMindMap = fileentry_sequence.get_path()
    adresseSite = folderentry_sequence.get_path()

    if adresseSite == "":
        adresseSite = str(Path.home() / "Downloads")

    # Rajouter appel fonction pour générer le site
    generer_pages(adresseMindMap, adresseSite)


def affichageEcranInit(cadreInitial, cadreFinal, styleButton):
    styleFrame1 = ttk.Style()
    styleFrame1.configure('frame1.TFrame', background='ivory')
    styleFrame2 = ttk.Style()
    styleFrame2.configure('frame2.TFrame', background='red')
    cadreInitial.pack()
    frame1 = ttk.Frame(cadreInitial, width=400,
                       height=130, style='frame1.TFrame')
    frame1.pack(side=TOP, fill=BOTH)
    frame2 = ttk.Frame(cadreInitial, width=400, height=70)
    frame2.pack(side=BOTTOM)
    frame3 = ttk.Frame(cadreInitial, width=80,
                       height=30, style='frame2.TFrame')
    frame3.place(x=125, y=138)

    global fileentry_sequence
    fileentry_sequence = FileEntry(cadreInitial, label="Fichier .mm :")
    fileentry_sequence.place(x=55, y=30)
    global folderentry_sequence
    folderentry_sequence = FolderEntry(cadreInitial, label="Enregistrer :")
    folderentry_sequence.place(x=55, y=70)
    styleBoutonErreur = ttk.Style()
    styleBoutonErreur.configure('W3.TButton', font=('calibri', 15, 'bold'),
                                foreground='RED', width=14)

    boutonGenerer = ttk.Button(frame3, text='Générer', style='W2.TButton', command=lambda: verificationFichier(
        fileentry_sequence.get_path(), cadreInitial, cadreFinal, boutonGenerer, label))
    boutonGenerer.pack(fill=BOTH)

    styleLabel = ttk.Style()
    styleLabel.configure('label.TLabel', font=(
        'calibri', 12, 'bold'), relief=FLAT)
    label = ttk.Label(frame3, text="Fichier .mm incorrect",
                      style='label.TLabel')


def ouvrirSite(adresse):
    if(adresse == ""):
        adresse = str(Path.home() / "Downloads")

    adresse = adresse + "/site/index.html"
    webbrowser.open("file:///" + adresse)


def affichageEcranFinal(cadreFinal, cadreInitial, styleButton):
    cadreFinal.pack()
    styleFrame1 = ttk.Style()
    styleFrame1.configure('frame1.TFrame', background='ivory')
    frame1 = ttk.Frame(cadreFinal, width=400,
                       height=130, style='frame1.TFrame')
    frame1.pack(side=TOP, fill=BOTH)
    frame1.propagate(False)

    frame2 = ttk.Frame(cadreFinal, width=400, height=70)
    frame2.pack(side=BOTTOM)

    frame3 = ttk.Frame(frame2, width=80, height=30)
    frame3.place(x=160, y=10)
    styleLabel = ttk.Style()
    styleLabel.configure('label.TLabel', font=(
        'calibri', 12, 'bold'), relief=GROOVE)
    label = ttk.Label(frame1, text="Site Web généré", style='label.TLabel')
    label.place(x=145, y=30)

    photo = PhotoImage(file='./src/images/valider.png')
    canvas = Canvas(frame1, width=45, height=45)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.image = photo
    canvas.place(x=175, y=65)

    boutonVisualiser = ttk.Button(frame2, text='Visualiser', style="W.TButton",
                                  command=lambda: ouvrirSite(folderentry_sequence.get_path()))
    boutonRedemarer = ttk.Button(frame2, text='Redémarer', style="W.TButton",  command=lambda: [
                                 forget(cadreFinal), retrieve(cadreInitial)])
    boutonVisualiser.place(x=280, y=20)
    boutonRedemarer.place(x=30, y=20)


def creationApplication(titreApplication):

    # Création fenêtre application

    window = Tk()
    window.title(titreApplication)
    window.geometry("400x200")
    window.iconphoto(False, PhotoImage(file="./src/images/icon.png"))
    window.resizable(width=0, height=0)

    # Fin création fenêtre application

    styleBoutonsEcranFinal = ttk.Style()
    styleBoutonsEcranFinal.configure('W.TButton', font=('calibri', 12, 'bold'),
                                     foreground='BLACK', width=10)

    styleBoutonEcranInit = ttk.Style()
    styleBoutonEcranInit.configure('W2.TButton', font=('calibri', 15, 'bold'),
                                   foreground='BLACK', width=14)

    cadreFinal = ttk.Frame(window)
    cadreInitial = ttk.Frame(window)
    affichageEcranInit(cadreInitial, cadreFinal, styleBoutonEcranInit)
    affichageEcranFinal(cadreFinal, cadreInitial, styleBoutonsEcranFinal)

    # print(fileentry_sequence.get_path()) #Permet de récupérer l'adresse du fichier.mm

    window.mainloop()


creationApplication('Générateur de site web')
