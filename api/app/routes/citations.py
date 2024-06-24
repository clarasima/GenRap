from flask import Blueprint, request, jsonify, abort
from app.utils.auth import token_required
from services.citations import get_citations_info
from app import publications_collection
from app import users_collection
from app import citations_collection
from bson import ObjectId

bp = Blueprint('citations', __name__)

@bp.route('/citations/refresh', methods=['POST'])
@token_required
def refresh_citations_info():
    try:
        data = request.json
        if not data or 'userId' not in data or 'publicationId' not in data:
            return jsonify({'error': 'userId or publicationId missing'}), 400
        
        user_id = data["userId"]
        publication_id = data["publicationId"]
        
        # Fetch user and publication from the database
        user = users_collection.find_one({"_id": user_id})
        publication = publications_collection.find_one({"_id": ObjectId(publication_id)})
        
        if not user:
            abort(404, description="User not found")
        if not publication:
            abort(404, description="Publication not found")
        
        # Check if the user has a scholar profile
        if not user.get("scholar_profile"):
            return jsonify({"message": "User does not have scholar profile."}), 400
        
        # Check if the publication has scholar.citations.href
        citation_href = publication.get("scholar", {}).get("citations", {}).get("href")
        if not citation_href:
            return jsonify({"error": "Publication does not have scholar citations href."}), 400
        try:
            # Call the get_citations_info function
            citation_info = get_citations_info(citation_href)
        except Exception as e:
            abort(500, description=f"An error occurred while extracting citations data: {e}")
        inserted_citations = []
        for id_citation in citation_info:
            # Check if the citation already exists in the database
            citation = citation_info[id_citation]
            if isinstance(citation, dict):  # Ensure citation is a dictionary
                existing_citation = citations_collection.find_one({
                    "user_id": user_id,
                    "publication_id": publication_id,
                    "citation.title": citation.get("title"),
                    "citation.year": citation.get("year"),
                    "citation.authors": citation.get("authors"),
                    "citation.conference": citation.get("conference")
                })
                if not existing_citation:
                    # Insert the new citation
                    citation_data = {
                        "user_id": user_id,
                        "publication_id": publication_id,
                        "citation": citation
                    }
                    citations_collection.insert_one(citation_data)
                    inserted_citations.append(citation_data)
        return jsonify({"message": "Citations refreshed successfully"}), 200
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")

@bp.route('/citations/update', methods=['POST'])
@token_required
def update_citation():
    data = request.json
    if not data or 'userId' not in data or 'updatedData' not in data:
        return jsonify({'error': 'userId or updatedData missing'}), 400
    
    user_id = data["userId"]
    citation_id = data.get("citationId")
    updated_data = data["updatedData"]
    
    # Remove _id if present in updatedData
    if '_id' in updated_data:
        del updated_data['_id']
    
    try:
        if citation_id:
            # Ensure the publication belongs to the user
            citation = citations_collection.find_one({"_id": ObjectId(citation_id)})
            if not citation:
                return jsonify({'error': 'Citation not found'}), 404
            
            # Update the publication
            result = citations_collection.update_one(
                {"_id": ObjectId(citation_id)},
                {"$set": {"edited":updated_data}}
            )
            
            if result.modified_count == 1:
                return jsonify({'message': 'Publication updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update publication'}), 500
        else:
            document = {}
            document["user_id"] = user_id
            document["citation"] = updated_data
            document["edited"] = updated_data
            document["addByUser"] = True
            # Insert a new publication
            result = citations_collection.insert_one(document)
            
            if result.inserted_id:
                return jsonify({'message': 'Publication created successfully', 'publicationId': str(result.inserted_id)}), 201
            else:
                return jsonify({'error': 'Failed to create publication'}), 500
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")




# needed for citations
@bp.route('/citations/<publication_id>', methods=['GET'])
@token_required
def get_pub_citations(publication_id):
    try:
        # Fetch citations from the database
        citations_cursor = citations_collection.find({ "publication_id": publication_id})
        citations = list(citations_cursor)
        
        if not citations:
            return jsonify({'error': 'No citations found for this publication for the given user.'}), 404  # 404 Not Found
        # Convert ObjectId to string for JSON serialization
        
        for citation in citations:
            if "_id" in citation:
                citation["_id"] = str(citation["_id"])
        
        return jsonify(citations)
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")
