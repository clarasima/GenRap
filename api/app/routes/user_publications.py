from flask import Blueprint, request, jsonify, abort
from app.utils.auth import token_required
from services.dblp import extractDBLP
from services.scholar import get_scholar_info
from app import publications_collection
from app import users_collection

from app.utils.publications import find_similar_publications


bp = Blueprint('user_publications', __name__)


@bp.route('/publications/user/<user_id>/refresh', methods=['POST'])
@token_required
def refresh_info(user_id):
    try:
        user = users_collection.find_one({"_id": user_id})
        if not user:
            abort(404, description="User not found")
        
        scholar = []
        if user["scholar_profile"]:
            url = user["scholar_profile"]
            scholar = get_scholar_info(url)
        
        dblp = []
        if user["dblp_profile"]:
            url = user["dblp_profile"]
            dblp = extractDBLP(url)
        
        matches = find_similar_publications(dblp, scholar)

        # Remove the "new" field from all documents for the user
        publications_collection.update_many({"user_id": user_id}, {"$unset": {"new": ""}})

        # Iterate over matches and update or insert documents
        for match in matches:
            try:
                if match.get("match"):
                    dblp_id = match["dblp"]["dblp_id"]
                    scholar_id = match["scholar"]["scholar_id"]
                    existing_dblp = publications_collection.find_one({"dblp.dblp_id": dblp_id, "user_id":user_id})
                    existing_scholar = publications_collection.find_one({"scholar.scholar_id": scholar_id, "user_id":user_id})
                    
                    if existing_dblp or existing_scholar:
                        if (existing_dblp and "match" not in existing_dblp) or (existing_scholar and "match" not in existing_scholar):
                            match["new"] = True
                            match["user_id"] = user_id
                            publications_collection.replace_one({"_id": existing_dblp["_id"] if existing_dblp else existing_scholar["_id"]}, match)
                    else:
                        match["new"] = True
                        match["user_id"] = user_id
                        publications_collection.insert_one(match)
                else:
                    if "dblp" in match and "dblp_id" in match["dblp"]:
                        dblp_id = match["dblp"]["dblp_id"]
                        existing_dblp = publications_collection.find_one({"dblp.dblp_id": dblp_id, "user_id":user_id})
                        if not existing_dblp:
                            match["new"] = True
                            match["user_id"] = user_id
                            publications_collection.insert_one(match)
                    if "scholar" in match and "scholar_id" in match["scholar"]:
                        scholar_id = match["scholar"]["scholar_id"]
                        existing_scholar = publications_collection.find_one({"scholar.scholar_id": scholar_id, "user_id":user_id})
                        if not existing_scholar:
                            match["new"] = True
                            match["user_id"] = user_id
                            publications_collection.insert_one(match)
            except Exception as e:
                # Log the error and continue processing the next match
                print(f"Error processing match: {match}, error: {e}")
        for match in matches:
            if "_id" in match:
                match["_id"] = str(match["_id"])
        return jsonify(matches) 
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description=f"An error occurred: {e}")


@bp.route('/publications/user/<user_id>', methods=['GET'])
@token_required
def get_publications(user_id):
    try:
        # Fetch the documents from the database
        publications_cursor = publications_collection.find({"user_id": user_id})
        publications = list(publications_cursor)
        
        if not publications:
            return jsonify({'error': 'No documents found for this user in the database. Try refreshing the data.'}), 404  # 404 Not Found
        
        # Define a custom sort key function
        def get_year(pub):
            def to_int(value):
                try:
                    return int(value)
                except (TypeError, ValueError):
                    return -float('inf')
            
            return max(
                to_int(pub.get('edited', {}).get('year', None)),
                to_int(pub.get('best', {}).get('year', None)),
                to_int(pub.get('dblp', {}).get('year', None)),
                to_int(pub.get('scholar', {}).get('year', None))
            )
        
        # Sort the publications using the custom sort key function
        publications.sort(key=get_year, reverse=True)
        
        # Convert ObjectId to string for JSON serialization
        for pub in publications:
            if "_id" in pub:
                pub["_id"] = str(pub["_id"])
        
        return jsonify(publications)
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")

