import csv
import json
from veza.oaa import VezaClient

# Initialize Veza client (replace with your API key and Veza URL)
veza_client = VezaClient(api_key="", base_url="https://lab-se.vezacloud.com")

# Define the custom application
app_name = "Dunder Mifflin Demo"
app = {
    "name": app_name,
    "application_type": "custom",
    "resources": [],
    "identities": [],
    "roles": [],
    "permissions": [],
    "identity_to_roles": [],
    "identity_to_permissions": [],
    "resource_to_permissions": []
}

# Read users
users = {}
with open("csv/users.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        users[row["name"]] = {
            "name": row["name"],
            "identity_type": "user",
            "email": row["email"],
            "department": row["department"]
        }
app["identities"] = list(users.values())

# Read roles
roles = set()
with open("csv/roles.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        roles.add(row["name"])
app["roles"] = [{"name": role} for role in roles]

# Read groups
groups = {}
with open("csv/groups.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        groups[row["name"]] = {
            "name": row["name"],
            "identity_type": "group",
            "identities": row["members"].split(",")
        }
app["identities"].extend(groups.values())

# Read user roles
identity_to_roles = []
with open("csv/user_roles.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        identity_to_roles.append({"identity": row["user"], "role": row["role"]})
app["identity_to_roles"] = identity_to_roles

# Read user groups (not directly used in Veza OAA payload but useful for validation)
with open("csv/user_groups.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pass  # Group memberships are already handled in groups.csv

# Define resources and permissions
resources = set()
permissions_set = set()
resource_to_permissions = {}
with open("csv/role_permissions.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        resources.add(row["resource"])
        permissions = row["permissions"].split(",")
        for perm in permissions:
            permissions_set.add(perm)
        if row["resource"] not in resource_to_permissions:
            resource_to_permissions[row["resource"]] = {}
        if row["role"] not in resource_to_permissions[row["resource"]]:
            resource_to_permissions[row["resource"]][row["role"]] = set()
        resource_to_permissions[row["resource"]][row["role"]].update(permissions)

app["resources"] = [{"name": resource, "resource_type": "system"} for resource in resources]
app["permissions"] = [{"name": perm, "description": f"{perm.capitalize()} access"} for perm in permissions_set]
app["resource_to_permissions"] = [
    {"resource": resource, "permissions": {role: list(perms) for role, perms in roles_perms.items()}}
    for resource, roles_perms in resource_to_permissions.items()
]

# Push the data to Veza
try:
    response = veza_client.create_application(app)
    print(f"Successfully created application: {app_name}")
    print(json.dumps(response, indent=2))
except Exception as e:
    print(f"Error creating application: {e}")
