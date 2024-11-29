import subprocess

def get_wifi_passwords():
    # Get the list of saved Wi-Fi profiles
    profiles = subprocess.check_output("netsh wlan show profiles").decode("utf-8", errors="backslashreplace").split("\n")
    wifi_list = []
    
    # Extract the names of all Wi-Fi profiles
    for profile in profiles:
        if "All User Profile" in profile:
            profile_name = profile.split(":")[1][1:-1]
            wifi_list.append(profile_name)
    
    wifi_passwords = {}

    # Get the passwords for each profile
    for wifi in wifi_list:
        try:
            results = subprocess.check_output(f'netsh wlan show profile "{wifi}" key=clear', shell=True).decode("utf-8", errors="backslashreplace")
            # Extract the password from the results
            password_line = [line for line in results.split("\n") if "Key Content" in line]
            if password_line:
                password = password_line[0].split(":")[1][1:-1]
                wifi_passwords[wifi] = password
            else:
                wifi_passwords[wifi] = "No password set"
        except subprocess.CalledProcessError:
            wifi_passwords[wifi] = "Error retrieving password"
    
    return wifi_passwords

# Get the saved Wi-Fi passwords
passwords = get_wifi_passwords()

# Display the Wi-Fi names and passwords
for wifi, password in passwords.items():
    print(f"Wi-Fi: {wifi} | Password: {password}")
