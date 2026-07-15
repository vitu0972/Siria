import tkinter as tk
from tkinter import messagebox

from interface.resultados import atualizar_tabela
from core.calculadora import calcular_risco
from core.classificador import classificar_risco, salvar_json
from theme import (
    BG, SURFACE, SURFACE2, BORDER, ACCENT, ACCENT_H, ACCENT2,
    COR_RISCO, BG_RISCO, TEXT, TEXT_DIM,
    F_BODY, F_BOLD, F_SMALL, F_SMALL_B, F_TITLE, F_MONO,
    PAD, PAD_S, PAD_L,
)


# ── helpers visuais ────────────────────────────────────────────────────────────

def _section_header(parent, title, subtitle=""):
    """Bloco de cabeçalho de seção estilo iOS Settings."""
    wrap = tk.Frame(parent, bg=SURFACE, pady=PAD_S)
    wrap.pack(fill="x")
    tk.Label(wrap, text=title, font=F_TITLE, bg=SURFACE, fg=ACCENT,
             anchor="w").pack(padx=PAD_L, anchor="w")
    if subtitle:
        tk.Label(wrap, text=subtitle, font=F_SMALL, bg=SURFACE, fg=TEXT_DIM,
                 anchor="w").pack(padx=PAD_L, anchor="w")
    return wrap


def _grouped_row(parent, label, hint="", is_last=False):
    """Linha de formulário dentro de um grupo iOS (label + entry)."""
    row = tk.Frame(parent, bg=SURFACE2)
    row.pack(fill="x")

    tk.Label(row, text=label, font=F_SMALL_B, bg=SURFACE2,
             fg=TEXT, width=16, anchor="w").pack(side="left", padx=(PAD, PAD_S), pady=PAD_S)

    if hint:
        tk.Label(row, text=hint, font=F_SMALL, bg=SURFACE2,
                 fg=TEXT_DIM).pack(side="right", padx=(0, PAD_S), pady=PAD_S)

    entry = tk.Entry(row, bg=SURFACE2, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", highlightthickness=0,
                     font=F_BODY, width=26)
    entry.pack(side="left", fill="x", expand=True, padx=(0, PAD), pady=PAD_S)

    if not is_last:
        sep = tk.Frame(parent, bg=BORDER, height=1)
        sep.pack(fill="x", padx=PAD)

    # efeito focus
    def _focus_in(_):
        row.configure(bg=SURFACE)
        entry.configure(bg=SURFACE)
    def _focus_out(_):
        row.configure(bg=SURFACE2)
        entry.configure(bg=SURFACE2)
    entry.bind("<FocusIn>", _focus_in)
    entry.bind("<FocusOut>", _focus_out)

    return entry


def _group_wrap(parent):
    """Container de grupo com bordas arredondadas via Frame."""
    outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    outer.pack(fill="x", padx=PAD_L, pady=(PAD_S, 0))
    inner = tk.Frame(outer, bg=SURFACE2)
    inner.pack(fill="x")
    return inner


# ── aba principal ──────────────────────────────────────────────────────────────

def criar_aba_cadastro(frame):
    frame.configure(bg=BG)

    _section_header(
        frame,
        "// NOVO REGISTRO DE RISCO",
        "Preencha os campos abaixo para calcular e classificar o risco.",
    )

    # ── scroll container
    canvas_scroll = tk.Canvas(frame, bg=BG, highlightthickness=0)
    vsb = tk.Scrollbar(frame, orient="vertical", command=canvas_scroll.yview,
                       bg=SURFACE, troughcolor=BG, relief="flat", width=6)
    canvas_scroll.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    content = tk.Frame(canvas_scroll, bg=BG)
    win = canvas_scroll.create_window((0, 0), window=content, anchor="nw")

    def _on_resize(e):
        canvas_scroll.itemconfig(win, width=e.width)
    def _on_frame(e):
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
    canvas_scroll.bind("<Configure>", _on_resize)
    content.bind("<Configure>", _on_frame)

    # ── secção: Identificação
    tk.Label(content, text="IDENTIFICAÇÃO", font=F_SMALL_B, bg=BG,
             fg=TEXT_DIM, anchor="w").pack(fill="x", padx=PAD_L,
                                            pady=(PAD, PAD_S // 2))

    grp1 = _group_wrap(content)
    entry_setor     = _grouped_row(grp1, "SETOR")
    entry_descricao = _grouped_row(grp1, "DESCRIÇÃO")
    entry_ativo     = _grouped_row(grp1, "ATIVO AFETADO", is_last=True)

    # ── secção: Métricas
    tk.Label(content, text="MÉTRICAS", font=F_SMALL_B, bg=BG,
             fg=TEXT_DIM, anchor="w").pack(fill="x", padx=PAD_L,
                                            pady=(PAD, PAD_S // 2))

    grp2 = _group_wrap(content)
    entry_probabilidade = _grouped_row(grp2, "PROBABILIDADE", "[ 1 a 5 ]")
    entry_impacto       = _grouped_row(grp2, "IMPACTO",       "[ 1 a 5 ]", is_last=True)

    # ── resultado badge
    badge_outer = tk.Frame(content, bg=BG)
    badge_outer.pack(fill="x", padx=PAD_L, pady=(PAD, 0))

    badge = tk.Frame(badge_outer, bg=SURFACE2, padx=PAD, pady=PAD_S)
    badge.pack(fill="x")

    badge_valor = tk.Label(badge, text="", font=(F_BOLD[0], 28, "bold"),
                            bg=SURFACE2, fg=TEXT)
    badge_valor.pack(side="left")

    badge_classif = tk.Label(badge, text="", font=F_BOLD,
                              bg=SURFACE2, fg=TEXT_DIM)
    badge_classif.pack(side="left", padx=PAD_S)

    # ── lógica (IDÊNTICA À ORIGINAL) ──────────────────────────────────────────
    def processar():
        setor     = entry_setor.get().strip()
        descricao = entry_descricao.get().strip()
        ativo     = entry_ativo.get().strip()

        if not all([setor, descricao, ativo]):
            messagebox.showerror("Erro", "Preencha todos os campos de texto.")
            return

        try:
            probabilidade = int(entry_probabilidade.get())
            impacto       = int(entry_impacto.get())
            if not (1 <= probabilidade <= 5 and 1 <= impacto <= 5):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro",
                "Probabilidade e Impacto devem ser números entre 1 e 5.")
            return

        risco         = calcular_risco(impacto, probabilidade)
        classificacao = classificar_risco(risco)

        dados = {
            "setor": setor,
            "descricao": descricao,
            "ativo_afetado": ativo,
            "probabilidade": probabilidade,
            "impacto": impacto,
            "calculo_risco": risco,
            "classificacao": classificacao,
        }

        salvar_json(dados)
        atualizar_tabela()

        cor = COR_RISCO.get(classificacao, TEXT)
        bg_cor = BG_RISCO.get(classificacao, SURFACE2)
        badge.configure(bg=bg_cor)
        badge_valor.configure(text=str(risco), fg=cor, bg=bg_cor)
        badge_classif.configure(
            text=f"► {classificacao}", fg=cor, bg=bg_cor)

        for e in [entry_setor, entry_descricao, entry_ativo,
                  entry_probabilidade, entry_impacto]:
            e.delete(0, tk.END)

    # ── botão CALCULAR
    btn_wrap = tk.Frame(content, bg=BG)
    btn_wrap.pack(fill="x", padx=PAD_L, pady=PAD)

    btn = tk.Button(
        btn_wrap,
        text="  CALCULAR RISCO  ",
        command=processar,
        bg=ACCENT, fg=BG,
        activebackground=ACCENT_H,
        activeforeground=BG,
        font=F_BOLD,
        relief="flat",
        cursor="hand2",
        padx=PAD, pady=PAD_S,
    )
    btn.pack(fill="x")
    btn.bind("<Enter>", lambda _: btn.configure(bg=ACCENT_H))
    btn.bind("<Leave>", lambda _: btn.configure(bg=ACCENT))
