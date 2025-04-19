from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- MySQL Configuration ----------
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'WordleProject'

mysql = MySQL(app)

# --------------------------
# A - Gestion des joueurs
# --------------------------

@app.route('/gamers/<joueur>', methods=['GET'])
def get_gamer(joueur):
    """
    Retourne les infos du joueur : login, parties jouées, gagnées, score, dernière connexion
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT login, games_played, games_won, score, last_login 
        FROM users WHERE login = %s
    """, (joueur,))
    row = cur.fetchone()
    cur.close()

    if row:
        return jsonify({
            'login': row[0],
            'games_played': row[1],
            'games_won': row[2],
            'score': row[3],
            'last_login': row[4].isoformat() if row[4] else None
        })
    else:
        return jsonify({'error': f'Utilisateur "{joueur}" non trouvé'}), 404

@app.route('/gamers/add/<joueur>/<pwd>', methods=['POST'])
def add_gamer(joueur, pwd):
    """
    Ajoute un joueur s'il n'existe pas, sinon retourne une erreur
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE login = %s", (joueur,))
    if cur.fetchone():
        cur.close()
        return jsonify({'error': 'Utilisateur déjà existant'}), 400

    cur.execute("""
        INSERT INTO users (login, password, last_login)
        VALUES (%s, %s, %s)
    """, (joueur, pwd, datetime.now()))
    mysql.connection.commit()

    cur.execute("SELECT id FROM users WHERE login = %s", (joueur,))
    new_id = cur.fetchone()[0]
    cur.close()

    return jsonify({'id': new_id})

@app.route('/gamers/login/<joueur>/<pwd>', methods=['POST'])
def login_gamer(joueur, pwd):
    """
    Connexion : met à jour la date de dernière connexion si mot de passe correct
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id FROM users WHERE login = %s AND password = %s
    """, (joueur, pwd))
    user = cur.fetchone()

    if user:
        cur.execute("UPDATE users SET last_login = %s WHERE id = %s", (datetime.now(), user[0]))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Connexion réussie'})
    else:
        cur.close()
        return jsonify({'error': 'Identifiants invalides'}), 401

@app.route('/gamers/logout/<joueur>/<pwd>', methods=['POST'])
def logout_gamer(joueur, pwd):
    """
    Déconnexion : valide simplement les identifiants
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE login = %s AND password = %s", (joueur, pwd))
    if cur.fetchone():
        cur.close()
        return jsonify({'message': 'Déconnexion réussie'})
    else:
        cur.close()
        return jsonify({'error': 'Identifiants invalides'}), 401
    
# -------------------------
# B - Consultation admin
# -------------------------

@app.route('/admin/top', defaults={'nb': 10}, methods=['GET'])
@app.route('/admin/top/<int:nb>', methods=['GET'])
def get_top_players(nb):
    """
    Retourne les <nb> meilleurs joueurs triés par score décroissant.
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT login, score 
        FROM users 
        ORDER BY score DESC 
        LIMIT %s
    """, (nb,))
    rows = cur.fetchall()
    cur.close()

    result = [{'login': row[0], 'score': row[1]} for row in rows]
    return jsonify(result)

@app.route('/admin/delete/joueur/<joueur>', methods=['DELETE'])
def delete_joueur(joueur):
    """
    Supprime le joueur donné s'il existe et retourne son id.
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE login = %s", (joueur,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({'error': f'Joueur "{joueur}" introuvable'}), 404

    user_id = row[0]
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'deleted_user_id': user_id})

@app.route('/admin/delete/def/<int:def_id>', methods=['DELETE'])
def delete_definition(def_id):
    """
    Supprime la définition spécifiée par son id.
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM definitions WHERE id = %s", (def_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({'error': f'Définition id={def_id} introuvable'}), 404

    cur.execute("DELETE FROM definitions WHERE id = %s", (def_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'deleted_definition_id': def_id})

# -----------------------------------
# C - Consultation des définitions
# ----------------------------------

@app.route('/word', defaults={'nb': 10, 'from_idx': 1}, methods=['GET'])
@app.route('/word/<int:nb>', defaults={'from_idx': 1}, methods=['GET'])
@app.route('/word/<int:nb>/<int:from_idx>', methods=['GET'])
def get_definitions(nb, from_idx):
    """
    Retourne un JSON avec <nb> mots à partir de l'ID >= <from_idx>.
    Pour chaque mot : word, id, def (liste de définitions).
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, word, definition 
        FROM definitions 
        WHERE id >= %s 
        ORDER BY id 
        LIMIT %s
    """, (from_idx, nb))
    rows = cur.fetchall()
    cur.close()

    # Grouper par mot
    result = {}
    for def_id, word, definition in rows:
        if word not in result:
            result[word] = {'id': def_id, 'def': []}
        result[word]['def'].append(definition)

    # Convertir en liste
    return jsonify(list(result.values()))

# -----------------------------------
# D - Page Web
# ----------------------------------

# ---------- Run server ----------
if __name__ == '__main__':
    app.run(debug=True)
