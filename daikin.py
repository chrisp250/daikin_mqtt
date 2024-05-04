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
        #print(data)
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
        self.p = p
        #print("Mode:",mode, ", Temperature:", temperature,", Humidity:",humidity,", Cooling setpoint:",coolingtemp_sp," , Heating setpoint:",heatingtemp_sp)


    #Process change of mode request
    def switch_mode(self,mode):
        p = self.p
        match mode:
            case "cool":
                e_3003 = '"00"' # Start command
                e_A002 = '"01"' # Running mode
                p["p_09"] = '"0A00"' #Auto fan speed
                p["p_01"] = '"0200"'
                print("AC Cool")
            case "dry":
                e_3003 = '"00"' # Start command
                e_A002 = '"01"' # Running mode
                p["p_01"] = '"0500"'
                print("AC Dry")
            case "heat":
                e_3003 = '"00"' # Start command
                e_A002 = '"01"' # Running mode
                p["p_01"] = '"0100"' #Heating mode
                p["p_0A"] = '"0A00"' #Auto fan speed
                #param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": '+e_A002+'}]},{"pn": "e_3003","pch": [{"pn": "p_2D","pv": '+e_3003+'}]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": '+p["p_01"]+'},{"pn": "p_03","pv": '+p["p_03"]+'},{"pn": "p_07","pv": '+p["p_07"]+'},{"pn": "p_08","pv": '+p["p_08"]+'},{"pn": "p_0A","pv": '+p["p_0A"]+'}]}]}]}}]}'
                #HA
                #param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": "01"      }]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": "0200"    },{"pn":"p_09","pv":"0500"},{"pn":"p_02","pv":"36"},{"pn":"p_05","pv":"0F0000"},{"pn":"p_06","pv":"000000"}]},{"pn":"e_3003","pch":[{"pn":"p_2D","pv":"00"}]}]}]}}]}'
                #r = requests.post(self.url, param)
                print("AC Heat")
            case "auto":
                print("AC Auto")
            case "fan_only":
                print("AC Fan Only")
            case "off":
                    e_A002 = '"00"'
                    e_3003 = '"01"' #Stop command
                    print("AC Off")

        match p["p_01"]:
            case '"0100"': #Heating mode
                self.decode_mode(e_A002,e_3003,p)
                param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": '+e_A002+'}]},{"pn": "e_3003","pch": [{"pn": "p_2D","pv": '+e_3003+'}]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": '+p["p_01"]+'},{"pn": "p_03","pv": '+p["p_03"]+'},{"pn": "p_07","pv": '+p["p_07"]+'},{"pn": "p_08","pv": '+p["p_08"]+'},{"pn": "p_0A","pv": '+p["p_0A"]+'}]}]}]}}]}'
            case '"0200"': #Cooling mode
                self.decode_mode(e_A002,e_3003,p)
                #Original
                #param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": '+e_A002+'}]},{"pn": "e_3003","pch": [{"pn": "p_2D","pv": '+e_3003+'}]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": '+p["p_01"]+'},{"pn": "p_02","pv": '+p["p_02"]+'},{"pn": "p_05","pv": '+p["p_05"]+'},{"pn": "p_06","pv": '+p["p_06"]+'},{"pn": "p_09","pv": '+p["p_09"]+'},{"pn": "p_0B","pv": '+p["p_0B"]+'},{"pn": "p_0C","pv": '+p["p_0C"]+'}]}]}]}}]}'
                # Modified
                #param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": '+e_A002+'}]},{"pn": "e_3003","pch": [{"pn": "p_2D","pv": '+e_3003+'}]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": '+p["p_01"]+'},{"pn": "p_02","pv": '+p["p_02"]+'},{"pn": "p_05","pv": '+p["p_05"]+'},{"pn": "p_06","pv": '+p["p_06"]+'},{"pn": "p_09","pv": '+p["p_09"]+'}]}]}]}}]}'
            case '"0500"': #Dehumidifier mode
                self.decode_mode(e_A002,e_3003,p)
                #param = '{"requests": [{"op": 3,"to": "/dsiot/edge/adr_0100.dgc_status","pc": {"pn": "dgc_status","pch": [{"pn": "e_1002","pch": [{"pn": "e_A002","pch": [{"pn": "p_01","pv": '+e_A002+'}]},{"pn": "e_3003","pch": [{"pn": "p_2D","pv": '+e_3003+'}]},{"pn": "e_3001","pch": [{"pn": "p_01","pv": '+p["p_01"]+'},{"pn": "p_22","pv": '+p["p_22"]+'},{"pn": "p_23","pv": '+p["p_23"]+'},{"pn": "p_27","pv": '+p["p_27"]+'},{"pn": "p_30","pv": '+p["p_30"]+'},{"pn": "p_31","pv": '+p["p_31"]+'}]}]}]}}]}'
            case _:
                print("Not there")
                return
        r = requests.post(self.url, param)

    # Decode Daikin command
    def decode_mode(self,e_A002,e_3003,p):
        match e_3003:
            case '"00"':
                print("Start command:", end = " ")
            case '"01"':
                print("Stop command:", end = " ")
            case '"02"':
                print("Change setting:", end = " ")
        
        match e_A002:
            case '"00"':
                print("Stopped", end = " ")
            case '"01"':
                print("Running", end = " ")

        match p["p_01"]:
            case '"0000"': #Fan mode
                print("/ Fan only mode")
            case '"0100"': #Heating mode
                print("/ Heater mode")
                print(p["p_03"],p["p_07"],p["p_08"],p["p_0A"])
            case '"0200"': #Cooling mode
                print("/ Cooling mode")
                print(p["p_02"],p["p_05"],p["p_06"],p["p_09"])
            case '"0300"':
                print("/ Auto mode")
            case '"0500"': #Dehumidifier mode
                print("/ Dehumidifier mode")
                print(p["p_22"],p["p_23"],p["p_27"])
