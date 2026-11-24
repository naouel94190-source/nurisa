# Reel « Sarah & Camila · Épisode 1 » (maman facless)

Fichier final : `sarah_camila_ep1_v14_un_clic.mp4` (1080×1920, 101 s, son inclus).

## Contenu
- Série fictive : personnages inventés. La mention figure sur la page de fin « Personnages fictifs ».
- Dialogue exact : voir `source/sc1_timing.json` (champ `events`).
- Sarah : texte écrit lettre par lettre, un clic de clavier par frappe (le dernier claquement de chaque frappe).
- Camila : trois points sans son, puis son d'apparition du message (`sfx/notif_message.mp3`).
- Pas de musique de fond.
- Fond à motifs beige sur toute la vidéo.
- Vitesse : +10 % (image et son).

## Reconstruire
Dans `source/` : `render.js` produit les images et `sfx.json` à partir de `index.html` ; `scripts/mix_sc1_clavier2.py` produit le son ; l'encodage et l'accélération se font avec ffmpeg.
