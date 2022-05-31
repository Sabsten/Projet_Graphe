# Projet_Graphe

L’ensemble des codes Python ayant étés nécessaires dans le cadre de la réduction de cette étude est disponible sur GitHub:
https://github.com/Sabsten/Projet_Graphe

# Contexte : 
L'un des enjeux principaux de notre époque, dans le but d'endiguer le phénomène de dérèglement climatique, sera de trouver des axes d’amélioration en ce qui concerne nos consommations d’énergie. Si certains domaines ont déjà entamés cette transition (maisons connectées avec optimisation du chauffage et de l’éclairage, véhicules électriques, réduction des déchets de l’industrie et de l’alimentaire, …), les scientifiques s’accordent à dire que ces efforts demeureront insuffisants. Il est primordial que les entreprises, les institutions et les individus acceptent de faire évoluer leurs habitudes et leur comportement afin de participer à cet effort commun. L’un des axes d’améliorations rapidement identifié est bien entendu l’optimisation des modes de transport et leurs performances en terme de temps et distance parcourue. 

Imminent acteur de ce secteur, l’ADEME (Agence de l’Environnement et de la Maîtrise de l’Energie) a dernièrement lancé un appel à manifestation d’intérêt (un mode de présélection des candidats qui seront invités à soumissionner lors de futures procédures de passation de marchés publics) dans le cadre d’un projet de réalisation de démonstrateurs et d’expérimentations de solutions de mobilité. Ces solutions pourront concerner tout aussi bien le transport de personnes mais également de marchandises, et devrons être applicables sur différents types de territoires.

Notre entreprise CesiCDP, composée de 5 personnes (Paul CALIMACHE, Sébastien CROUZET, Rabie HAMADOUCHE, Djilali OUADAH et Pierre YRIARTE) dispose d’ores et déjà de solides connaissances métiers concernant le domaine du transport, ayant déjà réalisé plusieurs études sur le thème de la Mobilité Multimodale Intelligente. Nous souhaitons donc aujourd’hui répondre à l’appel de l’ADEME, dans l’espoir d’obtenir la réalisation de ce travail. Cela devrait nous permettre de conquérir de nouveaux marchés tout en obtenant des financements solides pour la continuité de notre activité.

Etant libre de présenter toute piste de solution permettant de solutionner les problématiques d’ADEME en matière de maîtrise de l’énergie, nous avons choisi d’orienter notre étude sur l’optimisation des tournées de livraison. La problématique que nous souhaiterions résoudre serait de calculer le trajet le plus cours pour un véhicule de livraison sur un réseau routier (contenant un sous-ensemble de villes) permettant de rallier toutes les villes et redevenir à son point départ. Cet appel à manifestation d’intérêt étant très concurrentiel, nous avons cependant besoin d’identifier et de résoudre également des contraintes plus complexes de la gestion des transports. Parmi les premières à nous venir à l’esprit, il y a bien entendu la prise en compte du trafic sur la route, mais également d’autres subtilités relatives aux métiers du transport (besoin d’un véhicule spécifique pour certains produit transportés, différents points de prélèvements en départ du trajet….). Notre objectif sera de couvrir un maximum de cas de figure afin d’être en mesure de satisfaire l’ADEME et remporter l’appel d’offre.

# Contraintes

Obligatoires : 
1/ Retour du camion au point de départ 

2/ Durée totale du trajet optimisée

3/ Prise en compte du traffic selon la plage horaire

Facultatives/Suggestions CESI : 

4/ Impossibilité de livrer certains colis sur certaines plages horaires (possibilité d'attendre sur place en attendant la bonne heure)

5/ Plusieurs camions disponibles en simultané 

  --> Affection des objets aux différents camions dispos 
  
  --> Minimiser la date de retour du dernier camion (et non le temps de trajet total)
  
  --> Capacité des camions (2 ou 3 dimensions, JE SAIS PAS CE QUE CA VEUT DIRE) et encombrement des camions 
  
  --> Certains objets ne peuvent pas être transités dans tous les camions 
  
6/ Chaque objet a un point de collecte spécifique

# Collaborateurs

Yriarte Pierre
Ouadah Djilali
Crouzet Sébastien
Hamadouche Rabie
Calimache Paul

