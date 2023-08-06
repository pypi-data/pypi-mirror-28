=====
Usage
=====

To use jamf Pro API in a project::

    from jssapi import JSSApi

    """Initialize the api with your credentials"""
    api = JSSApi(url=JSS_URL, user=JSS_USER, pwd=JSS_PASS, dbhost=JSS_DB_HOST,
    db=JSS_DB_DB, dbuser=JSS_DB_USER, dbpasswd=JSS_DB_PASS)

    """Get all mobile devices and print their names"""
    devices = api.get(method='mobiledevices')

    for device in devices:
        print(device['name'])

    """Get device with ID #1 and print its name"""

    device = api.get(method='mobiledevices/id/1')
    print(device['location']['real_name'])


    """Set Wallpaper for device with ID #1"""
    import base64

    with open('temp.png',"rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    body = str("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_command><command>Wallpaper</command><wallpaper_setting>1</wallpaper_setting><wallpaper_content>") + \
           str(encoded_string) + \
           str("</wallpaper_content><mobile_devices><mobile_device><id>%s</id></mobile_device></mobile_devices></mobile_device_command>") % str(iid)
    api.post(method='mobiledevicecommands/command/Wallpaper',body=body)

