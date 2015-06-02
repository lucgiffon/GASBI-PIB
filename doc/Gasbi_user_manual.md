#Manuel d'utilisateur de Gasbi

---

<a id="sommaire"></a>

##Sommaire
1. [Qu'est-ce-que Gasbi](#ancre1)
2. [Prérequis](#ancre2)
3. [Installer les logiciels](#ancre3)
4. [Comprendre le fichier de configuration](#ancre4)
5. [Utiliser Gasbi](#ancre5)
6. [Comprendre l'organisation des fichiers de sortie](#ancre6)
7. [Comprendre le fichier de logs](#ancre6)
8. [Références](#ancre7)

---

<a id="ancre1"></a>

##1. Qu'est-ce-que Gasbi
Gasbi est un logiciel d'annotation automatique de génome mettant en scène plusieurs outils de recherche d'éléments génomique. 

* La recherche des 'Coding Sequences' (CDS) est assurée par les outils Glimmer3 et GeneMark.
* La recherche d'ARN de transfert (tRNA) est assurée par tRNAscan-SE.

La volonté de Gasbi est d'être utilisable pour n'importe quel génome d'organisme appartenant à la super-famille des *Proteobacteria*.

[remonter](#sommaire)

---

<a id="ancre2"></a>

##2. Prérequis
Pour utiliser Gasbi, vous devez etre sur un système d'exploitation Linux et avoir une version de Python ultérieure à Python3.0.
Le programme devrait fonctionner avec tout système Unix mais il a été uniquement testé avec Ubuntu14.04.

De plus, Gasbi fait appel aux logiciels suivants, qui doivent etre installés sur votre machine:

* Glimmer3
* GeneMark
* tRNAscan-SE 

[remonter](#sommaire)

---

<a id="ancre3"></a>

##3. Installer les logiciels
Pour que Gasbi puisse fonctionner, il faut que les logiciels qu'il utilise soient préalablement installés sur votre machine. Vous trouverez dans cette section:
    * des liens vers la documentation de chaque logiciel
    * des conseils pour organiser vos logiciels

Si vous ne savez pas où installer les logiciels, il est d'usage de créer un répertoire nommé bin dans votre répertoire home. Par exemple:

	mkdir /home/eric/bin

Ce répertoire devra contenir les fichiers exécutables des logiciels. Veillez à ce que ce répertoire soit compris dans la variable d'environnement $PATH de votre session:

*Note: Dans certaines distribution récentes de Linux, la variable d'environnement $PATH est mise à jour automatiquement lorsqu'un répertoire bin est détecté dans le home. Vous devrez peut-être redémarrer votre session pour le voir.*

	echo $PATH

 devrait retourner quelque chose avec:

	/home/eric/bin

si ce n'est pas le cas, vous pouvez modifier votre variable d'environnement $PATH avec par exemple:

	export PATH="$PATH":/home/eric/bin

**Attention**: Cette modification de la variable $PATH est temporaire, si vous souhaitez que votre répertoire bin perdure lors de vos prochaines session, il peut être judicieux d'ajouter cette ligne au fichier .profile présent dans votre répertoire home.

**Attention**: Il est possible que vousvouliez conserver les exécutables dans leur répertoire d'origine. Si tel est le cas, vous pouvez ajouter chacun des répertoires à la variable $PATH ou bien créer un lien virtuel de l'exécutable dans un répertoire présent dans le PATH:

	ln -s *fichier_source* *destination*

*Note: Veillez à ce que chaque programme que vous installez soit disponible depuis la console. Pour se faire, vous pouvez tenter une exécution manuelle de chaque programme ou bien tapez:*

	which *nom_de_l_executable*
  
*Ce qui devrait retourner le chemin pour atteindre l'executable.*

###Installation de Glimmer
Pour télécharger Glimmer, rendez-vous: [ici](https://ccb.jhu.edu/software/glimmer/).

Vous pouvez consulter la documentation officielle de Glimmer version 3.02: [ici](https://ccb.jhu.edu/software/glimmer/glim302notes.pdf).

###Installation de GeneMark
Pour télécharger GeneMark, rendez-vous: [ici](http://exon.gatech.edu/license_download.cgi) et téléchargez la version compatible avec votre système de 'GeneMark-ES / ET'.

Vous pouvez consulter la documentation officielle de GeneMark: [ici](http://www.genepro.com/Manuals/GM/Genemark_manual.aspx).

*Note: La section 'install' de la documentation officielle ne concerne que les détenteurs de la version CD-ROM de GeneMark. Vous trouverez des informations au sujet de l'installation sans CD-ROM dans le fichier compressé que vous avez téléchargé.*

###Installation de tRNAscan-SE
Pour télécharger tRNAscan-SE, rendez-vous: [ici](http://lowelab.ucsc.edu/tRNAscan-SE/).

Vous pouvez consulter la documentation officielle de tRNAscan-SE: [ici](http://lowelab.ucsc.edu/tRNAscan-SE/Manual/).

[remonter](#sommaire)

---

<a id="ancre4"></a>

##4. Comprendre le fichier de configuration
Dans le même répertoire que Gasbi (/.../GASBI-PIB/), vous trouverez un fichier appelé 'configuration_file'. C'est en modifiant ce fichier que vous pourrez modifier les paramètres de Gasbi.

Les lignes commençant par un '#' seront ignorées. Vous pouvez donc ajouter autant de commentaire que vous voulez, tant que chacune des ligne ajoutée commence par ce symbole suivi d'un espace.

Les options livrées par défaut sont celles qui ont été utilisées pour une utilisation de Gasbi dans le cadre de l'annotation d'un génome de *Pseudomonas aeruginosa*.

###Séparation des différents groupes d'outils
Les outils sont organisés en différents groupes:
* 'CDS Finding Tools'
* 'tRNA Finding Tools'
La séparation de ces groupes d''outils dans le fichier de configuration est faite grâce à la balise 'Group'.

###Séparation des différents outils
Les outils disponibles pour Gasbi sont les suivants:

* 'Glimmer'
* 'GeneMark'
* 'tRNAscan'

La séparation de ces outils dans le fichier de configuration est faite grâce à la balise 'Tool'.

###Séparation des sous-groupes d'options
Les options de chaque outil sont séparées en deux sous-groupes:

* 'Basic'
* 'Expert'

Les options dîtes 'Basic' correspondent aux options ne nécessitant pas de connaissance approfondie des outils et sont souvent nécessaires pour fournir une exécution de Gasbi adéquate au génome que vous étudiez.

Les options dîtes 'Expert' correspondent aux options nécessitant une certaine expertise des outils. Elles ne sont pas nécessaires pour une exécution élémentaire de Gasbi mais peuvent être utiles si jamais vous voulez affiner votre recherche. Dans le cas où vous ne savez pas quelle valeur associer à une option 'Expert', vous devriez laisser la valeur par défaut en tapant 'default'.

Vous trouverez une explication succincte des options 'Basic' dans le fichier de configuration mais pour plus d'informations, consultez la documentation officielle de chaque outil.

La séparation de ces sous-groupes d'options dans le fichier de configuration est faite grâce à la balise 'Subgroup'.

###Séparation des options
Lors de la lecture du fichier de configuration par Gasbi, toutes les lignes non-vides et constituées d'un ':' seront considérées comme des options potentielles. Cependant, veillez à ne pas ajouter de nouvelle ligne de ce type car chacune des options sera vérifiée avant l'exécution des outils. Veillez aussi à ne pas modifier le nom des options et à faire correspondre la valeur que vous spécifiez au type demandé.

###Options Générales
Les options définie comme 'générales' car utilisées par tous les outils sont regroupées au début du fichier de configuration dans la partie 'Group: General Options'.

####SEQUENCE_PATH:
L'option SEQUENCE_PATH doit être le chemin menant à la séquence du génome que vous souhaitez étudier. Cette séquence doit être au format FASTA.

####OUT_PATH:
L'option  OUT_PATH doit être le chemin menant au répertoire où vous désirez que les résultats soient stockés

####TAG:
L'option TAG doit être le nom que vous voulez donner à votre exécution du programme. Le répertoire de sortie prendra ce nom, tout comme les fichiers de résultats donnés par chacun des outils.

[remonter](#sommaire)

---

<a id="ancre5"></a>

##5. Utiliser Gasbi

Pour utiliser Gasbi, il vous suffit de vous placer dans le fichier source de Gasbi puis de lancer Gasbi avec python3:
	
	cd /.../GASBI-PIB/src/
	python3 Gasbi
  
###Changer de Fichier de Configuration
Pour utiliser un autre fichier de configuration que 'configuration_file', il faut que vous ouvriez le fichier Gasbi.py avec votre éditeur de texte préféré et que vous vous rendiez à la ligne 163 qui devrait être:

	config_file = 'configuration_file'
  
Ici, remplacez 'configuration_file' par le chemin d'accès au fichier de configuration que vous souhaitez utiliser. Si votre fichier de configuration personnel est situé dans votre répertoire Documents, cette ligne devrait ressembler à:

	config_file = '/home/eric/Documents/configuration_file_perso'
  
**Attention**: Si vous modifiez le fichier de configuration par défaut et qu'il ne fonctionne plus, vous trouverez un fichier de configuration valide dans le répertoire doc appelé 'configuration_file_default'. Veillez à ne **JAMAIS** modifier ce fichier de configuration. En théorie, il devrait être en lecture seule.

[remonter](#sommaire)

---

<a id="ancre6"></a>

##6. Comprendre les fichiers de sortie

###Organisation du répertoire de sorties

Le répertoire de sortie est spécifié par l'utilisateur.

Un répertoire portant le nom du 'TAG' spécifié par l'utilisateur sera crée. Ce répertoire contiendra les résultats de l'exécution de Gasbi.

Ce répertoire contiendra un sous-répertoire par outil lancé. Chacun de ces sous-répertoires contiendra les résultats de l'outil en question et les répertoires des outils préliminaires à son exécution.

Les fichiers de sortie produits par Gasbi sont stockés dans le répertoire de base.

###Structure des fichiers de sortie fournis par Gasbi

Les fichiers de sortie produits par Gasbi sont formatés en gff. Chaque ligne du fichier correspond à un résultat et chaque élément d'un résultat est séparé par une tabulation.

L'organisation des résultats est la suivante:

**Nom_du_genome outil type_de_resultat  id_du_resultat  position_start  position_stop score orientation conflit**

La colonne conflit indique s'il y a un conflit avec un autre résultat du fichier. Le nom spécifié à cette colonne se réfère à un autre résultat trouvé dont les positions se superposent avec le résultat de la ligne.

[remonter](#sommaire)

---

<a id="ancre7"></a>

##7. Comprendre le fichier de logs
Lors de chaque utilisation de Gasbi, un fichier caché .log situé dans le même répertoire que Gasbi (/.../GASBI-PIC/src/) est mis à jour avec les informations relatives à votre exécution. Chaque ligne de ce fichier devrait ressembler à:

	*date* :: *niveau_de_log* :: *information_associee*
  
Les différents niveaux de log sont:

0. CRITICAL: erreurs entrainant un arrêt immédiat du programme.
1. ERROR: erreurs entrainant un dysfonctionnement du programme.
2. WARNING: erreurs entrainant une perte de fonctionnalité du programme et pouvvant entrainer un résultat innatendu.
3. INFO: informations du déroulement du programme.
4. DEBUG: trace de chacune des étapes du programme. Ce niveau de log ne devrait être utilisé que dans le cadre d'une erreur dans l'exécution de Gasbi qui ne trouve pas de réponse conventionnelle.

Par défaut, le niveau de log est à 3, c'est à dire que les logs CRITICAL, ERROR, WARNING et INFO sont écrits.
Si vous souhaitez modifier le niveau de log, rendez-vous à la ligne 161 du fichier Gasbi.py et modifiez la valeur de la ligne:

    verbosity = *valeur_voulue*


[remonter](#sommaire)

---

<a id="ancre8"></a>

##8. Références

###Glimmer
* S. Salzberg, A. Delcher, S. Kasif, and O. White. Microbial gene identification using interpolated Markov models, Nucleic Acids Research 26:2 (1998), 544-548.
* A.L. Delcher, D. Harmon, S. Kasif, O. White, and S.L. Salzberg. Improved microbial gene identification with GLIMMER, Nucleic Acids Research 27:23 (1999), 4636-4641.
* A.L. Delcher, K.A. Bratke, E.C. Powers, and S.L. Salzberg. Identifying bacterial genes and endosymbiont DNA with Glimmer, Bioinformatics 23:6 (2007), 673-679.

###GeneMark
* Borodovsky, M., and McIninch, J. D. (1993) "GeneMark: Parallel gene recognition for both DNA strands," Comp. Chem., 17, pp. 123-133

###tRNAscan
* Fichant, G.A. and Burks, C. (1991) ``Identifying potential tRNA genes in genomic DNA sequences'', J. Mol. Biol., 220, 659-671.
* Eddy, S.R. and Durbin, R. (1994) ``RNA sequence analysis using covariance models'', Nucl. Acids Res., 22, 2079-2088.
* Pavesi, A., Conterio, F., Bolchi, A., Dieci, G., Ottonello, S. (1994) ``Identification of new eukaryotic tRNA genes in genomic DNA databases by a multistep weight matrix analysis of transcriptional control regions'', Nucl. Acids Res., 22, 1247-1256.
* Lowe, T.M. & Eddy, S.R. (1997) ``tRNAscan-SE: a program for improved detection of transfer RNA genes in genomic sequence'', Nucl. Acids Res., 25, 955-964. 

[remonter](#sommaire)
