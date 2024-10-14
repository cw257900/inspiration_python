# queries.py

# Define the GraphQL queries as static variables (Python strings)

gql_getAllObjects = """
{
    Get {
        PDF_COLLECTIONS {
            pdf_name
            pdf_content
            pdf_chunk_id
            _additional {
                id
            }
        }
    }
}
"""

gql_hybridSearchByText = """
{
    Get {
        PDF_COLLECTIONS(
            hybrid: {
                query: "does constitution talked about right of speech",
                alpha: 0.75
            }
            ) {
            pdf_name
            pdf_content
            pdf_chunk_id
            _additional {
                score
            }
        }
    }

}
"""

gql_getSingleObjectById = """
{
    Get {
        PDF_COLLECTIONS(where: {
            path: ["_additional", "id"],
            operator: Equal,
            valueString: "{uuid}"
        }) {
            pdf_name
            pdf_content
            pdf_chunk_id
            _additional {
                id
            }
        }
    }
}
"""

gql_queryObjectsByKeyword = """
{
    Get {
        PDF_COLLECTIONS(where: {
            path: ["pdf_content"],
            operator: Like,
            valueString: "{keyword}"
        }) {
            pdf_name
            pdf_content
            pdf_chunk_id
            _additional {
                id
            }
        }
    }
}
"""
