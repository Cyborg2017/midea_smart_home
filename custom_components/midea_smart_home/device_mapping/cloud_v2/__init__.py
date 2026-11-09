"""Cloud_v2 (Thing Model V2) device mappings.

Kept separate from the LAN device mappings: only devices recognised through
the Midea cloud Thing Model use these files.
"""
from importlib import import_module
from pathlib import Path
import logging

from .. import format_model

_LOGGER = logging.getLogger(__name__)

CLOUD_V2_MAPPINGS: dict[int, dict] = {}

def load_cloud_v2_mappings():
    """Load all cloud_v2 device mapping files."""
    mapping_dir = Path(__file__).parent

    if not mapping_dir.exists():
        _LOGGER.error("[mapping][cloud_v2] mapping directory not found: path=%s", mapping_dir)
        return

    try:
        files = list(mapping_dir.iterdir())

        for file in files:
            if file.name.endswith('.py') and file.name != '__init__.py' and file.name.startswith('T0x'):
                try:
                    module_name = f"{__package__}.{file.stem}"
                    module = import_module(module_name)

                    if hasattr(module, 'DEVICE_MAPPING'):
                        device_type = int(file.stem.replace('T0x', ''), 16)
                        CLOUD_V2_MAPPINGS[device_type] = module.DEVICE_MAPPING
                        _LOGGER.debug(
                            "[mapping][cloud_v2] loaded: file=%s device_type=0x%X",
                            file.stem, device_type
                        )
                except (ImportError, ValueError, AttributeError) as e:
                    _LOGGER.error("[mapping][cloud_v2] load failed: file=%s error=%s", file.name, e)
    except OSError as e:
        _LOGGER.error("[mapping][cloud_v2] directory iterate failed: error=%s", e)

load_cloud_v2_mappings()

def get_cloud_v2_mapping(device_type: int, model: str = "", sn8: str = "", category: str = "") -> dict:
    """Get cloud_v2 device mapping for specified device type.

    Args:
        device_type: Device type (e.g., 0x58)
        model: Device model string, used to get specific device mapping (highest priority)
        sn8: Device model code (8 digits), used to get specific device mapping
        category: Product category from cloud, used for default mapping fallback

    Returns:
        Device mapping dict, returns model mapping if available,
        otherwise sn8 mapping if available,
        otherwise default+category if exists, finally fallback to default
    """
    mapping = CLOUD_V2_MAPPINGS.get(device_type, {})

    if not mapping:
        return {}

    result = None

    formatted_model = format_model(model)
    if formatted_model:
        if formatted_model in mapping:
            result = mapping[formatted_model]
        else:
            for key in mapping:
                if isinstance(key, tuple) and formatted_model in key:
                    result = mapping[key]
                    break

    if result is None and sn8:
        if sn8 in mapping:
            result = mapping[sn8]
        else:
            for key in mapping:
                if isinstance(key, tuple) and sn8 in key:
                    result = mapping[key]
                    break

    if result is None and category:
        category_key = f"default_{category.replace('-', '_')}"
        if category_key in mapping:
            result = mapping[category_key]

    if result is None and "default" in mapping:
        result = mapping["default"]

    if result is None:
        result = mapping

    return result

def has_cloud_v2_mapping(device_type: int, model: str = "", sn8: str = "", category: str = "") -> bool:
    """Check if the resolved cloud_v2 mapping contains Thing Model entity configs.

    Args:
        device_type: Device type (e.g., 0x58)
        model: Device model string
        sn8: Device model code (8 digits)
        category: Product category from cloud

    Returns:
        True if any entity config carries a non-empty "thing_key", or carries
        both "module_code" and "actions" (the curtain cover form)
    """
    mapping = get_cloud_v2_mapping(device_type, model, sn8, category)
    entities = mapping.get("entities") or {}
    for platform_cfg in entities.values():
        if not isinstance(platform_cfg, dict):
            continue
        for cfg in platform_cfg.values():
            if not isinstance(cfg, dict):
                continue
            if cfg.get("thing_key"):
                return True
            if cfg.get("module_code") and cfg.get("actions"):
                return True
    return False

def get_thing_attribute_map(device_type: int, model: str = "", sn8: str = "", category: str = "") -> dict[str, str]:
    """Build an attribute -> thing_key map from the resolved cloud_v2 mapping.

    Args:
        device_type: Device type (e.g., 0x58)
        model: Device model string
        sn8: Device model code (8 digits)
        category: Product category from cloud

    Returns:
        Dict mapping each entity's "attribute" to its cloud Thing property
        path ("thing_key"). Only entity configs carrying both fields are
        included; the first occurrence of an attribute wins.
    """
    mapping = get_cloud_v2_mapping(device_type, model, sn8, category)
    entities = mapping.get("entities") or {}
    result: dict[str, str] = {}
    for platform_cfg in entities.values():
        if not isinstance(platform_cfg, dict):
            continue
        for cfg in platform_cfg.values():
            if not isinstance(cfg, dict):
                continue
            attribute = cfg.get("attribute")
            thing_key = cfg.get("thing_key")
            if attribute and thing_key and attribute not in result:
                result[attribute] = thing_key
    return result
