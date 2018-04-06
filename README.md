mercantil_scrapy
================

Este es un scraper para Mercantil.com, basado en Scrapy, stem, privoxy y TOR. El scraper se encuentra contenido en un contenedor Docker.

¿Cómo ejecutar?
===============

1. Primero debes instalar Docker (https://www.docker.com/community-edition).
2. Clonar este repositorio.
3. Abrir un Terminal, cambiar al directorio del repositorio y ejecutar.

```bash
docker build -t mercantil_scrapy .
```

Esto generará la imágen de Docker con las dependencias necesarias para ejecutar el scraper.

4. Una vez terminado el armado de la imagen, ejecuta `docker run -i -t mercantil_scrapy bash` en la Terminal. Esto lanzará una consola en el sistema virtual. Luego ejecuta `cd /home/mercantil && ./start.sh` para iniciar el proceso de webscraping.

El proceso demorará aproximadamente 1 semana ya que scrapy limitará las conexiones simultáneas para evitar posibles baneos de IP, y también cambiará la ip cada 10 items recolectados.



