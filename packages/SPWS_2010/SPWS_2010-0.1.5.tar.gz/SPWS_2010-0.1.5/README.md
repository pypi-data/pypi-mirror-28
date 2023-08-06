# SPWS-2010
Python Interface to SharePoint 2010 Web Services

# Usage
## Setup
PARAMS = {
	"Site URL" : "",
	"Site Name" : "",
	"Authorize" : {
		"User" : "",
		"Password" : ""
	}
}

SITE = {
	"responseType" : 'Admin',
	"returnValue" : False,
	"Url" : '',
	"Title" : '',
	"Description" : '',
	"Lcid" : '',
	"WebTemplate" : '',
	"OwnerLogin" : '',
	"OwnerName" : '',
	"OwnerEmail" : '',
	"PortalUrl" : '',
	"PortalName" : ''
}

## Permissions
Permissions(PARAMS).execute("GetPermissionCollection", {'responseType' : 'Permissions','returnValue' : True,'objectName' : PARAMS['Site Name'],'objectType' : 'List'})

## Lists
Lists(PARAMS).execute("AddList", {'responseType' : 'Lists', 'returnValue' : False, 'listName' : '', 'description' : '', 'templateID' : TEMP_ID['Custom List in Datasheet View']})
Lists(PARAMS).execute("DeleteList", {'responseType' : 'Lists', 'returnValue' : False, 'listName' : ''})

## Sites
Sites(PARAMS).execute("GetSite", {'responseType' : 'Site', 'returnValue' : True, 'SiteUrl' : PARAMS['Site URL']})

## Versions
Versions(PARAMS).execute("GetVersions", {'responseType' : 'Version','returnValue' : True, 'fileName' : ''})

## Views
Views(PARAMS).execute("GetViewCollection", {'responseType' : 'View','returnValue' : True, 'listName' : ''})

## Webs
Webs(PARAMS).execute("GetWebCollection", {'responseType' : 'Web', 'returnValue' : True})

## Admin
Admin(PARAMS).execute("CreateSite", SITE)
