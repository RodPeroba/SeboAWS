import requests, json

AWS_URL = "https://tj2hlk3wcl324qwfwg67pf7wxu0whozd.lambda-url.us-east-1.on.aws/"

def requestBook():
    """
    Run CLI interface to request book from sebo by sending a request to a url that activates a aws lambda function
    """

    book_name = input(
        "Qual livro você deseja solicitar? (Digite o nome do livro)")
    print(f"Você solicitou o livro: {book_name}")
    confirm = input("Confirmar solicitação? y/N: ")

    if confirm.lower() == "y":
        response = requests.get(url=AWS_URL, json=json.dumps({"livro": book_name}))
        print(response)
        if response.status_code == 200:
            print("Possuimos o livro solicitado, cheque seu email para mais informações.")
        if response.status_code == 403:
            print("Pedido não autorizado, você não possui permissão para solicitar livros.")
        else:
            print("Livro não encontrado, pedido foi adicionado a lista de espera.")
    elif confirm.lower() == "n":
        print("Solicitação cancelada.")
    else:
        print("Opção inválida. Solicitação cancelada.")

if __name__ == "__main__":
    requestBook()