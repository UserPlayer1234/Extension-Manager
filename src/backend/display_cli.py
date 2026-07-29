from src.backend.Extension import Extension

def print_extensions(extensions: list[Extension]):
    for extension in extensions:
        print(extension)

def prompt_create_form() -> bool:
    while True:
        answer = input("Would you like to create a new extension form? (y/n): ")
        match answer:
            case "y" | "Y":
                return True
            case "n" | "N":
                return False
            case _:
                print("ERROR: Please type a valid response.")

def print_form_url(url: str):
    print("Here is the responder link to the extension form:")
    print(url)