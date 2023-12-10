import sqlite3

connection = sqlite3.connect('TBHL.db', check_same_thread=False)
cursor = connection.cursor()
def CreateTables():
    agence_query = '''
    CREATE TABLE IF NOT EXISTS Agence(
        AgenceID INTEGER PRIMARY KEY AUTOINCREMENT,
        Adresse TEXT NOT NULL
    )
    '''
    cursor.execute(agence_query)
    chauffeur_query = '''
    CREATE TABLE IF NOT EXISTS Chauffeur(
        ChauffeurID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT NOT NULL,
        Prenom TEXT NOT NULL,
        Telephone INTEGER NOT NULL,
        Email TEXT NOT NULL,
        AgenceID INTEGER NOT NULL,
        FOREIGN KEY(AgenceID) REFERENCES Agence(AgenceID)
    )
    '''
    cursor.execute(chauffeur_query)
    type_query = '''
    CREATE TABLE IF NOT EXISTS Type(
        TypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Marque TEXT NOT NULL,
        Modele TEXT NOT NULL
    )
    '''
    cursor.execute(type_query)
    vehicule_query = '''
    CREATE TABLE IF NOT EXISTS Vehicule(
        VehiculeID INTEGER PRIMARY KEY AUTOINCREMENT,
        TypeID INTEGER NOT NULL,
        Immatriculation TEXT NOT NULL,
        DateAchat TEXT NOT NULL,
    )
    '''
    cursor.execute(vehicule_query)
    mission_query = '''
    CREATE TABLE IF NOT EXISTS Mission(
        MissionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT NOT NULL,
        HeureDebut TEXT NOT NULL,
        HeureFin TEXT NOT NULL,
        ChauffeurID INTEGER NOT NULL,
        VehiculeID INTEGER NOT NULL
    )
    '''
    cursor.execute(mission_query)
    revision_query = '''
    CREATE TABLE IF NOT EXISTS Revision(
        RevisionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT NOT NULL,
        Type TEXT NOT NULL,
        VehiculeID INTEGER NOT NULL,
        FOREIGN KEY(VehiculeID) REFERENCES Vehicule(VehiculeID)
    )
    '''
    cursor.execute(revision_query)
    connection.commit()

    def DeleteFromAgence(adress):
        cursor.execute('DELETE FROM Agence WHERE Adress = ?',[adress])
        connection.commit()

    def UpdateFromAgence(old_adress,new_adress):
        cursor.execute('UPDATE Agence SET Adress = ? WHERE Adress = ?',[old_adress,new_adress])
        connection.commit()

    def DeleteFromChauffeur(var,val):
        cursor.execute('DELETE FROM Chauffeur WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def UpdateFromChauffeur(var,val):
        cursor.execute('UPDATE Chauffeur SET {var} = ? WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def DeleteFromVehicule(var,val):
        cursor.execute('DELETE FROM Vehicule WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def UpdateFromChauffeur(var,val):
        cursor.execute('UPDATE Chauffeur SET {var} = ? WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def DeleteFromMission(var,val):
        cursor.execute('DELETE FROM Mission WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def UpdateFromMission(var,val):
        cursor.execute('UPDATE Mission SET {var} = ? WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()

    def InsertIntoRevision(Date,Type,VehiculeID):
        cursor.execute('INSERT INTO Revision(Date,Type,VehiculeID) VALUES(?,?,?)',[Date,Type,VehiculeID])
        connection.commit()

    def DeleteFromRevision(var,val):
        cursor.execute('DELETE FROM Revision WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()
        
    def UpdateFromRevision(var,val):
        cursor.execute('UPDATE Revision SET {var} = ? WHERE {var} = {val}'.format(var=var,val=val))
        connection.commit()
        