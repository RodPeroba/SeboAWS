import json
import boto3

# email sempre o mesmo para teste
EMAIL_USUARIO = "rodperoba@hotmail.com"
TABELA_LISTA_DE_ESPERA = "pedidos-em-espera-sebo"
TABELA_INVENTARIO_SEBO = "inventario-sebo"
SNS_TOPIC = "LivroNoInventarioSebo"
# Váriaveis do banco de dados
dynamodb = boto3.resource('dynamodb')
inventoryTable = dynamodb.Table(TABELA_INVENTARIO_SEBO)
waitingListTable = dynamodb.Table(TABELA_LISTA_DE_ESPERA)
sns = boto3.client("sns")


def lambda_handler(event, context):
    """
        Handler para conferir se algum livro da lista de espera foi adicionado
        Envia o email confirmando o livro no sebo e retira do inventario tal livro
    """
    print("Inicio do handler")
    # print("Evento: " + str(event))
    # print("Context: " + str(context))
    try:
        inventoryScan = inventoryTable.scan()
        waitingListScan = waitingListTable.scan()
        print(waitingListScan)
        for item in inventoryScan["Items"]:
            for requestedBook in waitingListScan["Items"]:
                print("Requested Book: ", requestedBook)
                if item["NomeDoLivro"] == requestedBook["Livro"] and item["Quantidade"] > 0:
                    print(
                        "O livro " + requestedBook["Livro"] + "está disponivel e na lista de espera!")
                    # Seleciona o topico certo para enviar o email
                    for topic in sns.list_topics()["Topics"]:
                        if SNS_TOPIC in topic['TopicArn']:
                            snsTopicArn = topic['TopicArn']
                            break
                    # Envia o email
                    sns.publish(
                        TopicArn=snsTopicArn,
                        Message="O livro " +
                        requestedBook["Livro"] + " está disponivel!",
                        Subject="Livro Disponível",
                        MessageStructure="raw"
                    )
                    inventoryTable.update_item(Key={
                        "NomeDoLivro": requestedBook["Livro"]
                    },
                        UpdateExpression="SET Quantidade = Quantidade - :val",
                        ExpressionAttributeValues={':val': 1}
                    )
    except Exception as e:
        print(e)
        raise e
    return
