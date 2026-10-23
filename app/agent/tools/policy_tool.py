from app.rag.semantic_search import search_policy


def policy_search_tool(query: str):
    """
    Agent tool for searching financial risk policies.
    """

    documents = search_policy(query)

    return {
        "query": query,
        "results": documents
    }


if __name__ == "__main__":

    query = "What should happen when a transaction is high risk?"

    result = policy_search_tool(query)

    print("\n--- Policy Search Tool ---")
    print("Query:", result["query"])

    print("\nPolicy Results:")

    for document in result["results"]:
        print(document)