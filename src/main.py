from config import (
    APP_NAME,
    APP_VERSION,
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_DRIVE_FOLDER_ID,
    OPENAI_API_KEY,
)

from drive_service.client import DriveClient

from parsers.parser_registry import ParserRegistry
from chunking.text_chunker import TextChunker
from embeddings.embedding_client import EmbeddingClient

from vector_store.qdrant_store import QdrantStore
from config import QDRANT_PATH, QDRANT_COLLECTION, SYNC_DATABASE_PATH

from sync.sync_manager import SyncManager

from retrieval.retriever import Retriever
from chat.chat_engine import ChatEngine




def main():
    print(f"Welcome to {APP_NAME}")
    print(f"Version: {APP_VERSION}")
    print()


    client = DriveClient(GOOGLE_CREDENTIALS_PATH)

    sync_manager = SyncManager(SYNC_DATABASE_PATH)

    store = QdrantStore(QDRANT_PATH)

    
    
    point_count = store.point_count(
        QDRANT_COLLECTION
    )

    synced_file_ids = sync_manager.get_all_file_ids()

    if point_count == 0 and len(synced_file_ids) > 0:

        print()
        print("⚠ Sync database exists but Qdrant is empty.")
        print("⚠ Forcing full re-index.")
        print()

        for file_id in synced_file_ids:
            sync_manager.remove_file(file_id)





    registry = ParserRegistry(client)




    drive_files = client.list_files(GOOGLE_DRIVE_FOLDER_ID)



    drive_file_ids = {
        file.id
        for file in drive_files
    }

    synced_file_ids = sync_manager.get_all_file_ids()  

    deleted_file_ids = synced_file_ids - drive_file_ids

    for file_id in deleted_file_ids:

        print(f"🗑 Removing deleted file {file_id}")

        store.delete_file(
            collection_name=QDRANT_COLLECTION,
            file_id=file_id,
        )

        sync_manager.remove_file(file_id)







    documents = []

    skipped_count = 0

    for drive_file in drive_files:

        if not sync_manager.is_modified(drive_file):
            skipped_count += 1
            continue
        
        print(f"↻ Processing {drive_file.name}")

        document = registry.parse(drive_file)

        store.delete_file(
            collection_name=QDRANT_COLLECTION,
            file_id=drive_file.id,
        )

        documents.append(document)

        sync_manager.mark_synced(drive_file)

    if skipped_count > 0:
        print(f"✓ Skipped {skipped_count} unchanged files")

    


    # Chunking stuff
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)
    if chunks:
        print(f"✓ Created {len(chunks)} chunks")


    if chunks:

        embedding_client = EmbeddingClient(OPENAI_API_KEY)

        embeddings = embedding_client.embed_texts(
            [chunk.text for chunk in chunks]
        )

        print(f"✓ Generated {len(embeddings)} embeddings")


        store.create_collection(
            collection_name=QDRANT_COLLECTION,
            vector_size=len(embeddings[0]),
        )

        print("✓ Connected to Qdrant")
        print("✓ Collection ready")

        store.upsert(
            collection_name=QDRANT_COLLECTION,
            chunks=chunks,
            embeddings=embeddings,
        )






        print("✓ Stored embeddings in Qdrant")

    else:

        print("✓ Everything is already synchronized.")

        embedding_client = EmbeddingClient(OPENAI_API_KEY)



    ##### CHATBOT STUFF ##################################################################################
    print()

    retriever = Retriever(
        embedding_client=embedding_client,
        vector_store=store,
        collection_name=QDRANT_COLLECTION,
    )

    chat = ChatEngine(
        retriever=retriever,
        embedding_client=embedding_client,
    )



    question = "Who wrote The Furies?"



    print()
    print("Question:")
    print(question)

    response = chat.ask(question)

    print()
    print("Answer:")
    print(response.answer)

    print()
    print("Citations:")

    for citation in response.citations:
        print(
            f"- {citation.document_name} "
            f"(chunk {citation.chunk_index})"
        )



    ####### END CHATBOT STUFF ####################################################################################


    sync_manager.close()





if __name__ == "__main__":
    main()