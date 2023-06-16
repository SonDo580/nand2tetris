# 16-bit Register
# for i in range(16):
#     print(f"Bit(in=in[{i}], load=load, out=out[{i}]);")

# RAM8
# for i in range(8):
#     print(f"Register(in=in, load=load{i+1}, out=out{i+1});")

# RAM64
# for i in range(8):
#     print(f"RAM8(in=in, load=load{i+1}, address=address[0..2], out=out{i+1});")

# RAM512
# for i in range(8):
#     print(f"RAM64(in=in, load=load{i+1}, address=address[0..5], out=out{i+1});")

# RAM4K
# for i in range(8):
#     print(f"RAM512(in=in, load=load{i+1}, address=address[0..8], out=out{i+1});")

# RAM16K
for i in range(4):
    print(f"RAM4K(in=in, load=load{i+1}, address=address[0..11], out=out{i+1});")
