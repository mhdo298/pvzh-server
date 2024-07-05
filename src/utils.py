import base64
import os
import time
from collections import OrderedDict

import blackboxprotobuf
from flask import request
from redis import Redis

r = Redis.from_url(os.environ['REDIS_URL'])

def root():
    return request.root_url[:-1].replace('http:', 'https:')

def get_id():
    return request.headers.get("eadp-persona-id")


def it_should_be_there_soon(key):
    for _ in range(20):
        sd = r.get(key)
        if sd is not None:
            return sd
        time.sleep(0.25)
    return b''


entity_model_typedef = OrderedDict({
    '1': OrderedDict({
        'name': '',
        'type': 'message',
        'field_order': ['1', '1',
                        '1', '1',
                        '1', '1',
                        '1', '1',
                        '1', '1',
                        '1', '1',
                        '1', '1',
                        '1',
                        '2'],
        'seen_repeated': True,
        'message_typedef': OrderedDict(
            {
                '1': OrderedDict({
                    'name': '',
                    'type': 'message',
                    'field_order': [
                        '3'],
                    'seen_repeated': True,
                    'message_typedef': OrderedDict(
                        {
                            '1': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '4'],
                                'message_typedef': OrderedDict({
                                    '4': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '12': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '13': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '16': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '28': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '35': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '66': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        }),
                                    '69': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [],
                                            'message_typedef': OrderedDict()
                                        })
                                })
                            }),
                            '3': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '2', '3'],
                                'message_typedef': OrderedDict({
                                    '2': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '3': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        })
                                })
                            }),
                            '10': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1', '2'],
                                'message_typedef': OrderedDict({
                                    '1': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '2': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        })
                                })
                            }),
                            '11': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [
                                        '1'],
                                    'message_typedef': OrderedDict(
                                        {
                                            '1': OrderedDict({
                                                'name': '',
                                                'type': 'int'
                                            })
                                        })
                                }),
                            '13': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [],
                                    'message_typedef': OrderedDict()
                                }),
                            '14': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [
                                        '1'],
                                    'message_typedef': OrderedDict(
                                        {
                                            '1': OrderedDict({
                                                'name': '',
                                                'type': 'int'
                                            })
                                        })
                                }),
                            '16': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1', '2', '3'],
                                'message_typedef': OrderedDict({
                                    '1': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '2': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '3': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        })
                                })
                            }),
                            '20': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1'],
                                'message_typedef': OrderedDict(
                                    {
                                        '1': OrderedDict({
                                            'name': '',
                                            'type': 'int'
                                        })
                                    })
                            }),
                            '21': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [
                                        '1'],
                                    'message_typedef': OrderedDict(
                                        {
                                            '1': OrderedDict({
                                                'name': '',
                                                'type': 'int'
                                            })
                                        })
                                }),
                            '24': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1', '2'],
                                'message_typedef': OrderedDict({
                                    '1': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'string'
                                        }),
                                    '2': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'string'
                                        })
                                })
                            }),
                            '26': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [],
                                    'message_typedef': OrderedDict()
                                }),
                            '28': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1', '1', '1',
                                    '1'],
                                'message_typedef': OrderedDict({
                                    '1': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [
                                                '1',
                                                '2'],
                                            'seen_repeated': True,
                                            'message_typedef': OrderedDict(
                                                {
                                                    '1': OrderedDict(
                                                        {
                                                            'name': '',
                                                            'type': 'int'
                                                        }),
                                                    '2': OrderedDict(
                                                        {
                                                            'name': '',
                                                            'type': 'int'
                                                        })
                                                })
                                        })
                                })
                            }),
                            '29': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1'],
                                'message_typedef': OrderedDict(
                                    {
                                        '1': OrderedDict({
                                            'name': '',
                                            'type': 'int'
                                        })
                                    })
                            }),
                            '32': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': ['1',
                                                    '2'],
                                    'message_typedef': OrderedDict(
                                        {
                                            '1': OrderedDict({
                                                'name': '',
                                                'type': 'message',
                                                'field_order': [
                                                    '1'],
                                                'message_typedef': OrderedDict({
                                                    '1': OrderedDict(
                                                        {
                                                            'name': '',
                                                            'type': 'int'
                                                        })
                                                })
                                            }),
                                            '2': OrderedDict(
                                                {
                                                    'name': '',
                                                    'type': 'int'
                                                })
                                        })
                                }),
                            '33': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1', '2', '3',
                                    '4'],
                                'message_typedef': OrderedDict({
                                    '1': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'message',
                                            'field_order': [
                                                '1',
                                                '1',
                                                '1'],
                                            'message_typedef': OrderedDict(
                                                {
                                                    '1': OrderedDict(
                                                        {
                                                            'name': '',
                                                            'type': 'message',
                                                            'field_order': [
                                                                '1',
                                                                '2'],
                                                            'seen_repeated': True,
                                                            'message_typedef': OrderedDict(
                                                                {
                                                                    '1': OrderedDict(
                                                                        {
                                                                            'name': '',
                                                                            'type': 'int'
                                                                        }),
                                                                    '2': OrderedDict(
                                                                        {
                                                                            'name': '',
                                                                            'type': 'int'
                                                                        })
                                                                })
                                                        })
                                                })
                                        }),
                                    '2': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '3': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        }),
                                    '4': OrderedDict(
                                        {
                                            'name': '',
                                            'type': 'int'
                                        })
                                })
                            }),
                            '34': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1'],
                                'message_typedef': OrderedDict(
                                    {
                                        '1': OrderedDict({
                                            'name': '',
                                            'type': 'int'
                                        })
                                    })
                            }),
                            '35': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [
                                        '1'],
                                    'message_typedef': OrderedDict(
                                        {
                                            '1': OrderedDict({
                                                'name': '',
                                                'type': 'int'
                                            })
                                        })
                                }),
                            '37': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1'],
                                'message_typedef': OrderedDict(
                                    {
                                        '1': OrderedDict({
                                            'name': '',
                                            'type': 'int'
                                        })
                                    })
                            }),
                            '54': OrderedDict({
                                'name': '',
                                'type': 'message',
                                'field_order': [
                                    '1'],
                                'message_typedef': OrderedDict(
                                    {
                                        '1': OrderedDict({
                                            'name': '',
                                            'type': 'string'
                                        })
                                    })
                            }),
                            '55': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [],
                                    'message_typedef': OrderedDict()
                                }),
                            '68': OrderedDict(
                                {
                                    'name': '',
                                    'type': 'message',
                                    'field_order': [
                                        '2'],
                                    'message_typedef': OrderedDict({
                                        '2': OrderedDict(
                                            {
                                                'name': '',
                                                'type': 'message',
                                                'field_order': [
                                                    '1',
                                                    '2'],
                                                'message_typedef': OrderedDict(
                                                    {
                                                        '1': OrderedDict(
                                                            {
                                                                'name': '',
                                                                'type': 'message',
                                                                'field_order': [
                                                                    '1'],
                                                                'message_typedef': OrderedDict(
                                                                    {
                                                                        '1': OrderedDict(
                                                                            {
                                                                                'name': '',
                                                                                'type': 'int'
                                                                            })
                                                                    })
                                                            }),
                                                        '2': OrderedDict(
                                                            {
                                                                'name': '',
                                                                'type': 'int'
                                                            })
                                                    })
                                            })
                                    })
                                })
                        })
                }),
                '2': OrderedDict({
                    'name': '',
                    'type': 'int'
                })
            })
    }),
    '2': OrderedDict({
        'name': '',
        'type': 'int'
    })
})
rng_typedef = OrderedDict({
    '1': OrderedDict({
        'name': '',
        'type': 'int'
    }),
    '2': OrderedDict({
        'name': '',
        'type': 'int'
    })
})
mask = ~(-1 << 60)


def make_entity_model(sd1, sd2):
    if sd1["Faction"] == "Zombies":
        zombie_sd = sd1
        plant_sd = sd2
    else:
        plant_sd = sd1
        zombie_sd = sd2

    zombie_id = zombie_sd["PlayerId"]
    zombie_hero = {
        "1": zombie_sd['HeroId'],
        "2": zombie_sd['HeroAssetId']
    }
    zombie_main_deck = [y for x in zombie_sd['Deck']['main'] for y in
                        [{
                            "1": -1,
                            "2": int(x)
                        }] * zombie_sd['Deck']['main'][x]]
    zombie_super_deck = [y for x in zombie_sd['Deck']['super'] for y in
                         [{
                             "1": -1,
                             "2": int(x)
                         }] * zombie_sd['Deck']['super'][x]]
    plant_id = plant_sd["PlayerId"]
    plant_hero = {
        "1": plant_sd['HeroId'],
        "2": plant_sd['HeroAssetId']
    }
    plant_main_deck = [y for x in plant_sd['Deck']['main'] for y in
                       [{
                           "1": -1,
                           "2": int(x)
                       }] * plant_sd['Deck']['main'][x]]
    plant_super_deck = [y for x in plant_sd['Deck']['super'] for y in
                        [{
                            "1": -1,
                            "2": int(x)
                        }] * plant_sd['Deck']['super'][x]]
    max_hand = 15
    max_health = 50
    if '1005433873053' in [plant_id, zombie_id]:
        max_hand = 10
        max_health = 20
    model_json = {
        "1": [
            {
                "1": [
                    {
                        "54": {
                            "1": zombie_id
                        }
                    }, {
                        "68": {
                            "2": {
                                "1": {
                                    "1": max_health  # initial health?
                                },
                                "2": 0
                            }
                        }
                    }, {
                        "37": {
                            "1": 0
                        }
                    },
                    {
                        "1": {
                            "28": {}
                        }
                    }, {
                        "11": {
                            "1": 1
                        }
                    }, {
                        "35": {
                            "1": 2
                        }
                    }, {
                        "21": {
                            "1": 3
                        }
                    }, {
                        "14": {
                            "1": 4
                        }
                    },
                    {
                        "32": {
                            "1": {
                                "1": 1
                            },
                            "2": 0
                        }
                    }, {
                        "33": {  # block meter chances
                            "1": {
                                "1": [{
                                    "1": 33,
                                    "2": 10
                                }, {
                                    "1": 34,
                                    "2": 20
                                }, {
                                    "1": 33,
                                    "2": 30
                                }]
                            },
                            "2": 2147483647,  # SuperBlockHealthThreshold?
                            "3": 0,
                            "4": 80  # block meter max
                        }
                    }, {
                        "55": {}
                    }, {
                        "1": {
                            "35": {}
                        }
                    }, {
                        "1": {
                            "66": {}
                        }
                    }, {
                        "1": {
                            "69": {}
                        }
                    },
                    {
                        "24": zombie_hero
                    }],
                "2": 0
            },
            {
                "1": [{
                    "10": {
                        "1": 0,
                        "2": 1
                    }
                }, {
                    "28": {
                        "1": zombie_main_deck
                    }
                }],
                "2": 1
            },
            {
                "1": [{
                    "34": {
                        "1": 1
                    }
                }, {
                    "28": {
                        "1": zombie_super_deck
                    }
                }],
                "2": 2
            }, {
                "1": [{
                    "20": {
                        "1": max_hand  # max hand size?
                    }
                }, {
                    "37": {
                        "1": 0
                    }
                }, {
                    "16": {
                        "1": 4,  # initial cards?
                        "2": 1,  # initial superpowers?
                        "3": 1  # cards per turn?
                    }
                }, {
                    "29": {
                        "1": 0
                    }
                },
                    {
                        "11": {
                            "1": 1
                        }
                    }, {
                        "35": {
                            "1": 2
                        }
                    }],
                "2": 3
            }, {
                "1": [{
                    "13": {}
                }],
                "2": 4
            }, {
                "1": [{
                    "54": {
                        "1": plant_id
                    }
                }, {
                    "68": {
                        "2": {
                            "1": {
                                "1": max_health
                            },
                            "2": 0
                        }
                    }
                }, {
                    "37": {
                        "1": 0
                    }
                },
                    {
                        "1": {
                            "16": {}
                        }
                    }, {
                        "11": {
                            "1": 6
                        }
                    }, {
                        "35": {
                            "1": 7
                        }
                    }, {
                        "21": {
                            "1": 8
                        }
                    }, {
                        "14": {
                            "1": 9
                        }
                    },
                    {
                        "32": {
                            "1": {
                                "1": 1
                            },
                            "2": 0
                        }
                    }, {
                        "33": {
                            "1": {
                                "1": [{
                                    "1": 33,
                                    "2": 10
                                }, {
                                    "1": 34,
                                    "2": 20
                                }, {
                                    "1": 33,
                                    "2": 30
                                }]
                            },
                            "2": 2147483647,
                            "3": 0,
                            "4": 80
                        }
                    }, {
                        "55": {}
                    }, {
                        "1": {
                            "35": {}
                        }
                    }, {
                        "1": {
                            "66": {}
                        }
                    }, {
                        "1": {
                            "69": {}
                        }
                    },
                    {
                        "24": plant_hero
                    }],
                "2": 5
            },
            {
                "1": [{
                    "10": {
                        "1": 0,
                        "2": 1
                    }
                }, {
                    "28": {
                        "1": plant_main_deck
                    }
                }],
                "2": 6
            },
            {
                "1": [{
                    "34": {
                        "1": 1
                    }
                }, {
                    "28": {
                        "1": plant_super_deck
                    }
                }],
                "2": 7
            },
            {
                "1": [{
                    "20": {
                        "1": max_hand
                    }
                }, {
                    "37": {
                        "1": 0
                    }
                }, {
                    "16": {
                        "1": 4,
                        "2": 1,
                        "3": 1
                    }
                }, {
                    "29": {
                        "1": 5
                    }
                },
                    {
                        "11": {
                            "1": 6
                        }
                    }, {
                        "35": {
                            "1": 7
                        }
                    }],
                "2": 8
            }, {
                "1": [{
                    "13": {}
                }],
                "2": 9
            }, {
                "1": [{
                    "26": {}
                }],
                "2": 10
            },

            {
                "1": [{
                    "3": {
                        "2": 0,
                        "3": -1
                    }
                }, {
                    "1": {
                        "13": {}
                    }
                }],
                "2": 11
            },
            {
                "1": [{
                    "3": {
                        "2": 1,
                        "3": -1
                    }
                }, {
                    "1": {
                        "12": {}
                    }
                }],
                "2": 12
            },
            {
                "1": [{
                    "3": {
                        "2": 2,
                        "3": -1
                    }
                }, {
                    "1": {
                        "12": {}
                    }
                }],
                "2": 13
            },
            {
                "1": [{
                    "3": {
                        "2": 3,
                        "3": -1
                    }
                }, {
                    "1": {
                        "12": {}
                    }
                }],
                "2": 14
            },
            {
                "1": [{
                    "3": {
                        "2": 4,
                        "3": -1
                    }
                }, {
                    "1": {
                        "4": {}
                    }
                }],
                "2": 15
            }],
        "2": 16
    }
    return base64.b64encode(blackboxprotobuf.encode_message(model_json, entity_model_typedef)).decode()


def make_rng(rng_seed):
    return base64.b64encode(blackboxprotobuf.encode_message({
        '1': rng_seed & mask,
        '2': 0
    }, rng_typedef)).decode()
