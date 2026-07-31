from importlib import import_module
from pathlib import Path
import logging
import re

_LOGGER = logging.getLogger(__name__)

DEVICE_MAPPINGS = {}

def format_model(model: str) -> str:
    """Format model string for device mapping lookup.

    Args:
        model: Original model string

    Returns:
        Formatted model string: lowercase, non-alphanumeric chars replaced with underscore
    """
    if not model:
        return ""
    formatted = model.lower()
    formatted = re.sub(r'[^a-z0-9]', '_', formatted)
    formatted = re.sub(r'_+', '_', formatted)
    formatted = formatted.strip('_')
    return formatted

def load_device_mappings():
    """Load all device mapping files."""
    mapping_dir = Path(__file__).parent

    if not mapping_dir.exists():
        _LOGGER.error("Device mapping directory does not exist: %s", mapping_dir)
        return

    try:
        files = list(mapping_dir.iterdir())

        for file in files:
            if file.name.endswith('.py') and file.name != '__init__.py':
                try:
                    module_name = f"{__package__}.{file.stem}"
                    module = import_module(module_name)

                    if hasattr(module, 'DEVICE_MAPPING'):
                        device_type = int(file.stem.replace('T0x', ''), 16)
                        DEVICE_MAPPINGS[device_type] = module.DEVICE_MAPPING
                        _LOGGER.info(
                            "Loaded device mapping: %s -> device type: 0x%X",
                            file.stem, device_type
                        )
                except (ImportError, ValueError, AttributeError) as e:
                    _LOGGER.error("Failed to load device mapping file %s: %s", file.name, e)
    except OSError as e:
        _LOGGER.error("Failed to iterate device mapping directory: %s", e)

load_device_mappings()

def get_device_mapping(device_type: int, model: str = "", sn8: str = "", category: str = "") -> dict:
    """Get device mapping for specified device type.

    Args:
        device_type: Device type (e.g., 0xFB)
        model: Device model string, used to get specific device mapping (highest priority)
        sn8: Device model code (8 digits), used to get specific device mapping
        category: Product category from cloud, used for default mapping fallback

    Returns:
        Device mapping dict, returns model mapping if available,
        otherwise sn8 mapping if available,
        otherwise default+category if exists, finally fallback to default
    """
    mapping = DEVICE_MAPPINGS.get(device_type, {})

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

def is_d9_polling_device(device_type: int, device_mapping: dict) -> bool:
    """Check if a T0xD9 device uses the dedicated poll thread.

    D9 devices whose initial_query contains only one drum key (da/db/dc)
    are polled by a dedicated thread; multi-drum devices rely on push.
    """
    if device_type != 0xD9:
        return False
    initial_keys = set()
    for query in device_mapping.get("initial_query") or []:
        if isinstance(query, set):
            initial_keys |= query
        elif isinstance(query, dict):
            initial_keys |= set(query.keys())
    return len(initial_keys) <= 1
