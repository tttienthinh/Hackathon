---
title: Notre équipe 19 lors du Hi Hackathon
author: TRAN-THUONG Tien-Thinh
abstract: Dans notre équipe 19, nous sommes parti sur différents algorithmes. Il s'est avéré que XGBoost a été la meilleure solution. Pour ma part j'ai travaillé sur les réseaux de neurones avec les modules Tensorflow et Keras.  
geometry: margin=1cm
---

## Description de ce que j'ai fait
J'ai tout d'abord fait du pré-processing sur les données, avec l'ensemble de l'équipe, nous avons discuté des variables les plus utiles et comment nous allions supprimer les outliers. J'ai pu apprendre à utiliser le $z-score$.  
Puis j'ai appliqué mon réseau de neurones directement sur mes données numériques, avec un résultat d'$explained\textunderscore variance\textunderscore score$ de $51\%$.  

## Ce que j'ai fait pour aller plus loin
J'ai réalisé un modèle que je n'ai pas pû entrainer jusqu'au bout par manque de temps. Permettez-moi de vous le présenter tout de même.  
![Schéma des 3 étapes d'entraînement du modèle](Schéma.png)  

La difficulté que j'ai repérée dans la base de données était le mélange entre données _numérique_ et _catégorisées_ ainsi que la quantité importante des données. J'ai donc entrainé deux modèles séparément, le premier sur les _données numériques_ sur le modèle d'une régression linéaire, et le second sur les _données catégorisées_ suivant le modèle d'_Encoder-Decoder_.  
Une fois les deux modèles entrainés, je retire les couches après la couche de neurones _vertes_ sur le schéma. Je suppose alors que les couches de neurones devant la couche de neurones _vertes_ ont une bonne compréhension des données en entrées. Je n'ai alors qu'à utiliser leurs sorties telles quelles et entrainer les deux dernières couches de neurones à prédire la consommation annuelle.  

En procédant ainsi, j'ai pu réduire le nombre de paramètres à entrainer à chaque fois et j'ai également séparé le traitement des données  _numérique_ et _catégorisées_.