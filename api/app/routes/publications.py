from flask import Blueprint, request, jsonify, abort
from app.utils.auth import token_required
from app import publications_collection
from bson import ObjectId

from app.utils.publications import find_similar_publications

bp = Blueprint('publications', __name__)

# needed for citations
@bp.route('/publications/<publication_id>/scholar', methods=['GET'])
@token_required
def get_publication_scholar(publication_id):
    try:
        publication = publications_collection.find_one({"_id": ObjectId(publication_id)})
        if not publication:
            abort(404, description="Publication not found")
        
        # Check if the user has a scholar profile
        if not publication.get("scholar"):
            return jsonify({"message": "Publication does not have scholar data."}), 400    
        return jsonify({"title":publication.get("scholar")}), 200
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")


@bp.route('/publications/<publication_id>/split', methods=['POST'])
@token_required
def split_publication(publication_id):
    try:
        # Find the matched publication
        matched_publication = publications_collection.find_one({"_id": ObjectId(publication_id), "match": True})
        if not matched_publication:
            return jsonify({'error': 'Matched publication not found'}), 404

        # Prepare new publications
        dblp_data = matched_publication.get('dblp')
        scholar_data = matched_publication.get('scholar')
        user_id = matched_publication.get('user_id')

        if not dblp_data or not scholar_data:
            return jsonify({'error': 'Matched publication does not contain both DBLP and Scholar data'}), 400
        dblp_doc ={}
        dblp_doc['user_id'] = user_id
        dblp_doc['dblp'] = dblp_data
        dblp_doc['new'] = True

        scholar_doc = {}
        scholar_doc['user_id'] = user_id
        scholar_doc['scholar'] = scholar_data
        scholar_doc['new'] = True

        dblp_result = publications_collection.insert_one(dblp_doc)
        scholar_result = publications_collection.insert_one(scholar_doc)

        dblp_id = dblp_result.inserted_id
        scholar_id = scholar_result.inserted_id

        # It is not a match
        publications_collection.update_one({"_id": ObjectId(publication_id)}, {"$set": {"match": False}})

        return jsonify({
            'message': 'Publication split successfully',
            'dblp_id': str(dblp_id),
            'scholar_id': str(scholar_id)
        })
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description=f"An error occurred: {e}")


@bp.route('/publications/<publication_id>', methods=['PUT'])
@token_required
def update_publication(publication_id):
    data = request.json
    if not data or 'userId' not in data or 'updatedData' not in data:
        return jsonify({'error': 'userId or updatedData missing'}), 400
    
    user_id = data["userId"]
    publication_id = data.get("publicationId")
    updated_data = data["updatedData"]
    
    # Remove _id if present in updatedData
    if '_id' in updated_data:
        del updated_data['_id']
    
    try:
        if publication_id:
            # Ensure the publication belongs to the user
            publication = publications_collection.find_one({"user_id": user_id, "_id": ObjectId(publication_id)})
            if not publication:
                return jsonify({'error': 'Publication not found or does not belong to this user'}), 404
            
            # Update the publication
            result = publications_collection.update_one(
                {"_id": ObjectId(publication_id)},
                {"$set": updated_data}
            )
            
            if result.modified_count == 1:
                return jsonify({'message': 'Publication updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update publication'}), 500
        else:
            # Add user_id to the updated_data
            updated_data['user_id'] = user_id
            # Insert a new publication
            result = publications_collection.insert_one(updated_data)
            
            if result.inserted_id:
                return jsonify({'message': 'Publication created successfully', 'publicationId': str(result.inserted_id)}), 201
            else:
                return jsonify({'error': 'Failed to create publication'}), 500
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")
