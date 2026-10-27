def greet_user(user_name: str) -> str:
    greeting = f"Hello, {user_name}!"
    return greeting

if __name__ == "__main__":
    message = greet_user("Developer")
    print(message)
