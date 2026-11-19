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
sns = boto3.client("sns")


def lambda_handler(event, context):

    print("Inicio do handler")
    # print("Evento: " + str(event))
    # print("Context: " + str(context))
    try:
        livroRequisitado = event['livro']
        dbScan = inventoryTable.scan()
        print(dbScan)
        for item in dbScan["Items"]:
            print(item)
            print(item["NomeDoLivro"] + str(item["Quantidade"]))
            if item["NomeDoLivro"] == livroRequisitado and item["Quantidade"] > 0:
                print("O livro " + livroRequisitado + " está disponível!")
                # Removendo 1 da quantidade de livros disponiveis
                inventoryTable.update_item(Key={
                    "NomeDoLivro": livroRequisitado
                },
                    UpdateExpression="SET Quantidade = Quantidade - :val",
                    ExpressionAttributeValues={':val': 1}
                )
                for topic in sns.list_topics()["Topics"]:
                    if SNS_TOPIC in topic['TopicArn']:
                        snsTopicArn = topic['TopicArn']
                        break
                # Envia o email
                sns.publish(
                    TopicArn=snsTopicArn,
                    Message="O livro " + livroRequisitado + " está disponivel!",
                    Subject="Livro Disponível",
                    MessageStructure="raw"
                )
                return {
                    "statusCode": 200,
                    "body": json.dumps("O livro " + livroRequisitado + " esta disponivel!\n Confira seu email para mais informações!"),
                }
        # Adicionar a fila de espera
        pedidosEmEsperaBD = dynamodb.Table(TABELA_LISTA_DE_ESPERA)
        pedidosEmEsperaBD.put_item(Item={
            "Livro": livroRequisitado,
            "Usuario": EMAIL_USUARIO
        })
        return {
            "statusCode": 200,
            "body": json.dumps("O livro " + livroRequisitado + " nao esta disponivel, mas seu email foi adicionado a fila de espera!"),
        }
    except Exception as e:
        print(e)
        raise e
