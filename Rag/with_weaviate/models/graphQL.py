# queries.py

# Define the GraphQL queries as static variables (Python strings)


gql_hybridsearch_withLimits =  """
{
    Get {
        PDF_COLLECTIONS(
            hybrid: {
                query: "{text}",
                alpha: 0.75
            },
            limit: {limit} 
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

gql_hybridSearchByText = """
{
    Get {
        PDF_COLLECTIONS(
            hybrid: {
                query: "{text}",
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
