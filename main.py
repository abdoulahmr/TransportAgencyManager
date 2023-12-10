from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
import sqlite3

app = Flask(__name__)
app.secret_key = "test"
connection = sqlite3.connect('TBHL.db', check_same_thread=False)
cursor = connection.cursor()

@app.route("/")
def home():
    return render_template("home.html")

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

@app.route("/lists")
def lists():
    chauffeure_list = cursor.execute('SELECT * FROM Chauffeur').fetchall()
    #chauffeure_list_by_name = cursor.execute('SELECT * FROM Chauffeur GROUP BY Nom').fetchall()
    #mission_list = cursor.execute("SELECT * FROM Mission").fetchall()
    #mission_list_between = cursor.execute("SELECT * FROM Mission WHERE Date BETWEEN ? AND ?",[stdate,nddate]).fetchall() #define stdate,nddate
    #mission_list_by_days = cursor.execute('''SELECT Mission.*, Chauffeur.* 
    #                                                FROM Mission JOIN Chauffeur ON Mission.ChauffeurID = Chauffeur.ChauffeurID
    #                                                GEOUP BY Date''').fetchall()
    #mission_list_by_days_chauff = cursor.execute('''SELECT Mission.*, Chauffeur.* 
    #                                                FROM Mission JOIN Chauffeur ON Mission.ChauffeurID = Chauffeur.ChauffeurID
    #                                                GROUP BY Date,ChauffeurID''').fetchall()
    #mission_list_by_days_chauff_vih = cursor.execute('''SELECT Mission.*, Chauffeur.*, Vehicule.* FROM Mission 
    #                                                        JOIN Chauffeur ON Mission.ChauffeurID = Chauffeur.ChauffeurID
    #                                                        JOIN Vehicule ON Vehicule.ChauffeurID = Chauffeur.ChauffeurID
    #                                                        GROUP BY Date,ChauffeurID,VehiculeID''').fetchall()
    #agence_list =  cursor.execute('SELECT * FROM Agence').fetchall()
    #vehicule_list =  cursor.execute('SELECT * FROM Vehicule').fetchall()
    ##mission_list_from =  cursor.execute("SELECT * FROM Mission WHERE Date > ?",[datefrom]).fetchall()#define date
    ##mission_list_to =  cursor.execute("SELECT * FROM Mission WHERE Date < ?",[dateto]).fetchall()#define date
    #mission_list_by_chauff =  cursor.execute("SELECT * FROM Mission GROUP BY ChauffeurID").fetchall()
    #mission_list_by_vih =  cursor.execute('''SELECT Mission.*, Vehicule.* FROM Mission 
    #                                                JOIN Vehicule ON Vehicule.ChauffeurID = Chauffeur.ChauffeurID
    #                                                GROUP BY VehiculeID''').fetchall()
    #
    return render_template("lists.html"
                           ,chauffeure_list=chauffeure_list)

if __name__ == "__main__":
    app.run(debug=True)