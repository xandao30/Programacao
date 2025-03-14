import mysql.connector
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from datetime import datetime
import pandas as pd
import os
import json
import logging
import re
from jinja2 import Templatepo

# Configuração de logging
logging.basicConfig(
    filename='publicador.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carregar configurações de um arquivo JSON
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    "db_host": "mysql07.centrointernacional.tv",
    "db_user": "centrointernac6",
    "db_password": "hOE21xm88X5",
    "db_name": "centrointernac6",
    "default_catid": 28,
    "default_user_id": 453
}

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return DEFAULT_CONFIG
    except Exception as e:
        logging.error(f"Erro ao carregar config: {str(e)}")
        return DEFAULT_CONFIG

config = load_config()

# Função para conectar ao banco de dados
def conectar_db():
    try:
        db = mysql.connector.connect(
            host=config["db_host"],
            user=config["db_user"],
            password=config["db_password"],
            database=config["db_name"]
        )
        return db
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco: {str(e)}")
        raise

# Função para obter o ID do usuário
def get_user_id(username, cursor):
    try:
        cursor.execute("SELECT id FROM y4kaq_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logging.error(f"Erro ao obter user_id para '{username}': {str(e)}")
        return None

# Função para obter o asset_id da categoria ou componente
def get_parent_asset_id(catid, cursor):
    try:
        cursor.execute("SELECT asset_id FROM y4kaq_categories WHERE id = %s", (catid,))
        category_asset = cursor.fetchone()
        if category_asset:
            return category_asset[0]
        
        cursor.execute("SELECT id FROM y4kaq_assets WHERE name = 'com_content'")
        component_asset = cursor.fetchone()
        return component_asset[0] if component_asset else 1
    except Exception as e:
        logging.error(f"Erro ao obter parent_asset_id para catid {catid}: {str(e)}")
        return 1

# Função para gerar alias
def gerar_alias(titulo):
    try:
        return re.sub(r'[^a-z0-9-]+', '-', titulo.lower()).strip('-')
    except Exception as e:
        logging.error(f"Erro ao gerar alias para '{titulo}': {str(e)}")
        return titulo.lower().replace(" ", "-")

# Template básico para HTML (opcional, pode ser ajustado)
template_html = """
<h1>{{ title }}</h1>
<p>{{ introtext }}</p>
<hr id="system-readmore" />
<p>{{ fulltext }}</p>
"""
template = Template(template_html)

# Função para publicar artigo
def publicar_artigo(title, introtext, fulltext, username, images_json="{}", db=None):
    close_db = False
    if db is None:
        db = conectar_db()
        close_db = True
    
    cursor = db.cursor()
    try:
        author_id = get_user_id(username, cursor)
        if not author_id:
            raise ValueError(f"Usuário '{username}' não encontrado!")
        
        alias = gerar_alias(title)
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql_content = """
            INSERT INTO `y4kaq_content` (`title`, `alias`, `introtext`, `fulltext`, `state`, `catid`, `created_by`, `access`, `language`, `images`, `urls`, `attribs`, `metadata`, `publish_up`, `created`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores_content = (
            title, alias, introtext, fulltext, 1, config["default_catid"], author_id, 2, "*",
            images_json, '{"urla":false,"urlatext":"","targeta":"","urlb":false,"urlbtext":"","targetb":"","urlc":false,"urlctext":"","targetc":""}',
            '{}', '{}', current_date, current_date
        )
        cursor.execute(sql_content, valores_content)
        article_id = cursor.lastrowid

        parent_asset_id = get_parent_asset_id(config["default_catid"], cursor)
        sql_assets = """
            INSERT INTO `y4kaq_assets` (`name`, `parent_id`, `title`, `rules`)
            VALUES (%s, %s, %s, %s)
        """
        asset_name = f"com_content.article.{article_id}"
        asset_rules = '{"core.delete":[],"core.edit":[],"core.edit.state":[]}'
        valores_assets = (asset_name, parent_asset_id, title, asset_rules)
        cursor.execute(sql_assets, valores_assets)
        asset_id = cursor.lastrowid

        sql_update_content = "UPDATE `y4kaq_content` SET `asset_id` = %s WHERE `id` = %s"
        cursor.execute(sql_update_content, (asset_id, article_id))

        db.commit()
        logging.info(f"Artigo '{title}' publicado com asset_id {asset_id}")
        return True
    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao publicar '{title}': {str(e)}")
        raise
    finally:
        cursor.close()
        if close_db:
            db.close()

# Função para publicar artigo via interface
def publicar_artigo_ui(event=None):
    try:
        title = entry_title.get().strip()
        introtext = entry_intro.get("1.0", tk.END).strip()
        fulltext = entry_full.get("1.0", tk.END).strip()
        username = entry_username.get().strip()

        if not all([title, introtext, fulltext, username]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        publicar_artigo(title, introtext, fulltext, username)
        messagebox.showinfo("Sucesso", f"Artigo '{title}' publicado!")
        entry_title.delete(0, tk.END)
        entry_intro.delete("1.0", tk.END)
        entry_full.delete("1.0", tk.END)
        entry_username.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao publicar: {str(e)}")

# Função para criar template
def criar_template():
    template_data = {
        'Título': ['Exemplo de Título 1'],
        'Introdução': ['Breve introdução aqui...'],
        'Texto Completo': ['Texto completo do artigo 1...'],
        'Usuário': ['admin'],
        'Imagem Intro': ['images/intro.jpg'],
        'Imagem Completa': ['images/full.jpg']
    }
    df = pd.DataFrame(template_data)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False, encoding='utf-8')
            else:
                df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Template salvo em: {file_path}")
            logging.info(f"Template criado: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar template: {str(e)}")
            logging.error(f"Erro ao salvar template: {str(e)}")

# Função para importar planilha
def importar_planilha():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path, encoding='utf-8') if file_path.endswith('.csv') else pd.read_excel(file_path)
        map_window = tk.Toplevel(janela)
        map_window.title("Mapear Colunas da Planilha")
        map_window.geometry("300x400")
        map_window.configure(background=DARK_BACKGROUND)

        map_frame = ttk.Frame(map_window, padding="10", style="TFrame")
        map_frame.pack(fill="both", expand=True)

        ttk.Label(map_frame, text="Selecione as colunas:", background=DARK_BACKGROUND, foreground=TEXT_COLOR).pack(pady=10)
        columns = df.columns.tolist()

        vars = {
            'Título': tk.StringVar(),
            'Introdução': tk.StringVar(),
            'Texto Completo': tk.StringVar(),
            'Usuário': tk.StringVar(),
            'Imagem Intro': tk.StringVar(),
            'Imagem Completa': tk.StringVar()
        }
        for label, var in vars.items():
            ttk.Combobox(map_frame, textvariable=var, values=columns, state="readonly", style="TCombobox").pack(pady=5)
            ttk.Label(map_frame, text=f"{label}:", background=DARK_BACKGROUND, foreground=TEXT_COLOR).pack()

        def confirmar_mapeamento():
            mapping = {k: v.get() for k, v in vars.items() if v.get()}
            if len(mapping) < 4:  # Pelo menos os 4 campos obrigatórios
                messagebox.showerror("Erro", "Selecione pelo menos Título, Introdução, Texto Completo e Usuário!")
                return

            db = conectar_db()
            total_artigos = 0
            try:
                for _, row in df.iterrows():
                    title = str(row[mapping['Título']]) if 'Título' in mapping else ""
                    introtext = str(row[mapping['Introdução']]) if 'Introdução' in mapping else ""
                    fulltext = str(row[mapping['Texto Completo']]) if 'Texto Completo' in mapping else ""
                    username = str(row[mapping['Usuário']]) if 'Usuário' in mapping else ""
                    
                    images_json = '{}'
                    if 'Imagem Intro' in mapping or 'Imagem Completa' in mapping:
                        images = {
                            "image_intro": str(row[mapping['Imagem Intro']]) if 'Imagem Intro' in mapping and pd.notna(row[mapping['Imagem Intro']]) else "",
                            "image_intro_alt": "",
                            "image_intro_caption": "",
                            "float_intro": "",
                            "image_fulltext": str(row[mapping['Imagem Completa']]) if 'Imagem Completa' in mapping and pd.notna(row[mapping['Imagem Completa']]) else "",
                            "image_fulltext_alt": "",
                            "image_fulltext_caption": "",
                            "float_fulltext": ""
                        }
                        images_json = json.dumps(images)

                    if not all([title, introtext, fulltext, username]):
                        logging.warning(f"Linha ignorada por dados incompletos: {title}")
                        continue

                    publicar_artigo(title, introtext, fulltext, username, images_json, db)
                    total_artigos += 1
                messagebox.showinfo("Sucesso", f"Importados {total_artigos} artigos!")
                map_window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar: {str(e)}")
            finally:
                db.close()

        ttk.Button(map_frame, text="Confirmar", command=confirmar_mapeamento, style="TButton").pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar planilha: {str(e)}")
        logging.error(f"Erro ao importar planilha: {str(e)}")

# Interface gráfica
janela = tk.Tk()
janela.title("Publicador de Artigos Joomla 3")
janela.geometry("600x800")
DARK_BACKGROUND = "#2C3E50"
PRIMARY_COLOR = "#4682B4"
TEXT_COLOR = "#FFFFFF"
INPUT_BG = "#465C71"
INPUT_FG = "#FFFFFF"

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background=DARK_BACKGROUND)
style.configure("TLabel", background=DARK_BACKGROUND, font=("Helvetica", 11, "bold"), foreground=TEXT_COLOR)
style.configure("TButton", background=PRIMARY_COLOR, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR, padding=12)
style.configure("TEntry", fieldbackground=INPUT_BG, font=("Helvetica", 10), foreground=INPUT_FG)
style.configure("TCombobox", fieldbackground=INPUT_BG, font=("Helvetica", 10), foreground=INPUT_FG)
style.configure("TLabelframe", background=DARK_BACKGROUND)
style.configure("TLabelframe.Label", background=DARK_BACKGROUND, font=("Helvetica", 12, "bold"), foreground=PRIMARY_COLOR)
style.map("TButton", background=[('active', '#356EA9'), ('pressed', '#2A5A8E')])

main_frame = ttk.Frame(janela, padding="15", style="TFrame")
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="Publicador de Artigos Joomla 3", font=("Helvetica", 16, "bold"), foreground=PRIMARY_COLOR).pack(pady=(0, 15))

input_frame = ttk.LabelFrame(main_frame, text="Insira os Detalhes do Artigo", padding="10", style="TLabelframe")
input_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(input_frame, text="Título:").pack(pady=5)
entry_title = ttk.Entry(input_frame, width=50)
entry_title.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Introdução:").pack(pady=5)
entry_intro = tk.Text(input_frame, height=5, width=50, font=("Helvetica", 10), bg=INPUT_BG, fg=INPUT_FG, bd=1, relief="solid")
entry_intro.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Texto Completo:").pack(pady=5)
entry_full = tk.Text(input_frame, height=10, width=50, font=("Helvetica", 10), bg=INPUT_BG, fg=INPUT_FG, bd=1, relief="solid")
entry_full.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Usuário do Site:").pack(pady=5)
entry_username = ttk.Entry(input_frame, width=30)
entry_username.pack(pady=5, padx=5, fill="x")
entry_username.bind("<Return>", publicar_artigo_ui)

button_frame = ttk.Frame(main_frame, padding="10", style="TFrame")
button_frame.pack(fill="x", pady=10)

ttk.Button(button_frame, text="📝 Publicar Artigo", command=publicar_artigo_ui).pack(side="left", padx=5, pady=5)
ttk.Button(button_frame, text="📤 Importar Planilha", command=importar_planilha).pack(side="left", padx=5, pady=5)
ttk.Button(button_frame, text="📥 Baixar Template", command=criar_template).pack(side="left", padx=5, pady=5)

janela.configure(background=DARK_BACKGROUND)
janela.mainloop()