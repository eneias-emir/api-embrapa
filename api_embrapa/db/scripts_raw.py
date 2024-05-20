class ScriptsRaw:
    """Classe com as scripts para acesso direto ao banco de dados."""

    STM_API_LOGIN = """
    create table LOGIN (
        ID            integer primary key autoincrement,
        USERNAME      text(100),
        PASSWORD      text(100)
    )
    """

    STM_DADOS_EMBRAPA = """
    create table DADOS_EMBRAPA (
        ID            integer primary key autoincrement,
        ID_ORIGEM     integer,
        OPT           text(10),
        DESC_OPT      text(100),
        SUBOPT        text(10),
        DESC_SUBOPT   text(100),
        GRUPO         text(50),
        CODIGO        text(50),
        DESCRICAO     text(100)
        )
    """

    STM_DADOS_EMBRAPA_ITENS = """
    create table DADOS_EMBRAPA_ITENS (
        ID               integer primary key autoincrement,
        ID_DADOS_EMBRAPA integer,
        OPT           text(10),
        ANO           integer,
        QTDE          real,
        VALOR         real)
    """


    STM_SELECT_DADOS_EMBRAPA = """
    select
        ID,
        ID_ORIGEM,
        OPT,
        DESC_OPT,
        SUBOPT,
        DESC_SUBOPT,
        GRUPO,
        CODIGO,
        DESCRICAO
    from DADOS_EMBRAPA
    where OPT = ?  
    """

    STM_SELECT_DADOS_EMBRAPA_ITENS = """
    select
        ID_DADOS_EMBRAPA,
        ANO,
        QTDE,
        VALOR
    from DADOS_EMBRAPA_ITENS
    where OPT = ?  
    order by ID_DADOS_EMBRAPA
    """

    STM_SELECT_DADOS_EMBRAPA_ITENS_ANO = """
    select
        ID_DADOS_EMBRAPA,
        ANO,
        QTDE,
        VALOR
    from DADOS_EMBRAPA_ITENS
    where OPT = ?  
    and ANO = ?
    order by ID_DADOS_EMBRAPA
    """



    STM_INSERT_DADOS_EMBRAPA = """
    insert into DADOS_EMBRAPA(ID_ORIGEM, 
                            OPT, 
                            DESC_OPT, 
                            SUBOPT, 
                            DESC_SUBOPT, 
                            GRUPO, 
                            CODIGO, 
                            DESCRICAO) 
                    values(?, ?, ?, ?, ?, ?, ?, ?) 
                    RETURNING ID
    """

    STM_INSERT_DADOS_EMBRAPA_ITENS = """
    insert into DADOS_EMBRAPA_ITENS(ID_DADOS_EMBRAPA, 
                            OPT,
                            ANO, 
                            QTDE, 
                            VALOR) 
                    values(?, ?, ?, ?, ?) 
    """

    STM_INSERT_DADOS_LOGIN = """
    insert into LOGIN(USERNAME, 
                    PASSWORD) 
                    values(?, ?) 
    """

    STM_SELECT_DADOS_LOGIN = """
    select
        ID,
        USERNAME,
        PASSWORD
    from LOGIN
    where USERNAME = ?  
    """
