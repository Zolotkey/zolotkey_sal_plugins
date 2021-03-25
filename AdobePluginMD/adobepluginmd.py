import sal.plugin
from server.models import PluginScriptRow

class AdobePluginMD(sal.plugin.DetailPlugin):

    description = 'Installed Adobe Plugins MachineDetail'
    supported_os_familyies = [sal.plugin.OSFamilies.darwin]

    def get_context(self, machine, **kwargs):
        context = self.super_get_context(machine, **kwargs)
        context['tite'] = self.description
        Adobeplugins = {}
        for num in range(0,10):
            item = PluginScriptRow.objects.filter(
                    submission__machine=machine,
                    submission__plugin__exact='AdobePlugins',
                    pluginscript_name='plugin%s' %(num))
            try: 
                dataoutput = item.first().pluginscript_data
                line = dataoutput.split(":")
                pluginname = line[1]
                val = {}
                val["app"] = line[0]
                val["pluginname"] = line[1]
                val["enabled"] = line[2]
                pluginkey = 'Plugin%s' %(num)
            except (AttributeError, ValueError):
                val = None
                pluginkey = 'None'
            Adobeplugins[pluginkey] = val

        context["data"] = Adobeplugins
        return context
