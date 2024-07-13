import os
import shutil
from subprocess import call, CalledProcessError

# Liste des dossiers et fichiers à obfusquer
items_to_obfuscate = ['config', 'services', 'controllers', 'hooks', 'ui', 'utils', 'main.py']

# Chemin du dossier de build
build_dir = os.path.join('build', 'obfuscated')

# Chemins des fichiers de configuration source
config_files_src = [
    os.path.join('config', 'user_config.json'),
    os.path.join('config', 'app_config.json')
]

# Nettoyer le dossier de build
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
os.makedirs(build_dir)

# Fonction pour obfusquer un dossier ou un fichier
def obfuscate_item(item):
    output_path = os.path.join(build_dir, item)
    if os.path.isdir(item):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    try:
        result = call(['pyarmor', 'gen', '--output', output_path, item])
        if result != 0:
            print(f"Erreur lors de l'obfuscation de {item}")
    except CalledProcessError as e:
        print(f"Erreur lors de l'exécution de pyarmor pour {item}: {e}")

# Fonction pour copier les fichiers de configuration
def copy_config_files():
    config_dest_dir = os.path.join(build_dir, 'config')
    if not os.path.exists(config_dest_dir):
        os.makedirs(config_dest_dir)
    for config_file in config_files_src:
        shutil.copy(config_file, config_dest_dir)

# Obfusquer chaque dossier ou fichier
for item in items_to_obfuscate:
    print(f"Obfuscation de {item}...")
    obfuscate_item(item)

# Copier les fichiers de configuration après l'obfuscation
copy_config_files()

print("Obfuscation terminée et fichiers de configuration copiés")
