#Pip Install pywhatkit

import pywhatkit

def sendwhatsapp(contact_number, vehicle_num, slot_number):
    pywhatkit.sendwhatmsg_instantly(contact_number,          #All variables must be of String type
    "Dear faculty, You have entered college premise with vehicle number: " + " "
    + vehicle_num + " " + "have been assigned the parking slot number" + " " + slot_number,
    15, 
    True)