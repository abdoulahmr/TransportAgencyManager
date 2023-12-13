from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "test"
connection = sqlite3.connect('TBHL.db', check_same_thread=False)
cursor = connection.cursor()

@app.route("/")
def home():
    agence_list = cursor.execute('SELECT * FROM Agence LIMIT 5').fetchall()
    chauffeure_list = cursor.execute('''SELECT Chauffeur.* ,Agence.Adresse
                                     FROM Agence
                                     JOIN  Chauffeur ON Chauffeur.AgenceID = Agence.AgenceID''').fetchall()
    vehicule_list = cursor.execute('''SELECT Vehicule.* ,Type.Marque, Type.Modele
                                   FROM Vehicule 
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID LIMIT 5''').fetchall()
    revision_list = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID LIMIT 5''').fetchall()
    mission_list = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                    Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                    Mission.* 
                                    FROM Mission
                                    JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                    JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                    JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    return render_template("home.html",agence_list=agence_list,chauffeure_list=chauffeure_list,
                            vehicule_list=vehicule_list,revision_list=revision_list,mission_list=mission_list)

@app.route("/agence",methods = ['GET' , 'POST'])
def agence():
    agence_list = cursor.execute('SELECT * FROM Agence').fetchall()
    if request.method == "POST":
        adress = request.form["adress"]
        cursor.execute('INSERT INTO Agence(Adresse) VALUES(?)',[adress])
        connection.commit()
        return redirect(url_for("agence"))
    return render_template("agencemanager.html",agence_list=agence_list)

@app.route('/agence/sup:<id>')
def deleteagence(id):
    cursor.execute("DELETE FROM Agence WHERE AgenceID = ?",[id])
    connection.commit()
    return redirect(url_for("agence"))

@app.route("/chauffeur",methods = ['GET' , 'POST'])
def chauffeur():
    agence_list = cursor.execute('SELECT * FROM Agence').fetchall()
    chauffeure_list = cursor.execute('''SELECT Chauffeur.* ,Agence.Adresse
                                     FROM Agence
                                     JOIN  Chauffeur ON Chauffeur.AgenceID = Agence.AgenceID''').fetchall()
    print(chauffeure_list)
    if request.method == "POST":
        nom = request.form['nom']
        prenom = request.form['prenom']
        telephone = request.form['telephone']
        email = request.form['email']
        agence = request.form['agence']
        cursor.execute('INSERT INTO Chauffeur(Nom,Prenom,Telephone,Email,AgenceID) VALUES(?,?,?,?,?)'
                        ,[nom,prenom,telephone,email,agence])
        connection.commit()
        return redirect(url_for('chauffeur'))
    return render_template("cheuffeurmanager.html",agence_list=agence_list,chauffeure_list=chauffeure_list)

@app.route('/chauffeur/sup:<id>')
def deletechauffeur(id):
    cursor.execute("DELETE FROM Chauffeur WHERE ChauffeurID = ?",[id])
    connection.commit()
    return redirect(url_for("agence"))

@app.route('/type',methods = ['GET' , 'POST'])
def type():
    modele_list = cursor.execute('SELECT * FROM Type').fetchall()
    if request.method == 'POST':
        marque = request.form['marque']
        modele = request.form['modele']
        cursor.execute('INSERT INTO Type(Marque,Modele) VALUES(?,?)',[marque,modele])
        connection.commit()
        return redirect(url_for('type'))
    return render_template("typemanager.html",modele_list=modele_list)

@app.route('/type/sup:<id>')
def deletetype(id):
    cursor.execute('DELETE FROM Type WHERE TypeID = ?',[id])
    connection.commit()
    return redirect(url_for('type'))

@app.route("/vehicule",methods = ['GET' , 'POST'])
def vehicule():
    modele_list = cursor.execute('SELECT * FROM Type').fetchall()
    vehicule_list = cursor.execute('''SELECT Vehicule.*, Type.* 
                                   FROM Vehicule
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    if request.method == "POST":
        immatriculation = request.form['immatriculation']
        date = request.form['dateachat']
        model = request.form['modele']
        cursor.execute('INSERT INTO Vehicule(TypeID,Immatriculation,DateAchat) VALUES(?,?,?)'
                        ,[model,immatriculation,date])
        connection.commit()
        return redirect(url_for('vehicule'))
    return render_template("vehiculemanager.html",vehicule_list=vehicule_list,modele_list=modele_list)

@app.route('/vehicule/sup:<id>')
def deletevehicule(id):
    cursor.execute('DELETE FROM Vehicule WHERE VehiculeID = ?',[id])
    connection.commit()
    return redirect(url_for('vehicule'))

@app.route("/mission",methods = ['GET' , 'POST'])
def mission():
    chauffeure_list = cursor.execute('SELECT * FROM Chauffeur').fetchall()
    vehicule_list = cursor.execute('SELECT * FROM Vehicule').fetchall()
    mission_list = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                    Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                    Mission.* 
                                    FROM Mission
                                    JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                    JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                    JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    if request.method == "POST":
        date = request.form['date']
        heurdebut = request.form['heurdebut']
        heurfin = request.form['heurfin']
        chauffeur = request.form['chauffeur']
        vehicule = request.form['vehicule']
        cursor.execute('INSERT INTO Mission(Date,HeureDebut,HeureFin,ChauffeurID,VehiculeID) VALUES(?,?,?,?,?)'
                        ,[date,heurdebut,heurfin,chauffeur,vehicule])
        connection.commit()
        return redirect(url_for('mission'))
    return render_template("missionmanager.html",chauffeure_list=chauffeure_list
                           ,vehicule_list=vehicule_list,mission_list=mission_list)

@app.route('/mission/sup:<id>')
def deletemission(id):
    cursor.execute('DELETE FROM Mission WHERE MissionID = ?',[id])
    connection.commit()
    return redirect(url_for('mission'))

@app.route("/revision",methods = ['GET' , 'POST'])
def revision():
    vehicule_list = cursor.execute('SELECT * FROM Vehicule').fetchall()
    revision_list = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    print(revision_list)
    if request.method == "POST":
        date = request.form['date']
        revtype = request.form['type']
        vehicule = request.form['vehicule']
        cursor.execute('INSERT INTO Revision(Date,Type,VehiculeID) VALUES(?,?,?)',[date,revtype,vehicule])
        connection.commit()
        return redirect(url_for("revision"))
    return render_template("revisionmanager.html",vehicule_list=vehicule_list,revision_list=revision_list)

@app.route('/revision/sup:<id>')
def deleterevision(id):
    cursor.execute('DELETE FROM Revision WHERE RevisionID = ?',[id])
    connection.commit()
    return redirect(url_for('revision'))

@app.route("/lists",methods = ['GET' , 'POST'])
def lists():
    chauffeure_list = cursor.execute('''SELECT Chauffeur.*, Agence.Adresse
                                FROM Chauffeur
                                JOIN Agence ON Chauffeur.AgenceID = Agence.AgenceID''').fetchall()
    chauffeure_list_by_name = cursor.execute('SELECT * FROM Chauffeur GROUP BY Nom').fetchall()
    mission_list = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                    Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                    Mission.* 
                                    FROM Mission
                                    JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                    JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                    JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    mission_list_between = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                    Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                    Mission.* 
                                    FROM Mission
                                    JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                    JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                    JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    mission_list_by_days = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                    Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                    Mission.* 
                                    FROM Mission
                                    JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                    JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                    JOIN Type ON Vehicule.TypeID = Type.TypeID
                                    GROUP BY Date''').fetchall()
    mission_list_by_days_chauff = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Date,Chauffeur.ChauffeurID''').fetchall()
    mission_list_by_days_chauff_vih = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Date,Chauffeur.ChauffeurID,Vehicule.VehiculeID''').fetchall()
    revision_list_betwen = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    agence_list = cursor.execute('SELECT * FROM Agence').fetchall()
    vehicule_list = cursor.execute('''
                                SELECT Type.Marque, Type.Modele, Vehicule.*
                                FROM Vehicule
                                JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    mission_list_from = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    mission_list_to = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID''').fetchall()
    mission_list_by_chauff = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Mission.ChauffeurID''').fetchall()
    mission_list_by_vih = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Mission.VehiculeID''').fetchall()
    mission_list_by_date_vih = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Mission.Date,Mission.VehiculeID''').fetchall()
    mission_list_by_chauf_vih = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        GROUP BY Mission.ChauffeurID,Mission.VehiculeID''').fetchall()
    revision_list = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    revision_list_from = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    revision_list_to = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                   FROM Revision
                                   JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                   JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    revision_list_between = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                    FROM Revision
                                    JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                    JOIN Type ON Type.TypeID = Vehicule.TypeID''').fetchall()
    revision_list_by_type = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                    FROM Revision
                                    JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                    JOIN Type ON Type.TypeID = Vehicule.TypeID
                                    GROUP BY Revision.Type''').fetchall()
    revision_list_by_vih = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                    FROM Revision
                                    JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                    JOIN Type ON Type.TypeID = Vehicule.TypeID
                                    GROUP BY Revision.VehiculeID''').fetchall()
    mission_agence_one = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        WHERE Chauffeur.AgenceID = 
                                            (SELECT AgenceID FROM Agence ORDER BY AgenceID LIMIT 1)''').fetchall()
    vehicule_list_no_revision = cursor.execute('''SELECT Vehicule.*, Type.Marque, Type.Modele
                                        FROM Vehicule
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        LEFT JOIN Revision ON Vehicule.VehiculeID = Revision.VehiculeID
                                        WHERE Revision.RevisionID IS NULL''').fetchall()
    chauffeure_list_no_mission = cursor.execute(''' SELECT Nom, Prenom
                                        FROM Chauffeur
                                        WHERE ChauffeurID NOT IN 
                                                (SELECT DISTINCT ChauffeurID FROM Mission)''').fetchall()
    chauffeure_list_by_mission_number = cursor.execute('''
                                        SELECT Chauffeur.Nom, Chauffeur.Prenom, COUNT(Mission.MissionID) AS TotalMissions
                                        FROM Chauffeur
                                        LEFT JOIN Mission ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        GROUP BY Chauffeur.ChauffeurID
                                        ORDER BY TotalMissions DESC''').fetchall()

    if request.method == "POST":
        stdate = request.form['stdate']
        nddate = request.form['nddate']
        datefrom = request.form['datefrom']
        dateto = request.form['dateto']
        mission_list_between = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        WHERE Date BETWEEN ? AND ?''',[stdate,nddate]).fetchall()
        mission_list_from = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        Mission.* 
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        WHERE Date >= ?''',[datefrom]).fetchall()
        mission_list_to = cursor.execute('''SELECT Chauffeur.Nom, Chauffeur.Prenom,
                                        Mission.* 
                                        Vehicule.Immatriculation, Type.Marque, Type.Modele,
                                        FROM Mission
                                        JOIN Chauffeur ON Chauffeur.ChauffeurID = Mission.ChauffeurID
                                        JOIN Vehicule ON Vehicule.VehiculeID = Mission.VehiculeID
                                        JOIN Type ON Vehicule.TypeID = Type.TypeID
                                        WHERE Date <= ?''',[dateto]).fetchall()
        revision_list_from = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                        FROM Revision
                                        JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                        JOIN Type ON Type.TypeID = Vehicule.TypeID
                                        WHERE Revision.Date < ?''',[datefrom]).fetchall()
        revision_list_to = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                        FROM Revision
                                        JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                        JOIN Type ON Type.TypeID = Vehicule.TypeID
                                        WHERE Revision.Date >= ?''',[dateto]).fetchall()
        revision_list_between = cursor.execute('''SELECT Revision.*, Vehicule.*, Type.* 
                                        FROM Revision
                                        JOIN Vehicule ON Vehicule.VehiculeID = Revision.VehiculeID
                                        JOIN Type ON Type.TypeID = Vehicule.TypeID
                                        WHERE Revision.Date BETWEEN ? AND ?''',[stdate,nddate]).fetchall()
    
    return render_template("lists.html",
                            chauffeure_list=chauffeure_list,chauffeure_list_by_name=chauffeure_list_by_name,
                            mission_list=mission_list,mission_list_between=mission_list_between,
                            mission_list_by_days=mission_list_by_days,mission_list_by_days_chauff=mission_list_by_days_chauff,
                            mission_list_by_days_chauff_vih=mission_list_by_days_chauff_vih,agence_list=agence_list,
                            vehicule_list=vehicule_list,mission_list_from=mission_list_from,
                            mission_list_to=mission_list_to,revision_list_betwen=revision_list_betwen,
                            mission_list_by_chauff=mission_list_by_chauff,mission_list_by_vih=mission_list_by_vih,
                            mission_list_by_date_vih=mission_list_by_date_vih,mission_list_by_chauf_vih=mission_list_by_chauf_vih,
                            revision_list=revision_list,revision_list_from=revision_list_from,
                            revision_list_to=revision_list_to,revision_list_between=revision_list_between,
                            revision_list_by_type=revision_list_by_type,revision_list_by_vih=revision_list_by_vih,
                            mission_agence_one=mission_agence_one,vehicule_list_no_revision=vehicule_list_no_revision,
                            chauffeure_list_no_mission=chauffeure_list_no_mission,
                            chauffeure_list_by_mission_number=chauffeure_list_by_mission_number)

if __name__ == "__main__":
    app.run(debug=True)