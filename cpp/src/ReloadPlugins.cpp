// Downloaded from https://developer.x-plane.com/code-sample/reloadplugins/


/*
	Reload Plugin
	Written by Sandy Barbour - 24/02/2004

	This examples shows how reload plugins
	This is handy for debugging as you don't have to stop XPlane
*/

#if IBM
#include <windows.h>
#endif
#include <string.h>
#include <stdio.h>

#include "XPLMPlugin.h"
#include "XPLMMenus.h"

static void ReloadPluginsMenuHandler(void * mRef, void * iRef);

/*
 * XPluginStart
 * 
 * Our start routine registers our window and does any other initialization we 
 * must do.
 * 
 */
PLUGIN_API int XPluginStart(
                        char * outName,
                        char * outSig,
                        char * outDesc)
{
	/* First we must fill in the passed in buffers to describe our
	 * plugin to the plugin-system. */
	XPLMMenuID id;
	int	item;

	strcpy(outName, "ReloadPlugins");
	strcpy(outSig, "xplanesdk.sandybarbour.ReloadPlugins");
	strcpy(outDesc, "A plugin that allows plugins to be reloaded.");
			
	item = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "ReloadPlugins", NULL, 1);

	id = XPLMCreateMenu("ReloadPlugins", XPLMFindPluginsMenu(), item, ReloadPluginsMenuHandler, NULL);
	XPLMAppendMenuItem(id, "Reload", (void *)"Reload plugins",1);

	/* We must return 1 to indicate successful initialization, otherwise we
	 * will not be called back again. */
	 
	return 1;
}

/*
 * XPluginStop
 * 
 * Our cleanup routine deallocates our window.
 * 
 */
PLUGIN_API void	XPluginStop(void)
{
}

/*
 * XPluginDisable
 * 
 * We do not need to do anything when we are disabled, but we must provide the handler.
 * 
 */
PLUGIN_API void XPluginDisable(void)
{
}

/*
 * XPluginEnable.
 * 
 * We don't do any enable-specific initialization, but we must return 1 to indicate
 * that we may be enabled at this time.
 * 
 */
PLUGIN_API int XPluginEnable(void)
{
	return 1;
}

/*
 * XPluginReceiveMessage
 * 
 * We don't have to do anything in our receive message handler, but we must provide one.
 * 
 */
PLUGIN_API void XPluginReceiveMessage(
                    XPLMPluginID inFromWho,
                    int          inMessage,
                    void *       inParam)
{
}


void ReloadPluginsMenuHandler(void * mRef, void * iRef)
{
	if (!strcmp((char *) iRef, "Reload plugins"))
	{
        XPLMReloadPlugins();
	}
}


