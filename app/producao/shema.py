from typing import Optional

from pydantic import BaseModel, Field, Extra


class ProducaoSchema(BaseModel):
    id: int
    produto: str
    report_item_id: int
    qtd_1970_em_l: int
    qtd_1971_em_l: int
    qtd_1972_em_l: int
    qtd_1973_em_l: int
    qtd_1974_em_l: int
    qtd_1975_em_l: int
    qtd_1976_em_l: int
    qtd_1977_em_l: int
    qtd_1978_em_l: int
    qtd_1979_em_l: int
    qtd_1980_em_l: int
    qtd_1981_em_l: int
    qtd_1982_em_l: int
    qtd_1983_em_l: int
    qtd_1984_em_l: int
    qtd_1985_em_l: int
    qtd_1986_em_l: int
    qtd_1987_em_l: int
    qtd_1988_em_l: int
    qtd_1989_em_l: int
    qtd_1990_em_l: int
    qtd_1991_em_l: int
    qtd_1992_em_l: int
    qtd_1993_em_l: int
    qtd_1994_em_l: int
    qtd_1995_em_l: int
    qtd_1996_em_l: int
    qtd_1997_em_l: int
    qtd_1998_em_l: int
    qtd_1999_em_l: int
    qtd_2000_em_l: int
    qtd_2001_em_l: int
    qtd_2003_em_l: int
    qtd_2004_em_l: int
    qtd_2005_em_l: int
    qtd_2006_em_l: int
    qtd_2007_em_l: int
    qtd_2008_em_l: int
    qtd_2009_em_l: int
    qtd_2010_em_l: int
    qtd_2011_em_l: int
    qtd_2012_em_l: int
    qtd_2013_em_l: int
    qtd_2014_em_l: int
    qtd_2015_em_l: int
    qtd_2016_em_l: int
    qtd_2017_em_l: int
    qtd_2018_em_l: int
    qtd_2019_em_l: int
    qtd_2020_em_l: int
    qtd_2021_em_l: int
    qtd_2022_em_l: int

    class Config:
        orm_mode = True
