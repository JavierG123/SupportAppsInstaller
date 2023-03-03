import tkinter as tk #tkinter para interfaz grafica
import winapps #manejo de apps en win2
import subprocess #manejo de apps en win2
import wget #descargar archivos de internet

# Lee los programas del archivo de programas
programas = open('SupportApps.txt','r').read().splitlines()

# Crea una funcion para obtener la lista de aplicaciones instaladas en la compu
def GetInstalledApps():
    ListOfApps=[]
    for app in winapps.list_installed():
        ListOfApps.append(app.name) #Crear una lista con las apps instaladas en la compu
    return(ListOfApps)

# Crea una funcion para comparar la lista de aplicaciones instaladas en la compu con el .txt que contiene las apps de soporte
#y obtener la lista con apps faltantes por instalar
def CompareApps(ListOfApps):
    aux = 0
    MissingApps=[]
    InstalledSupportApps=[]
    for j in programas:
        for i in ListOfApps:
            if j in i:
                aux = 1
        if aux == 0:
            MissingApps.append(j) # Guardar en una lista las apps de soporte que faltan por instalar
        else:
            aux = 0
    return MissingApps

# Lee los programas instalados
programas_instalados = GetInstalledApps()

# Crea la ventana principal
root = tk.Tk()
logo = tk.PhotoImage(file="mutant_icon.png")
root.iconphoto(False, logo)
root.title('Instalador de programas')

# Crear el diccionario con programa,url

# Abrir el archivo de texto
with open('repositorio.txt', 'r') as file:

    # Crear un diccionario vacío
    repositorio_de_archivos = {}

    # Leer el archivo línea por línea
    for line in file:

        # Dividir la cadena en dos partes usando una coma
        key, value = line.strip().split(',')

        # Agregar la clave y el valor al diccionario
        repositorio_de_archivos.update({key: value})

# Crea una etiqueta para la lista de programas
tk.Label(root, text='Programas a instalar:').pack()

# Crea una lista para guardar los checkboxes
checkboxes = []

# Crea los checkboxes para cada programa
chu=[tk.IntVar() for _ in programas]
for i, programa in enumerate(programas):
    programa = programa.strip()
    checkbox = tk.Checkbutton(root, text=programa, variable=chu[i])
    checkbox.pack()
    checkboxes.append(checkbox)

# Coloca check en las aplicaciones que faltan por instalar
MissingApps = CompareApps(GetInstalledApps())
for i in range(len(checkboxes)):
    for j in range(len(MissingApps)):   
        if checkboxes[i].cget("text") in MissingApps[j]:
            checkboxes[i].select()
                   

# Crea una función para instalar los programas seleccionados
def instalar_programas():
    for i, programa in enumerate(programas):
        if chu[i].get() == 1:
            # Descarga el instalador desde el repositorio de archivos
            url = repositorio_de_archivos[programa.strip()]
            if '.msi' in url:
                # Guarda el instalador en un archivo temporal
                response = wget.download(url,programa+'.msi')
                # Ejecuta el instalador
                subprocess.call(programa+'.msi', shell=True)
            else:
                # Guarda el instalador en un archivo temporal
                response = wget.download(url,programa+'.exe')
                # Ejecuta el instalador
                subprocess.call(programa+'.exe', shell=True)  

# Crea el botón "Instalar"
tk.Button(root, text='Instalar', command=instalar_programas).pack()

# PARA PRUEBAS
#fallo AnyDesk y WinSCP


# Ejecuta la ventana principal
root.mainloop()