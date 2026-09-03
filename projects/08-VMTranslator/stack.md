# Stack during function call

## Current working stack of the caller

```
     | ... |
SP ->
```

## Caller prepares to call callee

- Push arguments onto the stack.

```
     | ... |
     -------
     | arg | \
     | ... |  | nArgs
     | arg | /
     -------
SP ->
```

- Save return address (which instruction to execution next after the call is completed) and caller's segment pointers.

```
     | ...        |
     --------------
     | arg        | \
     | ...        |  | nArgs
     | arg        | /
     --------------
     | ret_addr   | \
     | saved LCL  |  |
     | saved ARG  |  | saved "frame" of caller
     | saved THIS |  |
     | saved THAT | /
     --------------
SP ->
```

- Reposition ARG and LCL for callee.

```
          | ...        |
          --------------
   ARG -> | arg        | \
          | ...        |  | nArgs
          | arg        | /
          --------------
          | ret_addr   | \
          | saved LCL  |  |
          | saved ARG  |  | saved "frame" of caller
          | saved THIS |  |
          | saved THAT | /
          --------------
SP, LCL ->
```

## Execute callee code

- Initialize local segment (save slots with value 0)

```
       | ...        |
       --------------
ARG -> | arg        | \
       | ...        |  | nArgs
       | arg        | /
       --------------
       | ret_addr   | \
       | saved LCL  |  |
       | saved ARG  |  | saved "frame" of caller
       | saved THIS |  |
       | saved THAT | /
       --------------
LCL -> | 0          | \
       | ...        | | nVars
       | 0          | /
       --------------
 SP ->
```

## Return from callee

- Push return value.

```
       | ...        | <- working stack of caller
       --------------
ARG -> | arg        | \
       | ...        |  | nArgs
       | arg        | /
       --------------
       | ret addr   | \
       | saved LCL  |  |
       | saved ARG  |  | saved "frame" of caller
       | saved THIS |  |
       | saved THAT | /
       --------------
LCL -> | 0          | \
       | ...        | | nVars
       | 0          | /
       --------------
       | ...        | <- working stack of callee
       | ret val    |
 SP ->
```

- Replace 1st slot in callee's ARG segment (argument 0, pushed by caller) with return value

```
       | ...        | <- working stack of caller
       --------------
ARG -> | ret val    | \
       | ...        |  | nArgs
       | arg        | /
       --------------
       | ret addr   | \
       | saved LCL  |  |
       | saved ARG  |  | saved "frame" of caller
       | saved THIS |  |
       | saved THAT | /
       --------------
LCL -> | local      | \
       | ...        | | nVars
       | local      | /
       --------------
       | ...        | <- working stack of callee
       | ret val    |
 SP ->
```

- Recycle memory used by caller (move SP, the space below return value is effectively wiped out).

```
       | ...        | <- working stack of caller
       --------------
ARG -> | ret val    |
 SP -> | arg 0      |
       | ...        |
       --------------
       | ret addr   | \
       | saved LCL  |  |
       | saved ARG  |  | saved "frame" of caller
       | saved THIS |  |
       | saved THAT | /
       --------------
LCL -> | local      |
       | ...        |
       | local      |
       --------------
       | ...        | <- working stack of callee
       | ret val    |
```

- Restore caller's segment pointers and jump to return address (using saved frame).

```
     | ...        | <- working stack of caller
     | ret val    |
SP ->
```
