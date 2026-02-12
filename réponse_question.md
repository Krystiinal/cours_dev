QUESTION 1 : quel est le principal inconvénient de cette façon de faire ?
---
current_user = get_current_user(request)
if not current_user:
    return redirect(url_for("auth.login_page"))
---

Réponse : c'est répétitif, on va répéter le même bout de code à chaque fois qu'on a besoin. 

--> Solution : les décorateurs permettent de factoriser une fonction


QUESTION 2 : Que se passe-t-il si le serveur redémarre ? Un utilisateur qui était connecté pourra-t-il accéder encore à /dashboard ?
Oui, tant que la durée de vie du cookie de sesssion est toujours là (24h). L'utilisateur connecté pourra toujours accéder au dashboard. 

QUESTION 3 : Comment un attaquant pourrait-il voler votre session ? Quelles protections avons-nous mises en place ?
Il pourrait nous voler notre id de session. Mais on a mis des protections contre le JS et contre les CSRF. 

QUESTION 4 : Pourquoi utilise-t-on secrets.token_hex() plutôt qu'un simple compteur (session_1, session_2, ...) ?
cela permet d'avoir des tokens générés aléatoirement. 