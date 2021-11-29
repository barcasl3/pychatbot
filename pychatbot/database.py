import mysql.connector
from mysql.connector import Error
from api_config import connection_config_dict
from months import monthsToNum


def get_szolgaltatas_ar(rovidites, idotartam, slot):
    try: 
        connection = mysql.connector.connect(**connection_config_dict)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * from szolgaltatasok where rovidites = '" + rovidites + "';")
            record = cursor.fetchone()
            if record != None and record[3] == 1:
                cursor.execute("select * from csomagok where rovidites = '" + rovidites + "';")
                adatok = cursor.fetchone()
                if adatok != None:
                    min_slot = adatok[3]
                    max_slot = adatok[4]
                    csomag_alapar = adatok[5]
                    ar_slotonkent = adatok[6]

                    if slot == -1: slot = min_slot

                    if(slot >= min_slot and slot <= max_slot and slot % 2 == 0):
                        szolg_ar = ((((slot - min_slot) / 2) * ar_slotonkent) + csomag_alapar) * idotartam
                        return szolg_ar
                    else:
                        return -1

                else:
                    return -1
            else:
                return -1
        
    except Error as e:
        print("Hiba történt a MySQL szerverhez való kapcsolódás során.", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_vps_ar(csomagnev):
    try: 
        connection = mysql.connector.connect(**connection_config_dict)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * from csomagok_vps where csomagnev = '" + csomagnev + "';")
            adatok = cursor.fetchone()
            if adatok != None:
                csomag_ara = adatok[2]
                return csomag_ara

            else:
                return -1
        
    except Error as e:
        print("Hiba történt a MySQL szerverhez való kapcsolódás során.", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_vps_adatok(csomagnev):
    try: 
        connection = mysql.connector.connect(**connection_config_dict)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * from csomagok_vps where csomagnev = '" + csomagnev + "';")
            adatok = cursor.fetchone()
            if adatok != None:
                csomag_ara = adatok[2]
                vcpu_magok = adatok[3]
                ram = adatok[4]
                ssd = adatok[5]
                ipv4 = adatok[6]

                vps_adatok = {
                    'csomag_ara': csomag_ara,
                    'vcpu_magok': vcpu_magok,
                    'ram': ram,
                    'ssd': ssd,
                    'ipv4': ipv4
                }
                return vps_adatok

            else:
                vps_adatok = {
                    'csomag_ara': -1,
                    'vcpu_magok': 0,
                    'ram': 0,
                    'ssd': 0,
                    'ipv4': 0
                }

                return vps_adatok
        
    except Error as e:
        print("Hiba történt a MySQL szerverhez való kapcsolódás során.", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
