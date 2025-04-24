from flask import Blueprint, jsonify
from src.extensions import limiter
import asyncio
test_bp = Blueprint("test_bp", __name__)

@test_bp.get('/test')
@limiter.limit("2 per minute")
async def test():

    await asyncio.sleep(2)

    return jsonify({
        "test": "Done"
    })