


class WebGetException(Exception):
	pass

class ContentTypeError(WebGetException):
	pass

class ArgumentError(WebGetException):
	pass

class FetchFailureError(WebGetException):
	pass


# Specialized exceptions for garbage site
# "protection" bullshit
class GarbageSiteWrapper(WebGetException):
	pass
class CloudFlareWrapper(GarbageSiteWrapper):
	pass
class SucuriWrapper(GarbageSiteWrapper):
	pass

