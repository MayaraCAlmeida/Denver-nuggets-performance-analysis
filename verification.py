import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", required=True, help="Caminho para o CSV")
args = parser.parse_args()

df = pd.read_csv(args.input, encoding="utf-8")

print(df.shape)
print(df.head())
