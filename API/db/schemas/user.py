def userSchema(user) -> dict:
    return {"id": str(user["_id"]), "username": user["username"], "email": user["email"]}


def usersSchema(users) -> list:
    return [userSchema(user) for user in users]
