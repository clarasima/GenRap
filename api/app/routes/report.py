from flask import Blueprint, request, abort, jsonify
from app.utils.auth import token_required
from bson import ObjectId
from app.utils.report import (
    validate_request_data,
    get_collection_and_filename,
    retrieve_documents,
    update_user_collection,
    sort_documents,
    create_txt_response,
    create_excel_response,
    create_csv_response
)

bp = Blueprint('report', __name__)

@bp.route('/generate', methods=['POST'])
@token_required
def generate_report():
    data = request.json
    format_type = data.get('format')
    if format_type not in ['txt', 'excel', 'csv']:
        return jsonify({"error": "Invalid format type"}), 400
    
    document_ids, doc_type, selected_fields = validate_request_data(data)
    try:
        object_ids = [ObjectId(doc_id) for doc_id in document_ids]
        collection, filename, additional_param = get_collection_and_filename(doc_type)
        documents = retrieve_documents(collection, object_ids)
        update_user_collection(documents, selected_fields)
        documents = sort_documents(documents, selected_fields)
        
        if format_type == 'txt':
            return create_txt_response(documents, selected_fields, filename, additional_param)
        elif format_type == 'excel':
            return create_excel_response(documents, selected_fields, filename, additional_param)
        elif format_type == 'csv':
            return create_csv_response(documents, selected_fields, filename)
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")

