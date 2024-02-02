# Utilisation de Nginx pour servir le contenu statique
FROM nginx:alpine

# Copier les fichiers statiques du frontend
COPY ./frontend/static /usr/share/nginx/html/static
COPY ./frontend/templates /usr/share/nginx/html

# Exposer le port pour Nginx
EXPOSE 80
