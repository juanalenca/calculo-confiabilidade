import numpy as np  # Biblioteca para cálculos numéricos, usada para criar arrays e realizar cálculos matemáticos 
import matplotlib.pyplot as plt  # Biblioteca para gerar gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite integrar gráficos matplotlib no Tkinter
import tkinter as tk  # Biblioteca padrão para criar interfaces gráficas em Python
from tkinter import filedialog, messagebox  # Módulos para diálogos de arquivos e mensagens de erro/sucesso
import csv  # Biblioteca para trabalhar com arquivos CSV

# Função para calcular a confiabilidade
def calcular_confiabilidade(t, mtbf):
    return np.exp(-t / mtbf)

# Função para gerar o gráfico da confiabilidade
def gerar_grafico(mtbf):
    tempos = np.linspace(0, 5 * mtbf, 100)
    confiabilidades = calcular_confiabilidade(tempos, mtbf)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempos, confiabilidades, label=f"MTBF = {mtbf}", color="#00A6FB")
    ax.set_xlabel("Tempo", color="white")
    ax.set_ylabel("Confiabilidade", color="white")
    ax.set_title("Curva de Confiabilidade", color="white")
    ax.legend()
    ax.grid(color="#444444")
    ax.tick_params(colors="white")
    fig.patch.set_facecolor("#121212")  # Fundo escuro moderno
    ax.set_facecolor("#1E1E1E")  # Fundo do gráfico
    
    return fig

# Função para calcular e exibir os resultados na interface
def calcular_e_mostrar():
    try:
        mtbf = float(entry_mtbf.get())
        t = float(entry_tempo.get())

        if mtbf <= 0 or t < 0:
            messagebox.showerror("Erro", "MTBF deve ser maior que zero e Tempo não pode ser negativo!")
            return

        confiabilidade = calcular_confiabilidade(t, mtbf)
        confiabilidade_percentual = confiabilidade * 100  # Converte para porcentagem
        resultado_var.set(f"Confiabilidade no tempo {t} (em horas): {confiabilidade_percentual:.2f}%")

        # Atualizar gráfico
        fig = gerar_grafico(mtbf)
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    except ValueError:
        messagebox.showerror("Erro", "Digite valores numéricos válidos!")

# Função para salvar os resultados em um arquivo de texto
def salvar_resultados():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(resultado_var.get())
        messagebox.showinfo("Sucesso", "Resultados salvos com sucesso!")

# Função para salvar os resultados em formato CSV
def salvar_resultados_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            mtbf = float(entry_mtbf.get())
            t = float(entry_tempo.get())
            confiabilidade = calcular_confiabilidade(t, mtbf)
            confiabilidade_percentual = confiabilidade * 100  # Converte para porcentagem

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tempo (h)", "MTBF (h)", "Confiabilidade (%)"])
                writer.writerow([t, mtbf, confiabilidade_percentual])
                
            messagebox.showinfo("Sucesso", "Resultados salvos em CSV com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos!")

# Função para salvar o gráfico gerado como imagem
def salvar_grafico():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        fig = gerar_grafico(float(entry_mtbf.get()))
        fig.savefig(file_path)
        messagebox.showinfo("Sucesso", "Gráfico salvo com sucesso!")

# Função para limpar os valores da interface
def limpar_valores():
    entry_mtbf.delete(0, tk.END)
    entry_tempo.delete(0, tk.END)
    resultado_var.set("")
    for widget in frame_grafico.winfo_children():
        widget.destroy()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Calculadora de Confiabilidade")
root.geometry("850x850")
root.configure(bg="#121212")  # Cor de fundo principal

# Frame principal
frame_main = tk.Frame(root, bg="#1E1E1E", bd=2, relief="groove")
frame_main.pack(pady=10, padx=10, fill="both", expand=True)

# Frame para entradas
frame_input = tk.Frame(frame_main, bg="#222222", bd=2, relief="ridge")
frame_input.pack(pady=10, padx=10, fill="x")

# Frame para o gráfico
frame_grafico = tk.Frame(frame_main, bg="#121212", bd=2, relief="ridge")
frame_grafico.pack(pady=10, padx=10, fill="both", expand=True)

# Título
titulo = tk.Label(frame_main, text="Calculadora de Confiabilidade", font=("Arial", 16, "bold"), bg="#1E1E1E", fg="#FFD700")
titulo.pack(pady=10)

# Campos de entrada
tk.Label(frame_input, text="MTBF (em horas):", bg="#222222", fg="#FCBF22", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_mtbf = tk.Entry(frame_input, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
entry_mtbf.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

frame_input.grid_columnconfigure(1, weight=1)

tk.Label(frame_input, text="Tempo (em horas):", bg="#222222", fg="#FCBF22", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_tempo = tk.Entry(frame_input, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
entry_tempo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Botão para calcular
btn_calcular = tk.Button(frame_input, text="Calcular", command=calcular_e_mostrar, bg="#5A189A", fg="white", font=("Arial", 12), relief="flat")
btn_calcular.grid(row=2, columnspan=2, pady=10)

# Label para exibir resultado
resultado_var = tk.StringVar()
label_resultado = tk.Label(frame_main, textvariable=resultado_var, font=("Arial", 14, "bold"), bg="#1E1E1E", fg="#FCBF22") 
label_resultado.pack(pady=10)

# Botões para salvar
frame_botoes = tk.Frame(frame_main, bg="#1E1E1E")
frame_botoes.pack(pady=10)

btn_salvar_txt = tk.Button(frame_botoes, text="Salvar em txt", command=salvar_resultados, bg="#5A189A", fg="white", font=("Arial", 12), relief="flat")
btn_salvar_txt.pack(side="left", padx=10)

btn_salvar_csv = tk.Button(frame_botoes, text="Salvar em csv", command=salvar_resultados_csv, bg="#5A189A", fg="white", font=("Arial", 12), relief="flat")
btn_salvar_csv.pack(side="left", padx=10)

btn_salvar_grafico = tk.Button(frame_botoes, text="Salvar Gráfico", command=salvar_grafico, bg="#5A189A", fg="white", font=("Arial", 12), relief="flat")
btn_salvar_grafico.pack(side="left", padx=10)

# Botão para limpar os valores
btn_limpar = tk.Button(frame_botoes, text="Limpar Valores", command=limpar_valores, bg="#FF4C4C", fg="white", font=("Arial", 12), relief="flat")
btn_limpar.pack(side="left", padx=10)

# Inicia o loop principal do Tkinter
root.mainloop()
