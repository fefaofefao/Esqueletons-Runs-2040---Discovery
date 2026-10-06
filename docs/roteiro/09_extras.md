# Roteiro — Falas transversais (o mundo reage)

Fase 4h. **Gerado por `tools/maps/extras.py`**, que roda depois de todas as regiões (`tools/maps/build_all.py`). Reúne falas que atravessam o jogo inteiro: o parceiro comentando o Prólogo e o Bosque, NPCs que mudam depois do Brás e do Ramalho, as **cartas do Bento** que chegam ao Rancho de cada cidade depois do Guardião, e o **pós-jogo** (lore nova em todas as cidades, Lia no farol e a família do Taro na Vila Maré).

## Falas (PT-BR)

### `extras/chegada_vila_mare`
- **SPK_LIA:** Uma vila de verdade! Tem cheiro de peixe e de pão. Qual dos dois a gente come primeiro? *(if partner_lia)*
- **SPK_TARO:** Barcos parados. Gente parada. Esse lugar tá esperando alguém fazer alguma coisa. *(if partner_taro)*
- *[flag x_vila_mare_visto = True]*

### `extras/chegada_rota_1`
- **SPK_LIA:** Árvores! Lá na praia só tinha coqueiro. Essas têm braço pra todo lado. *(if partner_lia)*
- **SPK_LIA:** Será que elas lembram de quando eram sementinhas? *(if partner_lia)*
- **SPK_TARO:** Três caminhos. Eu ia pelo do meio, mas tá cheio de raiz. *(if partner_taro)*
- *[flag x_rota_1_visto = True]*

### `extras/chegada_raizal`
- **SPK_LIA:** Cheiro de chá e de madeira molhada. Eu gosto daqui. *(if partner_lia)*
- **SPK_TARO:** Raiz em cima de raiz. Isso não é floresta, é prisão com folha. *(if partner_taro)*
- *[flag x_raizal_visto = True]*

### `extras/chegada_bosque_velho`
- **SPK_LIA:** Shhh... Esse lugar parece que tá dormindo. *(if partner_lia)*
- **SPK_TARO:** Tem alguém grande aqui. Dá pra sentir no chão. *(if partner_taro)*
- *[flag x_bosque_velho_visto = True]*

### `extras/reage_marola`
- **SPK_MAROLA:** O cais abriu! Hoje teve peixe fresco no Rancho. Os esqueletos só comeram o cheiro, mas adoraram.
- *[vai para `vila_mare/marola`]*

### `extras/reage_anzol`
- **SPK_ANZOL:** Com o cais aberto, chegou anzol novo. Pena que eu vendo chá de alga.
- *[vai para `vila_mare/anzol`]*

### `extras/reage_pipa`
- **SPK_PIPA:** Meu esqueleto ficou mais rápido. Ou eu fiquei mais lenta? Tô confusa.
- *[vai para `vila_mare/pipa`]*

### `extras/reage_cascalho`
- **SPK_CASCALHO:** O Brás perdeu? Então a lei do Rei tem fresta. Toda lei tem, jovem.
- *[vai para `vila_mare/cascalho`]*

### `extras/reage_tilia`
- **SPK_TILIA:** As raízes soltaram! Hoje mesmo mandei o primeiro doente pra casa, andando.
- *[vai para `bosque/tilia`]*

### `extras/reage_toco`
- **SPK_TOCO:** Estrada aberta, preço baixando. Não muito. Um pouquinho.
- *[vai para `bosque/toco`]*

### `extras/reage_graveto`
- **SPK_GRAVETO:** As raízes foram embora levando a minha marca de dente. Que orgulho.
- *[vai para `bosque/graveto`]*

### `extras/reage_hera`
- **SPK_HERA:** O Ramalho veio pedir desculpas pra vila. Trouxe lenha. Primo do Rei, mas educado.
- *[vai para `bosque/hera`]*

### `extras/reage_lenhador_velho`
- **SPK_LENHADOR_VELHO:** Estrada livre de novo. Agora só falta eu lembrar onde deixei o machado.
- *[vai para `bosque/velho`]*

### `extras/carta_1`
- **SPK_TILIA:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "Moleque! O cais abriu e a Jurema pescou um peixe do tamanho do Brás. O Brás não gostou da comparação."
- *(narração)* "Rede boa não é a mais forte, é a que tem nó bem dado. Cuida do teu parceiro. Bento."
- *[flag carta_bento_1 = True]*
- *[vai para `bosque/tilia`]*

### `extras/carta_2`
- **SPK_RUBI:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "A Marola jura que esqueleto cresce mais rápido quando é bem tratado. Eu juro que é a sopa dela."
- *(narração)* "Ouvi falar de mina e fumaça. Mar calmo nunca fez bom marinheiro. Segue em frente. Bento."
- *[flag carta_bento_2 = True]*
- *[vai para `minas/rubi`]*

### `extras/carta_3`
- **SPK_GARCA:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "Chegou chá de Raizal aqui. Tá todo mundo tomando, até quem não tava doente."
- *(narração)* "Uma coisa que eu não te contei: aquele teu papel de 'museu' tem o desenho do farol velho. Pensa nisso. Bento."
- *[flag carta_bento_3 = True]*
- *[vai para `pantano/garca`]*

### `extras/carta_4`
- **SPK_AMEIA:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "Meu avô dizia que o mar já foi de um rei menino que só olhava pra ele. Nunca entendi. Agora acho que entendo."
- *(narração)* "Se descobriu alguma coisa sobre você, guarda com carinho. Ou conta. Tu que sabe. Bento."
- *[flag carta_bento_4 = True]*
- *[vai para `ossorio/ameia`]*

### `extras/carta_5`
- **SPK_LAREIRA:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "Esfriou por aqui também. A vila fez fogueira na praia e cantou. O Brás cantou desafinado, claro."
- *(narração)* "Tô velho, mas reconheço quem tá chegando perto do fim da viagem. Não corre. Chega. Bento."
- *[flag carta_bento_5 = True]*
- *[vai para `picos/lareira`]*

### `extras/carta_6`
- **SPK_MORINGA:** Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.
- *(narração)* "Subi no farol pra limpar a lente. Pela primeira vez, ela brilhou um pouquinho. Sozinha."
- *(narração)* "Seja o que for que te espera no castelo: quem tem pra onde voltar nunca tá perdido. Bento."
- *[flag carta_bento_6 = True]*
- *[vai para `deserto/moringa`]*

### `extras/pos_cascalho`
- **SPK_CASCALHO:** Esqueletos livres, fazendo aniversário em paz de novo. Era só isso que eu queria ver antes de virar um.

### `extras/pos_hera`
- **SPK_HERA:** Sem coroa, os esqueletos do Bosque ficaram. Por amizade. Isso vale mais que qualquer ordem.

### `extras/pos_turmalina`
- **SPK_TURMALINA:** O sino da cidade tocou sozinho no dia em que a coroa quebrou. Acho que foi a Tia se despedindo.

### `extras/pos_sape`
- **SPK_SAPE:** A névoa nunca mais voltou. Mas às vezes alguém escreve "que fofo" nas cartas. Não sei quem.

### `extras/pos_brasao`
- **SPK_BRASAO:** O menino que só olhava o mar agora viaja com você. Eu sabia que um dia ele saía desse pátio.

### `extras/pos_pinhao`
- **SPK_PINHAO:** Primavera nos picos! A primeira em mil anos. As flores nem sabem direito o que fazer.

### `extras/pos_miragem`
- **SPK_MIRAGEM:** Os tambores tocam toda noite agora. Sempre com uma batida a mais. Pela rainha.

### `extras/lia_farol`
- **SPK_LIA:** Fui eu! Subi os duzentos degraus sozinha, no escuro. Nem tremi. Quer dizer, tremi um pouquinho.
- **SPK_LIA:** Agora, quando alguém se perder, é só olhar pra cá. Até você, se um dia voltar pra 2040.

### `extras/pais_vila`
- **SPK_MAE_TARO:** Você é o amigo do nosso Taro! Ele fala de você o tempo todo. Bom, "o tempo todo" pro Taro é três frases.
- **SPK_PAI_TARO:** Estamos fazendo os cem bolos que devemos. Já vamos no sétimo.

### `extras/taro_vila`
- **SPK_TARO:** Eles tão aqui. Inteiros. ...Eu tô bem. Para de me olhar assim.

### `extras/romeiro_cinza`
- **Romeiro da Cinza:** Antes da coroa, as minas davam cristal pra todo o reino. A rainha usou um deles na lente do farol.
- **Romeiro da Cinza:** Por isso a luz do farol é meio azulada. Pedra de mina tem lembrança.

### `extras/barqueira_lua`
- **Barqueira Lua:** No tempo do reino, as palafitas eram casas de verão da corte. A princesa vinha pescar sapo.
- **Barqueira Lua:** Nunca pescou nenhum. Soltava todos. Dizia que sapo também tem família.

### `extras/historiadora_pena`
- **Historiadora Tinta:** Esta estrada foi feita pro casamento do rei com a rainha do deserto. Mil bandeiras, uma pra cada convidado.
- **Historiadora Tinta:** Hoje sobraram poucas. Mas os esqueletos ainda marcham por ela como quem vai pra festa.

### `extras/pastora_neve`
- **Pastora Neve:** Lá no alto tem um mosteiro onde o sino nunca toca. Dizem que ele espera uma voz de muito longe.
- **Pastora Neve:** De quanto longe? Ninguém sabe. Talvez de mil anos.

### `extras/colecionador_eco`
- **Colecionador de Ecos:** Eu guardo ecos em garrafas. Este aqui é a risada de uma rainha, de mil anos atrás.
- **Colecionador de Ecos:** Se a tempestade passar, eu solto. Risada presa fica triste.

### `extras/salina`
- **Dona Salina:** Vendo sal desde menina. No tempo dos meus avós, esqueleto fazia aniversário com festa na praia inteira.
- **Dona Salina:** Agora é tudo baixinho, com medo do Rei. Bolo sem vela é só pão triste.

### `extras/siri`
- **Siri:** Eu tinha medo de esqueleto. Aí vi um soprando vela de aniversário. Não dá pra ter medo de quem sopra vela.

### `extras/seiva`
- **Seiva:** O Raizerno dorme no Bosque Velho desde antes da vila existir. Minha avó levava chá pra ele.
- **Seiva:** Ele nunca bebeu. Mas a árvore em volta dele cresceu cheirosa.

### `extras/cavaco`
- **Seu Cavaco:** Sou marceneiro. Fiz o berço de três gerações daqui. E agora faço berço pra esqueleto bebê.
- **Seu Cavaco:** Eles chutam a madeira dormindo. Igual criança. Igualzinho.

### `extras/livro_sino`
- *(narração)* Caderno de forja da Tia Fornalha
- *(narração)* "Sino de Brasal: bronze, cristal moído e uma risada do sobrinho. Sem a risada, o sino não afina."

### `extras/livro_musga`
- *(narração)* Receitas da Musga (roubadas pelo Bagre)
- *(narração)* "Chá de esquecer a tristeza: hortelã, mel e uma visita. A visita é o ingrediente principal."
- *(narração)* Na margem, a letra do Bagre: "Nunca consegui o terceiro ingrediente."

### `extras/livro_neve`
- *(narração)* Canções de inverno
- *(narração)* "Dorme, princesa, que a neve te cobre; quando acordar, o papai já sorriu." Uma canção de ninar da serra.

### `extras/livro_estrelas`
- *(narração)* Mapa das estrelas da Rosa
- *(narração)* Constelações com nomes à mão: "o Remo", "a Lamparina", "a Coroa Rachada".
- *(narração)* Ao pé da página: "Toda estrela é um farol de quem já se foi."

### `extras/floq_pede`
- **SPK_FLOQUINHO:** `DLG_PI_FLOQUINHO_AFTER` *(if alva_beaten)*
- **SPK_FLOQUINHO:** `DLG_PI_FLOQUINHO` *(if_not alva_beaten)*
- **SPK_FLOQUINHO:** Vai ter eleição pra prefeito de neve! Pergunta pra Lareira, pro Pinhão e pro Degelo em quem eles votam?
- *[flag eleicao_quest = True]*

### `extras/floq_espera`
- **SPK_FLOQUINHO:** Faltam votos! Lareira no Rancho, Pinhão e Degelo na praça.

### `extras/floq_ganhou`
- **SPK_FLOQUINHO:** Três votos pro Prefeito! Ganhou por unanimidade. Ele não disse nada, mas tá feliz. Toma, presente do gabinete.
- *[ação give_item: {"item": "reviver", "n": 1}]*
- *[ação give_item: {"item": "pocao_g", "n": 1}]*
- *[flag eleicao_done = True]*

### `extras/floq_depois`
- **SPK_FLOQUINHO:** O Prefeito já assinou três decretos. Todos de neve.

### `extras/voto_lareira`
- **SPK_LAREIRA:** Voto no Prefeito. Pelo menos ele não reclama da sopa.
- *[flag voto_lareira = True]*
- *[vai para `picos/lareira`]*

### `extras/voto_pinhao`
- **SPK_PINHAO:** No meu tempo, prefeito tinha nariz de cenoura e honra. Esse tem os dois. Voto nele.
- *[flag voto_pinhao = True]*
- *[vai para `picos/pinhao`]*

### `extras/voto_degelo`
- **SPK_DEGELO:** Votar num boneco de neve? ...Tá, ele é mais rápido que o prefeito de verdade.
- *[flag voto_degelo = True]*
- *[vai para `picos/degelo`]*

### `extras/grao_pede`
- **SPK_GRAO:** A rainha liberou os tambores! Mas ninguém lembra o ritmo de guiar caravana. Os Batuque sabem. Pergunta pra eles?
- *[flag ritmo_quest = True]*

### `extras/grao_feito`
- **SPK_GRAO:** Tum, tum-tum, PÁ! Ouviu? Lá longe, uma caravana respondeu! Toma, a cidade agradece.
- *[ação sfx: {"name": "birthday"}]*
- *[ação give_item: {"item": "pocao_g", "n": 2}]*
- *[flag ritmo_done = True]*

### `extras/grao_depois`
- **SPK_GRAO:** Já contei: hoje chegaram onze caravanas. Bem mais fácil que contar areia.

### `extras/batuque_ritmo`
- **SPK_BATUQUE:** O ritmo da caravana? Tum, tum-tum, PÁ. Três batidas e uma de esperança. Leva pro Grão.
- *[flag ritmo_aprendido = True]*

### `extras/cama_vila`
- **SPK_LIA:** Cama de verdade! Eu acordei numa caverna fria, sabia? Aqui é bem melhor. *(if partner_lia)*
- **SPK_TARO:** Eu durmo de botas. Vai que alguém precisa de ajuda no meio da noite. *(if partner_taro)*

### `extras/cama_raizal`
- **SPK_LIA:** No túnel eu tremi. Mas fui. Tremer e ir ao mesmo tempo conta como coragem? *(if partner_lia)*
- **SPK_TARO:** O Ramalho riu o tempo todo. Meu pai também ria assim. Alto demais. *(if partner_taro)*

### `extras/cama_brasal`
- **SPK_LIA:** A Tia Fornalha cuida demais. Será que eu cuido demais da minha lamparina? *(if partner_lia)*
- **SPK_TARO:** Guardei o lenço da minha mãe na mochila. Não conta pra ninguém. Ele cheira a casa. *(if partner_taro)*

### `extras/cama_brejo`
- **SPK_LIA:** A Musga só queria visita. Se eu morasse numa torre, eu ia querer também. *(if partner_lia)*
- **SPK_TARO:** Castelo. Eles tão no castelo. Agora eu sei pra onde correr. Isso já ajuda. *(if partner_taro)*

### `extras/cama_ossorio`
- **SPK_LIA:** Você é da família do Rei... Mas pra mim você continua sendo você. Tá? *(if partner_lia)*
- **SPK_TARO:** Neto de rei. Tá. Continua chato igual. *(if partner_taro)*

### `extras/cama_geada`
- **SPK_LIA:** A Alva congelou tudo pra esperar o pai. Eu também esperei, no escuro. Esperar sozinho é o pior. *(if partner_lia)*
- **SPK_TARO:** Eu disse que tinha medo. Em voz alta. Não foi tão ruim quanto eu achava. *(if partner_taro)*

### `extras/cama_palmeiral`
- **SPK_LIA:** Amanhã é o castelo. Promete uma coisa? Não coloca aquela coroa. *(if partner_lia)*
- **SPK_TARO:** Amanhã eu vejo meus pais. Ou não. ...Dorme logo, que eu não consigo. *(if partner_taro)*

### `extras/pos_marola`
- **SPK_MAROLA:** O Rei Esqueleto no meu Rancho! Deita aí, Majestade. Aqui todo mundo é igual na hora da sopa.
- *[vai para `vila_mare/marola`]*

### `extras/pos_tilia`
- **SPK_TILIA:** Os esqueletos não obedecem mais ninguém, e mesmo assim vêm deitar aqui. Isso é confiança.
- *[vai para `bosque/tilia`]*

### `extras/pos_rubi`
- **SPK_RUBI:** O Rancho encheu de novo! Mineiro com esqueleto no colo, igual antigamente.
- *[vai para `minas/rubi`]*

### `extras/pos_garca`
- **SPK_GARCA:** Ninguém tosse mais. Agora o barulho do Rancho é ronco. Prefiro mil vezes.
- *[vai para `pantano/garca`]*

### `extras/pos_ameia`
- **SPK_AMEIA:** Acabou o toque de recolher, acabou o dormir em formação. Agora cada um dorme torto, do jeito que gosta.
- *[vai para `ossorio/ameia`]*

### `extras/pos_lareira`
- **SPK_LAREIRA:** Primavera! Apaguei a lareira pela primeira vez em um ano. Até estranhei.
- *[vai para `picos/lareira`]*

### `extras/pos_moringa`
- **SPK_MORINGA:** Com as caravanas de volta, tem água, tem tâmara e tem fofoca. Rancho cheio é Rancho feliz.
- *[vai para `deserto/moringa`]*

### `extras/pos_anzol`
- **SPK_ANZOL:** Vendo até pro Rei agora. Ele pediu desconto. Rei pedindo desconto, veja só.
- *[vai para `vila_mare/anzol`]*

### `extras/pos_toco`
- **SPK_TOCO:** Estrada cheia, preço justo. Quase justo. Justo pra mim.
- *[vai para `bosque/toco`]*

### `extras/pos_cobre`
- **SPK_COBRE:** Minério voltou, freguês voltou, até o sino voltou a tocar. Só o meu bigode não voltou ao normal.
- *[vai para `minas/cobre`]*

### `extras/pos_junco`
- **SPK_JUNCO:** Erva amarga de volta na prateleira! Ninguém compra. Ninguém precisa. Melhor problema do mundo.
- *[vai para `pantano/junco`]*

### `extras/pos_dobrao`
- **SPK_DOBRAO:** Sem autorização do quartel! Rasguei a minha. Emoldurei os pedaços.
- *[vai para `ossorio/dobrao`]*

### `extras/pos_cachecol`
- **SPK_CACHECOL:** Primavera é péssimo pra quem vende cachecol. Vou vender chapéu de sol.
- *[vai para `picos/cachecol`]*

### `extras/pos_canela`
- **SPK_CANELA:** Caravana nova todo dia. O preço agora é o da alegria: um pouco mais baixo.
- *[vai para `deserto/canela`]*

### `extras/pos_jurema`
- **SPK_JUREMA:** Prometi o primeiro peixe pra você. Guardei o maior. Tá salgado há uma semana, mas é seu.

### `extras/pos_seu_remo`
- **SPK_REMO:** Os meninos cresceram tanto que agora a sopa esfria esperando eles. Volta pra uma revanche quando quiser.

### `extras/pos_vo_concha`
- **SPK_CONCHA:** Fiz um bolo com cem velas pro Rei. Ele demorou meia hora pra soprar. Família é isso.

### `extras/pos_irmao_galho`
- **SPK_GALHO:** A gente aprendeu a não empurrar o turno de ninguém. Agora a gente só empurra balanço.

### `extras/pos_pai_musgo`
- **SPK_MUSGO:** Esporo continua sendo tempero. Mas agora é por gosto, não por veneno.

### `extras/pos_bigorna`
- **SPK_BIGORNA:** Forjei um sino novo pra cidade. Pus uma risada dentro, igual à receita da Tia.

### `extras/pos_viseira`
- **SPK_VISEIRA:** Dispensei a tropa. Agora a gente treina Sintonia dançando. Funciona melhor, vai entender.

### `extras/pos_tamara`
- **SPK_TAMARA:** Meu camelo voltou! Trouxe três amigos. Agora quem precisa trocar de montaria sou eu.

### `extras/pos_agata`
- **SPK_AGATA:** Sem gás na mina, meu perfume acabou. Agora uso lavanda. Os esqueletos estranharam.

### `extras/pos_bagre`
- **SPK_BAGRE:** Pesquei um peixe tão grande que ele me pescou de volta. Brincadeira. Mais ou menos.

### `extras/pos_lamina`
- **SPK_LAMINA:** Sem gelo, eu patino na lama. É mais lento, mas muito mais engraçado.

### `extras/pos_batuque`
- **SPK_BATUQUE:** Tum, tum-tum, PÁ! A gente toca toda noite. Os vizinhos reclamam com ritmo.

### `extras/pos_bras_depois`
- **SPK_BRAS:** Agora eu fiscalizo peixe fresco. Peixe não reclama. Quase sempre.

### `extras/pos_bloqueio`
- **SPK_BLOQUEIO:** Saí da cidade pela primeira vez em um ano. Voltei no mesmo dia. Saudade da cinza.

### `extras/pos_fel`
- **SPK_FEL:** Agora faço xarope de mel. A receita da Musga era: um pouco de tudo e muita saudade.

### `extras/pos_grade`
- **SPK_GRADE:** A senha agora é "bom dia". Todo mundo acerta. Que tédio maravilhoso.

### `extras/pos_pingente`
- **SPK_PINGENTE:** Derreti um pouco também. Não o corpo, o coração. Não conta pro sargento.

### `extras/pos_sandalo`
- **SPK_SANDALO:** Pode entrar de sandália. Pode até dançar. A rainha deixou um bilhete dizendo isso.

### `extras/obj_tr_portrait1`
- *(narração)* Retrato da família: sete pessoas sorrindo na praia, diante de um farol novinho.

### `extras/obj_tr_portrait2`
- *(narração)* Um desenho de giz: a família inteira, feita por uma criança. O menino se desenhou maior que todos.

### `extras/obj_tr_throne`
- *(narração)* O trono está vazio. Pela primeira vez em mil anos, ninguém precisa sentar nele.

### `extras/obj_mu_duna`
- *(narração)* "Rainha Duna, construtora do Farol do Litoral (restaurado em 2031)."

### `extras/obj_mu_king`
- *(narração)* "Ossárion, último rei de Ossório. Morreu sem herdeiros, dizem os livros."

### `extras/obj_mu_map`
- *(narração)* Mapa do litoral em 2040: as mesmas três baías. A do meio se chama Baía do Farol.

## Contagem
Cerca de **1896 palavras** de texto de jogo em PT-BR.
