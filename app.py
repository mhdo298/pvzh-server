import os

from flask import Flask, request
import json
from urllib.parse import urlparse
import time
import psycopg2
from entity_model import make_entity_model, make_rng

result = urlparse(os.environ['DATABASE_URL'])
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
connection = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=port)
connection.set_session(autocommit=True)

app = Flask(__name__)


@app.route('/matchmaking/v1/createChallenge', methods=['POST'])
def create_challenge():
    data = request.get_json()
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    challenged = data['o']
    faction = player_data["Faction"]
    cursor = connection.cursor()
    gid = challenger + challenged
    ogid = challenged + challenger
    seed_contribution = int.from_bytes(os.urandom(4))
    if faction == "Plants":
        cursor.execute(
            "INSERT INTO matches(game_id, plants_sd, rng_seed) VALUES(%(gid)s, %(sd)s, %(seed)s) ON CONFLICT (game_id) DO UPDATE SET plants_sd = excluded.plants_sd, rng_seed = matches.rng_seed # excluded.rng_seed",
            {
                "gid": gid,
                "sd": data['sd'],
                "seed": seed_contribution
            })
        cursor.execute(
            "INSERT INTO matches(game_id, plants_sd, rng_seed) VALUES(%(gid)s, %(sd)s, %(seed)s) ON CONFLICT (game_id) DO UPDATE SET plants_sd = excluded.plants_sd, rng_seed = matches.rng_seed # excluded.rng_seed",
            {
                "gid": ogid,
                "sd": data['sd'],
                "seed": seed_contribution
            })
    else:
        cursor.execute(
            "INSERT INTO matches(game_id, zombies_sd, rng_seed) VALUES(%(gid)s, %(sd)s, %(seed)s) ON CONFLICT (game_id) DO UPDATE SET zombies_sd = excluded.zombies_sd, rng_seed = matches.rng_seed # excluded.rng_seed",
            {
                "gid": gid,
                "sd": data['sd'],
                "seed": seed_contribution
            })
        cursor.execute(
            "INSERT INTO matches(game_id, zombies_sd, rng_seed) VALUES(%(gid)s, %(sd)s, %(seed)s) ON CONFLICT (game_id) DO UPDATE SET zombies_sd =  excluded.zombies_sd, rng_seed = matches.rng_seed # excluded.rng_seed",
            {
                "gid": ogid,
                "sd": data['sd'],
                "seed": seed_contribution
            })
    cursor.close()
    return {
        "ty": "JoinMatch",
        "eta": 0,
        "gi": challenged
    }


@app.route('/matchmaking/v1/joinMatch', methods=['POST'])
def join_match():
    pid = request.headers.get("eadp-persona-id")
    data = request.get_json()
    gi = data['gi']
    gid = pid + gi
    f = data["f"]
    cursor = connection.cursor()
    for _ in range(10):
        if f == "P":
            cursor.execute("SELECT zombies_sd FROM matches WHERE game_id = %s", [gid])
        else:
            cursor.execute("SELECT plants_sd FROM matches WHERE game_id = %s", [gid])
        sd = cursor.fetchone()
        if sd:
            payload = {
                "ty": "MatchReady",
                "sd": json.dumps(sd[0]),
                "gi": gi,
                "or": 50
            }
            break
    else:
        payload = {}
    cursor.close()
    return payload


@app.route('/pvp/v1/initGame', methods=['POST'])
def init_game():
    pid = request.headers.get("eadp-persona-id")
    data = request.get_json()
    gi = data['gi']
    gid = pid + gi
    cursor = connection.cursor()
    for _ in range(10):
        cursor.execute("DELETE FROM matches WHERE game_id = %s RETURNING plants_sd, zombies_sd, rng_seed", [gid])
        sd = cursor.fetchone()
        if sd:
            payload = {
                "entityModel": make_entity_model(sd[1], sd[0]),
                "rngSeedData": make_rng(sd[2]),
                "ec": "CgQgACgA",
                "sc": "",
                "tec": "",
                "cec": "EAE=",
                "ty": "InitialGameState",
                "plays": "{}",
                "gst": "0"
            }
            break
    else:
        payload = {}
    cursor.close()
    return payload


@app.route('/pvp/v1/pvpSendUpdate', methods=['POST'])
def pvp_send_update():
    data = request.get_json()
    gi = data['gi']
    l = data['playId']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO match_actions(receiver_id, l, payload) VALUES(%s, %s, %s)",
                   [gi, l, json.dumps(data)])
    cursor.close()
    return {
        "ty": "PlayResponse",
        "p": "Play"
    }


@app.route('/pvp/v1/pvpPoll', methods=['POST'])
def pvp_poll():
    pid = request.headers.get("eadp-persona-id")
    data = request.get_json()
    l = int(data['l'])
    cursor = connection.cursor()
    for _ in range(2):
        cursor.execute("DELETE FROM match_actions WHERE receiver_id = %s AND l = %s RETURNING payload",
                       [pid, l])
        sd = cursor.fetchone()
        if sd:
            payload = {
                "m": [json.dumps(sd[0])],
                "l": l + 1,
                "ty": "PvpMessages"
            }
            break
    else:
        payload = {
            "m": [],
            "l": 0,
            "ty": "PvpMessages"
        }
    cursor.close()
    return payload


@app.route('//plantsvszombiesheroes-android-live.json', methods=['GET'])
def load():
    return json.loads(
        """{
  "Properties": {
    "AllowCheatsDev": true,
    "AllowCheatsTest": true,
    "AllowCheatsLoadTest": true,
    "AllowCheatsProd": true,
    "AllowCheatsStage": true,
    "AntelopeSocialActive": true,
    "AssetBundlesEndpointProd": "https://pvzheroes-live.ecs.popcap.com/assetbundles",
    "CertainEloKValue": 60,
    "CertainEloKValue_Hi": 70,
    "CertainEloKValue_Lo": 50,
    "CertainPvPEloKValue": 60,
    "CertainPvPEloKValue_Hi": 70,
    "CertainPvPEloKValue_Lo": 50,
    "CopernicusUrlProd": "https://stats.popcap.com",
    "CraftingBaseUrlProd": "https://pvz-heroes.awspopcap.com/crafting/",
    "DraperCheat_AgeVerified": "",
    "DraperCheat_ClientTest": "",
    "DraperCheat_ClientVersion": "",
    "DraperCheat_ConsecutiveLosses": "",
    "DraperCheat_ConsecutiveWins": "",
    "DraperCheat_DaysSinceInstall": "",
    "DraperCheat_PWinsSinceSessionStart": "",
    "DraperCheat_PrchGoldPack": "",
    "DraperCheat_PrimarySide": "",
    "DraperCheat_PurchasedSecondaryBundle": "",
    "DraperCheat_PurchasedStarterBundle": "",
    "DraperCheat_SilverCardsOwned": "",
    "DraperCheat_TotGems": "",
    "DraperCheat_TotSpent": "",
    "DraperCheat_TotalPlantPvEWins": "",
    "DraperCheat_TotalZombiePvEWins": "",
    "DraperCheat_ZWinsSinceSessionStart": "",
    "DraperCheat_uuid": "",
    "DraperServerProd": "draper-pvzhprd.awspopcap.com",
    "EnableSwrve": true,
    "InitialEloKValue": 125,
    "InitialEloKValue_Hi": 150,
    "InitialEloKValue_Lo": 100,
    "InitialGemBalance": 400,
    "InitialGemBalance_B": 450,
    "InitialPvPEloKValue": 125,
    "InitialPvPEloKValue_Hi": 150,
    "InitialPvPEloKValue_Lo": 100,
    "InitialPveElo": 1600,
    "InitialPveElo_Hi": 1600,
    "InitialPveElo_Lo": 1600,
    "InstallNoteDaysFromInstall": 1,
    "IsArenaLocked": false,
    "LocalNoteCooldown": 6,
    "LocalNoteMaxHour": 22,
    "LocalNoteMinHour": 7,
    "LocalNoteSquelchList": "events",
    "MaxConcurrentDownloads_Standard": 8,
    "MinimumAppVersion": "1.50.2",
    "MinimumAppVersionHeaderTextKey": "AppOutOfDate_ThanksForPlaying_Header",
    "MinimumAppVersionTextKey": "UPDATE_REQUIRED",
    "MultiplayerBaseUrlProd": """+ os.environ['SERVER_URL']+""",
    "OocOfferCount": 2,
    "PersistenceBaseUrlProd": "https://pvz-heroes.awspopcap.com/persistence/",
    "AccountBaseUrlProd": "https://pvz-heroes.awspopcap.com/accnt/",
    "PvEProvisionPeriodLength": 14,
    "PvPGamesAtInitialK": 10,
    "PvPGamesAtInitialK_Hi": 10,
    "PvPGamesAtInitialK_Lo": 10,
    "QuestsBaseUrlProd": "https://pvz-heroes.awspopcap.com/quests/",
    "QuestsGamesAwayThreshold": 2,
    "QuestsWithNotes": "F_UnlockZombieHQ;F_UnlockPlantHero3;F_UnlockZombieHero2",
    "RefreshTimeLimit": 5,
    "SwrveApiKeyDev": "Pge8Oqxm0gNyZA4Tdodn",
    "SwrveApiKeyLoadTest": 2327,
    "SwrveApiKeyProd": "LmNlV6PosMdtv9HcAJQF",
    "SwrveApiKeyStage": "LmNlV6PosMdtv9HcAJQF",
    "SwrveGameIdDev": 2327,
    "SwrveGameIdProd": 2342,
    "SwrveGameIdStage": 2342,
    "TeslaBaseUrlProd": "https://m.help.ea.com",
    "TurnOffNarratives_HeroIntro": false,
    "TurnOffNarratives_HeroIntro_False": false,
    "TurnOffNarratives_HeroIntro_True": true,
    "TurnOffNarratives_PlantHQ": false,
    "TurnOffNarratives_PlantHQ_False": false,
    "TurnOffNarratives_PlantHQ_True": true,
    "TurnOffNarratives_Progression": false,
    "TurnOffNarratives_Progression_False": false,
    "TurnOffNarratives_Progression_True": true,
    "TurnOffNarratives_Prologue": false,
    "TurnOffNarratives_Prologue_False": false,
    "TurnOffNarratives_Prologue_True": true,
    "TurnOffNarratives_ZombieHQ": false,
    "TurnOffNarratives_ZombieHQ_False": false,
    "TurnOffNarratives_ZombieHQ_True": true,
    "UnsupportedIosDevices": "",
    "casualPvpLossSilver": 5,
    "casualPvpLossSilver_Hi": 5,
    "casualPvpLossSilver_Lo": 5,
    "casualPvpLossSilver_Me": 5,
    "casualPvpWinSilver": 10,
    "casualPvpWinSilver_Hi": 20,
    "casualPvpWinSilver_Lo": 5,
    "casualPvpWinSilver_Me": 10,
    "localnote_control": "NOTIFICATION_REMINDER",
    "localnote_group_a": "NOTIFICATION_REMINDER_A",
    "pveBossWinSilverDelta": 0,
    "pveBossWinSilverDelta_Hi": 0,
    "pveBossWinSilverDelta_Lo": -30,
    "pveBossWinSilverDelta_Me": 0,
    "pveLossSilverDelta": 0,
    "pveLossSilverDelta_Hi": 5,
    "pveLossSilverDelta_Lo": 0,
    "pveLossSilverDelta_Me": 0,
    "pveWinSilverDelta": 0,
    "pveWinSilverDelta_Hi": 5,
    "pveWinSilverDelta_Lo": -5,
    "pveWinSilverDelta_Me": 0,
    "rankedPvpLossSilver": 5,
    "rankedPvpLossSilver_Hi": 5,
    "rankedPvpLossSilver_Lo": 5,
    "rankedPvpLossSilver_Me": 5,
    "rankedPvpWinSilver": 20,
    "rankedPvpWinSilver_Hi": 30,
    "rankedPvpWinSilver_Lo": 10,
    "rankedPvpWinSilver_Me": 20,
    "pvpSendPlayRetryCount": 3,
    "pvpSendPlayRetryDelay": 5,
    "pvpPollRetryCount": 3,
    "pvpPollRetryDelay": 5,
    "PvpInactivityTime": 120,
    "AssetBundleDownloadTimeout": 30,
    "MaxConcurrentBackgroundDownloads_Standard": 1,
    "IdentityBaseUrlProd": "https://pvz-heroes.awspopcap.com/identity/",
    "casualPvpWinEventPoints": 15,
    "rankedPvpWinEventPoints": 15,
    "pveWinEventPoints": 10,
    "challengePvpWinEventPoints": 0,
    "RewardBaseUrlProd": "https://pvz-heroes.awspopcap.com/eaSquared/",
    "pveBossWinEventPoints": 10,
    "eventPointBoostOneMatch": 5,
    "eventPointBoostTwoMatches": 10,
    "PurchaseEventPointsSkuGroupName": "default",
    "eventsBoostMax": 1,
    "eventsBoostRecharge": 4,
    "PurchaseEventBoostTopOffSkuGroupName": "default",
    "Ea2RelativeRewardUrl": "v1/checkForRewards",
    "IncentivizedAdRewardPollerRetries": 2,
    "MaxMemoryInMegabytes": 350,
    "SupersonicPlacementRewardMappings": "DefaultRewardedVideo=default_reward_table",
    "WatchAdSoftLockExitTimeout": 10,
    "IncentivizedAdRewardPollerSecondsBetweenRetries": 2.5,
    "IncentivizedAdsDisallowedAndroidVersions": "17;18",
    "sparksToGemsRatio": "default",
    "sparksToGemsRatio_con": "convenience",
    "casualPvpWinGold": 15,
    "casualPvpLossGold": 5,
    "rankedPvpWinGold": 20,
    "rankedPvpLossGold": 5,
    "pveWinGold": 10,
    "pveLossGold": 5,
    "botdWinGold": 10,
    "botdLossGold": 5,
    "MaxAspectRatio": 1.86,
    "DailyBattleRetryDelaySeconds": 3600,
    "LogglyBaseUrlDev": "https://logs-01.loggly.com",
    "LogglyBaseUrlTest": "https://logs-01.loggly.com",
    "LogglyBaseUrlStage": "https://logs-01.loggly.com",
    "LogglyBaseUrlLoadTest": "https://logs-01.loggly.com",
    "LogglyBaseUrlProd": "https://popcap.loggly.com",
    "SeasonResetCountdownWindowInHours": 168
  },
  "Throttles": {
    "Crafting": {
      "value": 0.3
    },
    "Ecomm": {
      "value": 1
    },
    "ErrorLogging": {
      "value": 1
    },
    "Funnel": {
      "value": 0.3
    },
    "GameCurrency": {
      "value": 0.3
    },
    "Gameplay_PvE": {
      "value": 0.3
    },
    "Gameplay_PvP": {
      "value": 0.3
    },
    "HockeyAppErrors": {
      "value": 1
    },
    "Patch": {
      "value": 0.01
    },
    "PvP_Data": {
      "value": 1
    },
    "PvpBackgroundEvent": {
      "value": 0.3
    },
    "Quests": {
      "value": 0.3
    },
    "SessionStart": {
      "value": 1
    },
    "UIBehavior": {
      "value": 0.3
    },
    "gameplay_pvp_start": {
      "value": 0.3
    },
    "PvP_Match_Progress": {
      "value": 0.3
    },
    "Social": {
      "value": 0.3
    },
    "Transition": {
      "value": 0.3
    },
    "ScheduledEvents": {
      "value": 1
    },
    "FeaturedStoreOffers": {
      "value": 1
    },
    "AllStoreOffers": {
      "value": 1
    },
    "DraperInterstitials": {
      "value": 1
    },
    "GetActiveQuests": {
      "value": 1
    },
    "IncentivizedAds": {
      "value": 1
    },
    "IncentivizedAds2": {
      "value": 1
    },
    "StingerEvent": {
      "value": 0
    },
    "NewPlayersInitiallySelectZombieFactionInPvP": {
      "value": 0.5
    },
    "NewPlayersMustMakeFactionSelectionInPvP": {
      "value": 0
    },
    "ServerAuthoritativePvp": {
      "value": 0
    },
    "PackOpeningGroupByPack": {
      "value": 0
    },
    "FancyDeckSelector": {
      "value": 1
    },
    "FancyDeckSelectorFlippyTappy": {
      "value": 1
    },
    "MonitorMemory": {
      "value": 0
    },
    "DeckEditor": {
      "value": 1
    },
    "StoreVideoAds": {
      "value": 1
    },
    "HeroPurchase": {
      "value": 1
    },
    "ShowFullPveProgressionCounter": {
      "value": 1
    },
    "BattleOfTheDay": {
      "value": 1
    },
    "HeroLevels": {
      "value": 0
    },
    "Inbox": {
      "value": 1
    },
    "LogglyLevelVerbose": {
      "value": 0
    },
    "LogglyLevelDebug": {
      "value": 0
    },
    "LogglyLevelWarning": {
      "value": 0
    },
    "LogglyLevelError": {
      "value": 0.1
    },
    "LogglyLevelAssert": {
      "value": 0.1
    },
    "LogglyLevelException": {
      "value": 0.1
    },
    "PvpSeasonComplete": {
      "value": 1
    },
    "OfflineForMaintenance": {
      "value": 0
    },
    "SeasonResetCountdownTimer": {
      "value": 1
    },
    "SkipDailyBattleRetryTimerOnAdClose": {
      "value": 1
    },
    "PackOpeningDeckRecipes": {
      "value": 1
    },
    "RandomBattles": {
      "value": 1
    },
    "ReportIncentivizedAdDiagnosticInfo": {
      "value": 0.01
    },
    "Credits": {
      "value": 1
    }
  }
}
""")


@app.route('/seasons/v1/history', methods=['GET'])
def get_seasons_history():
    return {
        "seasons": {},
        "version": None,
        "id": request.headers.get("eadp-persona-id")
    }


@app.route('/pvp/v1/playerPvpData', methods=['GET'])
def get_player_pvp_data():
    return {
        "gamesPlayed": 0,
        "stars": 0,
        "id": request.headers.get("eadp-persona-id"),
        "version": None,
        "season": "season_73",
        "wins": 0,
        "losses": 0,
        "mmr": 1600,
        "rank": 50,
        "streakBonus": 0,
        "wonLastGame": False
    }


if __name__ == '__main__':
    app.run()
