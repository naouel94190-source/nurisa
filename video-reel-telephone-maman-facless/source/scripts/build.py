import json, re
M = [
 ('S', "Salam Camila ! Tu es où ? Les enfants ont enfin dormi, je peux respirer 5 minutes."),
 ('C', "Wa alayki salam ! Je suis dans le canapé, j'ai une nouvelle à te dire."),
 ('S', "Ah ? Tu as déménagé ?"),
 ('C', "Non ! Je me suis lancée dans une formation. En ligne, depuis chez moi."),
 ('S', "Une formation de quoi ?"),
 ('C', "Marketing digital. Je sais, ça sonne bizarre."),
 ('S', "Ça sonne surtout loin de nous. Tu as déjà fait quoi dans ce domaine ?"),
 ('C', "Rien encore ! Je commence juste. Je ne suis pas experte, et je ne te dis pas que je gagne déjà de l'argent."),
 ('S', "Franchement, tu as du courage. Moi je fais le ménage, les devoirs, les repas… et le soir je me demande ce que j'ai fait de moi."),
 ('C', "Je te comprends. Il y a des jours où je me disais exactement la même chose."),
 ('S', "Et tes enfants ? Tu n'as pas peur que ça prenne sur leur temps ?"),
 ('C', "Si, bien sûr. J'ai choisi des créneaux après leur coucher et je le leur explique. C'est un équilibre à trouver, inchaAllah."),
 ('S', "Tu as l'air sereine. Moi je pense que c'est trop tard pour moi, je n'ai ni diplôme ni expérience."),
 ('C', "Je pensais ça aussi. Le plus dur, c'est de commencer, pas d'avoir déjà tout compris."),
 ('S', "Dis-moi au moins, c'est quoi le marketing digital ? Là je suis perdue."),
 ('C', "Je te raconte demain, promis. Ça va te faire sourire."),
]
WR, WT = 4.5, 6.0
ev, cur = [], 1.6
for who, txt in M:
    w = len(re.findall(r"\w+", txt))
    if who == 'S':
        ts = cur + 0.2; td = max(1.1, w / WT); show = ts + td
        ev.append({'who': 'S', 'text': txt, 'tstart': round(ts, 2), 'show': round(show, 2), 'tdur': round(td, 2)})
        cur = show + max(1.2, w / WR) + 0.25
    else:
        ts = cur + 0.2; td = max(1.1, w / WT); show = ts + td
        ev.append({'who': 'C', 'text': txt, 'tstart': round(ts, 2), 'show': round(show, 2), 'tdur': round(td, 2)})
        cur = show + max(1.2, w / WR) + 0.25
closing = {'at': round(cur, 2), 'hold': 8.0}
total = round(cur + closing['hold'] + 0.5, 2)
json.dump({'events': ev, 'closing': closing, 'total': total}, open('sc1_timing.json', 'w'), ensure_ascii=False, indent=1)
open('sc1_timing.js', 'w', encoding='utf-8').write('window.DM = ' + json.dumps({'events': ev, 'closing': closing, 'total': total}, ensure_ascii=False) + ';')
print('total', total, 'messages', len(ev))
