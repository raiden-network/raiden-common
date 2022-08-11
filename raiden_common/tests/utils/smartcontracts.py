import os

from solcx import compile_files
from web3.contract import Contract
from web3.types import TxReceipt

from raiden_common.network.rpc.client import JSONRPCClient
from raiden_common.utils.typing import Any, Dict, T_TransactionHash, TokenAmount, Tuple
from raiden_contracts.contract_manager import ContractManager


def is_tx_hash_bytes(bytes_: Any) -> bool:
    """
    Check wether the `bytes_` is a bytes object with the correct number of bytes
    for a transaction,
    but do not query any blockchain node to check for transaction validity.
    """
    if isinstance(bytes_, T_TransactionHash):
        return len(bytes_) == 32
    return False


def deploy_token(
    deploy_client: JSONRPCClient,
    contract_manager: ContractManager,
    initial_amount: TokenAmount,
    decimals: int,
    token_name: str,
    token_symbol: str,
    token_contract_name: str,
) -> Contract:
    contract_proxy, _ = deploy_client.deploy_single_contract(
        contract_name=token_contract_name,
        contract=contract_manager.get_contract(token_contract_name),
        constructor_parameters=(initial_amount, decimals, token_name, token_symbol),
    )
    return contract_proxy


def compile_files_cwd(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """change working directory to contract's dir in order to avoid symbol
    name conflicts"""
    # get root directory of the contracts
    compile_wd = os.path.commonprefix(args[0])
    # edge case - compiling a single file
    if os.path.isfile(compile_wd):
        compile_wd = os.path.dirname(compile_wd)
    # remove prefix from the files
    if compile_wd[-1] != "/":
        compile_wd += "/"
    file_list = [x.replace(compile_wd, "") for x in args[0]]
    cwd = os.getcwd()
    try:
        os.chdir(compile_wd)
        compiled_contracts = compile_files(
            source_files=file_list,
            # We need to specify output values here because py-solc by default
            # provides them all and does not know that "clone-bin" does not exist
            # in solidity >= v0.5.0
            output_values=["abi", "asm", "ast", "bin", "bin-runtime"],
            **kwargs,
        )
    finally:
        os.chdir(cwd)
    return compiled_contracts


def compile_test_smart_contract(name: str) -> Tuple[Dict[str, Any], str]:
    """Compiles the smart contract `name`."""
    contract_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "smart_contracts", f"{name}.sol")
    )
    contracts = compile_files_cwd([contract_path])
    contract_key = os.path.basename(contract_path) + ":" + name

    return contracts, contract_key


def deploy_rpc_test_contract(
    deploy_client: JSONRPCClient, name: str
) -> Tuple[Contract, TxReceipt]:

    contracts, contract_key = compile_test_smart_contract(name)

    contract_proxy, receipt = deploy_client.deploy_single_contract(
        contract_name=name, contract=contracts[contract_key]
    )

    return contract_proxy, receipt


def get_list_of_block_numbers(item):
    """Creates a list of block numbers of the given list/single event"""
    if isinstance(item, list):
        return [element["blockNumber"] for element in item]

    if isinstance(item, dict):
        block_number = item["blockNumber"]
        return [block_number]

    return []
