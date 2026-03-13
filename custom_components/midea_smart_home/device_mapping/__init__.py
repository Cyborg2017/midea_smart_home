from importlib import import_module
from pathlib import Path
import logging

_LOGGER = logging.getLogger(__name__)

DEVICE_MAPPINGS = {}

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

def get_device_mapping(device_type: int, sn8: str = "", category: str = "") -> dict:
    """Get device mapping for specified device type.

    Args:
        device_type: Device type (e.g., 0xFB)
        sn8: Device model code (8 digits), used to get specific device mapping
        category: Product category from cloud, used for default mapping fallback

    Returns:
        Device mapping dict, returns sn8 mapping if available, 
        otherwise default+category if exists, finally fallback to default
    """
    mapping = DEVICE_MAPPINGS.get(device_type, {})

    if not mapping:
        return {}

    result = None
    
    if sn8:
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
