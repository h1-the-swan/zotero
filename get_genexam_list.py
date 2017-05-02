import sys, os, time
from datetime import datetime
from timeit import default_timer as timer

ZOTERO_LIBRARY_ID = os.environ.get('ZOTERO_LIBRARY_ID')
ZOTERO_LIBRARY_TYPE = os.environ.get('ZOTERO_LIBRARY_TYPE') or 'user'
ZOTERO_API_KEY = os.environ.get('ZOTERO_API_KEY')

from pyzotero import zotero

import logging
logging.basicConfig(format='%(asctime)s %(name)s.%(lineno)d %(levelname)s : %(message)s',
        datefmt="%H:%M:%S",
        level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = logging.getLogger('__main__').getChild(__name__)

def load_zotero(library_id=ZOTERO_LIBRARY_ID,
                library_type=ZOTERO_LIBRARY_TYPE,
                api_key=ZOTERO_API_KEY):
    zot = zotero.Zotero(library_id, library_type, api_key)
    return zot

def get_genexam_coll_id(zot, coll_name='general_exam'):
    colls = zot.collections()
    genexam_coll_id = ''
    for coll in colls:
        this_coll_name = coll['data'].get('name')
        if this_coll_name == coll_name:
            genexam_coll_id = coll['data']['key']
            break
    if not genexam_coll_id:
        raise RuntimeError('Could not find Collection ID for {}'.format(coll_name))
    return genexam_coll_id


def main(args):
    zot = load_zotero()
    genexam_coll_id = get_genexam_coll_id(zot, coll_name='general_exam')
    subcolls = zot.collections_sub(genexam_coll_id)
    subcoll_items = {}
    for subcoll in subcolls:
        subcoll = subcoll['data']
        k = subcoll['key']
        subcoll_items[k] = {'name': subcoll['name']}
        subcoll_items[k]['items'] = zot.collection_items(k)
    ###
    logger.debug(subcoll_items)


if __name__ == "__main__":
    total_start = timer()
    logger = logging.getLogger(__name__)
    logger.info(" ".join(sys.argv))
    logger.info( '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) )
    import argparse
    parser = argparse.ArgumentParser(description="get general exam list from zotero library")
    parser.add_argument("--debug", action='store_true', help="output debugging info")
    global args
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('debug mode is on')
    else:
        logger.setLevel(logging.INFO)
    main(args)
    total_end = timer()
    logger.info('all finished. total time: {:.2f} seconds'.format(total_end-total_start))
