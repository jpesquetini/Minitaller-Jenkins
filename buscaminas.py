from tkinter import *;from tkinter import messagebox,ttk # GUI
from PIL import Image,ImageTk # Manipulacion de imagenes
import random, time, threading, json # Procesamientos, guardado de archivos, etc

# Obtiene los datos del ranking
def ranking():
        try:
            with open("Datos/data.json","r") as f: # Abre el archivo para lectura
                data=json.load(f)
            if data == []:
                messagebox.showwarning("Error","Aún no hay victorias registradas")
            else:
                eznom="";eztime="";mednom="";medtime="";difnom="";diftime="";exnom="";extime=""
                for i in data:
                    match i["dificultad"]:
                        case "Facil":
                            eznom+=i["nombre"]+"\n"
                            eztime+=str(i["tiempo"])+"\n"
                        case "Medio":
                            mednom+=i["nombre"]+"\n"
                            medtime+=str(i["tiempo"])+"\n"
                        case "Dificil":
                            difnom+=i["nombre"]+"\n"
                            diftime+=str(i["tiempo"])+"\n"
                        case "Experto":
                            exnom+=i["nombre"]+"\n"
                            extime+=str(i["tiempo"])+"\n"
                rank = Toplevel(root)
                rank.geometry("600x600")
                rank.resizable(0,0) 
                tabs=ttk.Notebook(rank) # Crea el widget de las pestañas
                tabs.pack(fill='both',expand=1) # Permite que ocupe toda la ventana
                # Crea las pestañas
                facil=ttk.Frame(tabs)
                medio=ttk.Frame(tabs)
                dificil=ttk.Frame(tabs)
                experto=ttk.Frame(tabs)
                # Asigna los labels a las ventanas
                titulos=["Facil","Medio","Dificil","Experto"]
                for i in [facil,medio,dificil,experto]:
                    tabs.add(i,text=titulos[[facil,medio,dificil,experto].index(i)])
                    Label(i,text=titulos[[facil,medio,dificil,experto].index(i)],font="Hack 20",anchor="center",height="2").pack()
                    Label(i,text="Segundos").place(x="50",y="90",anchor="center")
                    Label(i,text="Persona").place(x="500",y="90",anchor="center")
                ttk.Label(facil,text=eztime).place(x="50",y="120",anchor="center")
                ttk.Label(facil,text=eznom).place(x="500",y="120",anchor="center") 
                ttk.Label(medio,text=medtime).place(x="50",y="120",anchor="center")
                ttk.Label(medio,text=mednom).place(x="500",y="120",anchor="center") 
                ttk.Label(dificil,text=diftime).place(x="50",y="120",anchor="center")
                ttk.Label(dificil,text=difnom).place(x="500",y="120",anchor="center") 
                ttk.Label(experto,text=extime).place(x="50",y="120",anchor="center")
                ttk.Label(experto,text=exnom).place(x="500",y="120",anchor="center")                
        except FileNotFoundError: # El decode error sucede cuando el archivo json esta vacio
            messagebox.showwarning("Error","Aun no hay victorias registradas")
        except json.decoder.JSONDecodeError:
            messagebox.showerror("Error","Los datos estan corruptos, por favor borre el archivo \"data.json\" en la carpeta Datos")

# Guarda datos en el ranking
def guardarRanking(tiempo,nombre,dificultad):
    global guardado
    if dificultad == "Personalizado":
        messagebox.showerror("Error","Los tableros personalizados no son guardados en el ranking")
        return
    if nombre == "":
        messagebox.showerror("Error","Digite un nombre")
    else:
        try:
            try:
            
                with open("Datos/data.json","r") as f: # Abre el archivo para leer
                        data=json.load(f) 
            except FileNotFoundError: # Si no existe el archivo, tomara una lista vacia
                data=[]
            if guardado == True: # Si ya se ha guardado una vez la misma victoria, entonces no permitirá que se haga otra vez
                messagebox.showwarning("Error","Solo se puede registrar 1 vez cada victoria")
            else:
                califica = True
                facil=[];medio=[];dificil=[];experto=[]
                data.append({"nombre":nombre,"tiempo":tiempo,"dificultad":dificultad})
                data.sort(key=lambda x:x["tiempo"]) # Ordena los datos de menor a mayor tiempo
                for i in data: # Los descompone por dificultad, cada dificultad tiene su top 10
                    match i["dificultad"]:
                        case "Facil":
                            facil.append((i["nombre"],i["tiempo"],i["dificultad"]))
                        case "Medio":
                            medio.append((i["nombre"],i["tiempo"],i["dificultad"]))
                        case "Dificil":
                            dificil.append((i["nombre"],i["tiempo"],i["dificultad"]))
                        case "Experto":
                            experto.append((i["nombre"],i["tiempo"],i["dificultad"]))
                for i in [facil,medio,dificil,experto]:
                    if len(i) > 10: # Si hay mas de 10 puestos en una categoria
                        if i[-1] == (nombre,tiempo,dificultad): # Si el ultimo elemento es el que se acaba de añadir, significa que no esta en el top 10
                            messagebox.showinfo("Aviso","No calificas en los 10 primeros, intenta conseguir un mejor tiempo!")
                            califica = False
                            break # no tiene sentido seguir con el bucle, porque solo se añade un elemento a la vez
                        else: # En caso contrario, borra el ultimo puesto
                            del data[data.index({"nombre": i[-1][0], "tiempo" : i[-1][1],"dificultad": i[-1][2]})]
                            break 
                if califica == True: # Si se acaba de eliminar del top, entonces no hace falta guardar los datos en el archivo
                    with open("Datos/data.json","w") as f: # Vuelve a abrir el archivo, para escritura, si no existia, lo va a crear
                        data=json.dump(data,f,indent=2)
                        messagebox.showinfo("Ranking","Datos guardados correctamente!")
                        guardado=True
        except json.decoder.JSONDecodeError: # En caso de que la decodificacion falle
            messagebox.showerror("Error","Los datos estan corruptos, por favor borre el archivo \"data.json\" en la carpeta Datos e intente de nuevo")
def salirRoot(): # Pequeña funcion para mostrar un aviso y prevenir salidas no intencionales
    if messagebox.askyesno("Aviso","Seguro que quieres salir?"):
        root.destroy()
def menu(): # Crea el menú principal
    global tempo,guardado
    # Reset de variables de bandera y temporizador
    tempo = IntVar()
    tempo.set(0)
    guardado = False 
    for widgets in root.winfo_children():
        widgets.destroy()
    # Creacion del menu principal
    Label(text="Buscaminas",font="Hack 30",height="2",anchor="center").pack()
    Label(image=logo).pack()
    Button(text="Facil",width="10",command=lambda:ventanaJuego(8,8,10,"Facil")).pack() #8x8 10 minas
    Button(text="Medio",width="10",command=lambda:ventanaJuego(10,10,15,"Medio")).pack() #10x10 15 minas
    Button(text="Dificil",width="10",command=lambda:ventanaJuego(12,12,25,"Dificil")).pack() # 12x12 25 minas
    Button(text="Experto",width="10",command=lambda:ventanaJuego(15,15,40,"Experto")).pack() # 15x15 40 minas
    Button(text="Personalizado",width="10",command=personalizado).pack() # Personalizado
    Button(text="Ranking",command=lambda:ranking(),width="7",).place(x=5,y=5) # Ranking
def personalizado():
    custom=Toplevel(root)
    custom.geometry("500x300")
    custom.resizable(0,0)
    filas = IntVar()
    columnas = IntVar()
    minas = IntVar()
    Label(custom,text="Partida Personalizada",font="Hack 15",height="2",anchor="center").pack()
    Label(custom,text="Filas").pack()
    Entry(custom,textvariable=filas).pack()
    Label(custom,text="Columnas").pack()
    Entry(custom,textvariable=columnas).pack()
    Label(custom,text="Numero de minas").pack()
    Entry(custom,textvariable=minas).pack()
    Button(custom,text="Jugar",command=lambda:ventanaJuego(filas.get(),columnas.get(),minas.get(),"Personalizado")).pack(side="bottom") 
    Button(custom,text="Cancelar",command=menu).pack(side="bottom")
    
def ventanaJuego(filas,columnas,minas,dificultad):
    # Creacion de la ventana principal con los botones sin asignar
    global botones,tablero,restantes,OGmina,OGbandera,IMGmina,IMGbandera,conBandera,clickeados,ganado # Variables a las que podran acceder cualquier funcion, Es importante definir ciertas cosas en esta funcion, porque asi evito que se sobreescriban.
    # Los botones deben adaptarse a la geometria de la ventana (920x720)
    perdido = False
    if filas == 0 or columnas == 0 or minas == 0:
        messagebox.showerror("Error","No se han ingresado valores")        
    elif filas * columnas - 9 < minas: # Las minas deben caber, ese menos 9 es contando la zona segura inicial
        messagebox.showerror("Error","Las minas no caben en el tablero")
    elif filas * columnas < 25:
        messagebox.showerror("Error","Las dimensiones minimas del tablero son de 5x5 (25 celdas)")
    elif filas*columnas > 400: # Se debe seguir el limite de 5x5 y 20x20
        messagebox.showerror("Error","Las dimensiones maximas del tablero son de 20x20 (400 celdas)")
    else:
        anchoBoton = 1000//columnas
        alturaBoton = 600//filas # Al restarle 120, queda bien colocado
        # Imagenes:
        IMGbandera = OGbandera.resize((anchoBoton//3,alturaBoton//2)) # La razon de que se escale con las dimensiones divididas, es para que no se estire de más en tableros simetricos y encaje bien en el botón
        IMGmina = OGmina.resize((anchoBoton//3,alturaBoton//2)) 
        IMGbandera=ImageTk.PhotoImage(IMGbandera)
        IMGmina=ImageTk.PhotoImage(IMGmina)
        # Creacion del tablero
        for widgets in root.winfo_children():
            widgets.destroy()
        Button(root,text="Salir",command=salir).place(x=920,y=10)
        Button(root,text="Reiniciar",command=lambda:reiniciar(filas,columnas,minas,dificultad)).place(x=820,y=10)
        restantes=IntVar()
        restantes.set((filas*columnas)-minas) # Calculo de casillas restantes
        conBandera=[]    
        Label(root,text="Casillas restantes:").pack() # Estas dos lineas son las que mostraran las casillas restantes
        Label(root,textvariable=restantes).pack()
        tableroVacio=[]
        for i in range(filas): # Crea una matriz con ceros con las dimensiones indicadas
            fila=[]
            for j in range(columnas):
                fila.append(0)
            tableroVacio.append(fila)
        botones={}
        for indicefila,valfila in enumerate(tableroVacio): # Crea los botones y los coloca
            for indicecolumna,valcolumna in enumerate(valfila):   
                boton=Button(bg="lightgray",highlightbackground="white",command=lambda f=indicefila,c=indicecolumna:genTablero(filas,columnas,minas,(f,c),dificultad)) # Si no asigno esas variables, todos los botones tendran el mismo valor de indice (por alguna razon)
                botones[indicefila,indicecolumna]=boton
                boton.bind("<Button-3>",lambda e,f=indicefila,c=indicecolumna:bandera(f,c)) # Con el bind, tkinter siempre devuelve como primer valor el evento, pero no lo ocupamos (dure TIEMPO para darme cuenta). Por eso esta esa "e" ahi
                boton.place(x=indicecolumna*anchoBoton,y=(indicefila*alturaBoton)+60,height=alturaBoton,width=anchoBoton)
        clickeados=[]
def salir():
    global tempo,perdido
    if messagebox.askyesno("Salir","¿Esta seguro que desea salir?"):
        perdido = True
        tempo.set(0)
        menu()
def reiniciar(filas,columnas,minas,dificultad):
    global tempo,perdido
    if messagebox.askyesno("Reiniciar","¿Esta seguro que desea reiniciar? El tablero será diferente"):
        perdido = True
        tempo.set(0) # Reinicia el tempo
        ventanaJuego(filas,columnas,minas,dificultad) # Genera de nuevo el tablero, con las mismas dimensiones y minas 
         
def temporizador(): # Temporizador que consta de 1 variable a la que se le suma 1 por cada segundo
    global tempo,ganado,perdido
    while ganado == False and perdido == False: # Si no se ha perdido o ganado, el tempo sigue
        tempo.set(tempo.get()+1)
        time.sleep(1)
     
def genTablero(largofila,largocolumna,minas,primerclick,dificultad): # Funcion que genera el tablero del juego, dada por el largo (por ejemplo, 8 si es 8x8) y el numero de minas
    global tablero,restantes,OGmina,OGbandera,IMGmina,IMGbandera,tempo,perdido,ganado
    tablero = []
    celdas=[]
    pesos=[]
    # Para que las minas tiendan a las esquinas, voy a usar random.choices(), lo que me permite asignarle un peso a cada celda, usando la distancia que tienen hacia el centro
    centro = (largofila//2,largocolumna//2)
    for i in range(largofila):
        fila=[]
        for j in range(largocolumna):
            fila.append(0)
            celdas.append((i,j))
            # El peso de los vecinos del centro siempre es 2, para que las casillas que lo rodean directamente no tengan minas, uso este condicional
            if (i-centro[0])**2 + (j-centro[1])**2 <= 2 or (i-primerclick[0])**2 + (j-primerclick[1])**2 <= 2: # El primer click tambien se asegura, al igual que las casillas que lo rodean.
                pesos.append(0)
            else:
                pesos.append((i-centro[0])**2 + (j-centro[1])**2) # La distancia del centro a la celda sera el peso
        tablero.append(fila) 
    # Colocacion de las minas
    for mina in range(minas): 
        celda=random.choices(celdas,pesos)
        fila=celda[0][0];columna=celda[0][1] # Random.choices() devuelve algo como [(i,j)], por lo que es necesario el primer indice
        while tablero[fila][columna] == -1: # Si cae en una casilla que es -1, buscara otra celda
            celda=random.choices(celdas,pesos)
            fila=celda[0][0];columna=celda[0][1]
        tablero[fila][columna] = -1
    # Deteccion de las minas cerca de cada celda, para asignarle un numero a cada una
    for fila,i in enumerate(tablero): 
        for celda,j in enumerate(tablero[fila]):
            if tablero[fila][celda] == -1:
                continue
            for indicefila in [-1,0,1]: # Para ahorrarnos ifs, se hace un bucle con los indices que ocupamos evaluar
                for indicecelda in [-1,0,1]:
                    if (indicefila,indicecelda) != (0,0):
                        vecinoFila = fila+indicefila # Estas variables son para hacer mas legible el codigo
                        vecinoCelda= celda+indicecelda
                        if vecinoFila>=0 and vecinoFila < largofila and vecinoCelda >=0 and vecinoCelda<largocolumna: # Verificar que la celda este en la tableroriz
                            if tablero[vecinoFila][vecinoCelda]==-1:
                                tablero[fila][celda]+=1 # Si detecta una mina cerca, el numero subirá
    # Redefino el valor de cada boton con el correspondiente a la matriz
    for indicefila,valfila in enumerate(tablero):
        for indicecolumna,valcolumna in enumerate(valfila):   
            if valcolumna == -1:
                botones[indicefila,indicecolumna].config(command=lambda f=indicefila,c=indicecolumna:boom(f,c))
            else:
                botones[indicefila,indicecolumna].config(command=lambda f=indicefila,c=indicecolumna:libre(f,c,dificultad))
    libre(primerclick[0],primerclick[1],dificultad) # Se activa la casilla recien clickeada
    perdido=False;ganado=False # Inicializo la variable que detiene el temporizador si se pierde o reinicia 
    threading.Thread(target=temporizador).start() # inicia el temporizador
    Label(root,text="Segundos transcurridos: ").place(x=80,y=20)
    Label(root,textvariable=tempo).place(x=250,y=20)

def bandera(f,c): # Colocacion de banderas con click derecho
    global conBandera,botones,IMGbandera,clickeados
    if (f,c) not in clickeados:
        if (f,c) not in conBandera: # Si no tiene bandera, se le pone, y si ya tiene, se le quita
            conBandera.append((f,c))
            botones[(f,c)].config(image=IMGbandera)
        else:
            conBandera.pop(conBandera.index((f,c)))
            botones[(f,c)].config(image="")

def libre(f,c,dificultad): # Funcion que se ejecuta cuando se clickea una casilla libre
    global tablero,botones,restantes,clickeados,conBandera
    if (f,c) not in clickeados and (f,c) not in conBandera: # Solo se hara el procesamiento si el boton no ha sido clickeado, si el boton tiene bandera, se impide que se clickee
        clickeados.append((f,c))
        restantes.set(restantes.get()-1)
        if tablero[f][c] == 0:
            botones[f,c].config(bg="darkgray",highlightbackground="darkgray")
            visitados=[(f,c)]
            pendientes=[(f,c)]
            while pendientes !=[]:
                fila,columna = pendientes.pop() #pop devuelve el elemento recien eliminado, por lo que aprovecho esto para simular una cola
                for direccionFila in [-1,0,1]:
                    for direccionColumna in [-1,0,1]:
                        if (direccionFila,direccionColumna) != (0,0): # Para que no se active en la casilla misma
                            vecFila,vecColu=fila+direccionFila,columna+direccionColumna
                            if vecFila>=0 and vecFila < len(tablero) and vecColu >=0 and vecColu<len(tablero[0]): # Comprobar que este en el tablero
                                if (vecFila,vecColu) not in visitados and tablero[vecFila][vecColu] != -1: # Si ha sido visitado antes o si es una mina, lo ignora
                                    visitados.append((vecFila,vecColu)) # Lo agrega a visitados
                                    boton = botones[vecFila,vecColu]
                                    if tablero[vecFila][vecColu] == 0:
                                        if (vecFila,vecColu) in conBandera:
                                            conBandera.pop(conBandera.index((vecFila,vecColu)))
                                            boton.config(image="")
                                        boton.config(bg="darkgray",highlightbackground="darkgray")
                                        pendientes.append((vecFila,vecColu))
                                        if (vecFila,vecColu) not in clickeados:
                                            restantes.set(restantes.get()-1)
                                            clickeados.append((vecFila,vecColu))
                                    else:
                                        boton.config(text=tablero[vecFila][vecColu])
                                        if (vecFila,vecColu) in conBandera:
                                            boton.config(image="")
                                            boton.config(bg="lightgray",highlightbackground="white")
                                            conBandera.pop(conBandera.index((vecFila,vecColu)))
                                        if (vecFila,vecColu) not in clickeados:
                                            restantes.set(restantes.get()-1)
                                            clickeados.append((vecFila,vecColu))
        else:
            boton=botones[f,c]
            botones[(f,c)].config(image="")
            boton.config(text=tablero[f][c])
    if restantes.get() == 0:
        victoria(dificultad)
def victoria(dificultad):
    global ganado
    ganado = True
    victoria=Toplevel(root)
    victoria.geometry("500x300")
    victoria.resizable(0,0)
    victoria.grab_set() # Hace que la ventana sea modal, o sea, bloquea la ventana del tablero para que no sea interactuable
    nombre=StringVar()
    Label(victoria,text="Victoria!",font="Hack 15",height="2",anchor="center").pack()
    Label(victoria,text="Tiempo transcurrido").pack()
    Label(victoria,text=f"{tempo.get()} segundos").pack()
    Label(victoria,text="Nombre a registrar: ").pack()
    Entry(victoria,textvariable=nombre).pack()
    Button(victoria,text="Guardar",command=lambda:guardarRanking(tempo.get(),nombre.get(),dificultad)).pack()
    Button(victoria,text="Volver al menu",command=menu).pack()
    victoria.protocol("WM_DELETE_WINDOW",menu)
    
def boom(f,c): # Funcion que se ejecuta cuando se clickea una mina
    global tablero,botones,IMGmina,conBandera,perdido
    if (f,c) not in conBandera: # Solo se procederá si no tiene bandera
        for indice in botones:
            if tablero[indice[0]][indice[1]] == -1:
                boton=botones[indice]
                boton.config(image=IMGmina)
        derrota=Toplevel(root)
        derrota.geometry("500x300")
        derrota.resizable(0,0)
        derrota.grab_set()
        Label(derrota,text="Has perdido",font="Hack 15",height="2",anchor="center").pack()
        Label(derrota,text="Tiempo transcurrido").pack()
        Label(derrota,text=f"{tempo.get()} segundos").pack()
        Button(derrota,text="Volver al menu",command=menu).pack()
        perdido=True 
        derrota.protocol("WM_DELETE_WINDOW",menu)

root = Tk()
root.title("Buscaminas")
root.geometry("1000x900")
root.resizable(0, 0)
logo=PhotoImage(file="Datos/logo.png")
OGbandera=Image.open("Datos/bandera.png") # Abro las imagenes para procesarlas
OGmina=Image.open("Datos/mina.png")
root.protocol("WM_DELETE_WINDOW",salirRoot)
menu() # Prepara el menú
root.mainloop() # Invoca la ventana