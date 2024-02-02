# Utilisation d'une image Python
FROM python:3.8

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du backend
COPY ./backend /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port sur lequel Flask s'exécute
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "app.py"]
