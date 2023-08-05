import json
from functools import reduce
from pprint import pprint
from pprint import pformat
import logging 
import copy 

logging.basicConfig(format="%(asctime)s - %(name)s - [ %(levelname)s ] - [ %(filename)s:%(funcName)s():%(lineno)s ] - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def print_json(object):
    item = json.dumps(object, indent=4, sort_keys=True)
    return item

def tabify(response):

  table = ''

  # If we dont have converted JSON object, lets try to do that first
  if not isinstance(response, dict):
    try:
        response = json.loads(response)
    except Exception as e:
        raise Exception("Unable to convert response to JSON, reason: %s, please ensure you are sending either valid JSON or a python DICT to this method" % (e))

  print "tabify response: "
  pprint(response)
  print "\n\n"


  if response.get('aggregations'):
    tree = collectBucket(response['aggregations'])
    logger.debug('tabify tree: %s' % print_json(tree))
    table = flatten(tree);

  print "\n\nOUR TABLE:"
  pprint(table)
  return table

def collectBucket(node, stack=[]):
    logger.debug('## new instance ##')
    if not node:
        return
    
    logger.debug("collectBucket node:\n%s" % (print_json(node)))
    logger.debug("collectBucket node type: %s" % type(node))
    logger.debug("collectBucket stack:\n%s" % (print_json(stack)))

    keys = node.keys()
    logger.debug("collectBucket keys: %s" % (keys))

    for i, key in enumerate(keys):
        value = node[key]
        #newstack = copy.deepcopy(stack)
        stack.append(key)

        logger.debug("collectBucket loop key => %s,\nvalue => \n%s" % (key, print_json(value)))
        logger.debug("collectBucket loop stack value: %s" % print_json(stack))
        logger.debug("collectBucket loop value type: %s" % type(value))

        if isinstance(value, list):
            logger.debug("collectBucket is running extractTree()")
            logger.debug('## end instance ##')
            return extractTree(value, stack)

        if "buckets" in key and len(value.keys()) > 1:
            logger.debug("collectBuckets() - found a key => buckets")
            logger.debug('running extractBuckets() with a value of %s' % (print_json(value)))
            logger.debug('## end instance ##')
            return extractBuckets(value, stack)

        logger.debug('running collectBucket() with key = %s' % key)
        logger.debug('## end instance ##')
        return collectBucket(value, stack)
    

    logger.debug('## end instance ##')
    return node


def extractBuckets(buckets, stack):
    logger.debug("extractBuckets called:  buckets: %s, stack: %s" % (print_json(buckets),print_json(stack)))
    keys = buckets.keys() 
    logger.debug('extractBuckets() keys: %s' % print_json(keys))
    results = [] 
    for i, key in enumerate(buckets):
        value = buckets[key]

        currentObject = collectBucket({key: value})

        if not currentObject:
            continue 
    
        currentObject[ stack[ len(stack) - 2 ] ] = key 
        results.append(currentObject)
    return results 

# def mapBucket(bucket, stack):
#     tree = {}
#     logger.debug('## new instance ##')
#     logger.debug('bucket:\n%s' % (print_json(bucket)))
#     logger.debug('stack:\n%s' % (print_json(stack)))
#     keys = bucket.keys()
#     logger.debug('bucket keys:\n%s' % (print_json(keys)))
#     for key in keys:
#         value = bucket[key]
#         stack.append(key)

#         logger.debug("bucket key: %s" % key)
#         logger.debug("bucket value: %s" % value)
#         logger.debug("bucket stack: %s" % stack)

#         if isinstance(value, dict):
#             if 'value' in value:
#                 logger.debug('we found value in our value variable')
#                 value = value['value']
#             else:
#                 logger.debug('mapBuckets - running collectBucket()')
#                 value = collectBucket(value, stack)

#         logger.debug("our key == %s, stack == %s, value == %s" % (key, stack, value))

#         if key == 'key':
#             key = stack[ len(stack) - 2 ]
#             #key = stack[0]
#             logger.debug("key found, mapping key as '%s', with a value of '%s'" % (key,value))

#         logger.debug('tree:\n%s' % print_json(tree))

#         tree[key] = value

#     logger.debug('## end instance ##')
#     return tree

# def extractTree(buckets, stack):
#     logger.debug('## new instance ##')
#     logger.debug("extractTree buckets:\n %s" % (print_json(buckets)))
#     logger.debug("extractTree stack:\n %s" % (print_json(stack)))
#     items = []
#     for bucket in buckets:
#         logger.debug('extractTree bucket:\n%s' % print_json(bucket))
#         items.append(mapBucket(bucket, stack))
#     logger.debug('extractTree items: %s' % (print_json(items)))

#     logger.debug('## end instance ##')
#     return items

def extractTree(buckets, stack):
  tree = {}
  for bucket in buckets:
    for key in bucket.keys():
      value = bucket[key]
      if isinstance(value,dict):
        if "value" in value:
          value = value["value"]
        else: 
          stack = stack[:]
          stack.append(key)
          value = collectBucket(value, stack)
      if key == "key":
        key = stack[len(stack) - 2]
      tree[key] = value
  logger.debug('STACK:\n%s' % (print_json(stack)))
  logger.debug('TREE:\n%s' % (print_json(tree)))
  return tree

def flatten(tree, parentNode={}):
    if not tree:
        logger.debug('no tree found, returning a list')
        return []

    if not isinstance(tree, list):
        logger.debug('tree is not a list, converting it to one')
        tree = [tree]


    logger.debug('flatten tree:\n%s' % (print_json(tree))) 
    for k, childNode in tree.items():
        print k, 
        childNode
        #childNode.update(parentNode)

    for node in tree:
        childTrees = childNode.keys()

        logger.debug("childTrees: %s" % childTrees)

        if len(childTrees) > 0: 
            childTree = childTrees[0]
            if len(childTree) == 0:
                return node 
            return flatten(childTree, node)

    # if isinstance(tree, list):
    #     logger.debug("I got a list here")
    #     return tree
    # elif isinstance(tree, dict):
    #     childTrees = tree.keys()
    #     logger.debug("I found childTrees")
    #     childTrees_length = len(childTrees)
    #     logger.debug("childTrees length: %s" % childTrees_length)
    #     logger.debug("childTrees: %s" % childTrees)

    return tree
