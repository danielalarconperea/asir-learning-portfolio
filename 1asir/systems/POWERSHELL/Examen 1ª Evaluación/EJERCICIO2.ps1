do{
    $repetir="N"
    $fecha=read-host "dime una fecha de la cual partir la busqueda de archivos. DD-MM-AAAA"
    $formatofecha=get-date $fecha
    $dir=Get-ChildItem -Directory | Where-Object LastWriteTime -ge $formatofecha
    if(($dir).count -ne 0){
        $dir
    }else{
        $repetir=read-host "No existe ningun archivo creado por esa fecha o mas tarde. ¿Quieres introducir una fecha diferente S/N?"
    }
}while($repetir -eq "s" -or $repetir -eq "S")