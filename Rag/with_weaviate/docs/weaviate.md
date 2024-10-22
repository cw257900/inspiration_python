
settings:

<weaviate.Collection config={
  "name": "PDF_COLLECTION",
  "description": "PDF Collection with embeddings by Weaviate",
  "generative_config": {
    "generative": "generative-cohere",
    "model": {}
  },
  "inverted_index_config": {
    "bm25": {
      "b": 0.75,
      "k1": 1.2
    },
    "cleanup_interval_seconds": 60,
    "index_null_state": true,
    "index_property_length": true,
    "index_timestamps": true,
    "stopwords": {
      "preset": "en",
      "additions": null,
      "removals": null
    }
  },
  "multi_tenancy_config": {
    "enabled": false,
    "auto_tenant_creation": false,
    "auto_tenant_activation": false
  },
  "properties": [
    {
      "name": "page_content",
      "description": null,
      "data_type": "text",
      "index_filterable": true,
      "index_range_filters": false,
      "index_searchable": true,
      "nested_properties": null,
      "tokenization": "word",
      "vectorizer_config": {
        "skip": false,
        "vectorize_property_name": true
      },
      "vectorizer": "text2vec-openai"
    },
    {
      "name": "page_number",
      "description": null,
      "data_type": "int",
      "index_filterable": true,
      "index_range_filters": false,
      "index_searchable": false,
      "nested_properties": null,
      "tokenization": null,
      "vectorizer_config": {
        "skip": false,
        "vectorize_property_name": true
      },
      "vectorizer": "text2vec-openai"
    },
    {
      "name": "source",
      "description": null,
      "data_type": "text",
      "index_filterable": true,
      "index_range_filters": false,
      "index_searchable": true,
      "nested_properties": null,
      "tokenization": "word",
      "vectorizer_config": {
        "skip": false,
        "vectorize_property_name": true
      },
      "vectorizer": "text2vec-openai"
    }
  ],
  "references": [],
  "replication_config": {
    "factor": 1,
    "async_enabled": false,
    "deletion_strategy": "DeleteOnConflict"
  },
  "reranker_config": null,
  "sharding_config": {
    "virtual_per_physical": 128,
    "desired_count": 1,
    "actual_count": 1,
    "desired_virtual_count": 128,
    "actual_virtual_count": 128,
    "key": "_id",
    "strategy": "hash",
    "function": "murmur3"
  },
  "vector_index_config": {
    "quantizer": {
      "cache": null,
      "rescore_limit": null
    },
    "cleanup_interval_seconds": 300,
    "distance_metric": "cosine",
    "dynamic_ef_min": 100,
    "dynamic_ef_max": 500,
    "dynamic_ef_factor": 8,
    "ef": -1,
    "ef_construction": 128,
    "filter_strategy": "sweeping",
    "flat_search_cutoff": 40000,
    "max_connections": 32,
    "skip": false,
    "vector_cache_max_objects": 1000000000000
  },
  "vector_index_type": "hnsw",
  "vectorizer_config": {
    "vectorizer": "text2vec-openai",
    "model": {
      "baseURL": "https://api.openai.com",
      "model": "text-embedding-3-small"
    },
    "vectorize_collection_name": true
  },
  "vectorizer": "text2vec-openai",
  "vector_config": null
}>