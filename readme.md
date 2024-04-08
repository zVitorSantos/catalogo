## Feito até agora:
1. Importar as bibliotecas necessárias (pandas, json, firebase_admin, cloudinary, etc.)

2. Definir as classes `CatalogModule`, `JsonModule`, `FirebaseModule` e `CloudinaryModule`.

3. Ler o arquivo Excel do catálogo usando a classe `CatalogModule`.

4. Filtrar os dados do catálogo para preencher as informações de cadastro inicial.

5. Converter os dados filtrados para JSON usando a classe `JsonModule`.

6. Criar uma instância da classe `CloudinaryModule` e obter os recursos do Cloudinary.

7. Para cada item nos dados JSON, verificar se existe uma imagem com a mesma referência no Cloudinary.

8. Se existir uma imagem correspondente, preencher o campo 'imagem' do item com o URL da imagem.

9. Criar uma instância da classe `FirebaseModule`.

10. Deletar os dados antigos do Firebase usando o método `delete_data` da classe `FirebaseModule`.

11. Salvar os dados JSON no Firebase usando o método `save_data_to_firebase` da classe `FirebaseModule`.

## Proximos passos:
1. Configurar o ambiente de desenvolvimento para Vue e Go.

2. Criar a estrutura básica do projeto Vue.

3. Implementar a interface do usuário para a exibição/filtragem de produtos e o gerenciamento de produtos (CRUD).

4. Configurar o ambiente de desenvolvimento para Go.

5. Implementar a API em Go para o gerenciamento de produtos (CRUD).

6. Integrar a API Go com o Firebase para armazenar os dados dos produtos.

7. Implementar a funcionalidade de upload de imagens na API Go.

8. Integrar a funcionalidade de upload de imagens com a Cloudinary para armazenar as imagens.

9. No frontend Vue, implementar a funcionalidade de upload de imagens que faz uma solicitação para a API Go.

10. Testar todas as funcionalidades para garantir que tudo esteja funcionando corretamente.