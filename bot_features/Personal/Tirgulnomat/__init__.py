from bot_framework.Feature.FeatureSettings import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="תרגול נוסף", _type=FeatureType.REGULAR_FEATURE, emoji='🚨')
