import datetime, sys, os
def get_building_handles(state):
    global srfPairs, allHandles
    if not highRiseBool:
        srfPairs = {
            "Front-1": "Back-1",
            "Back-1": "Front-1",
            "Left-1": "Right-1",
            "Right-1": "Left-1",
        }
    else:
        srfPairs = {
            "Surface 302": "Surface 326",
            "Surface 326": "Surface 302",
            "Surface 310": "Surface 314",
            "Surface 314": "Surface 310",
        }
    allHandles = {}
    allHandles['sensor'] = {}
    allHandles['actuator'] = {}
    for key in srfPairs.keys():
        allHandles['sensor'][key] = ep_api.exchange.get_variable_handle(state,
                                                                         "Surface Outside Face Temperature",
                                                                         key)
        allHandles['actuator'][key] = ep_api.exchange.get_actuator_handle(state,
        "Schedule:Compact", "Schedule Value", f"Srf-{key}-Tmp")
        # if any of the handles are invalid, raise an exception
        _hdlst = [allHandles['sensor'][key], allHandles['actuator'][key]]
        if any([x < 0 for x in _hdlst]):
            raise Exception("Error: Invalid handle for surface: "+key)
    
    allHandles['sensor']['oat'] = ep_api.exchange.get_variable_handle(state,"Site Outdoor Air Drybulb Temperature",
                                                                             "Environment")

def get_sensor_value(state):
    time_in_hours = ep_api.exchange.current_sim_time(state)
    _readable_time = datetime.timedelta(hours=time_in_hours)
    print('Time: ', _readable_time)
    sensor_values = {}
    for key in srfPairs.keys():
        sensor_values[key] = ep_api.exchange.get_variable_value(state, allHandles['sensor'][key])
    sensor_values['oat'] = ep_api.exchange.get_variable_value(state, allHandles['sensor']['oat'])
    return sensor_values

def set_actuators(state, to_set):
    for key in srfPairs.keys():
        if lwrBool:
            ep_api.exchange.set_actuator_value(state, allHandles['actuator'][key], to_set[key])
        else:
            ep_api.exchange.set_actuator_value(state, allHandles['actuator'][key], to_set['oat'])
def request_variables(state):
    ep_api.exchange.request_variable(state, "Site Outdoor Air Drybulb Temperature", "ENVIRONMENT")
    ep_api.exchange.request_variable(state, "Site Outdoor Air Humidity Ratio", "ENVIRONMENT")
def api_to_csv(state):
    orig = ep_api.exchange.list_available_api_data_csv(state)
    newFileByteArray = bytearray(orig)
    api_path = os.path.join(os.path.dirname(__file__), 'api_data.csv')
    newFile = open(api_path, "wb")
    newFile.write(newFileByteArray)
    newFile.close()
def timeStepHandler(state):
    global get_handle_bool
    if not get_handle_bool:
        get_building_handles(state)
        get_handle_bool = True
        # api_to_csv(state)
    warm_up = ep_api.exchange.warmup_flag(state)
    if not warm_up:
        sensor_values = get_sensor_value(state)
        print(sensor_values)
        set_actuators(state, sensor_values)
def init():
    sys.path.insert(0, '/usr/local/EnergyPlus-23-1-0/')
    sys.path.insert(0, 'C:/EnergyPlusV23-1-0')
    from pyenergyplus.api import EnergyPlusAPI
    global ep_api, get_handle_bool
    get_handle_bool = False
    ep_api = EnergyPlusAPI()
    state = ep_api.state_manager.new_state()
    ep_api.runtime.callback_begin_zone_timestep_before_set_current_weather(state, timeStepHandler)
    request_variables(state)
    return state

def main():
    state = init()
    weather_file_path = os.path.join("resources", "USA_CA_Hawthorne-Jack.Northrop.Field.722956_TMY3.epw")
    weather_file_path = os.path.join("resources", "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")
    if lwrBool:
        output_path = f"./{idfBase}-ep_trivial-LWR-True"
        idfFilePath = os.path.join("resources", idfBase+".idf")
    else:
        output_path = f"./{idfBase}-ep_trivial-LWR-False"
        idfFilePath = os.path.join("resources", idfBase+"-NoLWR.idf")
    sys_args = '-d', output_path, '-w', weather_file_path, idfFilePath
    ep_api.runtime.run_energyplus(state, sys_args)

if __name__ == '__main__':
    global lwrBool, highRiseBool, idfBase
    lwrBool = True
    highRiseBool = True
    if highRiseBool:
        idfBase = "Scalar_Simplified_HighOffice"
    else:
        idfBase = "5ZoneAirCooled"
    main()
