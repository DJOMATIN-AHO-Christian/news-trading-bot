"""Lancement du dashboard avec la clé API configurée."""
import os
import webbrowser
import time
from threading import Timer

# Configuration de la clé API
os.environ['NEWS_API_KEY'] = '775a6f27d15a4c86841a0558433c1687'

print("=" * 70)
print("  🎨 DASHBOARD PREMIUM - MODE RÉEL ACTIVÉ")
print("=" * 70)
print()
print("  ✅ Clé NewsAPI configurée")
print("  ✅ Analyse de sentiment réelle")
print("  ✅ Données de marché en temps réel")
print()
print("  🌐 URL: http://localhost:5000")
print()
print("  Le navigateur va s'ouvrir automatiquement...")
print("  Appuyez sur Ctrl+C pour arrêter le serveur")
print("=" * 70)
print()

# Open browser after 2 seconds
def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

Timer(0.5, open_browser).start()

# Start Flask server
from api_server import app
app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
