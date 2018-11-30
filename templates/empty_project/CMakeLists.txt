cmake_minimum_required(VERSION 3.5)
project(${CONTRACT_NAME}_example VERSION 1.0.0)

find_package(eosio.cdt)

### Generate the wasm and abi
add_contract( ${CONTRACT_NAME} ${CONTRACT_NAME} src/${CONTRACT_NAME}.cpp )

### add the path to where the ricardian contracts/clauses are found
target_compile_options( ${CONTRACT_NAME}.wasm PUBLIC -R${CMAKE_CURRENT_SOURCE_DIR}/resources )