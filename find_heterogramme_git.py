# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:52:23 2024

@author: maxim
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 20:05:38 2024

@author: Maxime
"""

#https://www.reddit.com/r/Enigmes/comments/1aravpd/la_plus_longue_phrase_en_utilisant_une_seule_fois/
import unidecode

def affiche(s):
    return f'"{s[1:]}", {str(nb_let(s))}, {str(lettres_manquantes(s))}'

def lettres_manquantes(s):
    return set(alphabet).difference(set(s.replace(" ", "")))


def est_heterogramme(w):
    w = w.replace(" ", "")
    return len(set(w)) == len(w)

def norm(w):
    w = unidecode.unidecode(w.strip()) #enleve accents
    w = w.replace("'", " ").replace("-", " ")
    return w.lower()

def nb_let(s):
    return len(s.replace(" ", ""))

#dictionnaire telecharge sur (https://www.3zsoftware.com/fr/listes.php)
dictionnaire_path = "liste_francais.txt"

with open(dictionnaire_path, 'r') as f:
    every_words = f.readlines()
    
print(f"nb mots avant : {len(every_words)}")

#enleve les accents, les ' et - et met en minuscule
every_words = [norm(w) for w in every_words] 
#enleve le mot si il a des caracteres speciaux
every_words = [w for w in every_words if w.isalpha()]
#enleve les mots avec deja des caracteres en double
every_words = [w for w in every_words if est_heterogramme(w)]
#trie les mots du plus long au plus petit
#every_words.sort(key=lambda w : len(w), reverse=True)

print(f"nb mots apres filtrage : {len(every_words)}")

alphabet = "abcdefghijklmnopqrstuvwxyz"
memo = {} #mots qui restent en fonction des contraintes de lettres

#ajoute dans memo les listes de mots n'ayant pas la lettre a, b, c, ...
for l in alphabet:
    r_words = []
    for w in every_words:
        if not l in w:
            r_words.append(w)
    
    memo[l] = set(r_words)

#solution de type "dynamic programming" avec un memo
#s est la phrase courante et r_words les mots qui sont encore disponible qu'on pourrait ajouter
def meilleur_heterogramme(s, r_words):
    if len(r_words) == 0:
        return s
    
    if len(r_words) == 1:
        return s+" "+list(r_words)[0]
        
    best_s = s
    #On teste les mots les plus long d'abord car ils sont plus contraignants
    for i, w in enumerate(sorted(list(r_words), key=lambda w : len(w), reverse=True)):
        new_s=s+" "+w
            
        banned_letters = "".join(sorted(set(new_s.replace(" ", ""))))
        #soit on connait deja la liste des mots qui restent
        if banned_letters in memo:
            new_r_words = memo.get(banned_letters)
        
        #soit on doit la calculer, ici en calculant des intersections de set de mots venant du memo
        else:
            new_banned_letters = "".join(sorted(set(w.replace(" ", ""))))
            new_r_words = set(r_words)
            for bl in new_banned_letters:
                new_r_words.intersection_update(memo[bl])
                if len(new_r_words) == 0:
                    break
                
                #on l'ajoute au memo
                memo[banned_letters] = new_r_words
            
        new_best_s = meilleur_heterogramme(new_s, new_r_words)
        
        if nb_let(new_best_s) >= nb_let(best_s):
            best_s = new_best_s
            if s=="":
                #si on est dans la "boucle principale" on affiche les resultats
                print(f"iteration {i} : {affiche(best_s)}")
    
    return best_s
    
res = meilleur_heterogramme("", set(every_words))