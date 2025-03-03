import os
import json
import uuid

def generate_uuid(search=None, replace=None, capitalize=False):
    if capitalize:
        return str(uuid.uuid4()).upper()
    if search and replace is not None:
        return str(uuid.uuid4()).replace(search, replace)
    return str(uuid.uuid4())

def ask_user():
    answer = input("Do you want to reset the Windsurf? (y/n): ")

    if answer == "y":
        reset_windsurf()
    
    return

def reset_windsurf():
    home = os.path.expanduser("~")

    windsurf = os.path.join(home, r'AppData\Roaming\Windsurf\User\globalStorage\storage.json')

    try:
        with open(windsurf, 'r', encoding="UTF-8") as f:
            data = json.load(f)

    except:
        print("Error: Windsurf not found")
        return
    
    # "telemetry.machineId": "187acf54cc71da2aa9bdab772214602e3edf5c459245ec132c41e960bd500ca3",
    # "telemetry.sqmId": "{0865FE45-0306-498C-86B1-1ED1125B1DF2}",
    # "telemetry.devDeviceId": "e395944e-d1d4-4bae-9776-fbf8b2c0bf50",

    data["telemetry.machineId"] = generate_uuid(search="-", replace="") + generate_uuid(search="-", replace="")
    data["telemetry.sqmId"] = "{" + generate_uuid(capitalize=True) + "}"
    data["telemetry.devDeviceId"] = generate_uuid()

    try:
        with open(windsurf, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            print("Windsurf reseted")
    except:
        print("Error: Reset interrupted")
        return

def main():
    print("Windsurf Resetter by OwPor\n")
    
    ask_user()

if __name__ == "__main__":
    main()