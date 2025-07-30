import json
import os
import random
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import tkinter as tk

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  


class Personne:
    def __init__(self, identifiant, mot_de_passe):
        self.__id = identifiant
        self.__mdp = mot_de_passe

    def get_id(self):
        return self.__id

    def get_mdp(self):
        return self.__mdp

    def set_mdp(self, nouveau_mdp):
        self.__mdp = nouveau_mdp

    def verifier_mdp(self, mot_de_passe):
        return self.__mdp == mot_de_passe


class Compte:
    def __init__(self, numero, solde):
        self.__numero = numero
        self.__solde = solde

    def get_numero(self):
        return self.__numero

    def get_solde(self):
        return self.__solde

    def deposer(self, montant):
        self.__solde += montant

    def retirer(self, montant):
        if self.__solde >= montant:
            self.__solde -= montant
            return True
        return False


class Client(Personne):
    def __init__(self, identifiant, mot_de_passe, num_compte, solde):
        Personne.__init__(self, identifiant, mot_de_passe)
        self.__compte = Compte(num_compte, solde)

    def get_compte(self):
        return self.__compte


class Agent(Personne):
    def __init__(self):
        Personne.__init__(self, "agent", "0000")


class BanqueSystem:
    def __init__(self):
        self.__clients = {}
        self.__agent = Agent()
        self.__load_data()

    def get_clients(self):
        return self.__clients

    def __load_data(self):
        if os.path.exists("user_data.json"):
            try:
                with open("user_data.json", "r") as f:
                    data = json.load(f)
                for cid in data["clients"]:
                    infos = data["clients"][cid]
                    identifiant = int(cid)
                    mdp = infos["mdp"]
                    compte = infos["compte"]
                    solde = infos["solde"]
                    self.__clients[identifiant] = Client(identifiant, mdp, compte, solde)
            except Exception as e:
                print(f"Erreur lors du chargement des données: {e}")

    def __save_data(self):
        data = {"clients": {}}
        for cid in self.__clients:
            client = self.__clients[cid]
            data["clients"][str(cid)] = {
                "mdp": client.get_mdp(),
                "compte": client.get_compte().get_numero(),
                "solde": client.get_compte().get_solde()
            }
        try:
            with open("user_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")

    def ajouter_client(self, mot_de_passe, solde):
        nouvel_id = 1
        while nouvel_id in self.__clients:
            nouvel_id += 1
        numero_compte = int(str(nouvel_id) + str(random.randint(100, 999)))
        self.__clients[nouvel_id] = Client(nouvel_id, mot_de_passe, numero_compte, solde)
        self.__save_data()
        return nouvel_id

    def supprimer_client(self, id_client):
        if id_client in self.__clients:
            del self.__clients[id_client]
            self.__save_data()
            return True
        return False

    def authentifier_client(self, id_client, mot_de_passe):
        if id_client in self.__clients:
            return self.__clients[id_client].verifier_mdp(mot_de_passe)
        return False

    def authentifier_agent(self, mot_de_passe):
        return self.__agent.verifier_mdp(mot_de_passe)

    def sauvegarder(self):
        self.__save_data()


class DialogueModerne(ctk.CTkToplevel):
    def __init__(self, parent, titre, message, type_input="text"):
        super().__init__(parent)
        self.title(titre)
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.result = None
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        prompt_label = ctk.CTkLabel(main_frame, text=message, font=ctk.CTkFont(size=16))
        prompt_label.pack(pady=(10, 20))
        
        if type_input == "password":
            self.entry = ctk.CTkEntry(main_frame, placeholder_text="Saisir le mot de passe", show="*", width=300)
        else:
            self.entry = ctk.CTkEntry(main_frame, placeholder_text="Saisir la valeur", width=300)
        self.entry.pack(pady=10)
        self.entry.focus()
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ok_button = ctk.CTkButton(button_frame, text="Valider", command=self.ok_clicked, width=100)
        ok_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Annuler", command=self.cancel_clicked, width=100)
        cancel_button.pack(side="left", padx=10)
        
        self.bind('<Return>', lambda e: self.ok_clicked())
        self.entry.bind('<Return>', lambda e: self.ok_clicked())
    
    def ok_clicked(self):
        self.result = self.entry.get()
        self.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.destroy()


class BanqueApp:
    def __init__(self):
        self.__root = ctk.CTk()
        self.__root.title("Système Bancaire")
        self.__root.geometry("800x600")
        self.__root.minsize(600, 400)
        
        try:
            self.__root.iconbitmap("JA-logo.ico")
        except:
            pass
        
        self.__systeme = BanqueSystem()
        self.__client_id = None
        
        self.__root.grid_columnconfigure(0, weight=1)
        self.__root.grid_rowconfigure(0, weight=1)
        
        self.__afficher_login()

    def __effacer_fenetre(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def __afficher_login(self):
        self.__effacer_fenetre()
        
        main_frame = ctk.CTkFrame(self.__root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 30))
        
        title_label = ctk.CTkLabel(header_frame, text="🏦 Système Bancaire", 
                                  font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Solutions Bancaires Sécurisées", 
                                     font=ctk.CTkFont(size=16), text_color="gray")
        subtitle_label.pack(pady=(5, 0))
        
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.grid(row=1, column=0, pady=20, padx=50, sticky="ew")
        login_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(login_frame, text="Connexion", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, pady=(30, 20))
        
        ctk.CTkLabel(login_frame, text="ID Utilisateur:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, sticky="w", padx=30, pady=(10, 5))
        self.__entry_id = ctk.CTkEntry(login_frame, placeholder_text="Saisir votre ID", 
                                      width=300, height=40)
        self.__entry_id.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        ctk.CTkLabel(login_frame, text="Mot de passe:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, sticky="w", padx=30, pady=(10, 5))
        self.__entry_mdp = ctk.CTkEntry(login_frame, placeholder_text="Saisir votre mot de passe", 
                                       show="*", width=300, height=40)
        self.__entry_mdp.grid(row=4, column=0, padx=30, pady=(0, 25))
        
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, pady=(0, 30))
        
        client_btn = ctk.CTkButton(button_frame, text="🏠 Connexion Client", 
                                  command=self.__login_client, width=160, height=40,
                                  font=ctk.CTkFont(size=14))
        client_btn.pack(side="left", padx=10)
        
        agent_btn = ctk.CTkButton(button_frame, text="👤 Connexion Agent", 
                                 command=self.__login_agent, width=160, height=40,
                                 font=ctk.CTkFont(size=14))
        agent_btn.pack(side="left", padx=10)
        
        theme_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        theme_frame.grid(row=2, column=0, pady=10)
        
        theme_switch = ctk.CTkSwitch(theme_frame, text="Mode Sombre", command=self.__toggle_theme)
        theme_switch.pack()
        theme_switch.select()
        
        self.__entry_mdp.bind('<Return>', lambda e: self.__login_client())

    def __toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def __login_client(self):
        identifiant = self.__entry_id.get().strip()
        mot_de_passe = self.__entry_mdp.get()
        
        if not identifiant or not mot_de_passe:
            self.__show_error("Veuillez remplir tous les champs")
            return
            
        if identifiant.isdigit() and self.__systeme.authentifier_client(int(identifiant), mot_de_passe):
            self.__client_id = int(identifiant)
            self.__menu_client()
        else:
            self.__show_error("Identifiants client invalides")

    def __login_agent(self):
        mot_de_passe = self.__entry_mdp.get()
        if self.__systeme.authentifier_agent(mot_de_passe):
            self.__menu_agent()
        else:
            self.__show_error("Mot de passe agent invalide")

    def __menu_client(self):
        self.__effacer_fenetre()
        client = self.__systeme.get_clients()[self.__client_id]
        
        main_frame = ctk.CTkFrame(self.__root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        
        sidebar = ctk.CTkFrame(main_frame, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        sidebar.grid_propagate(False)
        
        user_frame = ctk.CTkFrame(sidebar)
        user_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(user_frame, text="👤", font=ctk.CTkFont(size=40)).pack(pady=10)
        ctk.CTkLabel(user_frame, text=f"Client #{client.get_id()}", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkLabel(user_frame, text=f"Compte: {client.get_compte().get_numero()}", 
                    font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(5, 10))
        
        menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_frame.pack(fill="x", padx=20, pady=20)
        
        buttons = [
            ("💰 Consulter Solde", self.__afficher_solde),
            ("💳 Déposer", self.__deposer),
            ("💸 Retirer", self.__retirer),
            ("🔒 Changer MDP", self.__changer_mdp),
            ("🚪 Déconnexion", self.__afficher_login)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(menu_frame, text=text, command=command, 
                               width=200, height=40, font=ctk.CTkFont(size=14))
            btn.pack(pady=5)
        
        self.__content_frame = ctk.CTkFrame(main_frame)
        self.__content_frame.grid(row=0, column=1, sticky="nsew")
        
        welcome_frame = ctk.CTkFrame(self.__content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(welcome_frame, text="Bienvenue dans votre Compte", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=40)
        
        balance_frame = ctk.CTkFrame(welcome_frame)
        balance_frame.pack(pady=20)
        
        ctk.CTkLabel(balance_frame, text="Solde Actuel", 
                    font=ctk.CTkFont(size=18)).pack(pady=(20, 10))
        ctk.CTkLabel(balance_frame, text=f"{client.get_compte().get_solde():.2f} DH", 
                    font=ctk.CTkFont(size=36, weight="bold"), text_color="green").pack(pady=(0, 20))

    def __afficher_solde(self):
        client = self.__systeme.get_clients()[self.__client_id]
        self.__show_info("Solde du Compte", f"Votre solde actuel est: {client.get_compte().get_solde():.2f} DH")

    def __deposer(self):
        dialog = DialogueModerne(self.__root, "Déposer de l'Argent", "Saisir le montant à déposer:")
        self.__root.wait_window(dialog)
        
        if dialog.result:
            try:
                montant = float(dialog.result)
                if montant > 0:
                    client = self.__systeme.get_clients()[self.__client_id]
                    client.get_compte().deposer(montant)
                    self.__systeme.sauvegarder()
                    self.__show_success(f"Dépôt de {montant:.2f} DH effectué avec succès")
                    self.__menu_client()
                else:
                    self.__show_error("Le montant doit être positif")
            except ValueError:
                self.__show_error("Veuillez saisir un nombre valide")

    def __retirer(self):
        dialog = DialogueModerne(self.__root, "Retirer de l'Argent", "Saisir le montant à retirer:")
        self.__root.wait_window(dialog)
        
        if dialog.result:
            try:
                montant = float(dialog.result)
                if montant > 0:
                    client = self.__systeme.get_clients()[self.__client_id]
                    if client.get_compte().retirer(montant):
                        self.__systeme.sauvegarder()
                        self.__show_success(f"Retrait de {montant:.2f} DH effectué avec succès")
                        self.__menu_client()
                    else:
                        self.__show_error("Solde insuffisant")
                else:
                    self.__show_error("Le montant doit être positif")
            except ValueError:
                self.__show_error("Veuillez saisir un nombre valide")

    def __changer_mdp(self):
        dialog = DialogueModerne(self.__root, "Changer Mot de Passe", "Saisir le nouveau mot de passe:", "password")
        self.__root.wait_window(dialog)
        
        if dialog.result:
            client = self.__systeme.get_clients()[self.__client_id]
            client.set_mdp(dialog.result)
            self.__systeme.sauvegarder()
            self.__show_success("Mot de passe modifié avec succès")

    def __menu_agent(self):
        self.__effacer_fenetre()
        
        main_frame = ctk.CTkFrame(self.__root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        
        sidebar = ctk.CTkFrame(main_frame, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        sidebar.grid_propagate(False)
        
        agent_frame = ctk.CTkFrame(sidebar)
        agent_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(agent_frame, text="👤", font=ctk.CTkFont(size=40)).pack(pady=10)
        ctk.CTkLabel(agent_frame, text="Agent Bancaire", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkLabel(agent_frame, text="Administrateur", 
                    font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(5, 10))
        
        menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_frame.pack(fill="x", padx=20, pady=20)
        
        buttons = [
            ("➕ Ajouter Client", self.__ajouter_client),
            ("❌ Supprimer Client", self.__supprimer_client),
            ("👥 Voir tous les Clients", self.__voir_clients),
            ("💾 Exporter Données", self.__exporter),
            ("🚪 Déconnexion", self.__afficher_login)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(menu_frame, text=text, command=command, 
                               width=200, height=40, font=ctk.CTkFont(size=14))
            btn.pack(pady=5)
        
        self.__content_frame = ctk.CTkFrame(main_frame)
        self.__content_frame.grid(row=0, column=1, sticky="nsew")
        
        self.__show_dashboard()

    def __show_dashboard(self):
        for widget in self.__content_frame.winfo_children():
            widget.destroy()
        
        dashboard_frame = ctk.CTkFrame(self.__content_frame)
        dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(dashboard_frame, text="Tableau de Bord Agent", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        
        stats_frame = ctk.CTkFrame(dashboard_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        clients = self.__systeme.get_clients()
        total_clients = len(clients)
        total_balance = sum(client.get_compte().get_solde() for client in clients.values())
        
        ctk.CTkLabel(stats_frame, text=f"Total Clients: {total_clients}", 
                    font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkLabel(stats_frame, text=f"Solde Total Banque: {total_balance:.2f} DH", 
                    font=ctk.CTkFont(size=18)).pack(pady=10)

    def __voir_clients(self):
        for widget in self.__content_frame.winfo_children():
            widget.destroy()
        
        clients_frame = ctk.CTkFrame(self.__content_frame)
        clients_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(clients_frame, text="Tous les Clients", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        scrollable_frame = ctk.CTkScrollableFrame(clients_frame, height=400)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        clients = self.__systeme.get_clients()
        for client_id, client in clients.items():
            client_frame = ctk.CTkFrame(scrollable_frame)
            client_frame.pack(fill="x", pady=5)
            
            info_text = f"ID: {client_id} | Compte: {client.get_compte().get_numero()} | Solde: {client.get_compte().get_solde():.2f} DH"
            ctk.CTkLabel(client_frame, text=info_text, font=ctk.CTkFont(size=14)).pack(pady=10)

    def __ajouter_client(self):
        dialog = DialogueModerne(self.__root, "Ajouter Client", "Saisir le mot de passe du nouveau client:", "password")
        self.__root.wait_window(dialog)
        
        if not dialog.result:
            return
        
        mdp = dialog.result
        
        balance_dialog = DialogueModerne(self.__root, "Ajouter Client", "Saisir le solde initial:")
        self.__root.wait_window(balance_dialog)
        
        if balance_dialog.result:
            try:
                solde = float(balance_dialog.result)
                if solde >= 0:
                    nouvel_id = self.__systeme.ajouter_client(mdp, solde)
                    self.__show_success(f"Client ajouté avec succès!\nID Client: {nouvel_id}")
                    self.__show_dashboard()
                else:
                    self.__show_error("Le solde initial ne peut pas être négatif")
            except ValueError:
                self.__show_error("Veuillez saisir un nombre valide pour le solde")

    def __supprimer_client(self):
        dialog = DialogueModerne(self.__root, "Supprimer Client", "Saisir l'ID du client à supprimer:")
        self.__root.wait_window(dialog)
        
        if dialog.result and dialog.result.isdigit():
            client_id = int(dialog.result)
            if self.__systeme.supprimer_client(client_id):
                self.__show_success("Client supprimé avec succès")
                self.__show_dashboard()
            else:
                self.__show_error("Client non trouvé")
        elif dialog.result:
            self.__show_error("Veuillez saisir un ID client valide")

    def __exporter(self):
        self.__systeme.sauvegarder()
        self.__show_success("Données exportées avec succès vers 'user_data.json'")

    def __show_error(self, message):
        messagebox.showerror("Erreur", message)

    def __show_success(self, message):
        messagebox.showinfo("Succès", message)

    def __show_info(self, title, message):
        messagebox.showinfo(title, message)

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    app = BanqueApp()
    app.run()