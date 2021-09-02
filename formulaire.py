#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 08:21:42 2021

@author: ejetzer
"""

import tkinter as tk

from configparser import ConfigParser

import pyperclip


class Modèle:
    
    def __init__(self, f: str, section: str = 'default'):
        self.fichier = f
        self.config = ConfigParser(interpolation=None)
        self.config.read(f)
        self.section = section
    
    def kargs(self):
        formations = {}
        modèle = ''
        
        section = self.config[self.section]
        for clé in section.keys():
            if clé == 'modèle':
                f = section[clé]
                with open(f) as f:
                    modèle = f.read()
            else:
                formations[clé] = section[clé]
        
        return {'formations': formations, 'modèle': modèle}

class Formulaire(tk.Frame):
    
    def __init__(self, formations: dict[str, str], modèle: str, master=None):
        self.formations = formations
        self.modèle = modèle
        self.lien = '[{texte}]({url})'
        super().__init__(master=master)
        
        self.créer_champs()
    
    def pack(self, *args, **kargs):
        tk.Label(master=self, text='Nom').pack(anchor='e')
        self.champs['nom'].pack(anchor='w')
        tk.Label(master=self, text='Responsable').pack(anchor='e')
        self.champs['responsable'].pack(anchor='w')
        self.champs['formations'].pack()
        tk.Button(master=self, text='Copier', command=lambda: self.copier()).pack()
        super().pack(*args, **kargs)
        
    def grid(self, *args, **kargs):
        super().grid(*args, **kargs)
    
    def créer_champs(self):
        self.nom = tk.StringVar()
        self.responsable = tk.StringVar()
        self.champs = {'nom': tk.Entry(master=self, textvariable=self.nom),
                       'formations': tk.Listbox(master=self,
                                                selectmode='multiple'),
                       'responsable': tk.Entry(master=self, textvariable=self.responsable)}
        
        for f in self.formations:
            self.champs['formations'].insert(tk.END, f)
    
    def get(self):
        formations = []
        for curseur in self.champs['formations'].curselection():
            formations.append(self.champs['formations'].get(curseur))
            
        return {'nom': self.nom.get(),
                'formations': formations,
                'responsable': self.responsable.get()}
    
    def copier(self):
        valeurs = self.get()
        
        formations = ''
        for f in valeurs['formations']:
            url = self.formations[f]
            formations += f'- [{f}]({url}]\n'
        valeurs['formations'] = formations
        
        résultat = self.modèle.format(**valeurs)
        pyperclip.copy(résultat)


if __name__ == '__main__':
    racine = tk.Tk()
    modèle = Modèle('teams.config')
    fenêtre = Formulaire(master=racine, **modèle.kargs())
    fenêtre.pack()
    racine.mainloop()