2o Trabalho de Distribuição e Concorrência 2026.2
Aluno: Rodrigo Peroba de Souza

O trabalho pede para que se crie um sistema serveless utilizando a AWS e simulando um sebo, o usuário pede o livro pela interface e é notificado por email e pela interface caso o livro esteja disponivel, caso o livro não esteja disponivel, o usuário é adicionado a lista de espera e quando o livro pedido for adicionado ao inventário, ele recebe um email avisando que o livro está disponível
    
Há um diagrama do esquema nos arquivos como .png

O que foi feito:

    Interface em CLI para compra de livros no sebo

    Na AWS temos:

        3 funcões lambdas:

        - Check-sebo-inventory(FL1) checa se item pedido pela interface esta disiponivel, envia email caso esteja e caso não esteja disponivel, adiciona na lista de espera
        - Check-waiting-list(FL2) é acionada toda vez que a tabela do inventário é atualizada e checa se algum livro da lista de espera foi adicionado
        - Load-sebo-inventory(FL3) carrega os dados do bucket na tabela do inventário

        2 tabelas no DynamoDB:
        
        - Tabela(T1) de livros disponiveis no sebo ( inventário ), com nome e quantidade do livro em estoque
        - Tabela(T2) de lista de espera, com nome do livro pedido e email de quem pediu (email esta mockado)

        1 Bucket:
        
        - Bucket(B3) para adicionar livros a tabela de inventário, adiciona um arquivo .txt ao bucket com o nome inventarioSebo e na formatação correta para os livros serem adicionados a tabela
            
            Formatação do inventarioSebo - em formato de csv
            
            livro,quantidade
            [NomeDoLivro],[Quantidade]
            [NomeDoLivro],[Quantidade]
            [NomeDoLivro],[Quantidade]

Problemas conhecidos:

    A interface não consegue acessar a URL do função lambda "Check-sebo-inventory" para fazer o pedido dos livros, retorna 403 ao request