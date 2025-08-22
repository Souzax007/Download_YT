import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
from main import baixar_audio 
import yt_dlp
import time

# ---------------- Funções ----------------
def animate_download():
    global animating
    animating = True
    while animating:
        for frame in ["Baixando.", "Baixando..", "Baixando...", "Baixando...."]:
            if not animating:
                break
            status_label.config(text=frame)
            status_label.update()
            time.sleep(0.5)

def stop_animation():
    global animating
    animating = False

def download_video(url, pasta):
    """Baixa vídeo em melhor qualidade"""
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s')
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        stop_animation()
        status_label.config(text="Download concluído!")
        messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso!")
        listar_arquivos()
    except Exception as e:
        stop_animation()
        messagebox.showerror("Erro", f"Erro ao baixar vídeo: {e}")

def start_download(is_audio):
    global pasta_download
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Insira uma URL válida!")
        return
    if not pasta_download:
        pasta_download = filedialog.askdirectory()
        if not pasta_download:
            messagebox.showerror("Erro", "Nenhuma pasta selecionada!")
            return
    status_label.config(text="Iniciando download...")
    
    # Animação
    threading.Thread(target=animate_download, daemon=True).start()
    
    # Download
    if is_audio:
        threading.Thread(
            target=lambda: (baixar_audio(url, pasta_download), stop_animation(), listar_arquivos()),
            daemon=True
        ).start()
    else:
        threading.Thread(
            target=lambda: (download_video(url, pasta_download),),
            daemon=True
        ).start()

def listar_arquivos():
    if pasta_download:
        try:
            arquivos = os.listdir(pasta_download)
            lista_arquivos.delete(0, tk.END)
            for arquivo in arquivos:
                if arquivo.endswith(('.mp3', '.mp4', '.webm', '.mkv')):
                    lista_arquivos.insert(tk.END, arquivo)
        except Exception:
            pass

def reproduzir_arquivo():
    selecionado = lista_arquivos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um arquivo para reproduzir!")
        return
    arquivo = lista_arquivos.get(selecionado[0])
    caminho_completo = os.path.join(pasta_download, arquivo)
    try:
        if os.name == 'nt':
            os.startfile(caminho_completo)
        else:
            subprocess.call(('xdg-open' if os.name == 'posix' else 'open', caminho_completo))
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {str(e)}")

def escolher_pasta():
    global pasta_download
    nova_pasta = filedialog.askdirectory()
    if nova_pasta:
        pasta_download = nova_pasta
        listar_arquivos()
        status_label.config(text=f"Pasta definida: {pasta_download}")

# ---------------- Interface ----------------
tk_root = tk.Tk()
tk_root.title("YouTube Downloader")
tk_root.geometry("500x500")
tk_root.configure(bg="#333")

pasta_download = ""

title_label = tk.Label(tk_root, text="YouTube Downloader", font=("Arial", 16, "bold"), bg="#333", fg="white")
title_label.pack(pady=10)

url_entry = tk.Entry(tk_root, width=50)
url_entry.pack(pady=10)

btn_frame = tk.Frame(tk_root, bg="#333")
btn_frame.pack(pady=10)

download_video_btn = tk.Button(btn_frame, text="Baixar Vídeo", command=lambda: start_download(False), bg="#0073e6", fg="white")
download_video_btn.pack(side=tk.LEFT, padx=10)

download_audio_btn = tk.Button(btn_frame, text="Baixar Áudio (MP3 320kbps)", command=lambda: start_download(True), bg="#00cc44", fg="white")
download_audio_btn.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(tk_root, text="", font=("Arial", 12), bg="#333", fg="white")
status_label.pack(pady=10)

lista_arquivos = tk.Listbox(tk_root, width=60, height=12)
lista_arquivos.pack(pady=10)

play_button = tk.Button(tk_root, text="Reproduzir", command=reproduzir_arquivo, bg="#ffaa00", fg="black")
play_button.pack(pady=5)

choose_folder_btn = tk.Button(tk_root, text="Selecionar Pasta", command=escolher_pasta, bg="#5555ff", fg="white")
choose_folder_btn.pack(pady=5)

tk_root.mainloop()
