import numpy as np  # Biblioteca para cálculos numéricos, usada para criar arrays e realizar cálculos matemáticos
import matplotlib.pyplot as plt  # Biblioteca para gerar gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite integrar gráficos matplotlib no Tkinter
import tkinter as tk  # Biblioteca padrão para criar interfaces gráficas em Python
from tkinter import filedialog, messagebox  # Módulos para diálogos de arquivos e mensagens de erro/sucesso

def calcular_confiabilidade(t, mtbf):
    #Calcula a confiabilidade com base na fórmula: confiabilidade = e^(-t/MTBF)
    return np.exp(-t / mtbf)

def gerar_grafico(mtbf):
    #Gera o gráfico da confiabilidade
    tempos = np.linspace(0, 5 * mtbf, 100)
    confiabilidades = calcular_confiabilidade(tempos, mtbf)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempos, confiabilidades, label=f"MTBF = {mtbf}")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Confiabilidade")
    ax.set_title("Curva de Confiabilidade")
    ax.legend()
    ax.grid()
    
    return fig

def calcular_e_mostrar():
    try:
        mtbf = float(entry_mtbf.get())
        t = float(entry_tempo.get())
        confiabilidade = calcular_confiabilidade(t, mtbf)
        resultado_var.set(f"Confiabilidade no tempo {t}: {confiabilidade:.4f}")
        
        # Atualizar gráfico
        fig = gerar_grafico(mtbf)
        for widget in frame_grafico.winfo_children():  # Remove gráficos anteriores
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    except ValueError:
        messagebox.showerror("Erro", "Digite valores numéricos válidos!")

def salvar_resultados():
    #Salva os resultados em um arquivo de texto
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(resultado_var.get())
        messagebox.showinfo("Sucesso", "Resultados salvos com sucesso!")

def salvar_grafico():
    #Salva o gráfico gerado como PNG
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        fig = gerar_grafico(float(entry_mtbf.get()))
        fig.savefig(file_path)
        messagebox.showinfo("Sucesso", "Gráfico salvo com sucesso!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Calculadora de Confiabilidade")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

frame_grafico = tk.Frame(root)
frame_grafico.pack()

# Campos de entrada
tk.Label(frame_input, text="MTBF:").grid(row=0, column=0)
entry_mtbf = tk.Entry(frame_input)
entry_mtbf.grid(row=0, column=1)

tk.Label(frame_input, text="Tempo:").grid(row=1, column=0)
entry_tempo = tk.Entry(frame_input)
entry_tempo.grid(row=1, column=1)

# Botão para calcular
btn_calcular = tk.Button(frame_input, text="Calcular", command=calcular_e_mostrar)
btn_calcular.grid(row=2, columnspan=2, pady=5)

# Label para exibir resultado
resultado_var = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado_var, font=("Arial", 12, "bold"))
label_resultado.pack()

# Botões para salvar
btn_salvar_txt = tk.Button(root, text="Salvar Resultado", command=salvar_resultados)
btn_salvar_txt.pack(pady=2)

btn_salvar_grafico = tk.Button(root, text="Salvar Gráfico", command=salvar_grafico)
btn_salvar_grafico.pack(pady=2)

root.mainloop()
