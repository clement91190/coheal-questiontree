projectsmartdiagnostics
=======================
Cette partie du projet, consiste en : 
 
	- un script qui va générer les questions en crawlant des fichiers, ou urls pour construire en sortie une arborescence de questions. 

	- un server flask (faire le tuto sur http://flask.pocoo.org/) qui permet d'interagir directement pour medecins/étudiants qui vont nous aider dans le projet, afin qu'ils modifient les questions, ainsi que l'arborescence. 

La base de donée utilisée est mongodb et on va se servir de mongoengine (ORM) construit par dessus pymongo, tous les objets de la base de donnée, doivent donc hériter de Document

On mets dans ce google doc toutes les idées de d'architecture
https://docs.google.com/document/d/1hogmolg01Et5NvuGjuxNtgo-_J9qZXwtp3g524WG9dI/edit


