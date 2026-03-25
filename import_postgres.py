#  Denver Nuggets — Import CSV → PostgreSQL


# Tem que configurar no env a variável de ambiente DATABASE_URL antes de rodar
# Por exemplo: DATABASE_URL=postgresql://postgres:senha@localhost:5432/DenverNuggets
# Só consegui assim, não consegui passar a senha diretamente na string de conexão do SQLAlchemy
# mesmo usando o formato recomendado.


import os
import sys

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


def main():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("❌  DATABASE_URL não encontrada.")
        print("    Crie um arquivo .env com:")
        print(
            "    DATABASE_URL=postgresql://postgres:SUASENHA@localhost:5432/DenverNuggets"
        )
        sys.exit(1)

    engine = create_engine(db_url)

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS denver_nuggets CASCADE"))
        conn.commit()

    df = pd.read_csv("denver_nuggets_clean.csv", encoding="utf-8-sig")
    df.to_sql("denver_nuggets", engine, if_exists="append", index=False)

    print(f"✅  {len(df)} linhas importadas na tabela 'denver_nuggets'")


if __name__ == "__main__":
    main()
