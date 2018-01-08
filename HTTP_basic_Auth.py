from flask.ext.httpauth import HTTPBasicAuth # For HTTP basic auth

users = {
    "vorovik": "python123",
    "susan": "bye"
}

def auths():
    auth = HTTPBasicAuth()
    @auth.get_password
    def get_pw(username):
        if username in users:
            return users.get(username)
        return None
    return auth

auth =auths()
