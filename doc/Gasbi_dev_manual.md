#Manuel de Maintenance de Gasbi

---

<a id="sommaire"></a>

##Sommaire

1. [Environnement](#ancre1)
2. [Les Classes](#ancre2)
3. [Le Processus](#ancre3)
4. [Ajout d'un nouvel Outil](#ancre4)
5. [Conventions](#ancre5)

---

<a id="ancre1"></a>

##1. Environnement

###Système d'exploitation

Gasbi est supposé fonctionner dans n'importe quel système d'exploitation UNIX mais les tests ont été effectués uniquement sur Linux (distribution Ubuntu14.04).

###Language

Gasbi fonctionne dans un environnement python3+.

###Bibliothèques

Gasbi utilise des bibliothèques installées par défaut avec python3:

* os
* time
* unittest

Aucune bibliothèque supplémentaire n'est nécessaire.

[remonter](#sommaire)

---

<a id="ancre2"></a>

##2. Les Classes

Vous trouverez un diagramme de classe au format .dia et .jpeg dans le répertoire doc sous le nom de fichier 'class_diagram'.

Dans cette partie, vous trouverez la localisation des classes dans le répertoire GASBI-PIB. Pour obtenir un descriptif détaillé des classes, veuillez consultez la pydoc de chacune d'elle dans le répertoire:

    /.../GASBI-PIB/doc/pydoc

###Gasbi

####La classe Gasbi est couplée au main du programme:

    /.../GASBI-PIB/src/Gasbi.py

###Gestion des Options

####OptionManager
        
    /.../GASBI-PIB/src/util/Options/OptionManager.py
    
####OptionList

    /.../GASBI-PIB/src/util/Options/OptionList.py

####Option

    /.../GASBI-PIB/src/util/Options/Option.py

###Gestion des Outils

####Tool

    /.../GASBI-PIB/src/tool/Tool.py

####CDSFindingTool

    /.../GASBI-PIB/src/tool/CDSFindingTool.py

####Glimmer

    /.../GASBI-PIB/src/tool/Glimmer.py

####GeneMark

    /.../GASBI-PIB/src/tool/GeneMark.py

####tRNAFindingTool

    /.../GASBI-PIB/src/tool/tRNAFindingTool.py

####tRNAScan

    /.../GASBI-PIB/src/tool/TRNAScan.py

###Gestion des résultats

####ResultManager

    /.../GASBI-PIB/src/util/Results/ResultManager.py

####CDSFindingToolResultManager

    /.../GASBI-PIB/src/util/Results/CDSFindingToolResultManager.py

####CDSList

    /.../GASBI-PIB/src/util/Results/CDSList.py
    
####CDS

    /.../GASBI-PIB/src/util/Results/CDS.py

####tRNAFindingToolResultManager

    /.../GASBI-PIB/src/util/Results/tRNAFindingToolResultManager.py

####tRNAList

    /.../GASBI-PIB/src/util/Results/tRNAList.py

####tRNA

    /.../GASBI-PIB/src/util/Results/tRNA.py
    
###Utilitaires

####Constant

    /.../GASBI-PIB/src/util/Constant.py

####Checker

    /.../GASBI-PIB/src/util/Checker.py

####Logger

    /.../GASBI-PIB/src/util/Logger.py
  
####Singleton

    /.../GASBI-PIB/src/Singleton.py

[remonter](#sommaire)

---

<a id="ancre3"></a>

##3. Le Processus

Vous trouverez un diagramme de processus au format .dia et .jpeg dans le répertoire doc sous le nom de fichier 'process\_diagram'.

Ci-après, une description de chacune des étapes du programme, en référence au diagramme de processus.

###Gestion des Options

1. set\_options(configuration\_file): Gasbi demande à OptionManager de récupérer les options présentes dans le fichier de configuration.
2. \_\_init\_\_(): A chaque fois qu'une ligne contenant une option est trouvée, OptionManager crée un Objet Option avec tous ses attributs (nom, outil, groupe, sous-groupe, valeur).
3. append(Option): Chaque option crée est ajoutée à l'OptionList qui doit la contenir (une par outil).
4. check\_options(): Gasbi demande à l'OptionManager de vérifier l'intégrité des options.
5. check\_options(): OptionManager demande à chaque outil de vérifier ses propres options.
6. get\_options(): Avant d'instancier chaque outil, Gasbi demande à l'OptionManager ses options.

###Gestion des Outils

7. start(): Gasbi demande à chaque outil de s'exécuter. Les outils instanciés sont stockés dans un dictionnaire tool\_objects.

###Gestion des résultats

8. set\_tools(): Gasbi donne aux ResultManager les outils qui ont été exécutés sous la forme d'une liste.
9. check\_output(): Gasbi demande aux ResultManager de vérifier les fichiers de sortie des outils.
10. check\_output(): Les ResultManager demandent à leurs outils de vérifier l'intégrité de leurs sorties.
11. parse\_output(): Gasbi demande aux ResultManager de récupérer les résultats.
12. parse\_output(): Les ResultManager demandent à chacun de leurs outils de récupérer leurs résultats.
13. \_\_init\_\_(): A chaque fois qu'une ligne contenant un résultat est trouvée par l'outil, l'outil crée un Objet Result (CDS ou tRNA) contenant les attributs du résultat.
14. append(Result): Chaque Result crée est ajouté au ResultList qui doit le contenir (CDSList ou tRNAList)
15. perform\_analysis(): Gasbi demande aux ResultManager de regrouper les résultats du même type, les trier et déterminer l'existence ou non d'un conflit.
16. write\_outfile(): Gasbi demande aux ResultManager d'écrire les fichiers de sortie au format gff.

[remonter](#sommaire)

---

<a id="ancre4"></a>

##4. Ajout d'un nouvel Outil

Le procédé 'Orienté objet' du code de Gasbi permet un ajout simple d'un nouvel outil suivant ces quelques étapes:

1. Mettre à jour le fichier de configuration avec les options du nouvel Outil.
2. Ajouter l'outil à la liste TOOLS_LIST de la classe Constant.
3. Créer la classe correspondant à votre outil et la classe intermédiaire de votre outil si nécessaire.

[remonter](#sommaire)

---

<a id="ancre5"></a>

##5. Conventions

Le code a été écrit suivant les normes PEP8 et PEP257.

[remonter](#sommaire)