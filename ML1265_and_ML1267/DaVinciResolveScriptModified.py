#! /usr/bin/env python

import sys
import imp
import os

# This is a minimally modified BlackMagic Resolve API loader for
# external scripting in Resolve Studio.
# Igor Ridanovic www.metafide.com

def get_resolve():

    script_module = None
    try:
        import fusionscript as script_module
    except ImportError:
        # Look for installer based environment variables:
        import os
        lib_path=os.getenv('RESOLVE_SCRIPT_LIB')
        if lib_path:
            try:
                script_module = imp.load_dynamic('fusionscript', lib_path)
            except ImportError:
                pass
        if not script_module:
            # Look for default install locations:
            ext='.so'
            if sys.platform.startswith('darwin'):
                path = '/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/'
            elif sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
                ext = '.dll'
                path = 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\'
            elif sys.platform.startswith('linux'):
                path = '/opt/resolve/libs/Fusion/'

            try:
                script_module = imp.load_dynamic('fusionscript', path + 'fusionscript' + ext)
            except ImportError:
                pass

    if script_module:
        sys.modules[__name__] = script_module

        # Added these two lines.
        resolve = script_module.scriptapp('Resolve')
        return resolve

    else:
        raise ImportError('Could not locate module dependencies')


if __name__ == '__main__':
    # This is how we make a resolve instance.
    resolve = get_resolve()

    # Tnen we can test if it works. Print the current project name.
    projectManager = resolve.GetProjectManager()
    currentProject = projectManager.GetCurrentProject()
    print(currentProject.GetName())
