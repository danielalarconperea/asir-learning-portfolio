# Publishing Guide

Pasos recomendados para publicar este portfolio en GitHub.

## Opcion recomendada

Crear un repo nuevo llamado:

```text
asir-learning-portfolio
```

Luego, desde esta carpeta:

```powershell
git add .
git commit -m "Organize ASIR learning portfolio"
git remote add origin https://github.com/danielalarconperea/asir-learning-portfolio.git
git push -u origin main
```

## Despues de publicarlo

1. Fijar `asir-learning-portfolio` en el perfil de GitHub.
2. Actualizar el repo `danielalarconperea/danielalarconperea` con el contenido de `PROFILE_README_DRAFT.md`.
3. Archivar o renombrar los repos antiguos `1ASIR`, `2ASIR` y `python` cuando confirmes que el nuevo repo esta bien.

## Nota sobre videos

El repositorio ignora videos (`*.mp4`, `*.mov`, `*.avi`) para evitar que GitHub quede pesado. Los videos grandes que se sacaron de la version publicable estan en:

```text
../large-media-excluded/
```

