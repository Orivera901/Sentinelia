#Importaciones
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import messagebox
import tkinter as tk
import socket
import threading
import json
import io

#Variables
DatosJson = {}
Computadoras = {}
current_id = 1
lock = threading.Lock()

#Assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_Inicio = OUTPUT_PATH / Path(r"assets\FrameInicio")
ASSETS_PATH_Vinculacion = OUTPUT_PATH / Path(r"assets\FrameVinculacion")
ASSETS_PATH_Monitoreo = OUTPUT_PATH / Path(r"assets\FrameMonitoreo")

def relative_to_assets_Inicio(path: str) -> Path:
    return ASSETS_PATH_Inicio / Path(path)

def relative_to_assets_Vinculacion(path: str) -> Path:
    return ASSETS_PATH_Vinculacion / Path(path)

def relative_to_assets_Monitoreo(path: str) -> Path:
    return ASSETS_PATH_Monitoreo / Path(path)

#Iniciar Server
def IniciarServidor(Puerto):
    HiloServer = threading.Thread(target=Conexion, args=(Puerto,))
    HiloServer.daemon = True
    HiloServer.start()

#Configurar Server
def Conexion(Puerto):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", Puerto))
        s.listen(5)

        while True:
            try:
                Conn, Addr = s.accept()
                MensajeCliente = threading.Thread(target=ManejarCliente, args=(Conn, Addr))
                MensajeCliente.start()
            except socket.timeout:
                messagebox.showerror("Error", "Se acabo el tiempo de espera del servidor")
    except:
        messagebox.showerror("Error", "No se pudo crear el servidor")
        s.close()
    finally:
        s.close()

#Recibir Datos
def ManejarCliente(Conn, Addr):
    global DatosJson
    global Computadoras
    global current_id
    global lock
    try:
        while True:
            Data = Conn.recv(5 * 1024 * 1024) 
            if not Data:
                Conn.close()
                break
            
            if b'|' in Data:
                data_part, image_part = Data.split(b'|', 1)

                try:
                    DatosJson = json.loads(data_part.decode('utf-8'))
                except json.JSONDecodeError as e:
                    continue
                except UnicodeDecodeError as e:
                    continue

                if 'data' in DatosJson and isinstance(DatosJson['data'], dict):
                    DatosJson = DatosJson['data']

                with lock:
                    if Addr[0] not in Computadoras:
                        identificador = f"PC{current_id}"
                        current_id += 1
                        Computadoras[Addr[0]] = {'id': identificador, 'data': DatosJson}
                    else:
                        identificador = Computadoras[Addr[0]]['id']
                        Computadoras[Addr[0]]['data'] = DatosJson

                    try:
                        if image_part:
                            imagen = Image.open(io.BytesIO(image_part))
                            imagen = imagen.resize((430, 300))
                            Computadoras[Addr[0]]['image'] = ImageTk.PhotoImage(imagen)
                    except Exception as e:
                        continue
    except Exception as e:
        print(f"Error en envío de datos: {e}")

def ActualizarImagen(imagen_data, imagen_label):
    try:
        if not imagen_data:
            return
        
        imagen_pil = Image.open(io.BytesIO(imagen_data))
        imagen_pil = imagen_pil.resize((400, 300), Image.ANTIALIAS)
        imagen_tk = ImageTk.PhotoImage(imagen_pil)

        imagen_label.config(image=imagen_tk)
        imagen_label.image = imagen_tk
        imagen_label.update_idletasks()
    except IOError as e:
        print(f"Error al abrir la imagen: {e}")
    except Exception as e:
        print(f"Error al actualizar la imagen: {e}")

#Ventana de App
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1440x1024")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(
            side="top", 
            fill="both", 
            expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Inicio,Vinculacion,Monitoreo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Inicio")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Inicio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        #Ventana Inicio
        canvas = tk.Canvas(
            self,
            bg = "#FFFFFF",
            height = 1024,
            width = 1440,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(282.0,629.0,600.0,991.0,fill="#F2F2F2",outline="")
        canvas.create_rectangle(644.0,623.0,963.0,986.0,fill="#F2F2F2",outline="")
        canvas.create_rectangle(1006.0,623.0,1325.0,986.0,fill="#F2F2F2",outline="")
        canvas.create_rectangle(0.0,0.0,182.0,1024.0,fill="#175F88",outline="")

        #Imagenes Inicio
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets_Inicio("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets_Inicio("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets_Inicio("image_3.png"))
        self.image_image_4 = tk.PhotoImage(file=relative_to_assets_Inicio("image_4.png"))
        self.image_image_5 = tk.PhotoImage(file=relative_to_assets_Inicio("image_5.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets_Inicio("button_1.png"))
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets_Inicio("button_2.png"))
        self.button_image_3 = tk.PhotoImage(file=relative_to_assets_Inicio("button_3.png"))

        canvas.create_image(803.0, 587.0, image=self.image_image_1)
        canvas.create_image(479.0,226.0,image=self.image_image_2)
        canvas.create_image(1023.0,293.0,image=self.image_image_3)
        canvas.create_image(803.0,791.0,image=self.image_image_4)
        canvas.create_image(91.0,41.0,image=self.image_image_5)

        #Elementos Inicio
        button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Vinculacion"),
            relief="flat")
        button_1.place(
            x=250.0,
            y=369.0,
            width=286.0,
            height=92.0
        )

        button_2 = tk.Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Monitoreo"),
            relief="flat"
        )
        button_2.place(
            x=6.0,
            y=173.0,
            width=165.0,
            height=89.0
        )

        button_3 = tk.Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Vinculacion"),
            relief="flat"
        )
        button_3.place(
            x=0.0,
            y=89.0,
            width=182.0,
            height=80.0
        )

class Vinculacion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()
    
    def AlHacerClick(self):
        puerto = self.entry_1.get()
        IniciarServidor(int(puerto))
        
        self.button_1.config(state="disabled")
    
    def create_widgets(self):
        #Ventana Vinculacion
        canvas = tk.Canvas(
            self,
            bg = "#FFFFFF",
            height = 1024,
            width = 1440,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(0.0,0.0,182.0,1024.0,fill="#175F88",outline="")

        #Imagenes Vinculacion
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_3.png"))
        self.image_image_4 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_4.png"))
        self.image_image_5 = tk.PhotoImage(file=relative_to_assets_Vinculacion("image_5.png"))
        self.entry_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("entry_1.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets_Vinculacion("button_1.png"))
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets_Vinculacion("button_2.png"))
        self.button_image_3 = tk.PhotoImage(file=relative_to_assets_Vinculacion("button_3.png"))

        canvas.create_image(573.0,174.0,image=self.image_image_1)
        canvas.create_image(304.0,303.0,image=self.image_image_2)
        canvas.create_image(816.0,43.0,image=self.image_image_3)
        canvas.create_image(816.0,735.0,image=self.image_image_4)
        canvas.create_image(91.0,41.0,image=self.image_image_5)
        canvas.create_image(466.5,351.5,image=self.entry_image_1)

        #Elementos Vinculacion
        self.entry_1 = tk.Entry(
            self,
            bd=0,
            bg="#E4EBF3",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=277.0,
            y=319.0,
            width=379.0,
            height=63.0
        )

        self.label_1 = tk.Label(
            self,
            text="Ip: " + socket.gethostbyname(socket.gethostname()),
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        )

        self.label_1.place(
            x=750.0,
            y=340.0
        )

        self.button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.AlHacerClick,
            relief="flat"
        )

        self.button_1.place(
            x=247.0,
            y=402.0,
            width=232.0,
            height=75.0
        )

        self.button_2 = tk.Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Monitoreo"),
            relief="flat"
        )
        self.button_2.place(
            x=6.0,
            y=173.0,
            width=165.0,
            height=89.0
        )

        self.button_3 = tk.Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Vinculacion"),
            relief="flat"
        )
        self.button_3.place(
            x=0.0,
            y=89.0,
            width=182.0,
            height=80.0
        )

class Monitoreo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

        self.main_frame = tk.Frame(self, bg="#F9F9F9")
        self.main_frame.place(x=210.0, y=170.0, anchor="nw")

        self.canvas = tk.Canvas(self.main_frame, bg="#F9F9F9", width=1200, height=800)
        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.pcs_frame = tk.Frame(self.canvas, bg="#F9F9F9")

        self.canvas.create_window((0, 0), window=self.pcs_frame, anchor="nw")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.pcs = []

        self.ActualizarDatos()

    def create_widgets(self):
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

        canvas.create_rectangle(0.0, 0.0, 182.0, 1024.0, fill="#175F88", outline="")

        #Imagenes Monitorio
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets_Monitoreo("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets_Monitoreo("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets_Monitoreo("image_3.png"))
        self.image_image_4 = tk.PhotoImage(file=relative_to_assets_Monitoreo("image_4.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets_Monitoreo("button_1.png"))
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets_Monitoreo("button_2.png"))

        canvas.create_image(816.0, 44.0, image=self.image_image_1)
        canvas.create_image(91.0, 41.0, image=self.image_image_2)
        canvas.create_image(815.0, 119.0, image=self.image_image_3)

        #Widgets Monitoreo
        button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Monitoreo"),
            relief="flat"
        )
        button_1.place(
            x=6.0,
            y=173.0,
            width=165.0,
            height=89.0
        )

        button_2 = tk.Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Vinculacion"),
            relief="flat"
        )
        button_2.place(
            x=0.0,
            y=89.0,
            width=182.0,
            height=80.0
        )
    
    #Contenedores de PCs
    def CrearContenedor(self, pc_data, index):
        pc_frame = tk.Frame(self.pcs_frame, bg="#F9F9F9")
        pc_frame.grid(row=0, column=index, padx=20, pady=10, sticky="nw")

        canvas = tk.Canvas(pc_frame, bg="#F9F9F9", width=430, height=549, highlightthickness=0)
        canvas.grid(row=0, column=0, rowspan=8, columnspan=2, sticky="nw")
        canvas.create_rectangle(10, 10, 420, 539, fill="#F9F9F9", outline="")

        tk.Label(
            pc_frame,
            image=self.image_image_4,
            bg="#F9F9F9"
        ).grid(row=0, column=0, columnspan=2, sticky="n", pady=(0, 10))

        tk.Label(
            pc_frame,
            text="PC {}".format(index + 1),
            anchor="nw",
            fg="#175F88",
            font=("DMSans Medium", 30 * -1),
            bg="#F9F9F9"
        ).grid(row=1, column=0, columnspan=2, sticky="w")

        tk.Label(
            pc_frame,
            text="Version: " + pc_data['data'].get("Version del ISO: ", "N/A"),
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        ).grid(row=2, column=0, sticky="w")

        tk.Label(
            pc_frame,
            text="Sistema Operativo: " + pc_data['data'].get("Sistema operativo: ", "N/A"),
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        ).grid(row=3, column=0, sticky="w")

        tk.Label(
            pc_frame,
            text="CPU: " + str(pc_data['data'].get("Uso de la CPU (%): ", "N/A")) + "%",
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        ).grid(row=4, column=0, sticky="w")

        tk.Label(
            pc_frame,
            text="Memoria: " + str(pc_data['data'].get("Memoria usada (%): ", "N/A")) + "%",
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        ).grid(row=5, column=0, sticky="w")

        tk.Label(
            pc_frame,
            text="Disco: " + str(pc_data['data'].get("Espacio usado (%): ", "N/A")) + "%",
            anchor="nw",
            fg="#909090",
            font=("DMSans Medium", 20 * -1),
            bg="#F9F9F9"
        ).grid(row=6, column=0, sticky="w")

        if index >= len(self.pcs):
            self.pcs.extend([{}] * (index + 1 - len(self.pcs)))
        if 'image' not in self.pcs[index]:
            self.pcs[index]['image_label'] = tk.Label(pc_frame, bg="#F9F9F9")
            self.pcs[index]['image_label'].grid(row=7, column=0, columnspan=2)

        if 'image' in pc_data and pc_data['image']:
            self.pcs[index]['image_label'].config(image=pc_data['image'])
            self.pcs[index]['image_label'].image = pc_data['image']

        return pc_frame

    def ActualizarDatos(self):
        global Computadoras

        for widget in self.pcs_frame.winfo_children():
            widget.destroy()

        self.pcs = [{} for _ in range(len(Computadoras))]

        for index, (pc_ip, pc_data) in enumerate(Computadoras.items()):
            pc_frame = self.CrearContenedor(pc_data, index)
            self.pcs_frame.grid_rowconfigure(index, weight=1)
            self.pcs_frame.grid_columnconfigure(index, weight=1)
            self.pcs.append(pc_frame)

        total_width = len(Computadoras) * (430 + 20) 
        total_height = 950
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

        self.after(2000, self.ActualizarDatos)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()