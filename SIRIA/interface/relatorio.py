import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

from IA.ia_service import gerar_relatorio
from theme import (
    BG, SURFACE, SURFACE2, BORDER, ACCENT, ACCENT_H, ACCENT2,
    TEXT, TEXT_DIM,
    F_BODY, F_BOLD, F_SMALL, F_SMALL_B, F_TITLE, F_MONO,
    PAD, PAD_S, PAD_L,
)

ARQUIVO = "riscos.json"


def criar_aba_relatorio(frame):
    frame.configure(bg=BG)

    # ── Cabeçalho ─────────────────────────────────────────────────────────────
    header = tk.Frame(frame, bg=SURFACE, pady=PAD_S)
    header.pack(fill="x")

    tk.Label(header, text="// RELATÓRIO DE IA", font=F_TITLE,
             bg=SURFACE, fg=ACCENT, anchor="w").pack(padx=PAD_L, anchor="w")
    tk.Label(header, text="Gerado automaticamente com base nos riscos cadastrados.",
             font=F_SMALL, bg=SURFACE, fg=TEXT_DIM, anchor="w").pack(padx=PAD_L, anchor="w")

    # ── Barra de controles ────────────────────────────────────────────────────
    ctrl = tk.Frame(frame, bg=BG)
    ctrl.pack(fill="x", padx=PAD_L, pady=(PAD, PAD_S))

    # Política PDF — esquerda
    pdf_lbl_static = tk.Label(ctrl, text="POLÍTICA PDF:", font=F_SMALL_B,
                               bg=BG, fg=TEXT_DIM)
    pdf_lbl_static.pack(side="left")

    pdf_var = tk.StringVar(value="")

    pdf_nome_lbl = tk.Label(ctrl, text="  padrão do sistema",
                             font=F_SMALL, bg=BG, fg=TEXT_DIM)
    pdf_nome_lbl.pack(side="left", padx=4)

    def selecionar_pdf():                                  # lógica ORIGINAL
        caminho = filedialog.askopenfilename(
            title="Selecione a política de risco",
            filetypes=[("PDF files", "*.pdf")],
        )
        if caminho:
            pdf_var.set(caminho)
            pdf_nome_lbl.config(
                text=f"  {os.path.basename(caminho)}", fg=ACCENT2)

    tk.Button(ctrl, text="ANEXAR PDF", command=selecionar_pdf,
              bg=SURFACE2, fg=TEXT_DIM,
              activebackground=BORDER, activeforeground=TEXT,
              font=F_SMALL_B, relief="flat", cursor="hand2",
              padx=PAD_S, pady=3).pack(side="left", padx=PAD_S)

    # Gerar — direita
    def gerar():                                           # lógica ORIGINAL
        if not os.path.exists(ARQUIVO):
            messagebox.showerror("Erro", "Nenhum risco cadastrado ainda.")
            return
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except Exception:
                dados = []
        if not dados:
            messagebox.showerror("Erro", "O arquivo de riscos está vazio.")
            return

        texto.config(state="normal")
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, "⟳  Gerando relatório, aguarde...\n\n")
        texto.config(state="disabled")
        frame.update()

        relatorio = gerar_relatorio(dados, caminho_pdf=pdf_var.get() or None)

        texto.config(state="normal")
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, relatorio)
        texto.config(state="disabled")

    btn_gerar = tk.Button(
        ctrl, text="  ► GERAR RELATÓRIO  ", command=gerar,
        bg=ACCENT, fg=BG,
        activebackground=ACCENT_H, activeforeground=BG,
        font=F_BOLD, relief="flat", cursor="hand2",
        padx=PAD, pady=4,
    )
    btn_gerar.pack(side="right")
    btn_gerar.bind("<Enter>", lambda _: btn_gerar.configure(bg=ACCENT_H))
    btn_gerar.bind("<Leave>", lambda _: btn_gerar.configure(bg=ACCENT))

    # ── Área de texto ─────────────────────────────────────────────────────────
    texto_wrap = tk.Frame(frame, bg=BORDER, padx=1, pady=1)
    texto_wrap.pack(expand=True, fill="both", padx=PAD_L, pady=(0, PAD_L))

    vsb = tk.Scrollbar(texto_wrap, bg=SURFACE, troughcolor=BG,
                        activebackground=ACCENT, relief="flat", width=6)
    vsb.pack(side="right", fill="y")

    texto = tk.Text(
        texto_wrap,
        bg=SURFACE2, fg=TEXT,
        insertbackground=ACCENT,
        wrap="word",
        font=F_MONO,
        relief="flat",
        padx=PAD, pady=PAD,
        spacing1=2, spacing3=4,
        yscrollcommand=vsb.set,
        state="disabled",
    )
    texto.pack(expand=True, fill="both")
    vsb.config(command=texto.yview)
