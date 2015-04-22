#Hadley
queries = {

    'hadley':{
        "$and": [
            {
                "text": {
                    "$options": "i",
                    "$regex": "hostag"
                }
            },
            {
                "$or": [
                    {
                        "$and": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "radio"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "host"
                                }
                            }
                        ]
                    },
                    {
                        "$and": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "hadley"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "cafe"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    },

    #Lakemba
    'lakemba':{
        "$or": [
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "lakemba"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "waziristani"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "khost"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "idp"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "73000"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "molana"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "masscr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kattankudi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aftaliban"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "rocklea"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "prolifer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baitul"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cntr"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "baitulhuda"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "darinday"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baitul"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "ahmadiyya"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "safaaq"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "auspil"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "darinday"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "youknowitmakessens"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "safaaq"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "vigil"
                                }
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "noslm1"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "harem"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "has_blog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "basimafays"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "loudspeak"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "wayne_o__oo_"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rockhampton"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "meshal"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "mamnoonhussain"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "erdog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "alexan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "needham"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mamnoon"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kutusi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "lepep"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "anerood"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aner"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mauritius"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "valder"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "prasad"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "jugnauth"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "abdulhamid"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "erdog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "museveni"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "savar"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mausoleum"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "thehil"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "dilma"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "ilham"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "deubet"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "xxvi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "offcial"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "exac"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "alarabiya_eng"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "clergi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "jamalrifi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "yesha"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aguirr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pscus"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pes4job"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "binyamin"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "parachin"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bjpsc"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "gibbon"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "turi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "nawazourlead"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "revengu"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bjpsc"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "indgreek"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "55hh"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "gibbon"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "weign"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "museveni"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "alexan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aleksandr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "xxvi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "text": {
                    "$options": "i",
                    "$regex": "kurabi"
                }
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "rocklea"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "rocklea"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "bantah"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "kabinet|dalaman|bicara|pemerintahannya|segelintir|ancaman|banner10jutacom|hadapi|kerajaannya"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "rocklea"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "kurabi|cntr|baitulhuda|baiturahim|bargah|73000|lidcomb|sameshit"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "shriek"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "rhet|movingforward|banislam|rapecultur|islamophonia"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "urumqai"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "antiislamophobia|joulestour|afx"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "iridewithyou"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "faithinhuman|support|citizen|whingefest|aussi|muslim|ridewithyou"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "intoconnect"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "spiegel|kassam|telesur|salim"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "islamor"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "banislam|challengin|illridewithyouwhenyoudenounceandfightislamist|impeachobama|islamophonia"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "antimuslim"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "antimu|twister|jpnet|sayfi|rxd"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "idlenomor"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "withmuslim|telesur|meshal|nationbrand|37su"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "melalui"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "kerudung|mayorita|wellridewithyou|tengah|forumadmin48|menit|solidarita|tolak|kampany"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "darinday"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lal"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "laal|musharaf|babari|ajmer"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "25yr"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "javi|130th|recept|gulan|karkuk|sunnysideoflif|aicc"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "nabha"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "wesam|zaynudin|charkawi"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "huda"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "gurgaon|tarbiyati|ajmer|arson"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "newsdesk"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "proudmp|sendinglight|niaz|jama|ahmadiyya|ahmadiyyatim|walthamstow|ktn"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "arrahman"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "charkawi|1687|babari"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "safaaq"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "baitul"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "25yr|arrahman|lal|nabha|huda|newsdesk"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "73000"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lcci|masscr|kattankudi|molana|aftaliban|kcci"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "73000"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "molana"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "masscr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kattankudi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aftaliban"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "baitulhuda"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "rocklea"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "prolifer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cntr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "darinday"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lal"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "laal|musharaf|babari|ajmer"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "25yr"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "javi|130th|recept|gulan|karkuk|sunnysideoflif|aicc"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "nabha"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "wesam|zaynudin|charkawi"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "huda"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "gurgaon|tarbiyati|ajmer|arson"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "newsdesk"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "proudmp|sendinglight|niaz|jama|ahmadiyya|ahmadiyyatim|walthamstow|ktn"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "arrahman"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "charkawi|1687|babari"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "bargah"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bigplan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "arrahman"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mufi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nabha"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "safaaq"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "baitul"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "25yr|arrahman|lal|nabha|huda|newsdesk"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "73000"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lcci|masscr|kattankudi|molana|aftaliban|kcci"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "auspil"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "obl"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "talban"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "enuf"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pahari"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hve"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bt"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "candycrush"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "admittin"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "channeladvisor"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "targetin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "jehadi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "exten"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "k24"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "viewd"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "moradabad"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "joinin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "paintin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "indianmus"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "jabalpur"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nextyear"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "byazubuik"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aryblog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rightnow"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bhopal"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "tis"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "barbecu"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "christma"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "unstitch"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pdsa"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mlt"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "holiday"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "fesit"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "weheart"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nextyear"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "norzi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "tgifibook"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "chocolatecoveredanyth"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "holiday"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "beataz"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "footbal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "dctid"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mounti"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "buzzhorn"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rougedownund"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "ladylov"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "funtim"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "changer"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "papistan"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hoppin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mollana"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "twidaq"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mko"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "moradabad"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "followi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aussiesanta"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mailbag"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "abortionclin"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "pommi"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bast"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "standup4kid"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cheappoint"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rue"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "daft"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "headshot"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "laanati"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "72virgin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "snipe"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "inglori"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "keepharbaugh"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "footbal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "dctid"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "titanfal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rougedownund"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nerdlandia"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "funtim"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "changer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rtz"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "bargah"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "kurabi"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lakemba"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "meshal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "morningmaga"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "waziristani"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "khost"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lakemba"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "idp"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "73000"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "molana"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "masscr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kattankudi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lcci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "aftaliban"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "rocklea"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "prolifer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cntr"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "baitulhuda"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "ahmadiyya"
                                        }
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "noslm1"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "harem"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "has_blog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "basimafays"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "loudspeak"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "wayne_o__oo_"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rockhampton"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "sameshit"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "dzi"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "zamachowiec"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "chyba"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "atak"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nieznani"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "zamach"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "ktrym"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "zakoczi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "przetrzymywanych"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "bargah"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bigplan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "arrahman"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mufi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nabha"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "crmoni"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "robl"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "stn"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "per"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pssupt"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bfp"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pice"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mun"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "persnl"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "psupt"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lgu"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "advan"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "tej"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "budynku"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "leci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kokolojiiji"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "polaci"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "digita"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "zdjcia"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "janwar"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "dzi"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "ktrym|zamachowiec|zamach|zakoczi|nieznani|atak|przetrzymywanych"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "bargah"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "arrahman|bigplan|mufi|nabha"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "crmoni"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "psupt|bfp|persnl|lgu|robl|stn|per|mun|pssupt|pice"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "sameshit"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "noslm1|loudspeak|73000|waziristani"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "baiturahim"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "auspil|harem|noslm1|punchlin|73000|waziristani"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "advan"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "leci|zdjcia|budynku|polaci|digita"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "janwar"
                                                }
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "jumma"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "reclaimpakistan|2offer|khutba|youssef|reclaimyourmosqu|2gather|nabha"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "jumma"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "2offer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "nabha"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "reclaimpakistan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "reclaimyourmosqu"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "khutba"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "2gather"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "youssef"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "baiturahim"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "rocklea"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "lidcomb"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bargah"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baitul"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "prolifer"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cntr"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "baiturahim"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lal"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "ajmer|qisaa|youssef|laal|musharaf|ikhalidw|babari"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "huda"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "tarbiyati|ajmer|arson|gurgaon"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "newsdesk"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "niaz|ahmadiyyatim|walthamstow|ktn|ahmadiyya|proudmp|jama|sendinglight"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "25yr"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "sunnysideoflif|javi|recept|130th|gulan|karkuk|aicc"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "baitul"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "wesam"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hasanov"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "gumi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "2015goal"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "juma"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "saima"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "walkoutoft"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "fazal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "shahid"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kyun"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "sermon"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "jumma"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "bargah"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kurabi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "rocklea"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baitulhuda"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baiturahim"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "bigplan"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "darinday"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "safaaq"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mufi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "charkawi"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hasina"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hasanov"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "gumi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mausoleum"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "mahdi"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mohsin"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "murtada"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mufi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "shahi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kaaba"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "abdirahman"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "hasina"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "tashkent"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "silkroadtour"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mohamoud"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "somalia"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "abdi"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "mausoleum"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "baitul"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "sameshit"
                                                }
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "baitulhuda"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "huda"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "baiturahim"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kurabi"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "morningmaga"
                        }
                    },
                    {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "saveoursanta"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "thegist"
                                        }
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "opchocol"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "wearyourheartonyoursleev"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cmti"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "makepeacenotwar"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "preju"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "meshal"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "eightjarjam"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "illfightwithyou"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "sa4p"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "farahat22222"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "alhaf"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "5australia"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "saudistocksnew"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "pleasekillmelast"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "withmuslim"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "tweeg"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "queridosantayoquiero"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "itstopswithn"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cmti"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "meshal"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "jewish"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "solida"
                                        }
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "icv"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "solida"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "gregkelley"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "cecco"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "wisest"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "wewillridewithyou"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "kasunod"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "sydneyhostagecris"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "has_blog"
                                                }
                                            },
                                            {
                                                "text": {
                                                    "$options": "i",
                                                    "$regex": "webdevelop"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "appa"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "guardi"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    },

    #Flag
    'flag':{
        "$and": [
            {
                "text": {
                    "$options": "i",
                    "$regex": "flag"
                }
            },
            {
                "$or": [
                    {
                        "$and": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "isi"
                                }
                            },
                            {
                                "$or": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "shahada"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "isil"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "islamicst"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "islam"
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "$and": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "isil"
                                }
                            },
                            {
                                "$or": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "fla"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "isi"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    },
    #Airspace
    'airspace':{
        "$or": [
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "flight"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "vh"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "narita"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "changi"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "sydneyairport"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "frequentfly"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "plane"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "quanta"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "airasia8501"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "a330"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "heathrow"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "no"
                        }
                    },
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "fli"
                        }
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "nofli"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "bsale"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "mansonfamili"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "air"
                        }
                    },
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "space"
                        }
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "airspac"
                        }
                    },
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "rerout"
                        }
                    }
                ]
            }
        ]
    },

    #Suicide
    'suicide':{
        "$or": [
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "vest"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "bomber"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "jacket"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "unifo"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "fullkitwank"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "rtcs"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "itrtg"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "headband"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "dasher"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "belt"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "pact"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "radioconvo"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "convo"
                                }
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "clayhunt"
                                        }
                                    },
                                    {
                                        "$or": [
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "taxextend"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "lawri|waikiki|nomi|chinstrap|ayer|hr5771|maher|mwananchi|tlo"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "legaci"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "emonopoli|downfa|bloodpledg|bloodgift|9780062194466|welker"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "clayhunt"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "svcxo|peshawarpschool"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "dantonvill"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "copernicus|lacoba|urbanfantasi|arrison|bloodpledg|mikmaq|bloodgift|tetep|ficstori|tima"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "oreilli"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "gopackgo|hr5771|imitationgam|maher|ica|mwananchi|tlo"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "bashirbilourshahe"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "feastday|bomber|rococo|bashir|gotttpgo|bilour|iraqiarmi|apsac|shershah"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "rtcs"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "bombin|bomber|minyoon|peshawarpschool"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "itrtg"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "likefuckillridewithyou|bombin|minyoon|mayweath"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "$and": [
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "belt"
                                                        }
                                                    },
                                                    {
                                                        "text": {
                                                            "$options": "i",
                                                            "$regex": "mujah|convo|vest|radioconvo|suicidebelt"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "mujah"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "itrtg"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "rtcs"
                                }
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "vetsris"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "iava"
                                        }
                                    }
                                ]
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "suicidebelt"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "backpack"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "fashionfil"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "tracksuit"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "strap"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "adida"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "varna"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "burka"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "headband"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "$and": [
                    {
                        "text": {
                            "$options": "i",
                            "$regex": "suicid"
                        }
                    },
                    {
                        "$or": [
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "fidayeen"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "babangida"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "zaharau"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "martydom"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "homocid"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "uppgift"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "sucid"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "istishadi"
                                }
                            },
                            {
                                "text": {
                                    "$options": "i",
                                    "$regex": "fyra"
                                }
                            },
                            {
                                "$and": [
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "utrik"
                                        }
                                    },
                                    {
                                        "text": {
                                            "$options": "i",
                                            "$regex": "svd"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

}