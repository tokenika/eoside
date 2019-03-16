
## First step: declare and define the smart contract

A smart contract is declared in its CPP header file, and it is defined in its source file.
Let us edit the header file.

The header includes 'eosiolib', containing the smart-contract API.

The green squiggle underneath an '#include' signal a deficiency. W can see what is missing:
it is 'boost/limits.hpp'.

We have localized the dependency. In our system it is '/home/cartman/opt/boost/include/boost/limits.hpp'.

The '#include' directive is clean now.
