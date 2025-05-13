from app.common.models import CoreModel

from app.config.db import load_all_models

load_all_models()

target_metadata = CoreModel.metadata
