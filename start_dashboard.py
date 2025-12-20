"""Quick launcher to start the HTML dashboard."""
import os
import webbrowser
import time
from threading import Timer

# Set demo API key
os.environ['NEWS_API_KEY'] = 'demo_key_for_testing'

print("=" * 70)
print("  🎨 LANCEMENT DU DASHBOARD HTML PREMIUM")
print("=" * 70)
print()
print("  ✨ Fonctionnalités:")
print("     • Design moderne avec glassmorphism")
print("     • Animations fluides et effets 3D")
print("     • Graphiques interactifs Chart.js")
print("     • Thème sombre premium")
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
