#!/usr/local/sal/Python.framework/Versions/Current/bin/python3

import os
import subprocess
import re
import sal

EXCMDTOOL = '/usr/local/adobecmd/MacOS/ExManCmd'


def main():
    from os import path
    if path.exists(EXCMDTOOL):
        extensions = get_extensions()
    else:
        extensions = {}
    sal.add_plugin_results('AdobePlugins', extensions)

def get_installed_apps():
    cmd_ia = [f'{EXCMDTOOL}', '--list', 'all']
    try:
        installed_apps = subprocess.check_output(cmd_ia,text=True)
    except subprocess.CalledProcessError:
        installed_apps = ''
    
    installed_apps_list = [] 
    for line in installed_apps.splitlines():
        adobe_apps = re.search(r"(Photoshop|Illustrator).*", line)
        if adobe_apps:
            app_installed = adobe_apps.group(0)
            installed_apps_list.append(app_installed)

    return installed_apps_list


def get_extensions():
    installed_apps_list = get_installed_apps()
    
    extensions_installed = {}
    app_info = {}
    for app in installed_apps_list:
        cmd_ie = [f'{EXCMDTOOL}', '--list', f'{app}']
        try:
            installed_extensions_line = subprocess.check_output(cmd_ie, text=True).splitlines()[3:]
        except subprocess.CalledProcessError:
            installed_extensions_line = ''
        installed_extensions_line.remove('')
        if installed_extensions_line:
            for i,extension_line in enumerate(installed_extensions_line):
                extension_split = extension_line.split()
                
                enabled = (extension_split[0] == "Enabled")
                extension_name = extension_split[1]
                version = extension_split[2]
                 
                app_info['plugin%d'%i] = "%s : %s : %s : %s" %(app, extension_name, enabled, version)
    return app_info

if __name__ == "__main__":
    main()
