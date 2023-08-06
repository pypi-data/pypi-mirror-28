from django_eth_events.models import Daemon, Block
from django_eth_events.web3_service import Web3Service
from django_eth_events.utils import remove_0x_head


class UnknownBlockReorg(Exception):
    pass

class NoBackup(Exception):
    def __init__(self, message, errors):
        super(NoBackup, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


def check_reorg():
    web3 = Web3Service().web3
    saved_block_number = Daemon.get_solo().block_number
    current_block_number = web3.eth.blockNumber

    if current_block_number >= saved_block_number:
        # check last saved block hash haven't changed
        blocks = Block.objects.all().order_by('-block_number')
        if blocks.count():
            # check if there was reorg
            for block in blocks:
                try:
                    node_block_hash = remove_0x_head(web3.eth.getBlock(block.block_number)['hash'])
                except:
                    raise UnknownBlockReorg
                if block.block_hash == node_block_hash:
                    # if is last saved block, no reorg
                    if block.block_number == saved_block_number:
                        return False, None
                    else:
                        # there was a reorg from a saved block, we can do rollback
                        return True, block.block_number

            # Exception, no saved history enough
            errors = {
                'saved_block_number': saved_block_number,
                'current_block_number': current_block_number,
                'las_saved_block_hash': blocks[0].block_hash
            }
            raise NoBackup(message='Not enough backup blocks, reorg cannot be rollback', errors=errors)

        else:
            # No backup data
            return False, None
    else:
        # check last common block hash haven't changed
        blocks = Block.objects.filter(block_number__lte=current_block_number).order_by('-block_number')
        if blocks.count():
            # check if there was reorg
            for block in blocks:
                try:
                    node_block_hash = remove_0x_head(web3.eth.getBlock(block.block_number)['hash'])
                except:
                    raise UnknownBlockReorg
                if block.block_hash == node_block_hash:
                    # if is last saved block, no reorg
                    if block.block_number == saved_block_number:
                        return False, None
                    else:
                        # there was a reorg from a saved block, we can do rollback
                        return True, block.block_number

            # Exception, no saved history enough
            errors = {
                'saved_block_number': saved_block_number,
                'current_block_number': current_block_number,
                'las_saved_block_hash': blocks[0].block_hash
            }
            raise NoBackup(message='Not enough backup blocks, reorg cannot be rollback', errors=errors)
        else:
            # No backup data
            return False, None
