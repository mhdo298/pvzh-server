import gzip
import os

from flask import Blueprint, redirect, request, make_response
from utils import r, assets
from gzip import compress

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')
mod_files = ['atlastagged/cardfaces_solar', 'autotagged/00005117150aa7244a2a79131a2a354a',
             'autotagged/00608d1c78ccba748a1c78d083e5e00a', 'autotagged/00781a37e3ad9434aabbd94ce2d10052',
             'autotagged/0088d63fdcdf1f249acd0d3f04e832a7', 'autotagged/011ff7f4f196c5e4bb76fa3596973525',
             'autotagged/01adc29c91063bc41ad1ca8e0e5ce1cf', 'autotagged/02a6386ace9444b0cba311a44585711b',
             'autotagged/02c94d7ebae2e2e45958e9fe2985b5b9', 'autotagged/03541dec7eccbe046a139873e2125d74',
             'autotagged/038985a27cdc7ae42841b42cc8320d5f', 'autotagged/03b5b49df7e28ca4b95a1d1f3c2c1c6e',
             'autotagged/03ce9ed1539ccff439ee76b9cbb170fa', 'autotagged/04e93565bef7ba34195366f5abc91ad9',
             'autotagged/053317fe6efea7648bd7826ee1e0d305', 'autotagged/0688d3398aeb14d119822a2fbbd347b1',
             'autotagged/0730566efa0de774eabe303a5e6b39af', 'autotagged/0778afd60e48b1347a5b7ac2b17d2f9d',
             'autotagged/08ac29c66bc5e4745bb23b04b4f81ff1', 'autotagged/08f5ded590832f647b00995a308aee30',
             'autotagged/08fff5dc22c7e654face3bdc04bd433e', 'autotagged/0903983a61db4446cb2d25547135dc76',
             'autotagged/0953390556d79304e86c2386de3598db', 'autotagged/0bb850317d313204290f6b9815049e69',
             'autotagged/0f5bc34124405114a8c7878a53fb404a', 'autotagged/134e8c00588dcf84a9e6364c15ac54f3',
             'autotagged/1394716b251c3404c9bbd26df4e1082b', 'autotagged/19280c869b623624998ed52454f61275',
             'autotagged/1a7121cac66b9034b9a11d214189aebc', 'autotagged/1b8f60b644a63ef478f0a172d889a0e7',
             'autotagged/205974c088b7c4a7dac393c6283e0bf9', 'autotagged/2070aa7a983a0b14eadbb0aca9e847ff',
             'autotagged/208fc7c05a9ef0a44962d240474e7e6d', 'autotagged/261c59a4c15b1d84185edf4282c0899e',
             'autotagged/2a9de134fd471467e990586650123114', 'autotagged/2ce69811c78004d1793379d11c683d96',
             'autotagged/49c2ed2476eda1f46a2ca4c212fe7f11', 'autotagged/4e043980c00974704b6d9573aa7b2918',
             'autotagged/51abd81c663c42c4f8c047c496cc5e47', 'autotagged/5d7c1ae54d8c62042a2615bb97a71f68',
             'autotagged/6d76caa6f42b5d04fb53b6e6dd36de08', 'autotagged/6df2f6b3e96accd4f93c44741558f6e1',
             'autotagged/73f16fe08d742cf4d86dfe28e08fd3d6', 'autotagged/7f013c62500fd2645a9f6c378fd59880',
             'autotagged/83194126b3bb84f76b15db7b348c68aa', 'autotagged/8d2e24e5b338161418be85985bb6e279',
             'autotagged/9abc406bc66ad204e9ff646702e62087', 'autotagged/9ee488c0dc3435c47b7f4742da962541',
             'autotagged/a34c352725264429ba5b9f83efbd102b', 'autotagged/a86107406238f7d46ad9a39c90cdec46',
             'autotagged/a9a9dcb1f463c4e29a3a7701994c15f8', 'autotagged/ab600bb30092942c5bfddd686f4be083',
             'autotagged/d55a98c062062e54e836638bae4a6764', 'autotagged/e89b39f08d38348a6b1ed0c9b19052fc',
             'cards/card_data', 'config/ai', 'config/progression/plant', 'config/progression/zombie_config_progression',
             'data_assets', 'deck_recipes/recipe_decks', 'fonts/inline_text_tag', 'loc/en', 'loc/es',
             'scrolling_textures']


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path: str):
    comps = '/'.join(path.split('/')[2:])
    if comps in mod_files:
        return redirect(os.environ['BUCKET_PATH'] + comps)
    if path.endswith('/manifest_version'):
        version = r.incr('manifest')
        return str(version)
    if path.endswith('/AssetPathsManifest'):
        version = r.get('manifest')
        content = gzip.compress(assets
                                .replace(b'"CARD_DATA_VERSION"', version)
                                .replace(b'"DATA_ASSETS_VERSION"', version)
                                .replace(b'"INLINE_TEXT_TAG_VERSION"', version)
                                .replace(b'"EN_VERSION"', version)
                                )
        response = make_response(content)
        response.headers['Content-length'] = len(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response
    # if 'If-None-Match' in request.headers.keys():
    #     return make_response('', 304)
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
