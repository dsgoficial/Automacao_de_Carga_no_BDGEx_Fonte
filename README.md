# Automacao_de_carga_no_BDGEx_Fonte
Enquanto não é realizada a migração do subsistema Fonte de Dados do BDGEx, o carregamento em lote é feito via automação de interface. No entanto, nas novas versões de navegadores, o plugin Selenium não tem conseguido fazer upload de arquivos. Por isso, foram criados esses scripts Python com a biblioteca Selenium para a automação dos processos.

A biblioteca selenium pode ser instalada através de 'pip install selenium' e é necessária para a execução dos códigos.

CarregadorProdutos.py: classe python cujos objetos carregam os produtos no Fonte a partir de XML com metadados. É necessário um csv de entrada com os caminhos dos arquivos a serem carregados. Os produtos podem ou não estar na Área de Tranferência do Fonte, mas se estiverem, devem estar na raiz. Os metadados podem ou não ser completos, mas se não forem, deve-se atentar para o preenchimento do csv com tal informação.

exemploprodutoscarregados.csv: exemplo de arquivo csv a ser inserido na classe CarregadorProdutos

importaGeoProdMatriciais.py: script para importar a geometria dos produtos para o banco de dados. A partir da realização dessa ação, será possível visualizar o produto para a verificação do correto carregamento antes da homologação.

homologaProdutos.py: script que homologa em lote produtos carregados. Deve ser utilizado com cautela (a sugestão é que seja utilizado apenas para produtos que estão sendo recarregados), pois não há qualquer validação nos dados sendo homologados.
