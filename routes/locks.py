from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models.locks import Locks
from models import db

locks_bp = Blueprint('locks_bp', __name__)

@locks_bp.route('/share-lock', methods=['POST'])
def share_lock():
    data = request.json
    lock = Locks(
        id=data['id'],
        bridge_id=data['bridge']['id'],
        bridge_name=data['bridge']['name'],
        bridge_location=data['bridge']['location'],
        shared_by=data['sharedBy']
    )
    db.session.add(lock)
    db.session.commit()
    return jsonify({'message': 'Lock shared', 'id': data['id']})

@locks_bp.route('/lock-status/<lock_id>', methods=['GET'])
def lock_status(lock_id):
    print(lock_id)
    lock = Locks.query.get(lock_id)
    if lock:
        return jsonify({
            'id': lock.id,
            'bridge': {
                'id': lock.bridge_id,
                'name': lock.bridge_name,
                'location': lock.bridge_location
            },
            'sharedBy': lock.shared_by,
            'status': lock.status,
            'sharedWith': lock.shared_with
        })
    return jsonify({'error': 'Lock not found'}), 404

@locks_bp.route('/accept-lock/<lock_id>', methods=['POST'])
def accept_lock(lock_id):
    print(lock_id)
    lock = Locks.query.get(lock_id)
    print(lock)
    if lock:
        print(lock.status)
        lock.status = 'accepted'
        print(lock.status)
        lock.shared_with = request.json.get('sharedWith', lock.shared_with)
        db.session.commit()
        return jsonify({'message': 'Lock accepted', 'id': lock_id})
    return jsonify({'error': 'Lock not found'}), 404

@locks_bp.route('/decline-lock/<lock_id>', methods=['POST'])
def decline_lock(lock_id):
    lock = Locks.query.get(lock_id)
    if lock:
        lock.status = 'declined'
        db.session.commit()
        return jsonify({'message': 'Lock declined', 'id': lock_id})
    return jsonify({'error': 'Lock not found'}), 404
