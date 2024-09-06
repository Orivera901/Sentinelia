#Librerias
from pathlib import Path
from PIL import ImageGrab
import tkinter as tk
import socket
import threading
import json
import psutil
import platform
import io
import os

#Variables
Mem = psutil.virtual_memory()
Disk = psutil.disk_usage("/")
Net = psutil.net_io_counters()
Vin = "Desvinculado"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_Inicio = OUTPUT_PATH / Path(r"assets\FrameInicio")
ASSETS_PATH_Vinculacion = OUTPUT_PATH / Path(r"assets\FrameVinculacion")

def relative_to_assets_Inicio(path: str) -> Path:
    return ASSETS_PATH_Inicio / Path(path)

def relative_to_assets_Vinculacion(path: str) -> Path:
    return ASSETS_PATH_Vinculacion / Path(path)

def IniciarCliente(Puerto, Ip, controller):
    HiloServer = threading.Thread(target=Conexion, args=(Puerto, Ip, controller))
    HiloServer.daemon = True
    HiloServer.start()

def CapturarPantalla():
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    return buffer.getvalue()

def Conexion(Puerto, Ip, controller):
    while True:
        global Vin
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((Ip, Puerto))

            while True:
                Datos = {
                    "IP:": Ip,

                    "Sistema operativo: ": platform.system(),
                    "Nombre del nodo: ": platform.node(),
                    "Version del ISO: ": platform.version(),
                    "Arquitectura: ": platform.architecture(),

                    "Uso de la CPU (%): ": psutil.cpu_percent(interval=1),
                    "Número de núcleos: ": psutil.cpu_count(logical=True),

                    "Memoria total (GB): ": Mem.total / (1024**3),
                    "Memoria usada (%): ": Mem.percent,
                    
                    "Espacio total en disco (GB): ": Disk.total / (1024**3),
                    "Espacio usado (%): ": Disk.percent,

                    "Bytes enviados: ": Net.bytes_sent,
                    "Bytes recibidos: ": Net.bytes_recv
                    }
                
                imagen_bytes = CapturarPantalla()
                    
                try:
                    DatosJson = json.dumps(Datos, indent=4)
                    s.sendall(b'{"data": ' + DatosJson.encode() + b'}' + b'|'+ imagen_bytes)
                    controller.Vin.set("Vinculado")
                except:
                    print("No se han podido enviar los datos")
        
        except Exception as e:
            print("No se ha podido conectar o error en la conexión:", e)
        finally:
            s.close()

        return Vin

#App
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1440x1024")
        self.resizable(False, False)

        self.Vin = tk.StringVar(value="Desvinculado")

        container = tk.Frame(self)
        container.pack(
            side="top", 
            fill="both", 
            expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Inicio, Vinculacion):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Inicio")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

#App Inicio
class Inicio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        #Pagina Inicio
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(0.0,0.0,182.0,1024.0,fill="#175F88",outline="")

        #Imagenes Inicio
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets_Inicio("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets_Inicio("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets_Inicio("image_3.png"))
        self.image_image_4 = tk.PhotoImage(file=relative_to_assets_Inicio("image_4.png"))
        self.image_image_5 = tk.PhotoImage(file=relative_to_assets_Inicio("image_5.png"))
        self.image_image_6 = tk.PhotoImage(file=relative_to_assets_Inicio("image_6.png"))
        self.image_image_7 = tk.PhotoImage(file=relative_to_assets_Inicio("image_7.png"))
        self.image_image_8 = tk.PhotoImage(file=relative_to_assets_Inicio("image_8.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets_Inicio("button_1.png"))

        canvas.create_image(803.0,587.0,image=self.image_image_1)
        canvas.create_image(441.0,810.0,image=self.image_image_2)
        canvas.create_image(803.0,804.0,image=self.image_image_3)
        canvas.create_image(1165.0,804.0,image=self.image_image_4)
        canvas.create_image(490.0,226.0,image=self.image_image_5)
        canvas.create_image(1023.0,293.0,image=self.image_image_6)
        canvas.create_image(803.0,791.0,image=self.image_image_7)
        canvas.create_image(91.0,41.0,image=self.image_image_8)

        #Elementos
        button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Vinculacion"),
            relief="flat"
        )
        button_1.place(
            x=250.0,
            y=369.0,
            width=286.0,
            height=92.0
        )

#App Vinculacion
class Vinculacion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        #Pagina Vinculacion
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(0.0,0.0,182.0,1024.0,fill="#175F88",outline="")

        #Imagenes Vinculacion
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_3.png"))
        self.image_image_4 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_4.png"))
        self.image_image_5 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_5.png"))
        self.image_image_6 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_6.png"))
        self.image_image_7 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_7.png"))
        self.entry_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("entry_1.png"))
        self.entry_image_2 = tk.PhotoImage(file=relative_to_assets_Vinculacion("entry_2.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("button_1.png"))
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets_Vinculacion("button_2.png"))

        canvas.create_image(574.0,174.0,image=self.image_image_1)
        canvas.create_image(294.0,304.0,image=self.image_image_2)
        canvas.create_image(311.0,403.0,image=self.image_image_3)
        canvas.create_image(816.0,43.0,image=self.image_image_4)
        canvas.create_image(801.0,757.0,image=self.image_image_5)
        canvas.create_image(981.0,353.0,image=self.image_image_6)
        canvas.create_image(91.0,41.0,image=self.image_image_7)
        canvas.create_image(466.5,353.5,image=self.entry_image_1)
        canvas.create_image(466.5,452.5,image=self.entry_image_2)

        #Elementos Vinculacion
        entry_1 = tk.Entry(
            self,
            bd=0,
            bg="#E4EBF3",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=277.0,
            y=321.0,
            width=379.0,
            height=63.0
        )

        entry_2 = tk.Entry(
            self,
            bd=0,
            bg="#E4EBF3",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=277.0,
            y=420.0,
            width=379.0,
            height=63.0
        )

        button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: IniciarCliente(int(entry_1.get()), entry_2.get(), self.controller),
            relief="flat"
        )
        button_1.place(
            x=749.0,
            y=420.0,
            width=232.0,
            height=75.0
        )

        self.label1 = tk.Label(
            self,
            text="Estado",
            anchor="nw",
            fg="#A6A6A6",
            font=("DMSans Medium", 55 * -1),
            bg="#F9F9F9"
        )
        self.label1.place(
            x=703.0,
            y=312.0
        )

        self.label2 = tk.Label(
            self,
            textvariable=self.controller.Vin,
            anchor="nw",
            fg="#5F8EC6",
            font=("DMSans Medium", 55 * -1),
            bg="#F9F9F9"
        )
        self.label2.place(
            x=703.0,
            y=312.0
        )

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()