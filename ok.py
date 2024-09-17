import customtkinter as ctk
from PIL import Image, ImageTk
import pygame
import numpy as np
import json  
import os  
from space_shooter.space import *

# Inicializa o Pygame
pygame.init()


class BaseWindow:
    def __init__(self, root, title, size):
        self.root = root
        self.window = ctk.CTkToplevel(self.root)
        self.window.title(title)
        self.window.geometry(size)

    def show(self):
        self.window.deiconify()

    def close(self):
        self.window.destroy()

class MainMenu(Game):
    def __init__(self, root, username=None):
        self.root = root
        self.root.title("Menu Principal")
        self.image= ctk.CTkImage(Image.open(join('images','lua.png')), size=(64,64))
        self.image1 = ctk.CTkImage(Image.open(join('images','opcao.png')), size=(36,36))
        self.image2 = ctk.CTkImage(Image.open(join('images','sair.png')), size=(32,32))
        self.image3 = ctk.CTkImage(Image.open(join('images','login.png')), size=(40,40))
        self.image4 = ctk.CTkImage(Image.open(join('images','create.png')), size=(40,40))

        self.username = username
        self.filepath = "usuarios.json"
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump([], file)

        if self.username:
            self.user_label = ctk.CTkLabel(self.root, text=f"Bem-vindo, {self.username}!")
            self.user_label.pack()

        self.root.geometry("720x540")

        # Criando um Tabview para dividir as opções do app e usuário
        self.tabview = ctk.CTkTabview(self.root, width=700, height=500)
        self.tabview.pack(pady=20)

        # Adicionando duas guias ao Tabview
        self.tabview.add("App Options")  
        self.tabview.add("User Options")  

        # Adicionando botões na aba de Opções do App
        self.start_button = ctk.CTkButton(self.tabview.tab("App Options"), text="Iniciar Jogo", command=self.start_game, image=self.image, hover_color='#3a2e3f', fg_color='transparent', text_color='black')
        self.start_button.pack(pady=20)
        self.options_button = ctk.CTkButton(self.tabview.tab("App Options"), text="Opções", command=self.show_options, hover_color='#3a2e3f', fg_color='transparent', text_color='black', image=self.image1)
        self.options_button.pack(pady=20)
        self.exit_button = ctk.CTkButton(self.tabview.tab("App Options"), text="Sair", command=self.root.quit, hover_color='#3a2e3f', fg_color='transparent', text_color='black', image=self.image2)
        self.exit_button.pack(pady=20)

        # Adicionando botões na aba de Opções do Usuário
        self.login_button = ctk.CTkButton(self.tabview.tab("User Options"), text="Login", command=self.login_account, hover_color='#3a2e3f', fg_color='transparent', text_color='black', image=self.image3)
        self.login_button.pack(pady=20)
        self.createaccount_button = ctk.CTkButton(self.tabview.tab("User Options"), text="Create Account", command=self.create_account, hover_color='#3a2e3f', fg_color='transparent', text_color='black', image=self.image4)
        self.createaccount_button.pack(pady=20)


    def hide_login_buttons(self):
        """Esconde os botões de login e criar conta"""
        self.login_button.pack_forget()
        self.createaccount_button.pack_forget()

    def show_login_buttons(self):
        """Mostra os botões de login e criar conta"""
        self.login_button.pack(pady=20)
        self.createaccount_button.pack(pady=20)

    def start_game(self):
        self.root.destroy()  # Fecha a janela principal do Tkinter
        game_instance = Game()  # Crie uma instância do seu jogo
        game_instance.run()  # Execute o jogo

    def show_options(self):
        options_window = Options(self.root)
        options_window.show()

    def create_account(self):
        login_window = createaccount(self.root, self.filepath)
        login_window.show()

    def login_account(self):
        login_window = login_acount(self.root, self, self.filepath)  
        login_window.show()

    def hide_menu(self):
        """Esconde todo o menu principal"""
        self.start_button.pack_forget()
        self.options_button.pack_forget()
        self.exit_button.pack_forget()
        self.hide_login_buttons()

    def show(self):
        """Método para exibir a interface do menu principal"""
        self.start_button.pack(pady=20)
        self.options_button.pack(pady=20)
        self.exit_button.pack(pady=20)
        if not self.username:
            self.show_login_buttons()

class Options(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Opções", "300x500")

        label = ctk.CTkLabel(self.window, text="Opções do Jogo", font=("Arial", 16))
        label.pack(pady=20)

        # Switch para mudar o modo de aparência (Claro/Escuro)
        self.appearance_label = ctk.CTkLabel(self.window, text="Modo de Aparência:").pack(pady=(10, 5))
        self.appearance_mode = "dark"  
        self.appearance_switch = ctk.CTkSwitch(self.window, text="Escuro", command=self.tema).pack(pady=(0, 20))

        # Exemplo de controle de volume
        self.volume_label = ctk.CTkLabel(self.window, fg_color='transparent', text_color='black')
        self.volume_label.pack(pady=(10, 5))

        self.volume_slider = ctk.CTkSlider(self.window, from_=0, to=100, number_of_steps=10, )
        self.volume_slider.set(50)  
        self.volume_slider.pack(pady=(0, 20))

        # Exemplo de controle de dificuldade
        self.difficulty_label = ctk.CTkLabel(self.window, text="Dificuldade:",)
        self.difficulty_label.pack(pady=(10, 5))

        self.difficulty_menu = ctk.CTkOptionMenu(self.window, values=["Fácil", "Médio", "Difícil"])
        self.difficulty_menu.set("Médio")  
        self.difficulty_menu.pack(pady=(0, 20))

        # Botão para salvar as configurações
        save_button = ctk.CTkButton(self.window, text="Salvar", command=self.salvar_opcoes,hover_color='#3a2e3f', fg_color='transparent', text_color='black')
        save_button.pack(pady=10)

        close_button = ctk.CTkButton(self.window, text="Fechar", command=self.close, hover_color='#3a2e3f', fg_color='transparent', text_color='black')
        close_button.pack(pady=10)

    def tema(self):
        """Alterna entre modo claro e escuro"""
        if self.appearance_mode == "dark":
            ctk.set_appearance_mode("light")  
            self.appearance_switch.configure(text="Escuro")
            self.appearance_mode = "light"
        else:
            ctk.set_appearance_mode("dark")  
            self.appearance_switch.configure(text="Claro")
            self.appearance_mode = "dark"

    def salvar_opcoes(self):
        volume = self.volume_slider.get()
        dificuldade = self.difficulty_menu.get()
        
class login_acount(BaseWindow):
    def __init__(self, root, main_menu, filepath):
        super().__init__(root, "Login", "700x400")
        self.main_menu = main_menu
        self.filepath = filepath

        self.image = ctk.CTkImage(Image.open(join('images','login.png')), size=(40,40))
        self.image1 = ctk.CTkImage(Image.open(join('images','info.png')), size=(40,40))
        self.image2 = ctk.CTkImage(Image.open(join('images','edit.png')), size=(40,40))
        self.image3 = ctk.CTkImage(Image.open(join('images','logout.png')), size=(40,40))
        self.image4 = ctk.CTkImage(Image.open(join('images','delete.png')), size=(40,40))

        ctk.CTkLabel(self.window, text="Faça login", width=55,height=50, font=("arial bond", 30)).pack(pady=20)
        
        self.caixa1 = ctk.CTkEntry(self.window, width=200, placeholder_text="Escreva seu username", height=50)
        self.caixa1.pack(pady=2)

        self.caixa2 = ctk.CTkEntry(self.window, width=200, show='*', placeholder_text="Escreva sua senha", height=50)
        self.caixa2.pack(pady=2)

        login_button = ctk.CTkButton(self.window, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.caixa1.get()
        senha = self.caixa2.get()
        text_var = ctk.StringVar(value=username)

        with open(self.filepath, 'r') as file:
            usuarios = json.load(file)

        for usuario in usuarios:
            if usuario['username'] == username and usuario['senha'] == senha:
                # Exibe uma imagem de login bem-sucedido
                image_label = ctk.CTkLabel(self.main_menu.tabview.tab("User Options"), text=None, image=self.image)
                image_label.pack(padx=20)

                # Exibe o nome de usuário
                login_label = ctk.CTkLabel(self.main_menu.tabview.tab("User Options"), textvariable=text_var)
                login_label.pack()

                # Esconde os botões de login e criar conta
                self.main_menu.hide_login_buttons()

                # Adiciona o botão "Exibir Informações"
                info_button = ctk.CTkButton(self.main_menu.tabview.tab("User Options"), text="Exibir Informações", command=lambda: self.exibir_informacoes_usuario(usuario), hover_color='#3a2e3f', fg_color='transparent', text_color='black', image= self.image1)
                info_button.pack(pady=10)

                # Botão para editar informações
                edit_button = ctk.CTkButton(self.main_menu.tabview.tab("User Options"), text="Editar Informações", command=lambda: self.editar_informacoes_usuario(usuario),hover_color='#3a2e3f', fg_color='transparent', text_color='black', image= self.image2)
                edit_button.pack(pady=10)

                # Botão de logout
                logout_button = ctk.CTkButton(self.main_menu.tabview.tab("User Options"), text="Logout", command=self.logout,hover_color='#3a2e3f', fg_color='transparent', text_color='black', image= self.image3)
                logout_button.pack(pady=10)

                # Botão para deletar a conta
                delete_button = ctk.CTkButton(self.main_menu.tabview.tab("User Options"), text="Deletar Conta", command=lambda: self.deletar_conta(usuario),hover_color='#3a2e3f', fg_color='transparent', text_color='black', image= self.image4)
                delete_button.pack(pady=10)

                self.close()
                return
            
    def exibir_informacoes_usuario(self, usuario):
        # Exibe mais informações do usuário ao clicar no botão
        info_window = ctk.CTkToplevel(self.root)  
        info_window.geometry("300x300")
            
        # Exibe as informações do usuário
        ctk.CTkLabel(info_window, text=f"Nome: {usuario['nome']}").pack(pady=5)
        ctk.CTkLabel(info_window, text=f"Usuário: {usuario['username']}").pack(pady=5)
        ctk.CTkLabel(info_window, text=f"Mês de Nascimento: {usuario['mes_nascimento']}").pack(pady=5)
        ctk.CTkLabel(info_window, text=f"Senha: {usuario['senha']}").pack(pady=5)  

    def editar_informacoes_usuario(self, usuario):
        # Cria uma nova janela para editar informações
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.geometry("400x400")
        
        # Labels e campos para editar os dados do usuário
        ctk.CTkLabel(edit_window, text="Editar Informações").pack(pady=10)

        nome_entry = ctk.CTkEntry(edit_window, width=200, placeholder_text="Nome Completo")
        nome_entry.insert(0, usuario['nome'])  # Preenche com o nome atual
        nome_entry.pack(pady=5)

        username_entry = ctk.CTkEntry(edit_window, width=200, placeholder_text="Username")
        username_entry.insert(0, usuario['username'])  # Preenche com o username atual
        username_entry.pack(pady=5)

        mes_entry = ctk.CTkOptionMenu(edit_window, values=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                                                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
        mes_entry.set(usuario['mes_nascimento'])  # Preenche com o mês de nascimento atual
        mes_entry.pack(pady=5)

        senha_entry = ctk.CTkEntry(edit_window, width=200, placeholder_text="Senha", show='*')
        senha_entry.insert(0, usuario['senha'])  # Preenche com a senha atual
        senha_entry.pack(pady=5)

        # Botão para salvar as edições
        salvar_button = ctk.CTkButton(edit_window, text="Salvar", command=lambda: self.salvar_edicoes_usuario(usuario, nome_entry.get(), username_entry.get(), mes_entry.get(), senha_entry.get(), edit_window))
        salvar_button.pack(pady=20)

    def salvar_edicoes_usuario(self, usuario, novo_nome, novo_username, novo_mes, nova_senha, edit_window):
        with open(self.filepath, 'r') as file:
            usuarios = json.load(file)

        # Atualiza as informações do usuário
        for u in usuarios:
            if u['username'] == usuario['username']:  
                u['nome'] = novo_nome
                u['username'] = novo_username
                u['mes_nascimento'] = novo_mes
                u['senha'] = nova_senha
                break

        # Escreve as informações atualizadas de volta no arquivo JSON
        with open(self.filepath, 'w') as file:
            json.dump(usuarios, file, indent=4)

        # Fecha a janela de edição
        edit_window.destroy()

    def logout(self):
        
        # Limpa as informações da interface do usuário
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.main_menu1 = MainMenu
        self.main_menu1(self.root)
        self.username = None

    def deletar_conta(self, usuario):
        """Deleta a conta do usuário e faz logout"""
        # Confirmação de exclusão
        confirm = ctk.CTkToplevel(self.root)
        confirm.title("Confirmar Exclusão")
        confirm.geometry("300x150")

        confirm_label = ctk.CTkLabel(confirm, text="Tem certeza que deseja deletar sua conta?")
        confirm_label.pack(pady=10)

        def confirmar_delecao():
            # Remove o usuário do arquivo JSON
            with open(self.filepath, 'r') as file:
                usuarios = json.load(file)

            # Filtra os usuários, removendo o usuário atual
            usuarios = [u for u in usuarios if u['username'] != usuario['username']]

            # Salva as alterações
            with open(self.filepath, 'w') as file:
                json.dump(usuarios, file, indent=4)

            confirm.destroy()
            self.logout()  

        # Botões de confirmação e cancelamento
        confirm_button = ctk.CTkButton(confirm, text="Deletar", command=confirmar_delecao)
        confirm_button.pack(pady=5)

        cancel_button = ctk.CTkButton(confirm, text="Cancelar", command=confirm.destroy)
        cancel_button.pack(pady=5)

class createaccount(BaseWindow):
    def __init__(self, root, filepath):
        super().__init__(root, "Criar Conta", "700x500")
        self.filepath = filepath

        # Frame para o conteúdo da janela
        content_frame = ctk.CTkFrame(self.window, width=680, height=340)
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Título
        title_label = ctk.CTkLabel(content_frame, text="Criar Conta", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Escolha do mês
        month_label = ctk.CTkLabel(content_frame, text="Escolha seu mês de nascimento:", font=("Arial", 12))
        month_label.pack(anchor='w', padx=10)

        self.mes = ctk.CTkOptionMenu(content_frame, values=[
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ])
        self.mes.pack(pady=10, padx=10, fill='x')

        # Entrada para nome completo
        name_label = ctk.CTkLabel(content_frame, text="Nome completo:", font=("Arial", 12))
        name_label.pack(anchor='w', padx=10)

        self.caixa = ctk.CTkEntry(content_frame, width=300, placeholder_text="Escreva seu nome completo")
        self.caixa.pack(pady=10, padx=10, fill='x')

        # Entrada para username
        username_label = ctk.CTkLabel(content_frame, text="Nome de usuário:", font=("Arial", 12))
        username_label.pack(anchor='w', padx=10)

        self.caixa1 = ctk.CTkEntry(content_frame, width=300, placeholder_text="Escreva seu username")
        self.caixa1.pack(pady=10, padx=10, fill='x')

        # Entrada para senha
        password_label = ctk.CTkLabel(content_frame, text="Crie sua senha:", font=("Arial", 12))
        password_label.pack(anchor='w', padx=10)

        self.caixa2 = ctk.CTkEntry(content_frame, width=300, show='*', placeholder_text="Crie uma senha")
        self.caixa2.pack(pady=10, padx=10, fill='x')

        # Botão de salvar
        salvar_button = ctk.CTkButton(content_frame, text="Salvar", command=self.save_account, font=("Arial", 14))
        salvar_button.pack(pady=20)

        # Checa se o usuário já está logado
        self.check_logged_in()

    def save_account(self):
        with open(self.filepath, 'r') as file:
            usuarios = json.load(file)

        # Adiciona um novo usuário
        usuarios.append({
            "nome": self.caixa.get(),
            "username": self.caixa1.get(),
            "senha": self.caixa2.get(),
            "mes_nascimento": self.mes.get()
        })

        with open(self.filepath, 'w') as file:
            json.dump(usuarios, file, indent=4)
        self.close()

        # Atualiza a janela para o estado de usuário logado
        self.logon()

    def check_logged_in(self):
        try:
            with open(self.filepath, 'r') as file:
                usuarios = json.load(file)

                # Verifica se há um usuário logado (isso pode variar conforme a lógica de login que você implementar)
                if usuarios:
                    ultimo_usuario = usuarios[-1]  
                    self.logon(ultimo_usuario)
                    
        except FileNotFoundError:
            pass
        

    def logon(self, usuario=None):
        if usuario:
            # Atualize a interface da janela com os dados do usuário
            self.caixa.insert(0, usuario["nome"])
            self.caixa1.insert(0, usuario["username"])
            self.mes.set(usuario["mes_nascimento"])
            pass