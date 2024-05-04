import requests
import json

#Common
#OP: Control (2: Reference system, 3: Control system)
#e_A002: p_01: Operation state after operation (00: Stop state, 01: Operation state)
#e_3003: p_2D: Control content (00: Start of operation, 01: Stop, 02: Change setting)
#e_3001: p_01: Driving mode (0000: blowing, 0100: heating, 0200: cooling, 0300: automatic, 0500: dehumidifying)

class Daikin:
    def __init__(self,address):
        self.url = "http://"+address+"/dsiot/multireq"
        print(self.url)
        exit

    def get_status(self):
        param_stat = '{"requests":[{"op":2, "to":"/dsiot/edge/adr_0100.dgc_status?filter=pv"}]}'
        r = requests.post(self.url, param_stat)
        data = r.json()
        self.temperature = int(json.dumps(data["responses"][0]["pc"]["pch"][2]["pch"][5]["pch"][0]["pv"]).strip('"'), 16) #Tempterature
        self.humidity = int(json.dumps(data["responses"][0]["pc"]["pch"][2]["pch"][5]["pch"][1]["pv"]).strip('"'), 16) #Humidity
        e_A002 = json.dumps(data["responses"][0]["pc"]["pch"][2]["pch"][3]["pch"][0]["pv"])
        p = {} #"p_**" of e_3001 is registered in the dictionary to make it easier to change the numerical value.

        for i in range(19):
            key = json.dumps(data["responses"][0]["pc"]["pch"][2]["pch"][14]["pch"][i]["pn"]).strip('"')
            val = json.dumps(data["responses"][0]["pc"]["pch"][2]["pch"][14]["pch"][i]["pv"])
            p[key] = val

        self.mode = "unknown"
        self.temperaturesp = 0
        match p["p_01"]:
            case '"0000"':
                self.mode = "fan_only"
            case '"0100"':
                self.mode = "heat"
                self.temperaturesp = int(p["p_03"].strip('"'), 16)/2
            case '"0200"':
                self.mode = "cool"
                self.temperaturesp = int(p["p_02"].strip('"'), 16)/2
            case '"0300"':
                self.mode = "auto"
                self.temperaturesp = int(p["p_1F"].strip('"'),16)
            case '"0500"':                
                self.mode = "dry"
        if e_A002[2] == '0': # Unit is turned off
            self.mode = "off"


#        state = e_A002[2]
#        mode = p["p_01"]
        coolingtemp_sp = int(p["p_02"].strip('"'), 16)/2
        heatingtemp_sp = int(p["p_03"].strip('"'), 16)/2
        #print("Mode:",mode, ", Temperature:", temperature,", Humidity:",humidity,", Cooling setpoint:",coolingtemp_sp," , Heating setpoint:",heatingtemp_sp)
