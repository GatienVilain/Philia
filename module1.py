import tkinter as tk
 
def verificationMois(valeur) :
    if not valeur :
        return True
    elif valeur.isdigit() and 1 <= int(valeur) <= 12 :
        return True
    return False
 
def changerEtatBoutonValidation(*args) :
    boutonValider['state'] = tk.ACTIVE if varMois.get() else tk.DISABLED
 
def enregistrerSaisies() :
    pass
 
root = tk.Tk()
 
varMois = tk.StringVar()
varMois.trace('w', changerEtatBoutonValidation)
champMois = tk.Entry(root, textvariable=varMois, width=10, font=('', 30))
champMois.grid()
_cmd = champMois.register(verificationMois)
# %P défini ce que l'Entry contiendra si on autorise ou non cette nouvelle valeur
champMois.configure(validatecommand=(_cmd, '%P'), validate='key')
champMois.focus_set()
 
boutonValider = tk.Button(root, text='valider', command=enregistrerSaisies, state=tk.DISABLED)
boutonValider.grid()
 
root.mainloop()