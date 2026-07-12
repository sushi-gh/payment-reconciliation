import pandas as pd

# 1. CSVを2つ読む
shanai = pd.read_csv("shiharai_shanai.csv", usecols=["支払No", "会社名", "金額"])
torihikisaki = pd.read_csv("shiharai_torihikisaki.csv", usecols=["支払No", "会社名", "金額"])

# 2. 支払Noで突合(外部結合=どっちかにしかない行も残す)
merged = pd.merge(
    shanai, torihikisaki,
    on="支払No", how="outer",
    suffixes=("_社内", "_取引先"),
    indicator=True
)

# 3. 差異を抽出
# 3-1. 片方にしかない行
kataho = merged[merged["_merge"] != "both"]

# 3-2. 両方にあるけど金額が違う行
ryoho = merged[merged["_merge"] == "both"]
kingaku_fuicchi = ryoho[ryoho["金額_社内"] != ryoho["金額_取引先"]]

# 4. 結果を表示
print("=== 片方にしかない支払 ===")
print(kataho)
print("\n=== 金額が一致しない支払 ===")
print(kingaku_fuicchi)

with pd.ExcelWriter("shogo_kekka.xlsx") as writer:
    kataho.to_excel(writer, sheet_name="片方のみ", index=False)
    kingaku_fuicchi.to_excel(writer, sheet_name="金額不一致", index=False)