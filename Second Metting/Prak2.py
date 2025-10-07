a = float(input("Masukkan angka pertama: "))
b = float(input("Masukkan angka kedau: "))
c = float(input("Masukkan angka ketiga: "))

if a > b and a> c:
  largest = a
elif b > a and b > c:
  largest = b
elif c > a and c > b:
  largest = c
else:
  largest = print("Tidak angka terbesar")

  print("Angka terbesar adalah: ", largest)