import pandas as pd
import sqlite3
from datetime import datetime

ARQUIVO_FORMS = "respostas_forms.csv"
DB = "ativos.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# =========================
# TABELAS DE NÍVEL
# =========================

cur.execute("""
CREATE TABLE IF NOT EXISTS empreendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    seq INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS ambientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendimento_id INTEGER,
    nome TEXT,
    seq INTEGER,
    UNIQUE(empreendimento_id, nome)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sistemas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ambiente_id INTEGER,
    nome TEXT,
    seq INTEGER,
    UNIQUE(ambiente_id, nome)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS ativos (
    asset_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id TEXT UNIQUE,
    empreendimento TEXT,
    ambiente TEXT,
    sistema TEXT,
    tipo_ativo TEXT,
    fabricante TEXT,
    modelo TEXT,
    criado_em TEXT
)
""")

# =========================
# FUNÇÕES
# =========================

def get_or_create_empreendimento(nome):
    cur.execute("SELECT id, seq FROM empreendimentos WHERE nome = ?", (nome,))
    r = cur.fetchone()

    if r:
        return r[0], r[1]

    cur.execute("SELECT COALESCE(MAX(seq),0)+1 FROM empreendimentos")
    seq = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO empreendimentos (nome, seq) VALUES (?, ?)",
        (nome, seq)
    )
    return cur.lastrowid, seq


def get_or_create_ambiente(emp_id, nome):
    cur.execute("""
        SELECT id, seq
        FROM ambientes
        WHERE empreendimento_id = ? AND nome = ?
    """, (emp_id, nome))

    r = cur.fetchone()

    if r:
        return r[0], r[1]

    cur.execute("""
        SELECT COALESCE(MAX(seq),0)+1
        FROM ambientes
        WHERE empreendimento_id = ?
    """, (emp_id,))

    seq = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO ambientes (empreendimento_id, nome, seq)
        VALUES (?, ?, ?)
    """, (emp_id, nome, seq))

    return cur.lastrowid, seq


def get_or_create_sistema(amb_id, nome):
    cur.execute("""
        SELECT id, seq
        FROM sistemas
        WHERE ambiente_id = ? AND nome = ?
    """, (amb_id, nome))

    r = cur.fetchone()

    if r:
        return r[0], r[1]

    cur.execute("""
        SELECT COALESCE(MAX(seq),0)+1
        FROM sistemas
        WHERE ambiente_id = ?
    """, (amb_id,))

    seq = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO sistemas (ambiente_id, nome, seq)
        VALUES (?, ?, ?)
    """, (amb_id, nome, seq))

    return cur.lastrowid, seq


def proximo_equipamento(sist_id):
    cur.execute("""
        SELECT COUNT(*)
        FROM ativos
        WHERE sistema = ?
    """, (str(sist_id),))

    return cur.fetchone()[0] + 1


# =========================
# IMPORTAÇÃO
# =========================

df = pd.read_csv(ARQUIVO_FORMS)

for _, row in df.iterrows():

    emp_nome = str(row["Empreendimento"]).strip()
    amb_nome = str(row["Ambiente"]).strip()
    sist_nome = str(row["Sistema"]).strip()

    tipo_ativo = str(row["Tipo do ativo"]).strip()
    fabricante = str(row.get("Fabricante", "")).strip()
    modelo     = str(row.get("Modelo", "")).strip()

    emp_id, emp_seq = get_or_create_empreendimento(emp_nome)
    amb_id, amb_seq = get_or_create_ambiente(emp_id, amb_nome)
    sist_id, sist_seq = get_or_create_sistema(amb_id, sist_nome)

    cur.execute("""
        SELECT COUNT(*)
        FROM ativos
        WHERE empreendimento = ?
          AND ambiente = ?
          AND sistema = ?
    """, (emp_nome, amb_nome, sist_nome))

    eq_seq = cur.fetchone()[0] + 1

    asset_id = f"{emp_seq:02d}-{amb_seq:02d}-{sist_seq:02d}-{eq_seq:03d}"

    cur.execute("""
        INSERT OR IGNORE INTO ativos
        (asset_id, empreendimento, ambiente, sistema,
         tipo_ativo, fabricante, modelo, criado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        asset_id,
        emp_nome,
        amb_nome,
        sist_nome,
        tipo_ativo,
        fabricante,
        modelo,
        datetime.now().isoformat()
    ))

conn.commit()
conn.close()

print("Importação hierárquica concluída.")
