CREATE DATABASE IF NOT EXISTS WordleProject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE WordleProject;

-- Table des gamers
CREATE TABLE IF NOT EXISTS gamers (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(50) NOT NULL UNIQUE,      -- Identifiant unique du joueur
    password VARCHAR(255) NOT NULL,            -- Mot de passe
    games_played INT DEFAULT 0,                -- Nombre de parties jouées
    games_won INT DEFAULT 0,                   -- Nombre de parties gagnées
    score INT DEFAULT 0,                       -- Score cumulé
    last_login DATETIME DEFAULT NULL           -- Date et heure de la dernière connexion
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table des définitions
CREATE TABLE IF NOT EXISTS definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    language VARCHAR(5) NOT NULL,              -- Langue du mot (ex : 'fr' ou 'en')
    source VARCHAR(100) NOT NULL,              -- Source de la définition (nom du fichier .puz ou autre)
    word VARCHAR(100) NOT NULL,                -- Le mot à trouver
    def_text TEXT NOT NULL                     -- L'indice/définition associé(e)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- exemple test dans la table definitions
INSERT INTO definitions (language, source, word, def_text) VALUES
   ('fr', 'moyenne80.puz', 'PEUREUSE', 'Qui n’aime pas dormir sans quelqu’un.'),
   ('fr', 'moyenne80.puz', 'OUI', 'Mot fatal.'),
   ('fr', 'moyenne80.puz', 'NID', 'Celui des amoureux est toujours chaud.');

