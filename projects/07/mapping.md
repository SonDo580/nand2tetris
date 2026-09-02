# Labels (assembly)

## SP

- refer to RAM[0].
- point to `stack` segment (RAM[256] -> RAM[2047]).

## LCL

- refer to RAM[1].
- point to `local` segment (method's local variables).

## ARG

- refer to RAM[2].
- point to `argument` segment (method's arguments).

## THIS

- refer to RAM[3].
- point to `this` segment (current object's fields).

## THAT

- refer to RAM[4].
- point to `that` segment (current array's elements).

# Segments (VM code)

## `local`, `argument`, `this`, `that`

- allocated dynamically on the RAM.
- accessing `segment i` <-> accessing `RAM[*segment_pointer + i]`
  - example: `local i` <-> `RAM[RAM[LCL] + i]`

## `constant`

- not a "real" segment.
- there's only `push constant i`, no `pop constant i`.

## `static`

- fixed: RAM[16] -> RAM[255].
- accessing `static i` within `Foo.vm` <-> accessing assembly variable `Foo.i`

## `temp`

- fixed (8-entry): RAM[5] -> RAM[12].
- accessing `temp i` <-> accessing `RAM[5 + i]`.

## `pointer`

- fixed, mapped on RAM[3] and RAM[4].
- accessing `pointer 0` <-> accessing `RAM[THIS]`.
- accessing `pointer 1` <-> accessing `RAM[THAT]`.

# Other

- R13, R14, R15: general purpose registers.
