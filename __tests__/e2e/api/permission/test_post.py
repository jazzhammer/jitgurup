import psycopg2
import requests
from __tests__.e2e.api.endpoint import API_BASE_URL

def getUserPermissions(user):
    response = requests.get(f"{API_BASE_URL}/users/permission?user_id={user['id']}")
    permissionJson = response.json()
    assert permissionJson is not None

def getUser():
    from jitgurup.settings import DATABASES
    defaultDb = DATABASES['default']
    connection = psycopg2.connect(
        database=defaultDb['NAME'],
        host=defaultDb['HOST'],
        port=defaultDb['PORT'],
        user=defaultDb['USER']
    )
    cursor = connection.cursor()
    cursor.execute(f"select id from auth_user where username='jitguruadmin'")
    user_id = cursor.fetchone()
    response = requests.get(f"{API_BASE_URL}/users/{user_id[0]}")
    userJson = response.json()
    return userJson

def testAll():
    jitguruadmin = getUser()
    getUserPermissions(jitguruadmin)