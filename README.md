# Projet_Graphe

L’ensemble des codes Python ayant étés nécessaires dans le cadre de la réduction de cette étude est disponible sur GitHub:
https://github.com/Sabsten/Projet_Graphe

# Contexte : 
L'un des enjeux principaux de notre époque, dans le but d'endiguer le phénomène de dérèglement climatique, sera de trouver des axes d’amélioration en ce qui concerne nos consommations d’énergie. Si certains domaines ont déjà entamés cette transition (maisons connectées avec optimisation du chauffage et de l’éclairage, véhicules électriques, réduction des déchets de l’industrie et de l’alimentaire, …), les scientifiques s’accordent à dire que ces efforts demeureront insuffisants. Il est primordial que les entreprises, les institutions et les individus acceptent de faire évoluer leurs habitudes et leur comportement afin de participer à cet effort commun. L’un des axes d’améliorations rapidement identifié est bien entendu l’optimisation des modes de transport et leurs performances en terme de temps et distance parcourue. 

Imminent acteur de ce secteur, l’ADEME (Agence de l’Environnement et de la Maîtrise de l’Energie) a dernièrement lancé un appel à manifestation d’intérêt (un mode de présélection des candidats qui seront invités à soumissionner lors de futures procédures de passation de marchés publics) dans le cadre d’un projet de réalisation de démonstrateurs et d’expérimentations de solutions de mobilité. Ces solutions pourront concerner tout aussi bien le transport de personnes mais également de marchandises, et devrons être applicables sur différents types de territoires.

Notre entreprise CesiCDP, composée de 5 personnes (Paul CALIMACHE, Sébastien CROUZET, Rabie HAMADOUCHE, Djilali OUADAH et Pierre YRIARTE) dispose d’ores et déjà de solides connaissances métiers concernant le domaine du transport, ayant déjà réalisé plusieurs études sur le thème de la Mobilité Multimodale Intelligente. Nous souhaitons donc aujourd’hui répondre à l’appel de l’ADEME, dans l’espoir d’obtenir la réalisation de ce travail. Cela devrait nous permettre de conquérir de nouveaux marchés tout en obtenant des financements solides pour la continuité de notre activité.

Etant libre de présenter toute piste de solution permettant de solutionner les problématiques d’ADEME en matière de maîtrise de l’énergie, nous avons choisi d’orienter notre étude sur l’optimisation des tournées de livraison. La problématique que nous souhaiterions résoudre serait de calculer le trajet le plus cours pour un véhicule de livraison sur un réseau routier (contenant un sous-ensemble de villes) permettant de rallier toutes les villes et revenir à son point de départ. Cet appel à manifestation d’intérêt étant très concurrentiel, nous avons cependant besoin d’identifier et de résoudre également des contraintes plus complexes de la gestion des transports. Parmi les premières à nous venir à l’esprit, il y a bien entendu la prise en compte du trafic sur la route, mais également d’autres subtilités relatives aux métiers du transport (besoin d’un véhicule spécifique pour certains produit transportés, différents points de prélèvements en départ du trajet….). Notre objectif sera de couvrir un maximum de cas de figure afin d’être en mesure de satisfaire l’ADEME et remporter l’appel d’offre.

# Contraintes

Notre solution devra répondre à un ensemble de problématiques relatives à la génération et l’optimisation d’une tournée de livraison sur un réseau routier composé d’un ensemble de villes à parcourir. L’objectif sera d’obtenir des tournées de durée optimale, permettant aux livreurs de revenir à leur point de départ et terminer leur journée le plus tôt possible et ne pas déborder de leurs horaires de travail. 

Notre algorithme devra prendre plusieurs facteurs en compte. Le premier facteur que nous intégrerons dans notre algorithme sera la connaissance du trafic habituel sur les axes routiers reliant les villes concernées par la livraison. Ce dernier devra être pris en compte dans le calcul du trajet,  afin par exemple d’éviter un axe de courte distance mais étant très régulièrement saturé.  

De plus, afin de maximiser les chances que notre projet soit retenu par l’ADEME, nous avons décidé d’implémenter deux contraintes supplémentaires afin de valoriser notre savoir-faire. D’une part, nous gérerons également l’affluence des routes en direct : le trajet le plus court sera recalculé à chaque passage dans une ville, en prenant en compte le trafic actuellement présent sur les axes de circulation. Enfin, afin de rendre notre travail plus professionnel et adapté à des problématiques réalistes, nous avons prévu de gérer plusieurs véhicules de livraison en simultané. Cette possibilité engendre plusieurs fonctionnalités à mettre en place : l’affectation des colis/objets aux différents camions (certains camions ne peuvent pas transporter certaines marchandises), la gestion de la capacité maximale de stockage des camion, et cette possibilité engendre également une modification majeure dans le fonctionnement de l’optimisation de la tournée : là où nous aurions uniquement souhaité obtenir la tournée dont la durée de réalisation et la plus courte, nous chercherons désormais la tournée permettant le retour le moins tardif pour le dernier camion à rentrer au dépôt (le dépôt est le point de départ et de fin de la tournée).

En termes mathématiques, nos recherches répondront au problème du « VRP », ou « Vehicule Routing Problem » (problème des tournées de véhicules). Il s’agit d’une classe de problèmes de recherche opérationnelle et d’optimisation combinatoire. Il a pour objectif de déterminer les tournées d’une flotte de véhicules afin de livrer une liste de clients, ou bien réaliser des tournées d’intervention (maintenances, réparations, contrôles…). Le but final étant de minimiser le coût de livraison des biens. 

Ainsi, le problème suivant :
 
Sera résolu à partir d’un graphe similaire :
 


# Collaborateurs

Yriarte Pierre
Ouadah Djilali
Crouzet Sébastien
Hamadouche Rabie
Calimache Paul

