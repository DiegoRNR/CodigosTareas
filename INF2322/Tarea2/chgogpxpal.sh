#! /usr/bin/bash
# Integrante: Diego Negrín
# Lee y asigna los 3 primeros parámetros
word=$1
count=$2
path=$3

# Mueve los índices de los argumentos para trabajar las opciones
shift 3

# Declara e inicializa variables para dueño, grupo y permisos
group=""
owner=""
permissions=""

# Verifica que opciones se ingresaron y asigna su argumento a la variable correspondiente 
while getopts ":g:o:p:" option;
do
  case $option in
    g) group=$OPTARG ;;
    o) owner=$OPTARG ;;
    p) permissions=$OPTARG ;;
  esac
done

# Busca archivos (recursivo default) y cuenta las ocurrencias de una palabra en cada archivo
find "$path" -type f -print0 | while IFS= read -r -d '' file; do
  occurrences=$(grep -o -- "$word" "$file" | wc -l)
  # Retorna el nombre del archivo y la cantidad de ocurrencias
  echo "$file:$occurrences"
# awk recibe el retorno previo, lo separa en ':' y verifica la cantidad de ocurrencias
done | awk -v count="$count" -F: '$2 >= count {print $1}' | while read -r file; do
      # Verifica si se recibio una opcion y cambia su correspondiente valor en el archivo
      if [ -n $owner ]; then
        chown "$owner" "$file"
      fi
      if [ -n $group ]; then
        chgrp "$group" "$file"
      fi
      if [ -n "$permissions" ]; then
        chmod "$permissions" "$file"
      fi
done
